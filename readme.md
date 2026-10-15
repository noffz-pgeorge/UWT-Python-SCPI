# UWT Python SCPI

Python clients for the NOFFZ UWT RF test service (SCPI over VXI-11), plus a gRPC
service for controlling an ESP32-C3 DUT, and an end-to-end RF demo that uses both.

```
Linux / dev container (python/demos/demo.py)
   ├── gRPC :50051 ──────► Windows PC: Noffz.Dut.Grpc.Service ── COM ──► ESP32-C3 (RF chamber)
   └── VXI-11 SCPI ──────► UWT / WPF service ──► NI VST + 32-port switch
```

- **TX tests:** the DUT transmits Wi-Fi or BLE. The VST measures power, ModAcc (EVM,
  frequency error, IQ impairments) and optionally SEM.
- **RX tests:** the VST's RFSG plays packets across a power sweep, the DUT counts them,
  and the demo reports PER, RSSI and sensitivity.

## Repository layout

```
.devcontainer/                     optional Python dev container
docs/                              NOFFZ UWT SCPI Commands Reference
proto/dut_control.proto            DUT control gRPC API (shared by .NET and Python)
dotnet/                            DUT control service and .NET client (Windows, .NET 8)
  Noffz.Dut.slnx
  Noffz.Espressif.ESP32C3.DutControls/   serial driver for the ESP32-C3 RF test firmware
  Noffz.Dut.Grpc.Service/                gRPC service (console app or Windows Service)
  Noffz.Dut.Grpc.Client/                 .NET client library (DutClient)
  Noffz.Dut.Grpc.Client.Sample/          smoke test console app
python/                            Python side (installable package: rf_demo)
  pyproject.toml                   package metadata and dependencies
  src/rf_demo/
    uwt/                           UWT SCPI clients
      instrument.py                VXI-11 base class; rf_port selects the switch port (inst<N>)
      wifi.py  bt.py  rfsg.py      Wi-Fi, BLE and RFSG clients
    dut/                           Python client for the DUT service
      client.py
      _generated/                  protoc output; do not edit (see tools/generate_stubs.sh)
  demos/
    demo.py                        RF demo CLI
    demo_sweep.py                  runs a predefined set of demo cases
  tools/generate_stubs.sh          regenerates the Python gRPC stubs from proto/
results/                           demo output (JSON), not tracked
```

---

## Development Guide

### Python setup

The Python code is an installable package. From the repo root:

```bash
pip install -e "python/[dev]"
```

`-e` (editable) points Python at the source folder, so `import rf_demo` works from any
directory and code changes take effect without reinstalling. The `[dev]` extra adds
`grpcio-tools`, which is only needed to regenerate the gRPC stubs. Dependencies are listed
in `python/pyproject.toml`.

### Optional: Development Containers (Docker + VS Code)

This project includes an **optional Dev Container** configuration that makes Python
development reproducible and isolated, without installing specific Python versions or
dependencies on the host.

> **Important:** The Dev Container is optional. A locally installed Python environment
> works too; run the install command from [Python setup](#python-setup).

#### What is a Dev Container?

A Dev Container is a Docker-based development environment that VS Code attaches to.
VS Code runs your workspace **inside a container** that has:

- A pinned Python version
- All required dependencies
- A consistent Linux environment

This avoids problems like:
- "Works on my machine"
- Conflicting Python versions
- Dependency drift between developers or customers

The package is installed (`pip install -e "python/[dev]"`) when the container is created.
After changing dependencies in `python/pyproject.toml`, rerun that command or run
**Dev Containers: Rebuild Container**.

The Dev Container is Python-only. The .NET service is built and run on Windows (see
[DUT control service](#dut-control-service-windows)).

### Dev Container setup when using WSL2 and instrument communication

When the dev container runs inside WSL2 on Windows, Docker needs mirrored networking and
direct NIC passthrough to communicate with instruments connected via Ethernet.

#### Prerequisites

1. **Configure WSL2 mirrored networking**

   Create or edit `.wslconfig` in your Windows user profile folder
   (`%USERPROFILE%\.wslconfig`, i.e. `C:\Users\<YourUsername>\.wslconfig`):

   ```ini
   [wsl2]
   networkingMode=mirrored
   ```

2. **Restart WSL**

   ```powershell
   wsl --shutdown
   ```

3. **Create the pass-through Docker network**

   Find the name of the network adapter connected to your instruments (for example
   "Ethernet 4", from `ipconfig` or `Get-NetAdapter`). Then run in Windows PowerShell:

   ```powershell
   docker network create -d transparent -o com.docker.network.windowsshim.interface="Ethernet 4" host_ethernet_net
   ```

4. **Open the project in the container**

   Use VS Code's **Reopen in Container** prompt.

From inside the container, reach the UWT service and the DUT service by their LAN IP
addresses. If you run the DUT service on your own PC, use that PC's LAN IP as well.

---

## DUT control service (Windows)

The service owns the ESP32-C3's COM port and exposes it over gRPC. The DUT runs
Espressif's RF non-signaling test firmware (RF test bin). Run the service on the PC
the DUT is plugged into, which is usually the same PC as the UWT/WPF service.

### Build

Requires the .NET 8 SDK or later.

```powershell
cd dotnet
dotnet build Noffz.Dut.slnx -c Release
```

### Configure

Edit `dotnet/Noffz.Dut.Grpc.Service/appsettings.json`:

```json
"Dut": { "DefaultPort": "COM8", "AutoOpen": false, "ReadTimeoutMs": 3000 },
"Kestrel": { "Endpoints": { "Grpc": { "Url": "http://0.0.0.0:50051", "Protocols": "Http2" } } }
```

- **`DefaultPort`:** used when a client opens a session without naming a port.
- **`AutoOpen`:** opens `DefaultPort` when the service starts.
- **Kestrel endpoint:** the gRPC listen address (plaintext HTTP/2).

### Run

Run it as a console app:

```powershell
dotnet run --project Noffz.Dut.Grpc.Service -c Release
```

Or install it as a Windows Service alongside the WPF service:

```powershell
dotnet publish Noffz.Dut.Grpc.Service -c Release -r win-x64 --self-contained false -o C:\Noffz\DutControl
sc.exe create NoffzDutControl binPath= "C:\Noffz\DutControl\Noffz.Dut.Grpc.Service.exe" start= auto
sc.exe start NoffzDutControl
New-NetFirewallRule -DisplayName "Noffz DUT gRPC" -Direction Inbound -Protocol TCP -LocalPort 50051 -Action Allow
```

### Smoke test

The sample app calls every RPC once (TX, stop, RX, fetch):

```powershell
dotnet run --project Noffz.Dut.Grpc.Client.Sample -- http://<service-pc>:50051 COM8
```

gRPC reflection is enabled, so `grpcurl -plaintext <service-pc>:50051 list` also works.

### Behavior

- One serial session, one command at a time. Concurrent calls queue.
- Starting any TX/RX mode sends `cmdstop` first if the DUT is busy.
- `FetchWlanRx` / `FetchBleRx` stop RX and return the packet counts. They fail with
  `FAILED_PRECONDITION` unless the matching RX mode was started.
- Error codes:
  - `FAILED_PRECONDITION`: no session open, or the DUT is in the wrong mode.
  - `INVALID_ARGUMENT`: out-of-range channel or power level.
  - `DEADLINE_EXCEEDED`: the firmware didn't answer.
  - `UNAVAILABLE`: serial port error.

`ESP32C3Control` returns the firmware's reply from its TX/RX start methods and adds
`BtRxFetchResult` / `WlanRxFetchResult`. The service depends on these, so a build of the
original `ESP32C3Control` DLL won't work with it.

---

## Python clients

### DUT control client

```python
from rf_demo.dut import DutClient, WifiRate

with DutClient("<service-pc>:50051", com_port="COM8") as dut:
    dut.wifi_tx(6, WifiRate.G_6M)          # transmit until stop()
    dut.stop()

    dut.wifi_rx_start(6, WifiRate.G_6M)    # count packets...
    res = dut.wifi_rx_stop()               # ...stop and fetch
    print(res.desired, res.per(1000), res.rssi_dbm)
```

`com_port=""` opens the service's default port. `com_port=None` connects without opening a
session. Connectivity check:

```bash
python -c "from rf_demo.dut import DutClient; print(DutClient('<service-pc>:50051', com_port=None).open().status())"
```

### UWT SCPI clients

```python
from rf_demo.uwt import BTClient, RfsgClient, WifiClient
```

### Regenerating the gRPC stubs

The stubs in `python/src/rf_demo/dut/_generated/` are checked in and need `grpcio>=1.84`
and `protobuf>=7.35`. After changing `proto/dut_control.proto`, or to match older package
versions, run (requires the `[dev]` extra):

```bash
python/tools/generate_stubs.sh
```

The .NET projects generate their code from the same proto at build time.

---

## RF demo

Run from the repo root (results are written to `results/` relative to the working
directory):

```bash
python python/demos/demo.py --ip <uwt-ip> --dut-service <service-pc>:50051 --dut-port COM8 --tx-port 1 -v <test> [options]
python python/demos/demo.py <test> --help        # all options for a test
```

In VS Code, the configurations in `.vscode/launch.json` run the same commands under the
debugger.

| Test | What happens |
|---|---|
| `wifi-tx` | DUT transmits Wi-Fi; the analyzer measures TXP, ModAcc (OFDM or DSSS by rate) and optionally SEM (`--sem`) |
| `ble-tx` | DUT transmits BLE; the analyzer measures TXP and ModAcc (plus 20 dB bandwidth for Classic packet types) |
| `wifi-rx` | RFSG power sweep; the DUT counts Wi-Fi packets; PER, RSSI and sensitivity |
| `ble-rx` | Same for BLE |
| `wifi-external` | Analyzer is set up (default 802.11ax, 80 MHz, 5.21 GHz), then waits for you to start a waveform on an external generator such as the RFmx SFP and press Enter; no DUT |

Results are printed and saved as JSON in `results/`.

### Examples

```bash
# Wi-Fi TX, channel 6, 802.11g 6 Mbps
python python/demos/demo.py --ip 192.168.141.60 --dut-service 192.168.141.60:50051 --dut-port COM8 --tx-port 1 -v \
    wifi-tx --channel 6 --rate G_6M --wlan-standard A_G --wlan-bw BW20

# BLE TX, RF channel 21 (2402 + 2*21 = 2444 MHz)
python python/demos/demo.py ... ble-tx --channel 21

# Wi-Fi RX sweep: start coarse to confirm the DUT counts packets, then go finer
python python/demos/demo.py ... wifi-rx --waveform <name> --packets-per-waveform <n> --start -50 --stop -90 --step -5
```

### External source (802.11ax)

```bash
python python/demos/demo.py --ip 192.168.141.60 --tx-port 1 -v wifi-external \
    --frequency-hz 5.21e9 --wlan-standard AX --wlan-bw BW80 --ref-level -10 --sem
```

The demo configures the analyzer, then prompts. Start the waveform in the generator
(same center frequency), press Enter to measure, or type `s` to skip. In
`python/demos/demo_sweep.py` these cases are in `WIFI_EXTERNAL_CASES` and run after the
DUT cases. `--dut-service` isn't needed for this test. The waveform needs idle time
between packets for the RF0 trigger; for a continuous waveform pass `--trigger-source ""`.

### Measurement settings that matter

- **Reference level** (`--ref-level`, default -28 dBm): set it about 8 dB above the peak
  power at the VST. In the chamber the radiated path loss is about 55–60 dB, so a 20 dBm
  DUT peaks around -36 dBm. A ref level sized for a conducted setup leaves the signal near
  the bottom of the ADC range.
- **Trigger** (`--trigger-source RF0`, threshold -20, delay -20 µs, quiet time 5 µs): the
  DUT transmits bursts at about 30 % duty cycle. Without an IQ power edge trigger the
  capture starts mid-packet and ModAcc results are meaningless: wrong detected rate,
  hundreds of kHz of "frequency error", huge IQ errors. The demo also enables TXP burst
  detection and ModAcc burst start detection.
- **Standard and bandwidth:** pass `--wlan-standard A_G --wlan-bw BW20` for legacy OFDM
  rates. Values are listed under `:CONFigure:WLAN:STANdard` and
  `:CONFigure:WLAN:CHANnel:BANDwidth` in the SCPI reference.
- **BLE channel numbering:** `--channel` is the BLE RF channel (0–39), f = 2402 + 2×ch MHz,
  which is what the firmware's `fcc_le_tx` takes. It is not the link-layer channel index
  (advertising channel 37 is RF channel 0, 2402 MHz).
- **BLE analyzer setup:** the demo sets `PacketTypeLE` and the data rate from `--rate`, and
  turns 20 dB bandwidth off for LE (it is a BR/EDR measurement and makes LE results NaN).
- **`psdu_crc: FAIL` on Wi-Fi TX is expected** with the RF test firmware. Its test payloads
  don't appear to carry a valid 802.11 FCS. Use the detected rate, symbol count, EVM and
  frequency error to judge the decode.
- **RX waveforms:** the DUT only counts packets at its configured rate ("desired"), and
  for BLE only packets whose access address matches its sync word (`0x71764129` by
  default). `--packets-per-waveform` must equal the number of packets in one playback of
  the waveform, or PER is wrong.

### Troubleshooting

| Symptom | Likely cause |
|---|---|
| `ModuleNotFoundError: No module named 'rf_demo'` | Package not installed in this environment; run `pip install -e "python/[dev]"` from the repo root |
| `VI_ERROR_RSRC_NFOUND`, "can't connect to server" on port 111 | The UWT service isn't configured for SCPI/VXI-11, or the firewall blocks port 111 and the VXI-11 core port |
| `DUT service not reachable` | DUT service not running, wrong IP, or port 50051 blocked by the firewall |
| `TimeoutError ... last state` | Trigger never fired (check `--trigger-threshold`) or wrong `--result-space` |
| `RFSG still generating after 30s` | Waveform repeats continuously; set `--repetition-mode` to finite |
| RX: 0 received at strong levels | Waveform rate or sync word doesn't match the DUT; check `raw` in the JSON |
| `DEADLINE_EXCEEDED` from the DUT service | Firmware didn't answer: wrong COM port, board not running the RF test bin, or it needs a power cycle |