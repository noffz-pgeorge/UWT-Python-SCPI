"""Scripted RF demo: sweep a fixed set of Wi-Fi and BLE cases on the DUT.

Edit the settings below, then run it or debug it from VS Code (F5, "Demo
sweep"). Everything opens once: one DUT session and one analyzer session per
standard, reused across the cases. Each case is wrapped so a failure is logged
and the sweep moves on (set STOP_ON_ERROR to stop at the first one instead).

The measurement code is shared with demo.py, so a case here behaves exactly
like the matching CLI command. Any CLI option can be overridden per case with
its argparse name (e.g. ref_level, trigger_threshold, wlan_standard).
"""
from __future__ import annotations

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, List

import demo
from ..uwt import BTClient, RfsgClient, WifiClient
from dut import DutClient

# --------------------------------------------------------------------------- #
# Station
# --------------------------------------------------------------------------- #
UWT_IP = "192.168.141.60"
DUT_SERVICE = "192.168.141.60:50051"
DUT_PORT = "COM8"           # "" = the service's DefaultPort
TX_PORT = 1                 # switch port for analyzer measurements
RX_PORT = 1                 # switch port for the RFSG
WIFI_EXTERNAL_PORT = 2
OUT_DIR = "results"

STOP_ON_ERROR = False       # True: stop at the first failing case (handy when debugging)
LOG_LEVEL = logging.INFO    # logging.DEBUG shows every DUT call

# --------------------------------------------------------------------------- #
# Cases. Keys are demo.py option names; anything omitted uses the CLI default.
# --------------------------------------------------------------------------- #
WIFI_COMMON = dict(wlan_standard="A_G", wlan_bw="BW20", ref_level=-28.0)

WIFI_TX_CASES: List[Dict] = [
    dict(name="Wi-Fi ch1 6M",   channel=1,  rate="G_6M"),
    dict(name="Wi-Fi ch6 24M",  channel=6,  rate="G_24M"),
    dict(name="Wi-Fi ch11 54M", channel=11, rate="G_54M"),
]

# Bluetooth RF test payloads: 10101010 (P_1010) for power, frequency offset,
# drift and df2; 11110000 (P_00001111 on the DUT, sent LSB first) for df1.
# The analyzer's payload pattern is set to match the DUT payload automatically.
BLE_COMMON = dict(power_level=15, ref_level=-28.0, trigger_threshold=-45.0,
                  payload="P_1010")

BLE_TX_CASES: List[Dict] = [
    # channel = BLE RF channel 0-39, f = 2402 + 2*ch MHz
    dict(name="BLE 2402 1M", channel=0,  rate="LE_1M"),
    dict(name="BLE 2444 1M", channel=21, rate="LE_1M"),
    dict(name="BLE 2480 2M", channel=39, rate="LE_2M"),
    dict(name="BLE 2444 1M df1", channel=21, rate="LE_1M", payload="P_00001111"),
    # Diagnostics for the 2480 2M result: rate vs. channel
    dict(name="BLE 2444 2M", channel=21, rate="LE_2M"),
    dict(name="BLE 2480 1M", channel=39, rate="LE_1M"),
]

# External source: the analyzer is configured, the sweep pauses for you to start
# the waveform on the generator (e.g. RFmx SFP), and measures when you press
# Enter ('s' + Enter skips). No DUT. frequency_hz must match the generator.
RUN_WIFI_EXTERNAL = True

WIFI_EXTERNAL_CASES: List[Dict] = [
    dict(name="Wi-Fi 6 80M ext", frequency_hz=7.015e9, wlan_standard="AX",
         wlan_bw="BW80", ref_level=-10.0, sem=True),
]

# RX sweeps need RFSG waveforms; fill these in and set the RUN flags to enable.
RUN_WIFI_RX = False
RUN_BLE_RX = False

WIFI_RX_CASES: List[Dict] = [
    dict(name="Wi-Fi RX ch6 6M", channel=6, rate="G_6M",
         waveform="<wifi 6M waveform>", packets_per_waveform=100,
         start=-50.0, stop=-90.0, step=-5.0),
]

BLE_RX_CASES: List[Dict] = [
    dict(name="BLE RX 2444 1M", channel=21, rate="LE_1M",
         waveform="<ble 1M waveform, access address 0x71764129>",
         packets_per_waveform=100, start=-50.0, stop=-95.0, step=-5.0),
]

log = logging.getLogger("sweep")


# --------------------------------------------------------------------------- #
# Plumbing
# --------------------------------------------------------------------------- #
def settings(test: str, **overrides):
    """CLI defaults for `test`, with overrides applied. Unknown keys raise,
    so a typo in a case doesn't silently fall back to a default."""
    argv = ["--ip", UWT_IP, "--dut-service", DUT_SERVICE, "--dut-port", DUT_PORT,
            "--tx-port", str(TX_PORT), "--rx-port", str(RX_PORT),
            "--out-dir", OUT_DIR, test]
    if test.endswith("-rx"):
        argv += ["--packets-per-waveform", "1"]   # required by the CLI; overridden below
    a = demo.build_parser().parse_args(argv)
    for key, value in overrides.items():
        if not hasattr(a, key):
            raise AttributeError(f"Unknown setting {key!r} for {test}")
        setattr(a, key, value)
    return a


def build(test: str, cases: List[Dict], common: Dict) -> List:
    """Resolve each case to (name, settings). Raises on unknown keys."""
    out = []
    for case in cases:
        case = dict(case)
        name = case.pop("name")
        out.append((name, settings(test, **{**common, **case})))
    return out


def run_case(test: str, name: str, a, fn: Callable) -> Dict:
    log.info("=== %s ===", name)
    t0 = time.monotonic()
    try:
        result = fn(a)                     # <- breakpoint here to step into a case
        result["case"] = name
        result["duration_s"] = round(time.monotonic() - t0, 2)
        demo.print_summary(result)
        return result
    except Exception as e:
        log.exception("%s failed", name)
        if STOP_ON_ERROR:
            raise
        return {"test": test.replace("-", "_"), "case": name, "error": f"{type(e).__name__}: {e}"}


def _num(text, scale=1.0, fmt="{:.2f}"):
    try:
        return fmt.format(float(text) * scale)
    except (TypeError, ValueError):
        return str(text)


def print_table(results: List[Dict]) -> None:
    print("\n" + "=" * 124)
    print(f"{'Case':<18} {'Freq MHz':>8}  Result")
    print("-" * 124)
    for r in results:
        freq = _num(r.get("freq_hz"), 1e-6, "{:.0f}") if "freq_hz" in r else ""
        if "error" in r:
            line = "ERROR " + r["error"]
        elif r.get("skipped"):
            line = "SKIPPED"
        elif r["test"] == "wifi_tx":
            s = r["summary"]
            line = (f"pwr {_num(s.get('burst_power_dbm'))} dBm  "
                    f"EVM {_num(s.get('rms_evm'))} dB  "
                    f"ferr {_num(s.get('freq_error_hz'), 1e-3)} kHz  "
                    f"rate idx {s.get('detected_rate_index')}  CRC {s.get('psdu_crc')}")
        elif r["test"] == "wifi_external":
            s = r["summary"]
            line = (f"{r.get('standard')} {r.get('bandwidth')}  "
                    f"pwr {_num(s.get('burst_power_dbm'))} dBm  "
                    f"EVM {_num(s.get('rms_evm'))} dB  "
                    f"ferr {_num(s.get('freq_error_hz'), 1e-3)} kHz  "
                    f"MCS {s.get('detected_mcs')}  CRC {s.get('psdu_crc')}"
                    + (f"  SEM {s.get('sem_status')}" if "sem_status" in s else ""))
        elif r["test"] == "ble_tx":
            s = r["summary"]
            # Initial frequency offset when the analyzer reports it, else the
            # peak frequency error (marked "pk").
            foff, label = s.get("freq_offset_hz"), "foff"
            if str(foff).strip().upper() in ("NAN", "NONE", ""):
                foff, label = s.get("peak_freq_error_hz"), "ferr pk"
            line = (f"pwr {_num(s.get('avg_power_dbm'))} dBm  "
                    f"{label} {_num(foff, 1e-3)} kHz  "
                    f"drift {_num(s.get('peak_drift_hz'), 1e-3)} kHz  "
                    f"df1 {_num(s.get('df1avg_hz'), 1e-3, '{:.0f}')}  "
                    f"df2 {_num(s.get('df2avg_hz'), 1e-3, '{:.0f}')} kHz  "
                    f"df2max {_num(s.get('df2max_above_threshold_pct'), 1, '{:.1f}')}%  "
                    f"[{r.get('payload')}]")
        else:
            s = r.get("sensitivity_dbm")
            line = f"sensitivity {'not reached' if s is None else f'{s:.1f} dBm'}  ({len(r['points'])} steps)"
        print(f"{r['case']:<18} {freq:>8}  {line}")
    print("=" * 124)


def save(results: List[Dict]) -> Path:
    Path(OUT_DIR).mkdir(parents=True, exist_ok=True)
    path = Path(OUT_DIR) / f"{datetime.now():%Y%m%d_%H%M%S}_sweep.json"
    path.write_text(json.dumps(results, indent=2, default=str))
    return path


# --------------------------------------------------------------------------- #
# Sweep
# --------------------------------------------------------------------------- #
def run_dut_cases(dut, kw, wifi_tx_cases, ble_tx_cases, wifi_rx_cases,
                  ble_rx_cases) -> List[Dict]:
    results: List[Dict] = []

    if wifi_tx_cases:
        with demo.session(WifiClient(rf_port=TX_PORT, **kw)) as wlan:
            for name, a in wifi_tx_cases:
                results.append(run_case("wifi-tx", name, a,
                                        lambda a: demo.wifi_tx(dut, wlan, a)))

    if ble_tx_cases:
        with demo.session(BTClient(rf_port=TX_PORT, **kw)) as bt:
            for name, a in ble_tx_cases:
                results.append(run_case("ble-tx", name, a,
                                        lambda a: demo.ble_tx(dut, bt, a)))

    if wifi_rx_cases or ble_rx_cases:
        with demo.session(RfsgClient(rf_port=RX_PORT, **kw)) as rfsg:
            for name, a in wifi_rx_cases:
                results.append(run_case("wifi-rx", name, a,
                                        lambda a: demo.rx_sweep(dut, rfsg, a, is_ble=False)))
            for name, a in ble_rx_cases:
                results.append(run_case("ble-rx", name, a,
                                        lambda a: demo.rx_sweep(dut, rfsg, a, is_ble=True)))
    return results


def main() -> None:
    logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s %(levelname)-5s %(message)s",
                        datefmt="%H:%M:%S")
    kw = dict(ip_addr=UWT_IP, timeout=10000)
    results: List[Dict] = []

    # Resolve every case first, so a typo fails before any hardware is touched.
    wifi_tx_cases = build("wifi-tx", WIFI_TX_CASES, WIFI_COMMON)
    ble_tx_cases = build("ble-tx", BLE_TX_CASES, BLE_COMMON)
    wifi_rx_cases = build("wifi-rx", WIFI_RX_CASES, {}) if RUN_WIFI_RX else []
    ble_rx_cases = build("ble-rx", BLE_RX_CASES, {}) if RUN_BLE_RX else []
    external_cases = (build("wifi-external", WIFI_EXTERNAL_CASES, {})
                      if RUN_WIFI_EXTERNAL else [])

    if wifi_tx_cases or ble_tx_cases or wifi_rx_cases or ble_rx_cases:
        with DutClient(DUT_SERVICE, com_port=DUT_PORT) as dut:
            log.info("DUT: %s", dut.status())
            results += run_dut_cases(dut, kw, wifi_tx_cases, ble_tx_cases,
                                     wifi_rx_cases, ble_rx_cases)

    # External-source cases don't use the DUT.
    if external_cases:
        with demo.session(WifiClient(rf_port=WIFI_EXTERNAL_PORT, **kw)) as wlan:
            for name, a in external_cases:
                results.append(run_case("wifi-external", name, a,
                                        lambda a: demo.wifi_external(wlan, a)))

    print_table(results)
    print(f"Saved {save(results)}")


if __name__ == "__main__":
    main()
