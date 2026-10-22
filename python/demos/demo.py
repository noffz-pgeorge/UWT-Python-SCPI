"""ESP32-C3 RF demo: drive the DUT through the DUT control gRPC service and
measure/stimulate it through the Noffz UWT SCPI API (VST analyzer + RFSG)
from a Linux machine.

Four flows:
    wifi-tx     DUT transmits Wi-Fi  -> analyzer measures TXP + ModAcc (+ SEM)
    ble-tx      DUT transmits BLE    -> analyzer measures TXP + ModAcc
                                        (+ 20 dB BW for Classic packet types)
    wifi-rx     RFSG plays Wi-Fi packets at a power sweep -> DUT counts -> PER
    ble-rx      RFSG plays BLE packets at a power sweep   -> DUT counts -> PER
    wifi-external  analyzer is configured, you start an external generator
                (e.g. the RFmx SFP) and press Enter, then it measures. No DUT.

Examples:
    python demo.py --ip 10.0.0.5 --dut-service 10.0.0.5:50051 wifi-tx --channel 6
    python demo.py --ip 10.0.0.5 --dut-service 10.0.0.5:50051 --dut-port COM5 \
        wifi-rx --waveform Wifi_6M_100pkt --packets-per-waveform 100 \
        --start -40 --stop -95 --step -5

The switch port is selected by `--tx-port` / `--rx-port`; each becomes the
`inst<N>` part of the VXI-11 resource for that client. Results are printed
and saved as JSON under ./results/.
"""
from __future__ import annotations

import argparse
import json
import logging
import time
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, Iterator, List, Optional

from noffz_uwt import BTClient, RfsgClient, WifiClient
from dut import (BLE_POWER_LEVEL_DBM, BlePayload, BleRate, DutClient, WifiRate,
                      ble_channel_freq_hz, wifi_channel_freq_hz)

log = logging.getLogger("demo")

BUSY_STATES = {"PROCESSING", "PENDING", "ACTIVE"}

# Field order of :FETch:BT:RESults<i>:TXP? and :MODacc? (UWT manual 3.7.0)
BT_TXP_FIELDS = [
    "avg_power_mean_dbm", "avg_power_max_dbm", "avg_power_min_dbm",
    "peak_power_max_dbm", "papr_max_db",
    "edr_gfsk_avg_power_mean_dbm", "edr_dpsk_avg_power_mean_dbm",
    "edr_dpsk_gfsk_ratio_mean_db",
]
BT_MODACC_FIELDS = [
    "br_initial_freq_error_max_hz", "br_peak_freq_drift_max_hz",
    "br_peak_freq_drift_rate_max_hz", "edr_devm_99pct_pct",
    "df1avg_max_hz", "df1avg_mean_hz", "df1avg_min_hz",
    "df2avg_max_hz", "df2avg_mean_hz", "df2avg_min_hz",
    "edr_header_freq_error_wi_max_hz", "edr_peak_freq_error_wi_w0_max_hz",
    "edr_peak_freq_error_w0_max_hz", "iq_origin_offset_mean_db",
    "le_initial_freq_error_hz", "le_initial_freq_drift_max_hz",
    "le_peak_freq_drift_max_hz", "le_peak_freq_drift_rate_max_hz",
    "le_peak_freq_error_max_hz",
    "min_df1max_min_hz", "min_df2max_min_hz", "peak_devm_max_pct",
    "peak_df2max_max_hz", "peak_rms_devm_max_pct",
    "pct_symbols_above_df2max_threshold", "pct_symbols_below_99pct_devm_limit",
    "rms_devm_mean_pct",
]


def parse_fields(text: str, names: List[str]) -> Dict[str, str]:
    """Split a comma-separated result string into named fields. If the count
    doesn't match (different service version), keep the raw string."""
    values = [v.strip() for v in text.split(",")]
    if len(values) != len(names):
        return {"raw": text}
    return dict(zip(names, values))


# Analyzer payload pattern matching each DUT payload. The pattern decides which
# ModAcc results are computed: df1 on 11110000, df2/offset/drift on 10101010.
BLE_ANALYZER_PATTERN = {
    BlePayload.P_1010: "Pattern10101010",
    BlePayload.P_00001111: "Pattern11110000",   # 0x0F sent LSB first = 11110000 on air
    BlePayload.PRBS9: "StandardDefined",
}

# :CONFigure:BT:DRATE values (bits/s) for LE packets
BLE_DRATE = {BleRate.LE_1M: 1000000, BleRate.LE_2M: 2000000}


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
@contextmanager
def session(client):
    """open()/disconnect() around a UWT client."""
    client.open()
    try:
        yield client
    finally:
        client.disconnect()


def wait_measurement(client, timeout_s: float = 15.0,
                     min_wait_s: float = 0.5, poll_s: float = 0.1) -> None:
    """Wait for an analyzer measurement started by initiate() to finish.

    The state can already read READY before the new acquisition starts, so
    READY only counts once we've seen a busy state or `min_wait_s` passed.
    """
    t0 = time.monotonic()
    seen_busy = False
    state = ""
    while time.monotonic() - t0 < timeout_s:
        state = client.get_measurement_state().upper()
        if state in BUSY_STATES:
            seen_busy = True
        elif state == "READY" and (seen_busy or
                                   time.monotonic() - t0 >= min_wait_s):
            return
        elif state == "OFF":
            raise RuntimeError("Analyzer measurement state is OFF")
        time.sleep(poll_s)
    raise TimeoutError(f"Measurement not READY after {timeout_s}s "
                       f"(last state: {state!r})")


def _truthy(text: str) -> bool:
    return text.strip().upper() in {"1", "TRUE", "ON", "YES"}


def wait_generation_done(rfsg: RfsgClient, timeout_s: float,
                         poll_s: float = 0.1) -> None:
    t0 = time.monotonic()
    while time.monotonic() - t0 < timeout_s:
        if not _truthy(rfsg.is_generating()):
            return
        time.sleep(poll_s)
    rfsg.abort()
    raise TimeoutError(f"RFSG still generating after {timeout_s}s")


def _drop_none(d: Dict) -> Dict:
    return {k: v for k, v in d.items() if v is not None}


# --------------------------------------------------------------------------- #
# TX flows: DUT transmits, analyzer measures
# --------------------------------------------------------------------------- #
def wifi_tx(dut: DutClient, wlan: WifiClient, a) -> Dict:
    rate = WifiRate[a.rate]
    freq = wifi_channel_freq_hz(a.channel)
    log.info("Wi-Fi TX: ch%d (%.0f MHz), %s, atten %.2f dB",
             a.channel, freq / 1e6, rate.name, a.atten_db)

    wlan.config_signal(**_drop_none(dict(
        center_frequency_hz=freq,
        standard=a.wlan_standard,
        channel_bw=a.wlan_bw,
        frequency_band=a.wlan_band)))
    if a.trigger_source:
        wlan.config_trigger(**_drop_none(dict(
            trigger_source=a.trigger_source,
            trigger_edge="RISING",
            trigger_threshold=a.trigger_threshold,
            trigger_delay_sec=a.trigger_delay_s,
            trigger_min_quiet_duration_sec=a.trigger_quiet_s)))
    wlan.config_power(reference_level_d_bm=a.ref_level,
                      txp_measurement_enabled=True,
                      txp_burst_detection_enabled=True)
    if rate.is_dsss:
        wlan.config_modacc_ofdm(ofdm_mod_acc_measurement_enabled=False)
        wlan.config_modacc_dsss(dsss_mod_acc_measurement_enabled=True,
                                dsss_mod_acc_burst_start_detection_enabled=True)
    else:
        wlan.config_modacc_dsss(dsss_mod_acc_measurement_enabled=False)
        wlan.config_modacc_ofdm(ofdm_mod_acc_measurement_enabled=True,
                                ofdm_mod_acc_burst_start_detection_enabled=True)
    wlan.config_sem(sem_measurement_enabled=a.sem)

    dut.wifi_tx(a.channel, rate, a.atten_db)
    try:
        time.sleep(a.settle_s)
        wlan.initiate(a.result_space)
        wait_measurement(wlan, a.meas_timeout_s)
        result = {
            "txp": wlan.fetch_txp(a.result_index),
            "modacc": (wlan.fetch_modacc_dsss(a.result_index) if rate.is_dsss
                       else wlan.fetch_modacc_ofdm(a.result_index)),
        }
        if a.sem:
            result["sem"] = wlan.fetch_sem(a.result_index)
    finally:
        dut.stop()

    m = result["modacc"]
    summary = {
        "psdu_crc": m.get("psdu_crc_status"),
        "burst_power_dbm": result["txp"].get("power_avg_mean"),
        "peak_power_dbm": result["txp"].get("power_max"),
        "rms_evm": m.get("rms_evm_mean") if rate.is_dsss
        else m.get("rms_evm_composite_mean"),
        "freq_error_hz": m.get("ferror_mean"),
    }
    if not rate.is_dsss:
        summary["detected_rate_index"] = m.get("msc_index")
        summary["data_symbols"] = m.get("symbol_number")
    if a.sem:
        summary["sem_status"] = result["sem"].get("status")
    return {"test": "wifi_tx", "channel": a.channel, "freq_hz": freq,
            "rate": rate.name, "summary": summary, "detail": result}


def ble_tx(dut: DutClient, bt: BTClient, a) -> Dict:
    rate = BleRate[a.rate]
    freq = ble_channel_freq_hz(a.channel)
    log.info("BLE TX: ch%d (%.0f MHz), %s, level %d (~%d dBm)",
             a.channel, freq / 1e6, rate.name, a.power_level,
             BLE_POWER_LEVEL_DBM[a.power_level])

    is_le = a.bt_packet_type == "PacketTypeLE"
    drate = a.bt_drate or (BLE_DRATE.get(rate) if is_le else None)
    bt.config_signal_and_packet(**_drop_none(dict(
        center_frequency=freq,
        drate=drate,
        access_address=a.bt_access_address,
        payload_mode=a.bt_payload_mode,
        payload_pattern=a.bt_payload_pattern or BLE_ANALYZER_PATTERN[BlePayload[a.payload]],
        packet_type=a.bt_packet_type,
        payload_length=a.payload_length)))
    if a.trigger_source:
        bt.config_trigger(**_drop_none(dict(
            source=a.trigger_source,
            edge="RISING",
            threshold=a.trigger_threshold,
            delay=a.trigger_delay_s,
            mq_time=a.trigger_quiet_s)))
    bt.config_power(ref_level=a.ref_level, txp_enable=True)
    bt.config_modacc(enable=True)
    # 20 dB bandwidth is a BR/EDR measurement; enabling it for LE packets
    # makes the whole measurement return NaN.
    bt.config_20db_bandwidth(enable=not is_le)

    dut.ble_tx(a.channel, a.power_level, length=a.payload_length,
               payload=BlePayload[a.payload],
               rate=rate)
    try:
        time.sleep(a.settle_s)
        bt.initiate(a.result_space)
        wait_measurement(bt, a.meas_timeout_s)
        result = {
            "txp": parse_fields(bt.fetch_tx_power(a.result_index), BT_TXP_FIELDS),
            "modacc": parse_fields(bt.fetch_modacc(a.result_index), BT_MODACC_FIELDS),
        }
        if not is_le:
            result["20db_bw"] = bt.fetch_20db_bandwidth(a.result_index)
    finally:
        dut.stop()

    t, m = result["txp"], result["modacc"]
    summary = {
        "avg_power_dbm": t.get("avg_power_mean_dbm"),
        "peak_power_dbm": t.get("peak_power_max_dbm"),
        # Offset/drift and df2 are defined on a 10101010 payload, df1 on 11110000.
        "freq_offset_hz": m.get("le_initial_freq_error_hz"),
        "peak_freq_error_hz": m.get("le_peak_freq_error_max_hz"),
        "peak_drift_hz": m.get("le_peak_freq_drift_max_hz"),
        "df1avg_hz": m.get("df1avg_mean_hz"),
        "df2avg_hz": m.get("df2avg_mean_hz"),
        "df2max_above_threshold_pct": m.get("pct_symbols_above_df2max_threshold"),
    }
    if "raw" in t or "raw" in m:
        summary["raw_txp"], summary["raw_modacc"] = t.get("raw"), m.get("raw")
    if "20db_bw" in result:
        summary["20db_bw_hz"] = result["20db_bw"].get("bandwidth")
    return {"test": "ble_tx", "channel": a.channel, "payload": a.payload,
            "freq_hz": freq, "rate": rate.name,
            "power_level": a.power_level,
            "summary": summary, "detail": result}


# --------------------------------------------------------------------------- #
# External source: the analyzer measures a signal you generate by hand (e.g. an
# 802.11ax waveform from the RFmx soft front panel). No DUT involved.
# --------------------------------------------------------------------------- #
def wifi_external(wlan: WifiClient, a, prompt: Callable[[str], str] = input) -> Dict:
    freq = a.frequency_hz
    log.info("Wi-Fi external: %.3f GHz, standard %s, bw %s, ref %.1f dBm",
             freq / 1e9, a.wlan_standard, a.wlan_bw, a.ref_level)

    wlan.config_signal(**_drop_none(dict(
        center_frequency_hz=freq,
        standard=a.wlan_standard,
        channel_bw=a.wlan_bw,
        
        frequency_band=a.wlan_band)))
    if a.trigger_source:
        wlan.config_trigger(**_drop_none(dict(
            trigger_source=a.trigger_source,
            trigger_edge="RISING",
            trigger_threshold=a.trigger_threshold,
            trigger_delay_sec=a.trigger_delay_s,
            trigger_min_quiet_duration_sec=a.trigger_quiet_s)))
    wlan.config_power(reference_level_d_bm=a.ref_level,
                      txp_measurement_enabled=True,
                      txp_burst_detection_enabled=True)
    wlan.config_modacc_dsss(dsss_mod_acc_measurement_enabled=False)
    wlan.config_modacc_ofdm(ofdm_mod_acc_measurement_enabled=True,
                            ofdm_mod_acc_burst_start_detection_enabled=True)
    wlan.config_sem(sem_measurement_enabled=a.sem)

    base = {"test": "wifi_external", "freq_hz": freq, "standard": a.wlan_standard,
            "bandwidth": a.wlan_bw, "ref_level_dbm": a.ref_level}
    #answer = prompt(f"\n>>> Analyzer ready: {a.wlan_standard or 'service default'} "
    #               f"{a.wlan_bw or ''} at {freq / 1e9:.3f} GHz on switch port {a.tx_port}.\n"
    #                f">>> Start the waveform on the generator, then press Enter "
    #                f"to measure (or type 's' + Enter to skip): ")
    #if answer.strip().lower().startswith("s"):
    #    log.info("Skipped by user")
    #    return {**base, "skipped": True, "summary": {}}

    wlan.initiate(a.result_space)
    wait_measurement(wlan, a.meas_timeout_s)
    result = {
        "txp": wlan.fetch_txp(a.result_index),
        "modacc": wlan.fetch_modacc_ofdm(a.result_index),
    }
    if a.sem:
        result["sem"] = wlan.fetch_sem(a.result_index)

    t, m = result["txp"], result["modacc"]
    summary = {
        "burst_power_dbm": t.get("power_avg_mean"),
        "peak_power_dbm": t.get("power_max"),
        "rms_evm": m.get("rms_evm_composite_mean"),
        "freq_error_hz": m.get("ferror_mean"),
        "detected_mcs": m.get("msc_index"),
        "data_symbols": m.get("symbol_number"),
        "psdu_crc": m.get("psdu_crc_status"),
    }
    if a.sem:
        summary["sem_status"] = result["sem"].get("status")
    return {**base, "summary": summary, "detail": result}


# --------------------------------------------------------------------------- #
# RX flows: RFSG transmits, DUT counts packets
# --------------------------------------------------------------------------- #
@dataclass
class RxPoint:
    rfsg_power_dbm: float
    power_at_dut_dbm: float
    sent: int
    received: int
    per: float
    rssi_dbm: float


@dataclass
class RxSweep:
    test: str
    freq_hz: float
    waveform: str
    per_limit: float
    points: List[RxPoint] = field(default_factory=list)

    @property
    def sensitivity_dbm(self) -> Optional[float]:
        """Lowest power at the DUT that still met the PER limit, provided
        every stronger level also passed."""
        best = None
        for p in sorted(self.points, key=lambda p: -p.power_at_dut_dbm):
            if p.per > self.per_limit:
                break
            best = p.power_at_dut_dbm
        return best


def _power_steps(start: float, stop: float, step: float) -> List[float]:
    if step == 0 or (stop - start) * step < 0:
        raise ValueError("step must move from start toward stop")
    n = int(round((stop - start) / step))
    return [round(start + i * step, 3) for i in range(n + 1)]


def rx_sweep(dut: DutClient, rfsg: RfsgClient, a, *, is_ble: bool) -> Dict:
    if is_ble:
        freq = ble_channel_freq_hz(a.channel)
        rate = BleRate[a.rate]
        start_rx = lambda: dut.ble_rx_start(a.channel, rate)
        stop_rx = dut.ble_rx_stop
        name = "ble_rx"
    else:
        freq = wifi_channel_freq_hz(a.channel)
        rate = WifiRate[a.rate]
        start_rx = lambda: dut.wifi_rx_start(a.channel, rate)
        stop_rx = dut.wifi_rx_stop
        name = "wifi_rx"

    sent = a.packets_per_waveform * a.cycles
    sweep = RxSweep(name, freq, a.waveform, a.per_limit)
    log.info("%s sweep: %.0f MHz, %s, %d packets/step, PER limit %.1f%%",
             name, freq / 1e6, a.waveform, sent, a.per_limit * 100)

    rfsg.config_signal(frequency=freq, waveform=a.waveform)
    rfsg.config_repetition(**_drop_none(dict(cycles=a.cycles,
                                             mode=a.repetition_mode)))
    fails_in_row = 0
    try:
        for level in _power_steps(a.start, a.stop, a.step):
            rfsg.config_signal(power_level=level)
            start_rx()
            rfsg.initiate()
            wait_generation_done(rfsg, a.gen_timeout_s)
            time.sleep(a.settle_s)
            res = stop_rx()
            got = res.desired
            point = RxPoint(level, round(level - a.path_loss_db, 2), sent,
                            got, round(res.per(sent), 4), res.rssi_dbm)
            sweep.points.append(point)
            log.info("  %7.1f dBm (DUT %7.1f): %4d/%d  PER %5.1f%%  RSSI %s",
                     level, point.power_at_dut_dbm, got, sent,
                     point.per * 100, f"{res.rssi_dbm:.1f}")
            fails_in_row = fails_in_row + 1 if point.per > a.per_limit else 0
            if a.stop_after_fails and fails_in_row >= a.stop_after_fails:
                log.info("  stopping: %d failing steps in a row", fails_in_row)
                break
    finally:
        rfsg.abort()
        dut.stop()

    out = asdict(sweep)
    out["sensitivity_dbm"] = sweep.sensitivity_dbm
    out["rate"] = rate.name
    return out


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _add_tx_common(p):
    p.add_argument("--ref-level", type=float, default=-28.0,
                   help="analyzer reference level in dBm; ~8 dB above the "
                        "peak power at the VST")
    p.add_argument("--trigger-source", default="RF0",
                   help="analyzer trigger source (IQ power edge on RF0); "
                        "empty string leaves the service's trigger untouched")
    p.add_argument("--trigger-threshold", type=float, default=-20.0,
                   help="IQ power trigger threshold")
    p.add_argument("--trigger-delay-s", type=float, default=-20e-6,
                   help="trigger delay; negative = pre-trigger so the "
                        "capture includes the preamble")
    p.add_argument("--trigger-quiet-s", type=float, default=5e-6,
                   help="minimum quiet time before a rising edge counts")
    p.add_argument("--settle-s", type=float, default=0.5)
    p.add_argument("--meas-timeout-s", type=float, default=15.0)


def _add_rx_common(p, default_waveform: str, default_limit: float):
    p.add_argument("--waveform", default=default_waveform,
                   help="waveform name in the RFSG waveform database")
    p.add_argument("--packets-per-waveform", type=int, required=True,
                   help="packets contained in one playback of the waveform")
    p.add_argument("--cycles", type=int, default=1,
                   help="waveform repetitions per power step")
    p.add_argument("--repetition-mode", default=None,
                   help="value for :CONFigure:RFSG:REPetition:MODE, if needed")
    p.add_argument("--start", type=float, default=-40.0)
    p.add_argument("--stop", type=float, default=-95.0)
    p.add_argument("--step", type=float, default=-5.0)
    p.add_argument("--path-loss-db", type=float, default=0.0,
                   help="loss from RFSG output to DUT antenna (chamber)")
    p.add_argument("--per-limit", type=float, default=default_limit)
    p.add_argument("--stop-after-fails", type=int, default=2,
                   help="end the sweep after N failing steps in a row (0=off)")
    p.add_argument("--settle-s", type=float, default=0.2)
    p.add_argument("--gen-timeout-s", type=float, default=30.0)


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ip", required=True, help="UWT service IP address")
    ap.add_argument("--dut-service", default=None,
                    help="DUT control gRPC service, host:port (DUT tests only)")
    ap.add_argument("--dut-port", default="",
                    help="DUT serial port on the service host (e.g. COM5); "
                         "empty uses the service's configured default")
    ap.add_argument("--tx-port", type=int, default=1,
                    help="switch port for analyzer measurements (inst<N>)")
    ap.add_argument("--rx-port", type=int, default=None,
                    help="switch port for RFSG (defaults to --tx-port)")
    ap.add_argument("--result-space", default="1",
                    help="value passed to :WLAN/:BT:INITiate")
    ap.add_argument("--result-index", type=int, default=1,
                    help="index used in :FETch:...:RESults<i>")
    ap.add_argument("--visa-timeout-ms", type=int, default=10000)
    ap.add_argument("--out-dir", default="results")
    ap.add_argument("-v", "--verbose", action="store_true")
    sub = ap.add_subparsers(dest="test", required=True)

    w = sub.add_parser("wifi-tx")
    w.add_argument("--channel", type=int, default=6)
    w.add_argument("--rate", default="G_6M", choices=WifiRate.__members__)
    w.add_argument("--atten-db", type=float, default=0.0)
    w.add_argument("--sem", action="store_true", help="also run SEM")
    w.add_argument("--wlan-standard", default=None)
    w.add_argument("--wlan-bw", default=None)
    w.add_argument("--wlan-band", default=None)
    _add_tx_common(w)

    b = sub.add_parser("ble-tx")
    b.add_argument("--channel", type=int, default=21,
                   help="BLE RF channel 0-39 (f = 2402 + 2*ch MHz)")
    b.add_argument("--rate", default="LE_1M", choices=BleRate.__members__)
    b.add_argument("--power-level", type=int, default=15, choices=range(16))
    b.add_argument("--payload-length", type=int, default=250)
    b.add_argument("--bt-access-address", default=None,
                   help="value for :CONFigure:BT:ACCess:ADDRess; the DUT uses "
                        "0x71764129 (check the manual for the expected format)")
    b.add_argument("--payload", default="PRBS9", choices=BlePayload.__members__,
                   help="DUT payload pattern (fcc_le_tx data_type)")
    b.add_argument("--bt-payload-mode", default=None,
                   help="value for :CONFigure:BT:PAYLoad:MODE")
    b.add_argument("--bt-payload-pattern", default=None,
                   help="value for :CONFigure:BT:PAYLoad:PATTern; defaults to the "
                        "pattern matching --payload")
    b.add_argument("--bt-drate", default=None,
                   help="value for :CONFigure:BT:DRATE; defaults from --rate for LE")
    b.add_argument("--bt-packet-type", default="PacketTypeLE",
                   help="value for :CONFigure:BT:PACKet:TYPE")
    _add_tx_common(b)

    wr = sub.add_parser("wifi-rx")
    wr.add_argument("--channel", type=int, default=6)
    wr.add_argument("--rate", default="G_6M", choices=WifiRate.__members__)
    _add_rx_common(wr, "Wifi_6M", 0.10)

    ex = sub.add_parser("wifi-external",
                        help="measure a signal from an external generator (no DUT); "
                             "prompts before measuring")
    ex.add_argument("--frequency-hz", type=float, default=5.21e9,
                    help="center frequency; must match the generator")
    ex.add_argument("--wlan-standard", default="AX")
    ex.add_argument("--wlan-bw", default="BW80")
    ex.add_argument("--wlan-band", default=None,
                    help="value for :CONFigure:WLAN:FREQuency:BAND (e.g. the 5 GHz band)")
    ex.add_argument("--sem", action="store_true", help="also run SEM")
    _add_tx_common(ex)
    ex.set_defaults(ref_level=-10.0)

    br = sub.add_parser("ble-rx")
    br.add_argument("--channel", type=int, default=21,
                   help="BLE RF channel 0-39 (f = 2402 + 2*ch MHz)")
    br.add_argument("--rate", default="LE_1M", choices=BleRate.__members__)
    _add_rx_common(br, "BLE_1M", 0.308)

    return ap


def run(a) -> List[Dict]:
    rx_port = a.rx_port if a.rx_port is not None else a.tx_port
    kw = dict(ip_addr=a.ip, timeout=a.visa_timeout_ms)
    results = []
    if a.test == "wifi-external":
        with session(WifiClient(rf_port=a.tx_port, **kw)) as wlan:
            results.append(wifi_external(wlan, a))
        return results
    if not a.dut_service:
        raise SystemExit("--dut-service is required for DUT tests")
    with DutClient(a.dut_service, com_port=a.dut_port) as dut:
        if a.test == "wifi-tx":
            with session(WifiClient(rf_port=a.tx_port, **kw)) as wlan:
                results.append(wifi_tx(dut, wlan, a))
        elif a.test == "ble-tx":
            with session(BTClient(rf_port=a.tx_port, **kw)) as bt:
                results.append(ble_tx(dut, bt, a))
        elif a.test in ("wifi-rx", "ble-rx"):
            with session(RfsgClient(rf_port=rx_port, **kw)) as rfsg:
                results.append(rx_sweep(dut, rfsg, a,
                                        is_ble=a.test == "ble-rx"))
    return results


def save(results: List[Dict], out_dir: str) -> Path:
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    path = Path(out_dir) / f"{datetime.now():%Y%m%d_%H%M%S}_{results[0]['test']}.json"
    path.write_text(json.dumps(results, indent=2, default=str))
    return path


def print_summary(r: Dict) -> None:
    print(f"\n== {r['test']} ==")
    if "points" in r:
        print(f"{'RFSG dBm':>9} {'@DUT dBm':>9} {'rx/sent':>11} {'PER':>7} {'RSSI':>7}")
        for p in r["points"]:
            print(f"{p['rfsg_power_dbm']:9.1f} {p['power_at_dut_dbm']:9.1f} "
                  f"{p['received']:5d}/{p['sent']:<5d} {p['per']*100:6.1f}% "
                  f"{p['rssi_dbm']:7.1f}")
        s = r["sensitivity_dbm"]
        print(f"Sensitivity (PER <= {r['per_limit']*100:.1f}%): "
              f"{'not reached' if s is None else f'{s:.1f} dBm at DUT'}")
    elif r.get("skipped"):
        print("  skipped")
    else:
        for k, v in r["summary"].items():
            print(f"  {k}: {v}")


def main() -> None:
    a = build_parser().parse_args()
    logging.basicConfig(level=logging.DEBUG if a.verbose else logging.INFO,
                        format="%(asctime)s %(levelname)-5s %(message)s",
                        datefmt="%H:%M:%S")
    results = run(a)
    for r in results:
        print_summary(r)
    print(f"\nSaved {save(results, a.out_dir)}")


if __name__ == "__main__":
    main()
