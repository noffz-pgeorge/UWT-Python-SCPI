from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DutState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DUT_STATE_CLOSED: _ClassVar[DutState]
    DUT_STATE_IDLE: _ClassVar[DutState]
    DUT_STATE_BLE_TX: _ClassVar[DutState]
    DUT_STATE_WLAN_TX: _ClassVar[DutState]
    DUT_STATE_BLE_RX: _ClassVar[DutState]
    DUT_STATE_WLAN_RX: _ClassVar[DutState]

class WlanDataRate(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WLAN_DATA_RATE_B_1M: _ClassVar[WlanDataRate]
    WLAN_DATA_RATE_B_2M: _ClassVar[WlanDataRate]
    WLAN_DATA_RATE_B_5M5: _ClassVar[WlanDataRate]
    WLAN_DATA_RATE_B_11M: _ClassVar[WlanDataRate]
    WLAN_DATA_RATE_G_48M: _ClassVar[WlanDataRate]
    WLAN_DATA_RATE_G_24M: _ClassVar[WlanDataRate]
    WLAN_DATA_RATE_G_12M: _ClassVar[WlanDataRate]
    WLAN_DATA_RATE_G_6M: _ClassVar[WlanDataRate]
    WLAN_DATA_RATE_G_54M: _ClassVar[WlanDataRate]
    WLAN_DATA_RATE_G_36M: _ClassVar[WlanDataRate]
    WLAN_DATA_RATE_G_18M: _ClassVar[WlanDataRate]
    WLAN_DATA_RATE_G_9M: _ClassVar[WlanDataRate]
    WLAN_DATA_RATE_N_MCS0: _ClassVar[WlanDataRate]
    WLAN_DATA_RATE_N_MCS1: _ClassVar[WlanDataRate]
    WLAN_DATA_RATE_N_MCS2: _ClassVar[WlanDataRate]
    WLAN_DATA_RATE_N_MCS3: _ClassVar[WlanDataRate]
    WLAN_DATA_RATE_N_MCS4: _ClassVar[WlanDataRate]
    WLAN_DATA_RATE_N_MCS5: _ClassVar[WlanDataRate]
    WLAN_DATA_RATE_N_MCS6: _ClassVar[WlanDataRate]
    WLAN_DATA_RATE_N_MCS7: _ClassVar[WlanDataRate]

class WlanBandwidth(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WLAN_BANDWIDTH_HT20: _ClassVar[WlanBandwidth]
    WLAN_BANDWIDTH_HT40: _ClassVar[WlanBandwidth]

class BleRate(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BLE_RATE_LE_1M: _ClassVar[BleRate]
    BLE_RATE_LE_2M: _ClassVar[BleRate]
    BLE_RATE_LE_CODED_125K: _ClassVar[BleRate]
    BLE_RATE_LE_CODED_500K: _ClassVar[BleRate]

class BlePayloadPattern(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BLE_PAYLOAD_PATTERN_P1010: _ClassVar[BlePayloadPattern]
    BLE_PAYLOAD_PATTERN_P00001111: _ClassVar[BlePayloadPattern]
    BLE_PAYLOAD_PATTERN_PRBS9: _ClassVar[BlePayloadPattern]
DUT_STATE_CLOSED: DutState
DUT_STATE_IDLE: DutState
DUT_STATE_BLE_TX: DutState
DUT_STATE_WLAN_TX: DutState
DUT_STATE_BLE_RX: DutState
DUT_STATE_WLAN_RX: DutState
WLAN_DATA_RATE_B_1M: WlanDataRate
WLAN_DATA_RATE_B_2M: WlanDataRate
WLAN_DATA_RATE_B_5M5: WlanDataRate
WLAN_DATA_RATE_B_11M: WlanDataRate
WLAN_DATA_RATE_G_48M: WlanDataRate
WLAN_DATA_RATE_G_24M: WlanDataRate
WLAN_DATA_RATE_G_12M: WlanDataRate
WLAN_DATA_RATE_G_6M: WlanDataRate
WLAN_DATA_RATE_G_54M: WlanDataRate
WLAN_DATA_RATE_G_36M: WlanDataRate
WLAN_DATA_RATE_G_18M: WlanDataRate
WLAN_DATA_RATE_G_9M: WlanDataRate
WLAN_DATA_RATE_N_MCS0: WlanDataRate
WLAN_DATA_RATE_N_MCS1: WlanDataRate
WLAN_DATA_RATE_N_MCS2: WlanDataRate
WLAN_DATA_RATE_N_MCS3: WlanDataRate
WLAN_DATA_RATE_N_MCS4: WlanDataRate
WLAN_DATA_RATE_N_MCS5: WlanDataRate
WLAN_DATA_RATE_N_MCS6: WlanDataRate
WLAN_DATA_RATE_N_MCS7: WlanDataRate
WLAN_BANDWIDTH_HT20: WlanBandwidth
WLAN_BANDWIDTH_HT40: WlanBandwidth
BLE_RATE_LE_1M: BleRate
BLE_RATE_LE_2M: BleRate
BLE_RATE_LE_CODED_125K: BleRate
BLE_RATE_LE_CODED_500K: BleRate
BLE_PAYLOAD_PATTERN_P1010: BlePayloadPattern
BLE_PAYLOAD_PATTERN_P00001111: BlePayloadPattern
BLE_PAYLOAD_PATTERN_PRBS9: BlePayloadPattern

class OpenSessionRequest(_message.Message):
    __slots__ = ("port", "read_timeout_ms")
    PORT_FIELD_NUMBER: _ClassVar[int]
    READ_TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
    port: str
    read_timeout_ms: int
    def __init__(self, port: _Optional[str] = ..., read_timeout_ms: _Optional[int] = ...) -> None: ...

class SessionStatus(_message.Message):
    __slots__ = ("is_open", "port", "state")
    IS_OPEN_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    is_open: bool
    port: str
    state: DutState
    def __init__(self, is_open: _Optional[bool] = ..., port: _Optional[str] = ..., state: _Optional[_Union[DutState, str]] = ...) -> None: ...

class CommandReply(_message.Message):
    __slots__ = ("response", "state")
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    response: str
    state: DutState
    def __init__(self, response: _Optional[str] = ..., state: _Optional[_Union[DutState, str]] = ...) -> None: ...

class BleTxRequest(_message.Message):
    __slots__ = ("channel_index", "power_level", "payload_length", "payload_pattern", "sync_word", "rate", "transmission_mode")
    CHANNEL_INDEX_FIELD_NUMBER: _ClassVar[int]
    POWER_LEVEL_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_LENGTH_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_PATTERN_FIELD_NUMBER: _ClassVar[int]
    SYNC_WORD_FIELD_NUMBER: _ClassVar[int]
    RATE_FIELD_NUMBER: _ClassVar[int]
    TRANSMISSION_MODE_FIELD_NUMBER: _ClassVar[int]
    channel_index: int
    power_level: int
    payload_length: int
    payload_pattern: BlePayloadPattern
    sync_word: int
    rate: BleRate
    transmission_mode: int
    def __init__(self, channel_index: _Optional[int] = ..., power_level: _Optional[int] = ..., payload_length: _Optional[int] = ..., payload_pattern: _Optional[_Union[BlePayloadPattern, str]] = ..., sync_word: _Optional[int] = ..., rate: _Optional[_Union[BleRate, str]] = ..., transmission_mode: _Optional[int] = ...) -> None: ...

class WlanTxRequest(_message.Message):
    __slots__ = ("channel", "rate", "attenuation_quarter_db", "bandwidth")
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    RATE_FIELD_NUMBER: _ClassVar[int]
    ATTENUATION_QUARTER_DB_FIELD_NUMBER: _ClassVar[int]
    BANDWIDTH_FIELD_NUMBER: _ClassVar[int]
    channel: int
    rate: WlanDataRate
    attenuation_quarter_db: int
    bandwidth: WlanBandwidth
    def __init__(self, channel: _Optional[int] = ..., rate: _Optional[_Union[WlanDataRate, str]] = ..., attenuation_quarter_db: _Optional[int] = ..., bandwidth: _Optional[_Union[WlanBandwidth, str]] = ...) -> None: ...

class BleRxRequest(_message.Message):
    __slots__ = ("channel_index", "sync_word", "rate")
    CHANNEL_INDEX_FIELD_NUMBER: _ClassVar[int]
    SYNC_WORD_FIELD_NUMBER: _ClassVar[int]
    RATE_FIELD_NUMBER: _ClassVar[int]
    channel_index: int
    sync_word: int
    rate: BleRate
    def __init__(self, channel_index: _Optional[int] = ..., sync_word: _Optional[int] = ..., rate: _Optional[_Union[BleRate, str]] = ...) -> None: ...

class WlanRxRequest(_message.Message):
    __slots__ = ("channel", "rate", "bandwidth")
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    RATE_FIELD_NUMBER: _ClassVar[int]
    BANDWIDTH_FIELD_NUMBER: _ClassVar[int]
    channel: int
    rate: WlanDataRate
    bandwidth: WlanBandwidth
    def __init__(self, channel: _Optional[int] = ..., rate: _Optional[_Union[WlanDataRate, str]] = ..., bandwidth: _Optional[_Union[WlanBandwidth, str]] = ...) -> None: ...

class BleRxResult(_message.Message):
    __slots__ = ("total_packets", "desired_packets", "rssi_dbm", "raw")
    TOTAL_PACKETS_FIELD_NUMBER: _ClassVar[int]
    DESIRED_PACKETS_FIELD_NUMBER: _ClassVar[int]
    RSSI_DBM_FIELD_NUMBER: _ClassVar[int]
    RAW_FIELD_NUMBER: _ClassVar[int]
    total_packets: int
    desired_packets: int
    rssi_dbm: float
    raw: str
    def __init__(self, total_packets: _Optional[int] = ..., desired_packets: _Optional[int] = ..., rssi_dbm: _Optional[float] = ..., raw: _Optional[str] = ...) -> None: ...

class WlanRxResult(_message.Message):
    __slots__ = ("correct_packets", "desired_packets", "rssi_dbm", "raw")
    CORRECT_PACKETS_FIELD_NUMBER: _ClassVar[int]
    DESIRED_PACKETS_FIELD_NUMBER: _ClassVar[int]
    RSSI_DBM_FIELD_NUMBER: _ClassVar[int]
    RAW_FIELD_NUMBER: _ClassVar[int]
    correct_packets: int
    desired_packets: int
    rssi_dbm: float
    raw: str
    def __init__(self, correct_packets: _Optional[int] = ..., desired_packets: _Optional[int] = ..., rssi_dbm: _Optional[float] = ..., raw: _Optional[str] = ...) -> None: ...
