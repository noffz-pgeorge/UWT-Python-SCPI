from uwt_visa_instrument import UwtVisaInstrument
from typing import List, Dict, Union, Tuple, Optional

class BTClient(UwtVisaInstrument):

    #region Parent Class
    def __init__(
        self, 
        ip_addr: str, 
        rf_port: int, 
        timeout: int = 5000, 
        visa_backend: str = "@py"
    ):
        """Explicit constructor wrapper so TestStand recognizes parameters."""
        super().__init__(ip_addr=ip_addr, rf_port=rf_port, timeout=timeout, visa_backend=visa_backend)

    def open(self) -> None:
        super().open()

    def write(self, command: str) -> None:
        super().write(command)

    def read(self) -> str:
        return super().read()

    def query(self, command: str) -> str:
        return super().query(command)

    def disconnect(self) -> None:
        super().disconnect()
    #endregion

    def initiate(self, result_space: str) -> None:
        """Initiates the analyzer for a specific result space."""
        self.write(f":BT:INITiate {result_space}")

    def get_measurement_state(self) -> str:
        """Returns the current state (READY, PROCESSING, OFF, PENDING, ACTIVE)."""
        return self.query(":BT:MEASurement:STATE?").strip()

    def reset(self) -> None:
        """Resets the analyzer to its default state."""
        self.write(":BT:RESet")

    #region Configure
    def config_trigger(
        self,
        delay: Optional[float] = None,
        edge: Optional[str] = None,
        mq_time: Optional[float] = None,
        source: Optional[str] = None,
        threshold: Optional[float] = None,
        timeout: Optional[float] = None
    ) -> None:
        """Configures Bluetooth trigger settings."""
        if delay is not None:
            self.write(f":TRIGger:BT:DELay {delay}")
        if edge is not None:
            self.write(f":TRIGger:BT:EDGE {edge}")
        if mq_time is not None:
            self.write(f":TRIGger:BT:MQTime {mq_time}")
        if source is not None:
            self.write(f":TRIGger:BT:SOURce {source}")
        if threshold is not None:
            self.write(f":TRIGger:BT:THReshold {threshold}")
        if timeout is not None:
            self.write(f":TRIGger:BT:TOUT {timeout}")

    def config_20db_bandwidth(
        self,
        avg_count: Optional[int] = None,
        avg_enable: Optional[bool] = None,
        enable: Optional[bool] = None,
        n_threads: Optional[int] = None,
        trace_enable: Optional[bool] = None
    ) -> None:
        """Configures 20dB Bandwidth settings."""
        if avg_count is not None:
            self.write(f":CONFigure:BT:20DB:AVG:COUNT {avg_count}")
        if avg_enable is not None:
            self.write(f":CONFigure:BT:20DB:AVG:ENABle {1 if avg_enable else 0}")
        if enable is not None:
            self.write(f":CONFigure:BT:20DB:ENABle {1 if enable else 0}")
        if n_threads is not None:
            self.write(f":CONFigure:BT:20DB:NTHReads {n_threads}")
        if trace_enable is not None:
            self.write(f":CONFigure:BT:20DB:TRACe:ENABle {1 if trace_enable else 0}")

    def config_acp(
        self,
        avg_count: Optional[int] = None,
        avg_enable: Optional[bool] = None,
        burst_sync_type: Optional[str] = None,
        enable: Optional[bool] = None,
        n_threads: Optional[int] = None,
        offset_mode: Optional[str] = None,
        offset_number: Optional[int] = None,
        trace_enable: Optional[bool] = None
    ) -> None:
        """Configures Adjacent Channel Power (ACP) measurement settings."""
        if avg_count is not None:
            self.write(f":CONFigure:BT:ACP:AVG:COUNT {avg_count}")
        if avg_enable is not None:
            self.write(f":CONFigure:BT:ACP:AVG:ENABle {1 if avg_enable else 0}")
        if burst_sync_type is not None:
            self.write(f":CONFigure:BT:ACP:BURSt:SYNC:TYPE {burst_sync_type}")
        if enable is not None:
            self.write(f":CONFigure:BT:ACP:ENABle {1 if enable else 0}")
        if n_threads is not None:
            self.write(f":CONFigure:BT:ACP:NTHReads {n_threads}")
        if offset_mode is not None:
            self.write(f":CONFigure:BT:ACP:OFFSet:MODE {offset_mode}")
        if offset_number is not None:
            self.write(f":CONFigure:BT:ACP:OFFSet:NUMBer {offset_number}")
        if trace_enable is not None:
            self.write(f":CONFigure:BT:ACP:TRACE:ENABle {1 if trace_enable else 0}")


    def config_signal_and_packet(
        self,
        access_address: Optional[str] = None,
        bd_address_lap: Optional[str] = None,
        channel: Optional[int] = None,
        cte_length: Optional[int] = None,
        cte_slot_duration: Optional[int] = None,
        drate: Optional[str] = None,
        center_frequency: Optional[float] = None,
        le_direction_finding_mode: Optional[str] = None,
        packet_type: Optional[str] = None,
        payload_length: Optional[int] = None,
        payload_mode: Optional[str] = None,
        payload_pattern: Optional[str] = None
    ) -> None:
        """Configures signal parameters and packet attributes."""
        if access_address is not None:
            self.write(f":CONFigure:BT:ACCess:ADDRess {access_address}")
        if bd_address_lap is not None:
            self.write(f":CONFigure:BT:BDADdress:LAP {bd_address_lap}")
        if channel is not None:
            self.write(f":CONFigure:BT:CHANnel {channel}")
        if cte_length is not None:
            self.write(f":CONFigure:BT:CTE:LENgth {cte_length}")
        if cte_slot_duration is not None:
            self.write(f":CONFigure:BT:CTE:SLOT:DURation {cte_slot_duration}")
        if drate is not None:
            self.write(f":CONFigure:BT:DRATE {drate}")
        if center_frequency is not None:
            self.write(f":CONFigure:BT:FREQuency:CENTer {center_frequency}")
        if le_direction_finding_mode is not None:
            self.write(f":CONFigure:BT:LE:DIRection:FINDing:MODE {le_direction_finding_mode}")
        if packet_type is not None:
            self.write(f":CONFigure:BT:PACKet:TYPE {packet_type}")
        if payload_length is not None:
            self.write(f":CONFigure:BT:PAYLoad:LENgth {payload_length}")
        if payload_mode is not None:
            self.write(f":CONFigure:BT:PAYLoad:MODE {payload_mode}")
        if payload_pattern is not None:
            self.write(f":CONFigure:BT:PAYLoad:PATTern {payload_pattern}")

    def config_frequency_range(
        self,
        avg_count: Optional[int] = None,
        avg_enable: Optional[bool] = None,
        enable: Optional[bool] = None,
        n_threads: Optional[int] = None,
        span: Optional[float] = None,
        trace_enable: Optional[bool] = None
    ) -> None:
        """Configures Frequency Range measurement parameters."""
        if avg_count is not None:
            self.write(f":CONFigure:BT:FRANge:AVG:COUNT {avg_count}")
        if avg_enable is not None:
            self.write(f":CONFigure:BT:FRANge:AVG:ENABle {1 if avg_enable else 0}")
        if enable is not None:
            self.write(f":CONFigure:BT:FRANge:ENABle {1 if enable else 0}")
        if n_threads is not None:
            self.write(f":CONFigure:BT:FRANge:NTHReads {n_threads}")
        if span is not None:
            self.write(f":CONFigure:BT:FRANge:SPAN {span}")
        if trace_enable is not None:
            self.write(f":CONFigure:BT:FRANge:TRACE:ENABle {1 if trace_enable else 0}")

    def config_modacc(
        self,
        avg_count: Optional[int] = None,
        avg_enable: Optional[bool] = None,
        burst_sync_type: Optional[str] = None,
        enable: Optional[bool] = None,
        iq_origin_offset_enable: Optional[bool] = None,
        n_threads: Optional[int] = None,
        trace_enable: Optional[bool] = None
    ) -> None:
        """Configures Modulation Accuracy (ModAcc) settings."""
        if avg_count is not None:
            self.write(f":CONFigure:BT:MODacc:AVG:COUNT {avg_count}")
        if avg_enable is not None:
            self.write(f":CONFigure:BT:MODacc:AVG:ENABle {1 if avg_enable else 0}")
        if burst_sync_type is not None:
            self.write(f":CONFigure:BT:MODacc:BURSt:SYNC:TYPE {burst_sync_type}")
        if enable is not None:
            self.write(f":CONFigure:BT:MODacc:ENABle {1 if enable else 0}")
        if iq_origin_offset_enable is not None:
            self.write(f":CONFigure:BT:MODacc:IQ:ORIGin:OFFSet:ENABle {1 if iq_origin_offset_enable else 0}")
        if n_threads is not None:
            self.write(f":CONFigure:BT:MODacc:NTHReads {n_threads}")
        if trace_enable is not None:
            self.write(f":CONFigure:BT:MODacc:TRACE:ENABle {1 if trace_enable else 0}")

    def config_power(
        self,
        ref_auto_initial: Optional[bool] = None,
        ref_level: Optional[float] = None,
        trace_enable: Optional[bool] = None,
        txp_avg_count: Optional[int] = None,
        txp_avg_enable: Optional[bool] = None,
        txp_burst_sync_type: Optional[str] = None,
        txp_enable: Optional[bool] = None,
        txp_n_threads: Optional[int] = None,
        txp_trace_enable: Optional[bool] = None
    ) -> None:
        """Configures power, reference levels, and TX Power (TXP) settings."""
        if ref_auto_initial is not None:
            self.write(f":CONFigure:BT:REFerence:AUTO:INITial {1 if ref_auto_initial else 0}")
        if ref_level is not None:
            self.write(f":CONFigure:BT:REFerence:LEVel {ref_level}")
        if trace_enable is not None:
            self.write(f":CONFigure:BT:TRACE:ENABle {1 if trace_enable else 0}")
        if txp_avg_count is not None:
            self.write(f":CONFigure:BT:TXP:AVG:COUNT {txp_avg_count}")
        if txp_avg_enable is not None:
            self.write(f":CONFigure:BT:TXP:AVG:ENABle {1 if txp_avg_enable else 0}")
        if txp_burst_sync_type is not None:
            self.write(f":CONFigure:BT:TXP:BURSt:SYNC:TYPE {txp_burst_sync_type}")
        if txp_enable is not None:
            self.write(f":CONFigure:BT:TXP:ENABle {1 if txp_enable else 0}")
        if txp_n_threads is not None:
            self.write(f":CONFigure:BT:TXP:NTHReads {txp_n_threads}")
        if txp_trace_enable is not None:
            self.write(f":CONFigure:BT:TXP:TRACE:ENABle {1 if txp_trace_enable else 0}")

    #endregion
    

    #region Fetch
    def fetch_results(self, index: int = 1) -> str:
        """Queries combined raw results string for a given result index."""
        return self.query(f":FETch:BT:RESults{index}?").strip()

    def fetch_20db_bandwidth(self, index: int = 1) -> Dict[str, str]:
        """Fetches 20dB Bandwidth results."""
        return {
            "bandwidth": self.query(f":FETch:BT:RESults{index}:20DB:BW?").strip(),
            "freq_high": self.query(f":FETch:BT:RESults{index}:20DB:FREQuency:HIGH?").strip(),
            "freq_low": self.query(f":FETch:BT:RESults{index}:20DB:FREQuency:LOW?").strip(),
            "power_peak": self.query(f":FETch:BT:RESults{index}:20DB:POWer:PEAK?").strip(),
        }

    def fetch_acp(self, index: int = 1, offset_index: int = 1) -> Dict[str, str]:
        """Fetches ACP (Adjacent Channel Power) measurement results."""
        return {
            "margin_lower": self.query(f":FETch:BT:RESults{index}:ACP:MARGIN:LOWer{offset_index}?").strip(),
            "margin_upper": self.query(f":FETch:BT:RESults{index}:ACP:MARGIN:UPPer{offset_index}?").strip(),
            "offset_lower_power_abs": self.query(f":FETch:BT:RESults{index}:ACP:OFFSet:LOWer:POWer:ABSolute?").strip(),
            "offset_lower_power_rel": self.query(f":FETch:BT:RESults{index}:ACP:OFFSet:LOWer:POWer:RELative?").strip(),
            "offset_upper_power_abs": self.query(f":FETch:BT:RESults{index}:ACP:OFFSet:UPPer:POWer:ABSolute?").strip(),
            "offset_upper_power_rel": self.query(f":FETch:BT:RESults{index}:ACP:OFFSet:UPPer:POWer:RELative?").strip(),
            "ref_channel_power": self.query(f":FETch:BT:RESults{index}:ACP:REFerence:CHANnel:POWer?").strip(),
        }

    def fetch_frequency_range(self, index: int = 1) -> Dict[str, str]:
        """Fetches Frequency Range results."""
        return {
            "freq_high": self.query(f":FETch:BT:RESults{index}:FRANge:FREQuency:HIGH?").strip(),
            "freq_low": self.query(f":FETch:BT:RESults{index}:FRANge:FREQuency:LOW?").strip(),
        }

    def fetch_modacc(self, index: int = 1) -> str:
        """Fetches Modulation Accuracy results (DEVM, Freq Drift, Freq Error, DF1/DF2, IQ Offsets)."""
        return self.query(f":FETch:BT:RESults{index}:MODacc?").strip()

    def fetch_tx_power(self, index: int = 1) -> str:
        """Fetches TX Power results (Avg/Peak power, DPSK/GFSK power, PAPR, Power Ratios)."""
        return self.query(f":FETch:BT:RESults{index}:TXP?").strip()

    #endregion


