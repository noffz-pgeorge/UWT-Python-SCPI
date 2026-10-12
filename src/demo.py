"""ESP32-C3 RF demo: drive the DUT through the DUT control gRPC service and
measure/stimulate it through the Noffz UWT SCPI API (VST analyzer + RFSG)
from a Linux machine.

Four flows:
    wifi-tx     DUT transmits Wi-Fi  -> analyzer measures TXP + ModAcc (+ SEM)
    ble-tx      DUT transmits BLE    -> analyzer measures TXP + ModAcc + 20 dB BW
    wifi-rx     RFSG plays Wi-Fi packets at a power sweep -> DUT counts -> PER
    ble-rx      RFSG plays BLE packets at a power sweep   -> DUT counts -> PER

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
from typing import Dict, Iterator, List, Optional

from bt_client import BTClient
from dut_grpc import (BLE_POWER_LEVEL_DBM, BleRate, DutClient, WifiRate,
                      ble_channel_freq_hz, wifi_channel_freq_hz)
from rfsg_client import RfsgClient
from wifi_client import WifiClient

log = logging.getLogger("demo")

BUSY_STATES = {"PROCESSING", "PENDING", "ACTIVE"}


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
    freq = ble_channel_freq_hz(a.channel_index)
    log.info("BLE TX: idx%d (%.0f MHz), %s, level %d (~%d dBm)",
             a.channel_index, freq / 1e6, rate.name, a.power_level,
             BLE_POWER_LEVEL_DBM[a.power_level])

    bt.config_signal_and_packet(**_drop_none(dict(
        center_frequency=freq,
        drate=a.bt_drate,
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
    bt.config_20db_bandwidth(enable=True)

    dut.ble_tx(a.channel_index, a.power_level, length=a.payload_length,
               rate=rate)
    try:
        time.sleep(a.settle_s)
        bt.initiate(a.result_space)
        wait_measurement(bt, a.meas_timeout_s)
        result = {
            "txp": bt.fetch_tx_power(a.result_index),
            "modacc": bt.fetch_modacc(a.result_index),
            "20db_bw": bt.fetch_20db_bandwidth(a.result_index),
        }
    finally:
        dut.stop()

    return {"test": "ble_tx", "channel_index": a.channel_index,
            "freq_hz": freq, "rate": rate.name,
            "power_level": a.power_level,
            "summary": {"txp": result["txp"],
                        "20db_bw_hz": result["20db_bw"].get("bandwidth")},
            "detail": result}


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
        freq = ble_channel_freq_hz(a.channel_index)
        rate = BleRate[a.rate]
        start_rx = lambda: dut.ble_rx_start(a.channel_index, rate)
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
    ap.add_argument("--dut-service", required=True,
                    help="DUT control gRPC service, host:port")
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
    b.add_argument("--channel-index", type=int, default=19)
    b.add_argument("--rate", default="LE_1M", choices=BleRate.__members__)
    b.add_argument("--power-level", type=int, default=15, choices=range(16))
    b.add_argument("--payload-length", type=int, default=37)
    b.add_argument("--bt-drate", default=None,
                   help="value for :CONFigure:BT:DRATE, e.g. the LE 1M enum")
    b.add_argument("--bt-packet-type", default=None)
    _add_tx_common(b)

    wr = sub.add_parser("wifi-rx")
    wr.add_argument("--channel", type=int, default=6)
    wr.add_argument("--rate", default="G_6M", choices=WifiRate.__members__)
    _add_rx_common(wr, "Wifi_6M", 0.10)

    br = sub.add_parser("ble-rx")
    br.add_argument("--channel-index", type=int, default=19)
    br.add_argument("--rate", default="LE_1M", choices=BleRate.__members__)
    _add_rx_common(br, "BLE_1M", 0.308)

    return ap


def run(a) -> List[Dict]:
    rx_port = a.rx_port if a.rx_port is not None else a.tx_port
    kw = dict(ip_addr=a.ip, timeout=a.visa_timeout_ms)
    results = []
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