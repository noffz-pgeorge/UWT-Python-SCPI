"""Python client for the DUT control gRPC service.
Method names and signatures match the earlier serial driver, so code
written against that keeps working.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import Optional

import grpc
from google.protobuf.empty_pb2 import Empty

from rf_demo.dut._generated import dut_control_pb2 as pb
from rf_demo.dut._generated import dut_control_pb2_grpc as pb_grpc

DEFAULT_SYNCW = 0x71764129


# --------------------------------------------------------------------------- #
# Enums: values are the proto/firmware codes, so they pass straight through.
# --------------------------------------------------------------------------- #
class WifiRate(IntEnum):
    B_1M = pb.WLAN_DATA_RATE_B_1M
    B_2M = pb.WLAN_DATA_RATE_B_2M
    B_5M5 = pb.WLAN_DATA_RATE_B_5M5
    B_11M = pb.WLAN_DATA_RATE_B_11M
    G_6M = pb.WLAN_DATA_RATE_G_6M
    G_9M = pb.WLAN_DATA_RATE_G_9M
    G_12M = pb.WLAN_DATA_RATE_G_12M
    G_18M = pb.WLAN_DATA_RATE_G_18M
    G_24M = pb.WLAN_DATA_RATE_G_24M
    G_36M = pb.WLAN_DATA_RATE_G_36M
    G_48M = pb.WLAN_DATA_RATE_G_48M
    G_54M = pb.WLAN_DATA_RATE_G_54M
    MCS0 = pb.WLAN_DATA_RATE_N_MCS0
    MCS1 = pb.WLAN_DATA_RATE_N_MCS1
    MCS2 = pb.WLAN_DATA_RATE_N_MCS2
    MCS3 = pb.WLAN_DATA_RATE_N_MCS3
    MCS4 = pb.WLAN_DATA_RATE_N_MCS4
    MCS5 = pb.WLAN_DATA_RATE_N_MCS5
    MCS6 = pb.WLAN_DATA_RATE_N_MCS6
    MCS7 = pb.WLAN_DATA_RATE_N_MCS7

    @property
    def is_dsss(self) -> bool:
        return self <= WifiRate.B_11M


class BleRate(IntEnum):
    LE_1M = pb.BLE_RATE_LE_1M
    LE_2M = pb.BLE_RATE_LE_2M
    LE_CODED_125K = pb.BLE_RATE_LE_CODED_125K
    LE_CODED_500K = pb.BLE_RATE_LE_CODED_500K


class BlePayload(IntEnum):
    P_1010 = pb.BLE_PAYLOAD_PATTERN_P1010
    P_00001111 = pb.BLE_PAYLOAD_PATTERN_P00001111
    PRBS9 = pb.BLE_PAYLOAD_PATTERN_PRBS9


class DutState(IntEnum):
    CLOSED = pb.DUT_STATE_CLOSED
    IDLE = pb.DUT_STATE_IDLE
    BLE_TX = pb.DUT_STATE_BLE_TX
    WLAN_TX = pb.DUT_STATE_WLAN_TX
    BLE_RX = pb.DUT_STATE_BLE_RX
    WLAN_RX = pb.DUT_STATE_WLAN_RX


# BLE TX power level index -> nominal dBm (ESP32-C3)
BLE_POWER_LEVEL_DBM = {i: d for i, d in enumerate(
    [-24, -21, -18, -15, -12, -9, -6, -3, 0, 3, 6, 9, 12, 15, 18, 20])}


def wifi_channel_freq_hz(channel: int) -> float:
    """2.4 GHz Wi-Fi channel number -> center frequency in Hz."""
    if channel == 14:
        return 2484e6
    if 1 <= channel <= 13:
        return (2407 + 5 * channel) * 1e6
    raise ValueError(f"Unsupported 2.4 GHz channel {channel}")


def ble_channel_freq_hz(channel: int) -> float:
    """BLE RF channel (0-39) -> center frequency in Hz: 2402 + 2*channel MHz.

    This is the channel number the RF test firmware's fcc_le_tx / rw_le_rx_per
    take (RF channel, not the link-layer channel index: advertising channel
    37 is RF channel 0 = 2402 MHz).
    """
    if not 0 <= channel <= 39:
        raise ValueError(f"Invalid BLE RF channel {channel} (0-39)")
    return (2402 + 2 * channel) * 1e6


# --------------------------------------------------------------------------- #
# Results
# --------------------------------------------------------------------------- #
@dataclass
class WifiRxResult:
    correct: int          # all packets received
    desired: int          # packets at the configured rate
    rssi_dbm: float
    raw: str

    def per(self, sent: int) -> float:
        return 1.0 - self.desired / sent if sent else float("nan")


@dataclass
class BleRxResult:
    total: int            # Res[0]
    desired: int          # Res[1]
    rssi_dbm: float
    raw: str

    def per(self, sent: int) -> float:
        return 1.0 - self.desired / sent if sent else float("nan")


@dataclass
class SessionStatus:
    is_open: bool
    port: str
    state: DutState


class DutError(RuntimeError):
    """A DUT service call failed. `code` is the grpc.StatusCode."""

    def __init__(self, method: str, err: grpc.RpcError):
        self.code = err.code()
        self.details = err.details()
        super().__init__(f"{method} failed: {self.code.name}: {self.details}")


# --------------------------------------------------------------------------- #
# Client
# --------------------------------------------------------------------------- #
class DutClient:
    """Talks to the DutControl gRPC service.

    Args:
        target: "host:port" of the service (plaintext HTTP/2).
        com_port: serial port on the service host to open on connect. Empty
            string opens the service's configured default port; None skips
            OpenSession (use when the service auto-opens the port).
        timeout_s: per-call deadline; keep it above the service's read timeout.
        close_session_on_exit: send CloseSession when this client closes.
    """

    def __init__(self, target: str, com_port: Optional[str] = "",
                 timeout_s: float = 15.0, close_session_on_exit: bool = False):
        self.target = target
        self.com_port = com_port
        self.timeout_s = timeout_s
        self.close_session_on_exit = close_session_on_exit
        self._channel: Optional[grpc.Channel] = None
        self._stub: Optional[pb_grpc.DutControlStub] = None

    # -- connection -------------------------------------------------------- #
    def open(self, connect_timeout_s: float = 5.0) -> "DutClient":
        self._channel = grpc.insecure_channel(self.target)
        try:
            grpc.channel_ready_future(self._channel).result(timeout=connect_timeout_s)
        except grpc.FutureTimeoutError:
            self._channel.close()
            self._channel = None
            raise ConnectionError(
                f"DUT service not reachable at {self.target}") from None
        self._stub = pb_grpc.DutControlStub(self._channel)
        if self.com_port is not None:
            self.open_session(self.com_port)
        return self

    def close(self) -> None:
        if self._stub is None:
            return
        try:
            self.stop()
            if self.close_session_on_exit:
                self.close_session()
        except DutError:
            pass
        finally:
            self._channel.close()
            self._channel = None
            self._stub = None

    def __enter__(self) -> "DutClient":
        return self.open()

    def __exit__(self, *exc) -> None:
        self.close()

    def _call(self, name: str, request=None):
        if self._stub is None:
            raise RuntimeError("DutClient is not connected; call open() first")
        try:
            return getattr(self._stub, name)(request or Empty(),
                                             timeout=self.timeout_s)
        except grpc.RpcError as err:
            raise DutError(name, err) from None

    # -- session ----------------------------------------------------------- #
    def open_session(self, port: str = "", read_timeout_ms: int = 0) -> SessionStatus:
        return self._status(self._call("OpenSession", pb.OpenSessionRequest(
            port=port, read_timeout_ms=read_timeout_ms)))

    def close_session(self) -> SessionStatus:
        return self._status(self._call("CloseSession"))

    def status(self) -> SessionStatus:
        return self._status(self._call("GetStatus"))

    @staticmethod
    def _status(s) -> SessionStatus:
        return SessionStatus(s.is_open, s.port, DutState(s.state))

    def stop(self) -> str:
        return self._call("Stop").response

    # -- Wi-Fi ------------------------------------------------------------- #
    def wifi_tx(self, channel: int, rate: WifiRate = WifiRate.G_6M,
                attenuation_db: float = 0.0, bw40: bool = False) -> str:
        """Start Wi-Fi TX; runs until stop() or another start."""
        return self._call("StartWlanTx", pb.WlanTxRequest(
            channel=channel, rate=int(rate),
            attenuation_quarter_db=int(round(attenuation_db * 4)),
            bandwidth=pb.WLAN_BANDWIDTH_HT40 if bw40 else pb.WLAN_BANDWIDTH_HT20,
        )).response

    def wifi_rx_start(self, channel: int, rate: WifiRate = WifiRate.G_6M,
                      bw40: bool = False) -> str:
        return self._call("StartWlanRx", pb.WlanRxRequest(
            channel=channel, rate=int(rate),
            bandwidth=pb.WLAN_BANDWIDTH_HT40 if bw40 else pb.WLAN_BANDWIDTH_HT20,
        )).response

    def wifi_rx_stop(self) -> WifiRxResult:
        r = self._call("FetchWlanRx")
        return WifiRxResult(r.correct_packets, r.desired_packets, r.rssi_dbm, r.raw)

    # -- BLE --------------------------------------------------------------- #
    def ble_tx(self, channel: int, power_level: int = 15,
               length: int = 250, payload: BlePayload = BlePayload.PRBS9,
               rate: BleRate = BleRate.LE_1M, syncw: int = DEFAULT_SYNCW,
               transmission_mode: int = 0) -> str:
        """Start BLE TX; runs until stop() or another start."""
        return self._call("StartBleTx", pb.BleTxRequest(
            channel_index=channel, power_level=power_level,
            payload_length=length, payload_pattern=int(payload),
            sync_word=syncw, rate=int(rate), transmission_mode=transmission_mode,
        )).response

    def ble_rx_start(self, channel: int, rate: BleRate = BleRate.LE_1M,
                     syncw: int = DEFAULT_SYNCW) -> str:
        return self._call("StartBleRx", pb.BleRxRequest(
            channel_index=channel, sync_word=syncw, rate=int(rate))).response

    def ble_rx_stop(self) -> BleRxResult:
        r = self._call("FetchBleRx")
        return BleRxResult(r.total_packets, r.desired_packets, r.rssi_dbm, r.raw)