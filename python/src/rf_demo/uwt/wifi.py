from uwt_visa_instrument import UwtVisaInstrument
from typing import List, Dict, Union, Tuple, Optional

class WifiClient(UwtVisaInstrument):

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
        self.write(f":WLAN:INITiate {result_space}")

    def get_measurement_state(self) -> str:
        """Returns the current state (READY, PROCESSING, OFF, PENDING, ACTIVE)."""
        return self.query(":WLAN:MEASurement:STATe?").strip()

    def reset(self) -> None:
        """Resets the analyzer to its default state."""
        self.write(":WLAN:RESet")

    #region Configure
    def config_trigger(
        self,
        trigger_delay_sec: Optional[float] = None,
        trigger_edge: Optional[str] = None,
        trigger_min_quiet_duration_sec: Optional[float] = None,
        trigger_source: Optional[str] = None,
        trigger_threshold: Optional[float] = None,
        trigger_timeout_sec: Optional[float] = None
    ) -> None:
        """Configures WLAN trigger settings."""
        if trigger_delay_sec is not None:
            self.write(f":TRIGger:WLAN:DELay {trigger_delay_sec}")
        if trigger_edge is not None:
            self.write(f":TRIGger:WLAN:EDGE {trigger_edge}")
        if trigger_min_quiet_duration_sec is not None:
            self.write(f":TRIGger:WLAN:MQTime {trigger_min_quiet_duration_sec}")
        if trigger_source is not None:
            self.write(f":TRIGger:WLAN:SOURce {trigger_source}")
        if trigger_threshold is not None:
            self.write(f":TRIGger:WLAN:THReshold {trigger_threshold}")
        if trigger_timeout_sec is not None:
            self.write(f":TRIGger:WLAN:TOUT {trigger_timeout_sec}")

    def config_signal(
        self,
        center_frequency_hz: Optional[float] = None,
        channel_bw: Optional[str] = None,
        frequency_band: Optional[str] = None,
        number_of_users: Optional[int] = None,
        ru_offset: Optional[int] = None,
        ru_size: Optional[int] = None,
        standard: Optional[str] = None,
        tx_power_class: Optional[str] = None
    ) -> None:
        """Configures channel, frequency, standard, and resource-unit signal parameters."""
        if center_frequency_hz is not None:
            self.write(f":CONFigure:WLAN:FREQuency:CENTer {center_frequency_hz}")
        if channel_bw is not None:
            self.write(f":CONFigure:WLAN:CHANnel:BANDwidth {channel_bw}")
        if frequency_band is not None:
            self.write(f":CONFigure:WLAN:FREQuency:BAND {frequency_band}")
        if number_of_users is not None:
            self.write(f":CONFigure:WLAN:USERs:NUMBer {number_of_users}")
        if ru_offset is not None:
            self.write(f":CONFigure:WLAN:RU:OFFSet {ru_offset}")
        if ru_size is not None:
            self.write(f":CONFigure:WLAN:RU:SIZE {ru_size}")
        if standard is not None:
            self.write(f":CONFigure:WLAN:STANdard {standard}")
        if tx_power_class is not None:
            self.write(f":CONFigure:WLAN:TX:POWer:CLASs {tx_power_class}")

    def config_modacc_dsss(
        self,
        dsss_data_decoding_enabled: Optional[bool] = None,
        dsss_mod_acc_acquisition_length: Optional[float] = None,
        dsss_mod_acc_acquisition_length_mode: Optional[str] = None,
        dsss_mod_acc_all_traces_enable: Optional[bool] = None,
        dsss_mod_acc_averaging_count: Optional[int] = None,
        dsss_mod_acc_averaging_enabled: Optional[bool] = None,
        dsss_mod_acc_burst_start_detection_enabled: Optional[bool] = None,
        dsss_mod_acc_chip_clock_error_connection_enabled: Optional[bool] = None,
        dsss_mod_acc_equalization_enabled: Optional[bool] = None,
        dsss_mod_acc_evm_unit: Optional[str] = None,
        dsss_mod_acc_frequency_error_correction_enabled: Optional[bool] = None,
        dsss_mod_acc_iq_origin_offset_correction_enabled: Optional[bool] = None,
        dsss_mod_acc_max_measurement_length: Optional[int] = None,
        dsss_mod_acc_measurement_enabled: Optional[bool] = None,
        dsss_mod_acc_measurement_offset: Optional[int] = None,
        dsss_mod_acc_number_of_analysis_threads: Optional[int] = None,
        dsss_mod_acc_power_custom_gate_start_time: Optional[float] = None,
        dsss_mod_acc_power_custom_gate_stop_time: Optional[float] = None,
        dsss_mod_acc_power_measurement_enabled: Optional[bool] = None,
        dsss_mod_acc_power_number_of_custom_gates: Optional[int] = None,
        dsss_mod_acc_pulse_shaping_filter_parameter: Optional[float] = None,
        dsss_mod_acc_pulse_shaping_filter_type: Optional[str] = None,
        dsss_mod_acc_spectrum_inverted_enabled: Optional[bool] = None
    ) -> None:
        """Configures DSSS Modulation Accuracy (ModAcc) settings."""
        if dsss_data_decoding_enabled is not None:
            self.write(f":CONFigure:WLAN:MODacc:DSSS:DATA:DECoding:ENABle {1 if dsss_data_decoding_enabled else 0}")
        if dsss_mod_acc_acquisition_length is not None:
            self.write(f":CONFigure:WLAN:MODacc:DSSS:ACQuisition:LENGth {dsss_mod_acc_acquisition_length}")
        if dsss_mod_acc_acquisition_length_mode is not None:
            self.write(f":CONFigure:WLAN:MODacc:DSSS:ACQuisition:LENGth:MODE {dsss_mod_acc_acquisition_length_mode}")
        if dsss_mod_acc_all_traces_enable is not None:
            self.write(f":CONFigure:WLAN:MODacc:DSSS:TRACe:ENABle {1 if dsss_mod_acc_all_traces_enable else 0}")
        if dsss_mod_acc_averaging_count is not None:
            self.write(f":CONFigure:WLAN:MODacc:DSSS:AVG:COUNt {dsss_mod_acc_averaging_count}")
        if dsss_mod_acc_averaging_enabled is not None:
            self.write(f":CONFigure:WLAN:MODacc:DSSS:AVG:ENABle {1 if dsss_mod_acc_averaging_enabled else 0}")
        if dsss_mod_acc_burst_start_detection_enabled is not None:
            self.write(f":CONFigure:WLAN:MODacc:DSSS:BURSt:STARt:DETection:ENABle {1 if dsss_mod_acc_burst_start_detection_enabled else 0}")
        if dsss_mod_acc_chip_clock_error_connection_enabled is not None:
            self.write(f":CONFigure:WLAN:MODacc:DSSS:CHIP:CERRor:CONNection:ENABle {1 if dsss_mod_acc_chip_clock_error_connection_enabled else 0}")
        if dsss_mod_acc_equalization_enabled is not None:
            self.write(f":CONFigure:WLAN:MODacc:DSSS:EQUalization:ENABle {1 if dsss_mod_acc_equalization_enabled else 0}")
        if dsss_mod_acc_evm_unit is not None:
            self.write(f":CONFigure:WLAN:MODacc:DSSS:EVM:UNIT {dsss_mod_acc_evm_unit}")
        if dsss_mod_acc_frequency_error_correction_enabled is not None:
            self.write(f":CONFigure:WLAN:MODacc:DSSS:FERRor:CORRection:ENABle {1 if dsss_mod_acc_frequency_error_correction_enabled else 0}")
        if dsss_mod_acc_iq_origin_offset_correction_enabled is not None:
            self.write(f":CONFigure:WLAN:MODacc:DSSS:IQ:ORIGin:OFFSet:CORRection:ENABle {1 if dsss_mod_acc_iq_origin_offset_correction_enabled else 0}")
        if dsss_mod_acc_max_measurement_length is not None:
            self.write(f":CONFigure:WLAN:MODacc:DSSS:MEASurement:LENGth:MAXimum {dsss_mod_acc_max_measurement_length}")
        if dsss_mod_acc_measurement_enabled is not None:
            self.write(f":CONFigure:WLAN:MODacc:DSSS:MEASurement:ENABle {1 if dsss_mod_acc_measurement_enabled else 0}")
        if dsss_mod_acc_measurement_offset is not None:
            self.write(f":CONFigure:WLAN:MODacc:DSSS:MEASurement:OFFSet {dsss_mod_acc_measurement_offset}")
        if dsss_mod_acc_number_of_analysis_threads is not None:
            self.write(f":CONFigure:WLAN:MODacc:DSSS:NTHReads {dsss_mod_acc_number_of_analysis_threads}")
        if dsss_mod_acc_power_custom_gate_start_time is not None:
            self.write(f":CONFigure:WLAN:MODacc:DSSS:POWer:CGATes:TIMe:STARt {dsss_mod_acc_power_custom_gate_start_time}")
        if dsss_mod_acc_power_custom_gate_stop_time is not None:
            self.write(f":CONFigure:WLAN:MODacc:DSSS:POWer:CGATes:TIMe:STOP {dsss_mod_acc_power_custom_gate_stop_time}")
        if dsss_mod_acc_power_measurement_enabled is not None:
            self.write(f":CONFigure:WLAN:MODacc:DSSS:POWer:MEASurement:ENABle {1 if dsss_mod_acc_power_measurement_enabled else 0}")
        if dsss_mod_acc_power_number_of_custom_gates is not None:
            self.write(f":CONFigure:WLAN:MODacc:DSSS:POWer:CGATes:NUMBer {dsss_mod_acc_power_number_of_custom_gates}")
        if dsss_mod_acc_pulse_shaping_filter_parameter is not None:
            self.write(f":CONFigure:WLAN:MODacc:DSSS:PSFilter:PARameter {dsss_mod_acc_pulse_shaping_filter_parameter}")
        if dsss_mod_acc_pulse_shaping_filter_type is not None:
            self.write(f":CONFigure:WLAN:MODacc:DSSS:PSFilter:TYPE {dsss_mod_acc_pulse_shaping_filter_type}")
        if dsss_mod_acc_spectrum_inverted_enabled is not None:
            self.write(f":CONFigure:WLAN:MODacc:DSSS:SPECtrum:INVerted:ENABle {1 if dsss_mod_acc_spectrum_inverted_enabled else 0}")

    def config_modacc_ofdm(
        self,
        ofdm_data_decoding_enabled: Optional[bool] = None,
        ofdm_mod_acc_acquisition_length_mode: Optional[str] = None,
        ofdm_mod_acc_acquisition_length_s: Optional[float] = None,
        ofdm_mod_acc_all_traces_enable: Optional[bool] = None,
        ofdm_mod_acc_amplitude_tracking_enabled: Optional[bool] = None,
        ofdm_mod_acc_averaging_count: Optional[int] = None,
        ofdm_mod_acc_averaging_enabled: Optional[bool] = None,
        ofdm_mod_acc_averaging_type: Optional[str] = None,
        ofdm_mod_acc_burst_start_detection_enabled: Optional[bool] = None,
        ofdm_mod_acc_channel_estimation_smoothing_enabled: Optional[bool] = None,
        ofdm_mod_acc_channel_estimation_smoothing_length: Optional[int] = None,
        ofdm_mod_acc_channel_estimation_type: Optional[str] = None,
        ofdm_mod_acc_common_clock_source_enabled: Optional[bool] = None,
        ofdm_mod_acc_evm_unit: Optional[str] = None,
        ofdm_mod_acc_frequency_error_estimation_method: Optional[str] = None,
        ofdm_mod_acc_iq_gain_imbalance_correction_enabled: Optional[bool] = None,
        ofdm_mod_acc_iq_impairments_estimation_enabled: Optional[bool] = None,
        ofdm_mod_acc_iq_impairments_model: Optional[str] = None,
        ofdm_mod_acc_iq_impairments_per_subcarrier_enabled: Optional[bool] = None,
        ofdm_mod_acc_iq_quadrature_error_correction_enabled: Optional[bool] = None,
        ofdm_mod_acc_iq_timing_skew_correction_enabled: Optional[bool] = None,
        ofdm_mod_acc_max_measurement_lenght: Optional[int] = None,
        ofdm_mod_acc_measurement_enabled: Optional[bool] = None,
        ofdm_mod_acc_measurement_mode: Optional[str] = None,
        ofdm_mod_acc_measurement_offset: Optional[int] = None,
        ofdm_mod_acc_noise_compensation_enabled: Optional[bool] = None,
        ofdm_mod_acc_noise_compensation_input_power_check_enabled: Optional[bool] = None,
        ofdm_mod_acc_noise_compensation_reference_level_coercion_limit_d_b: Optional[float] = None,
        ofdm_mod_acc_number_of_analysis_threads: Optional[int] = None,
        ofdm_mod_acc_optimize_dynamic_range_for_evm_enabled: Optional[bool] = None,
        ofdm_mod_acc_optimize_dynamic_range_for_evm_margin_d_b: Optional[float] = None,
        ofdm_mod_acc_phase_tracking_enabled: Optional[bool] = None,
        ofdm_mod_acc_power_custom_gate_start_time: Optional[float] = None,
        ofdm_mod_acc_power_custom_gate_stop_time: Optional[float] = None,
        ofdm_mod_acc_power_measurement_enabled: Optional[bool] = None,
        ofdm_mod_acc_power_number_of_custom_gates: Optional[int] = None,
        ofdm_mod_acc_spectrum_inverted_enabled: Optional[bool] = None,
        ofdm_mod_acc_symbol_clock_error_connection_enabled: Optional[bool] = None,
        ofdm_mod_acc_unused_tone_error_mask_reference: Optional[str] = None
    ) -> None:
        """Configures OFDM Modulation Accuracy (ModAcc) settings."""
        if ofdm_data_decoding_enabled is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:DATAl:DECoding:ENABle {1 if ofdm_data_decoding_enabled else 0}")
        if ofdm_mod_acc_acquisition_length_mode is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:ACQuisition:LENGth:MODE {ofdm_mod_acc_acquisition_length_mode}")
        if ofdm_mod_acc_acquisition_length_s is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:ACQuisition:LENGth {ofdm_mod_acc_acquisition_length_s}")
        if ofdm_mod_acc_all_traces_enable is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:TRACe:ENABle {1 if ofdm_mod_acc_all_traces_enable else 0}")
        if ofdm_mod_acc_amplitude_tracking_enabled is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:AMPLitude:TRACking:ENABle {1 if ofdm_mod_acc_amplitude_tracking_enabled else 0}")
        if ofdm_mod_acc_averaging_count is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:AVG:COUNt {ofdm_mod_acc_averaging_count}")
        if ofdm_mod_acc_averaging_enabled is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:AVG:ENABle {1 if ofdm_mod_acc_averaging_enabled else 0}")
        if ofdm_mod_acc_averaging_type is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:AVG:TYPE {ofdm_mod_acc_averaging_type}")
        if ofdm_mod_acc_burst_start_detection_enabled is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:BURSt:STARt:DETection:ENABle {1 if ofdm_mod_acc_burst_start_detection_enabled else 0}")
        if ofdm_mod_acc_channel_estimation_smoothing_enabled is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:CHANnel:ESTimation:SMOothing:ENABle {1 if ofdm_mod_acc_channel_estimation_smoothing_enabled else 0}")
        if ofdm_mod_acc_channel_estimation_smoothing_length is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:CHANnel:ESTimation:SMOothing:LENGth {ofdm_mod_acc_channel_estimation_smoothing_length}")
        if ofdm_mod_acc_channel_estimation_type is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:CHANnel:ESTimation:TYPE {ofdm_mod_acc_channel_estimation_type}")
        if ofdm_mod_acc_common_clock_source_enabled is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:COMMon:CLOCk:SOURce:ENABle {1 if ofdm_mod_acc_common_clock_source_enabled else 0}")
        if ofdm_mod_acc_evm_unit is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:EVM:UNIT {ofdm_mod_acc_evm_unit}")
        if ofdm_mod_acc_frequency_error_estimation_method is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:FERRor:ESTimation:METHod {ofdm_mod_acc_frequency_error_estimation_method}")
        if ofdm_mod_acc_iq_gain_imbalance_correction_enabled is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:IQ:GAIN:IMBalance:CORRection:ENABle {1 if ofdm_mod_acc_iq_gain_imbalance_correction_enabled else 0}")
        if ofdm_mod_acc_iq_impairments_estimation_enabled is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:IQ:IMPairments:ESTimation:ENABle {1 if ofdm_mod_acc_iq_impairments_estimation_enabled else 0}")
        if ofdm_mod_acc_iq_impairments_model is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:IQ:IMPairments:MODel {ofdm_mod_acc_iq_impairments_model}")
        if ofdm_mod_acc_iq_impairments_per_subcarrier_enabled is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:IQ:IMPairments:PSCarrier:ENABle {1 if ofdm_mod_acc_iq_impairments_per_subcarrier_enabled else 0}")
        if ofdm_mod_acc_iq_quadrature_error_correction_enabled is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:IQ:QERRor:CORRection:ENABle {1 if ofdm_mod_acc_iq_quadrature_error_correction_enabled else 0}")
        if ofdm_mod_acc_iq_timing_skew_correction_enabled is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:IQ:TIMing:SKEW:CORRection:ENABle {1 if ofdm_mod_acc_iq_timing_skew_correction_enabled else 0}")
        if ofdm_mod_acc_max_measurement_lenght is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:MEASurement:LENGth:MAXimum {ofdm_mod_acc_max_measurement_lenght}")
        if ofdm_mod_acc_measurement_enabled is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:MEASurement:ENABle {1 if ofdm_mod_acc_measurement_enabled else 0}")
        if ofdm_mod_acc_measurement_mode is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:MEASurement:MODE {ofdm_mod_acc_measurement_mode}")
        if ofdm_mod_acc_measurement_offset is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:MEASurement:OFFSet {ofdm_mod_acc_measurement_offset}")
        if ofdm_mod_acc_noise_compensation_enabled is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:NOISe:COMPensation:ENABle {1 if ofdm_mod_acc_noise_compensation_enabled else 0}")
        if ofdm_mod_acc_noise_compensation_input_power_check_enabled is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:NOISe:COMPensation:INPut:POWer:CHECk:ENABle {1 if ofdm_mod_acc_noise_compensation_input_power_check_enabled else 0}")
        if ofdm_mod_acc_noise_compensation_reference_level_coercion_limit_d_b is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:NOISe:COMPensation:REFerence:LEVel:COERcion:LIMit {ofdm_mod_acc_noise_compensation_reference_level_coercion_limit_d_b}")
        if ofdm_mod_acc_number_of_analysis_threads is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:NTHReads {ofdm_mod_acc_number_of_analysis_threads}")
        if ofdm_mod_acc_optimize_dynamic_range_for_evm_enabled is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:EVM:DRANge:OPTimize:ENABle {1 if ofdm_mod_acc_optimize_dynamic_range_for_evm_enabled else 0}")
        if ofdm_mod_acc_optimize_dynamic_range_for_evm_margin_d_b is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:EVM:DRANge:OPTimize:MARGin {ofdm_mod_acc_optimize_dynamic_range_for_evm_margin_d_b}")
        if ofdm_mod_acc_phase_tracking_enabled is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:PHASe:TRACking:ENABle {1 if ofdm_mod_acc_phase_tracking_enabled else 0}")
        if ofdm_mod_acc_power_custom_gate_start_time is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:POWer:CGATes:TIMe:STARt {ofdm_mod_acc_power_custom_gate_start_time}")
        if ofdm_mod_acc_power_custom_gate_stop_time is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:POWer:CGATes:TIMe:STOP {ofdm_mod_acc_power_custom_gate_stop_time}")
        if ofdm_mod_acc_power_measurement_enabled is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:POWer:MEASurement:ENABle {1 if ofdm_mod_acc_power_measurement_enabled else 0}")
        if ofdm_mod_acc_power_number_of_custom_gates is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:POWer:CGATes:NUMBer {ofdm_mod_acc_power_number_of_custom_gates}")
        if ofdm_mod_acc_spectrum_inverted_enabled is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:SPECtrum:INVerted:ENABle {1 if ofdm_mod_acc_spectrum_inverted_enabled else 0}")
        if ofdm_mod_acc_symbol_clock_error_connection_enabled is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:SYMBol:CERRor:CONNection:ENABle {1 if ofdm_mod_acc_symbol_clock_error_connection_enabled else 0}")
        if ofdm_mod_acc_unused_tone_error_mask_reference is not None:
            self.write(f":CONFigure:WLAN:MODacc:OFDM:UNUSed:TERRor:MASK:REFerence {ofdm_mod_acc_unused_tone_error_mask_reference}")

    def config_pwrramp(
        self,
        power_ramp_acquisition_length: Optional[float] = None,
        power_ramp_all_traces_enable: Optional[bool] = None,
        power_ramp_averaging_count: Optional[int] = None,
        power_ramp_averaging_enabled: Optional[bool] = None,
        power_ramp_measurement_enabled: Optional[bool] = None,
        power_ramp_number_of_analysis_threads: Optional[int] = None
    ) -> None:
        """Configures Power Ramp measurement settings."""
        if power_ramp_acquisition_length is not None:
            self.write(f":CONFigure:WLAN:PWRRamp:ACQuisition:LENGth {power_ramp_acquisition_length}")
        if power_ramp_all_traces_enable is not None:
            self.write(f":CONFigure:WLAN:PWRRamp:TRACe:ENABle {1 if power_ramp_all_traces_enable else 0}")
        if power_ramp_averaging_count is not None:
            self.write(f":CONFigure:WLAN:PWRRamp:AVG:COUNt {power_ramp_averaging_count}")
        if power_ramp_averaging_enabled is not None:
            self.write(f":CONFigure:WLAN:PWRRamp:AVG:ENABle {1 if power_ramp_averaging_enabled else 0}")
        if power_ramp_measurement_enabled is not None:
            self.write(f":CONFigure:WLAN:PWRRamp:MEASurement:ENABle {1 if power_ramp_measurement_enabled else 0}")
        if power_ramp_number_of_analysis_threads is not None:
            self.write(f":CONFigure:WLAN:PWRRamp:NTHReads {power_ramp_number_of_analysis_threads}")

    def config_sem(
        self,
        sem_all_traces_enable: Optional[bool] = None,
        sem_amplitude_correction_type: Optional[str] = None,
        sem_averaging_count: Optional[int] = None,
        sem_averaging_enabled: Optional[bool] = None,
        sem_averaging_type: Optional[str] = None,
        sem_mask_type: Optional[str] = None,
        sem_measurement_enabled: Optional[bool] = None,
        sem_number_of_analysis_threads: Optional[int] = None,
        sem_number_of_offsets: Optional[int] = None,
        sem_offset_relative_limit_start: Optional[float] = None,
        sem_offset_relative_limit_stop: Optional[float] = None,
        sem_offset_sideband: Optional[str] = None,
        sem_offset_start_frequency_hz: Optional[float] = None,
        sem_offset_stop_frequency_hz: Optional[float] = None,
        sem_span: Optional[float] = None,
        sem_span_auto: Optional[bool] = None,
        sem_sweep_time_auto: Optional[bool] = None,
        sem_sweep_time_interval_s: Optional[float] = None
    ) -> None:
        """Configures Spectrum Emission Mask (SEM) settings."""
        if sem_all_traces_enable is not None:
            self.write(f":CONFigure:WLAN:SEM:TRACe:ENABle {1 if sem_all_traces_enable else 0}")
        if sem_amplitude_correction_type is not None:
            self.write(f":CONFigure:WLAN:SEM:AMPLitude:CORRection:TYPE {sem_amplitude_correction_type}")
        if sem_averaging_count is not None:
            self.write(f":CONFigure:WLAN:SEM:AVG:COUNt {sem_averaging_count}")
        if sem_averaging_enabled is not None:
            self.write(f":CONFigure:WLAN:SEM:AVG:ENABle {1 if sem_averaging_enabled else 0}")
        if sem_averaging_type is not None:
            self.write(f":CONFigure:WLAN:SEM:AVG:TYPE {sem_averaging_type}")
        if sem_mask_type is not None:
            self.write(f":CONFigure:WLAN:SEM:MASK:TYPE {sem_mask_type}")
        if sem_measurement_enabled is not None:
            self.write(f":CONFigure:WLAN:SEM:MEASurement:ENABle {1 if sem_measurement_enabled else 0}")
        if sem_number_of_analysis_threads is not None:
            self.write(f":CONFigure:WLAN:SEM:NTHReads {sem_number_of_analysis_threads}")
        if sem_number_of_offsets is not None:
            self.write(f":CONFigure:WLAN:SEM:OFFSets:NUMBer {sem_number_of_offsets}")
        if sem_offset_relative_limit_start is not None:
            self.write(f":CONFigure:WLAN:SEM:OFFSet:RLIMit:STARt {sem_offset_relative_limit_start}")
        if sem_offset_relative_limit_stop is not None:
            self.write(f":CONFigure:WLAN:SEM:OFFSet:RLIMit:STOP {sem_offset_relative_limit_stop}")
        if sem_offset_sideband is not None:
            self.write(f":CONFigure:WLAN:SEM:OFFSet:SIDE:BAND {sem_offset_sideband}")
        if sem_offset_start_frequency_hz is not None:
            self.write(f":CONFigure:WLAN:SEM:OFFSet:FREQuency:STARt {sem_offset_start_frequency_hz}")
        if sem_offset_stop_frequency_hz is not None:
            self.write(f":CONFigure:WLAN:SEM:OFFSet:FREQuency:STOP {sem_offset_stop_frequency_hz}")
        if sem_span is not None:
            self.write(f":CONFigure:WLAN:SEM:SPAN {sem_span}")
        if sem_span_auto is not None:
            self.write(f":CONFigure:WLAN:SEM:SPAN:AUTO {1 if sem_span_auto else 0}")
        if sem_sweep_time_auto is not None:
            self.write(f":CONFigure:WLAN:SEM:SWEep:TIME:AUTO {1 if sem_sweep_time_auto else 0}")
        if sem_sweep_time_interval_s is not None:
            self.write(f":CONFigure:WLAN:SEM:SWEep:TIME:INTerval {sem_sweep_time_interval_s}")

    def config_power(
        self,
        reference_level_d_bm: Optional[float] = None,
        trace_enable: Optional[bool] = None,
        txp_all_traces_enable: Optional[bool] = None,
        txp_averaging_count: Optional[int] = None,
        txp_averaging_enabled: Optional[bool] = None,
        txp_burst_detection_enabled: Optional[bool] = None,
        txp_max_measurement_interval_s: Optional[float] = None,
        txp_measurement_enabled: Optional[bool] = None,
        txp_number_of_analysis_threads: Optional[int] = None
    ) -> None:
        """Configures reference level, trace enable, and TX Power (TXP) settings."""
        if reference_level_d_bm is not None:
            self.write(f":CONFigure:WLAN:REFerence:LEVel {reference_level_d_bm}")
        if trace_enable is not None:
            self.write(f":CONFigure:WLAN:TRACe:ENABle {1 if trace_enable else 0}")
        if txp_all_traces_enable is not None:
            self.write(f":CONFigure:WLAN:TXP:TRACe:ENABle {1 if txp_all_traces_enable else 0}")
        if txp_averaging_count is not None:
            self.write(f":CONFigure:WLAN:TXP:AVG:COUNt {txp_averaging_count}")
        if txp_averaging_enabled is not None:
            self.write(f":CONFigure:WLAN:TXP:AVG:ENABle {1 if txp_averaging_enabled else 0}")
        if txp_burst_detection_enabled is not None:
            self.write(f":CONFigure:WLAN:TXP:BURSt:DETection:ENABle {1 if txp_burst_detection_enabled else 0}")
        if txp_max_measurement_interval_s is not None:
            self.write(f":CONFigure:WLAN:TXP:MEASurement:INTerval:MAXimum {txp_max_measurement_interval_s}")
        if txp_measurement_enabled is not None:
            self.write(f":CONFigure:WLAN:TXP:MEASurement:ENABle {1 if txp_measurement_enabled else 0}")
        if txp_number_of_analysis_threads is not None:
            self.write(f":CONFigure:WLAN:TXP:NTHReads {txp_number_of_analysis_threads}")

    #endregion

    #region Fetch
    def fetch_modacc_dsss(self, index: int = 1) -> Dict[str, str]:
        """Fetches DSSS Modulation Accuracy (ModAcc) results."""
        return {
            "chip_cerror_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:DSSS:CHIP:CERRor:MEAN?").strip(),
            "chip_number": self.query(f":FETch:WLAN:RESults{index}:MODacc:DSSS:CHIP:NUMBer?").strip(),
            "data_power_avg_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:DSSS:DATA:POWer:AVG:MEAN?").strip(),
            "data_power_peak_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:DSSS:DATA:POWer:PEAK:MAXimum?").strip(),
            "evm_peak1999_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:DSSS:EVM:PEAK1999:MAXimum?").strip(),
            "evm_peak2007_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:DSSS:EVM:PEAK2007:MAXimum?").strip(),
            "evm_peak2016_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:DSSS:EVM:PEAK2016:MAXimum?").strip(),
            "ferror_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:DSSS:FERRor:MEAN?").strip(),
            "header_power_avg_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:DSSS:HEADer:POWer:AVG:MEAN?").strip(),
            "header_power_peak_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:DSSS:HEADer:POWer:PEAK:MAXimum?").strip(),
            "iq_gain_imbalance_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:DSSS:IQ:GAIN:IMBalance:MEAN?").strip(),
            "iq_origin_offset_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:DSSS:IQ:ORIGin:OFFSet:MEAN?").strip(),
            "iq_qerror_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:DSSS:IQ:QERRor:MEAN?").strip(),
            "payload_length": self.query(f":FETch:WLAN:RESults{index}:MODacc:DSSS:PAYLoad:LENGth?").strip(),
            "ppdu_power_avg_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:DSSS:PPDU:POWer:AVG:MEAN?").strip(),
            "ppdu_power_peak_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:DSSS:PPDU:POWer:PEAK:MAXimum?").strip(),
            "preamble_power_avg_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:DSSS:PREamble:POWer:AVG:MEAN?").strip(),
            "preamble_power_peak_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:DSSS:PREamble:POWer:PEAK:MAXimum?").strip(),
            "psdu_crc_status": self.query(f":FETch:WLAN:RESults{index}:MODacc:DSSS:PSDU:CRC:STATus?").strip(),
            "rms_evm_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:DSSS:RMS:EVM:MEAN?").strip(),
            "rms_merror_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:DSSS:RMS:MERRor:MEAN?").strip(),
            "rms_perror_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:DSSS:RMS:PERRor:MEAN?").strip(),
        }

    def fetch_modacc_dsss_decoded_bits(self, index: int = 1, bit_index: int = 1) -> Dict[str, str]:
        """Fetches decoded header/PSDU bits at a given bit index for DSSS ModAcc."""
        return {
            "header": self.query(f":FETch:WLAN:RESults{index}:MODacc:DSSS:HEADer:BITS:TRACe:DECoded{bit_index}?").strip(),
            "psdu": self.query(f":FETch:WLAN:RESults{index}:MODacc:DSSS:PSDU:BITS:TRACe:DECoded{bit_index}?").strip(),
        }

    def fetch_modacc_ofdm(self, index: int = 1) -> Dict[str, str]:
        """Fetches OFDM Modulation Accuracy (ModAcc) results."""
        return {
            "avg_type": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:AVG:TYPE?").strip(),
            "chain_data_rms_evm_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:CHAin:DATA:RMS:EVM:MEAN?").strip(),
            "chain_pilot_rms_evm_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:CHAin:PILot:RMS:EVM:MEAN?").strip(),
            "chain_rms_evm_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:CHAin:RMS:EVM:MAXimum?").strip(),
            "chain_rms_evm_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:CHAin:RMS:EVM:MEAN?").strip(),
            "chain_rms_evm_min": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:CHAin:RMS:EVM:MINimum?").strip(),
            "cross_power_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:CROSs:POWer:MEAN?").strip(),
            "data_power_avg_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:DATA:POWer:AVG:MEAN?").strip(),
            "data_power_peak_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:DATA:POWer:PEAK:MAXimum?").strip(),
            "feccoding_type": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:FECCoding:TYPE?").strip(),
            "ferror_ccdf_percents10": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:FERRor:CCDF:PERCents10?").strip(),
            "ferror_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:FERRor:MAXimum?").strip(),
            "ferror_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:FERRor:MEAN?").strip(),
            "ferror_min": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:FERRor:MINimum?").strip(),
            "he_ltf_power_avg_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:HE:LTF:POWer:AVG:MEAN?").strip(),
            "he_ltf_power_peak_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:HE:LTF:POWer:PEAK:MAXimum?").strip(),
            "he_siga_power_avg_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:HE:SIGa:POWer:AVG:MEAN?").strip(),
            "he_siga_power_peak_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:HE:SIGa:POWer:PEAK:MAXimum?").strip(),
            "he_sigb_power_avg_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:HE:SIGb:POWer:AVG:MEAN?").strip(),
            "he_sigb_power_peak_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:HE:SIGb:POWer:PEAK:MAXimum?").strip(),
            "he_sigb_symbols_number": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:HE:SIGb:SYMBols:NUMBer?").strip(),
            "he_stf_power_avg_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:HE:STF:POWer:AVG:MEAN?").strip(),
            "he_stf_power_peak_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:HE:STF:POWer:PEAK:MAXimum?").strip(),
            "ht_dltf_power_avg_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:HT:DLTF:POWer:AVG:MEAN?").strip(),
            "ht_dltf_power_peak_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:HT:DLTF:POWer:PEAK:MAXimum?").strip(),
            "ht_eltf_power_avg_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:HT:ELTF:POWer:AVG:MEAN?").strip(),
            "ht_eltf_power_peak_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:HT:ELTF:POWer:PEAK:MAXimum?").strip(),
            "ht_sig_power_avg_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:HT:SIG:POWer:AVG:MEAN?").strip(),
            "ht_sig_power_peak_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:HT:SIG:POWer:PEAK:MAXimum?").strip(),
            "ht_stf_power_avg_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:HT:STF:POWer:AVG:MEAN?").strip(),
            "ht_stf_power_peak_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:HT:STF:POWer:PEAK:MAXimum?").strip(),
            "interval_guard_type": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:INTerval:GUARd:TYPE?").strip(),
            "iq_gain_imbalance_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:IQ:GAIN:IMBalance:MAXimum?").strip(),
            "iq_gain_imbalance_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:IQ:GAIN:IMBalance:MEAN?").strip(),
            "iq_gain_imbalance_min": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:IQ:GAIN:IMBalance:MINimum?").strip(),
            "iq_origin_offser_rel_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:IQ:ORIGin:OFFSer:RELative:MEAN?").strip(),
            "iq_origin_offset_abs_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:IQ:ORIGin:OFFSet:ABSolute:MEAN?").strip(),
            "iq_qerror_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:IQ:QERRor:MAXimum?").strip(),
            "iq_qerror_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:IQ:QERRor:MEAN?").strip(),
            "iq_qerror_min": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:IQ:QERRor:MINimum?").strip(),
            "iq_timing_skew_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:IQ:TIMing:SKEW:MEAN?").strip(),
            "l_ltf_power_avg_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:L:LTF:POWer:AVG:MEAN?").strip(),
            "l_ltf_power_peak_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:L:LTF:POWer:PEAK:MAXimum?").strip(),
            "l_sig_power_avg_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:L:SIG:POWer:AVG:MEAN?").strip(),
            "l_sig_power_peak_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:L:SIG:POWer:PEAK:MAXimum?").strip(),
            "l_stf_power_avg_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:L:STF:POWer:AVG:MEAN?").strip(),
            "l_stf_power_peak_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:L:STF:POWer:PEAK:MAXimum?").strip(),
            "msc_index": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:MSC:INDex?").strip(),
            "pe_duration": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:PE:DURation?").strip(),
            "pe_power_avg_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:PE:POWer:AVG:MEAN?").strip(),
            "pe_power_power_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:PE:POWer:POWer:MAXimum?").strip(),
            "ppdu_power_avg_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:PPDU:POWer:AVG:MEAN?").strip(),
            "ppdu_power_power_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:PPDU:POWer:POWer:MAXimum?").strip(),
            "psdu_crc_status": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:PSDU:CRC:STATus?").strip(),
            "rel_iq_origin_offset_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:RELative:IQ:ORIGin:OFFSet:MAXimum?").strip(),
            "rel_iq_origin_offset_min": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:RELative:IQ:ORIGin:OFFSet:MINimum?").strip(),
            "ri_sig_power_avg_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:RI:SIG:POWer:AVG:MEAN?").strip(),
            "ri_sig_power_peak_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:RI:SIG:POWer:PEAK:MAXimum?").strip(),
            "rms_common_perror_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:RMS:COMMon:PERRor:MEAN?").strip(),
            "rms_evm_chain_data_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:RMS:EVM:CHAin:DATA:MEAN?").strip(),
            "rms_evm_chain_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:RMS:EVM:CHAin:MEAN?").strip(),
            "rms_evm_chain_pilot_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:RMS:EVM:CHAin:PILot:MEAN?").strip(),
            "rms_evm_composite_data_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:RMS:EVM:COMPosite:DATA:MEAN?").strip(),
            "rms_evm_composite_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:RMS:EVM:COMPosite:MEAN?").strip(),
            "rms_evm_composite_pilot_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:RMS:EVM:COMPosite:PILot:MEAN?").strip(),
            "rms_evm_stream_data_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:RMS:EVM:STReam:DATA:MEAN?").strip(),
            "rms_evm_stream_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:RMS:EVM:STReam:MEAN?").strip(),
            "rms_evm_stream_pilot_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:RMS:EVM:STReam:PILot:MEAN?").strip(),
            "rms_evm_stream_user_data_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:RMS:EVM:STReam:USER:DATA:MEAN?").strip(),
            "rms_evm_stream_user_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:RMS:EVM:STReam:USER:MEAN?").strip(),
            "rms_evm_stream_user_pilot_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:RMS:EVM:STReam:USER:PILot:MEAN?").strip(),
            "ru_offset": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:RU:OFFSet?").strip(),
            "ru_size": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:RU:SIZe?").strip(),
            "space_time_streams_number": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:SPACe:TIME:STReams:NUMBer?").strip(),
            "spectral_flatness_margin": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:SPECtral:FLATness:MARGin?").strip(),
            "spectral_flatness_margin_scarrier_index": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:SPECtral:FLATness:MARGin:SCARrier:INDex?").strip(),
            "spectral_fmargin1_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:SPECtral:FMARgin1:MAXimum?").strip(),
            "spectral_fmargin1_min": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:SPECtral:FMARgin1:MINimum?").strip(),
            "stream_data_rms_evm_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:STReam:DATA:RMS:EVM:MEAN?").strip(),
            "stream_pilot_rms_evm_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:STReam:PILot:RMS:EVM:MEAN?").strip(),
            "stream_rms_evm_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:STReam:RMS:EVM:MAXimum?").strip(),
            "stream_rms_evm_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:STReam:RMS:EVM:MEAN?").strip(),
            "stream_rms_evm_min": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:STReam:RMS:EVM:MINimum?").strip(),
            "symbol_cerror_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:SYMBol:CERRor:MAXimum?").strip(),
            "symbol_cerror_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:SYMBol:CERRor:MEAN?").strip(),
            "symbol_cerror_min": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:SYMBol:CERRor:MINimum?").strip(),
            "symbol_number": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:SYMBol:NUMBer?").strip(),
            "user_power_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:USER:POWer:MAXimum?").strip(),
            "user_power_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:USER:POWer:MEAN?").strip(),
            "user_power_min": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:USER:POWer:MINimum?").strip(),
            "user_stream_rms_evm_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:USER:STReam:RMS:EVM:MAXimum?").strip(),
            "user_stream_rms_evm_min": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:USER:STReam:RMS:EVM:MINimum?").strip(),
            "users_number": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:USERs:NUMBer?").strip(),
            "utone_error_margin": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:UTONe:ERRor:MARGin?").strip(),
            "utone_error_margin_ru_index": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:UTONe:ERRor:MARGin:RU:INDex?").strip(),
            "vht_ltf_power_avg_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:VHT:LTF:POWer:AVG:MEAN?").strip(),
            "vht_ltf_power_peak_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:VHT:LTF:POWer:PEAK:MAXimum?").strip(),
            "vht_siga_power_avg_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:VHT:SIGa:POWer:AVG:MEAN?").strip(),
            "vht_siga_power_peak_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:VHT:SIGa:POWer:PEAK:MAXimum?").strip(),
            "vht_sigb_power_avg_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:VHT:SIGb:POWer:AVG:MEAN?").strip(),
            "vht_sigb_power_peak_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:VHT:SIGb:POWer:PEAK:MAXimum?").strip(),
            "vht_stf_power_avg_mean": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:VHT:STF:POWer:AVG:MEAN?").strip(),
            "vht_stf_power_peak_max": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:VHT:STF:POWer:PEAK:MAXimum?").strip(),
        }

    def fetch_modacc_ofdm_decoded_bits(self, index: int = 1, bit_index: int = 1) -> Dict[str, str]:
        """Fetches decoded field bits (L-SIG, SIG, SIG-B, U-SIG, EHT-SIG, Service, PSDU) at a given bit index for OFDM ModAcc."""
        return {
            "ehtsig": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:MODacc:OFDM:DECoded:EHTSig:BITS:TRACe{bit_index}?").strip(),
            "lsig": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:MODacc:OFDM:DECoded:LSIG:BITS:TRACe{bit_index}?").strip(),
            "psdu": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:MODacc:OFDM:DECoded:PSDU:BITS:TRACe{bit_index}?").strip(),
            "service": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:MODacc:OFDM:DECoded:SERVice:BITS:TRACe{bit_index}?").strip(),
            "sig": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:MODacc:OFDM:DECoded:SIG:BITS:TRACe{bit_index}?").strip(),
            "sigb": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:MODacc:OFDM:DECoded:SIGB:BITS:TRACe{bit_index}?").strip(),
            "usig": self.query(f":FETch:WLAN:RESults{index}:MODacc:OFDM:MODacc:OFDM:DECoded:USIG:BITS:TRACe{bit_index}?").strip(),
        }

    def fetch_txp(self, index: int = 1) -> Dict[str, str]:
        """Fetches TX Power (TXP) results."""
        return {
            "avg_power_max": self.query(f":FETch:WLAN:RESults{index}:TXP:AVG:POWer:MAXimum?").strip(),
            "avg_power_min": self.query(f":FETch:WLAN:RESults{index}:TXP:AVG:POWer:MINimum?").strip(),
            "papr": self.query(f":FETch:WLAN:RESults{index}:TXP:PAPR?").strip(),
            "peak_power_mean": self.query(f":FETch:WLAN:RESults{index}:TXP:PEAK:POWer:MEAN?").strip(),
            "peak_power_min": self.query(f":FETch:WLAN:RESults{index}:TXP:PEAK:POWer:MINimum?").strip(),
            "power_avg_mean": self.query(f":FETch:WLAN:RESults{index}:TXP:POWer:AVG:MEAN?").strip(),
            "power_max": self.query(f":FETch:WLAN:RESults{index}:TXP:POWer:MAXimum?").strip(),
            "power_min": self.query(f":FETch:WLAN:RESults{index}:TXP:POWer:MINimum?").strip(),
        }

    def fetch_sem(self, index: int = 1) -> Dict[str, str]:
        """Fetches Spectrum Emission Mask (SEM) summary results."""
        return {
            "all": self.query(f":FETch:WLAN:RESults{index}:SEM:ALL?").strip(),
            "meas": self.query(f":FETch:WLAN:RESults{index}:SEM:MEAS?").strip(),
            "meas_all": self.query(f":FETch:WLAN:RESults{index}:SEM:MEAS:ALL?").strip(),
            "meas_freq": self.query(f":FETch:WLAN:RESults{index}:SEM:MEAS:FREQuency?").strip(),
            "meas_ibandwidth": self.query(f":FETch:WLAN:RESults{index}:SEM:MEAS:IBANDwidth?").strip(),
            "meas_power": self.query(f":FETch:WLAN:RESults{index}:SEM:MEAS:POWer?").strip(),
            "offset_margin": self.query(f":FETch:WLAN:RESults{index}:SEM:OFFSet:MARGin?").strip(),
            "offset_power": self.query(f":FETch:WLAN:RESults{index}:SEM:OFFSet:POWer?").strip(),
            "power_total": self.query(f":FETch:WLAN:RESults{index}:SEM:POWer:TOTal?").strip(),
            "status": self.query(f":FETch:WLAN:RESults{index}:SEM:STATus?").strip(),
        }

    def fetch_sem_carrier(self, index: int = 1, carrier_index: int = 1) -> Dict[str, str]:
        """Fetches per-carrier Spectrum Emission Mask (SEM) results."""
        return {
            "raw": self.query(f":FETch:WLAN:RESults{index}:SEM:CCARrier{carrier_index}?").strip(),
            "freq_peak": self.query(f":FETch:WLAN:RESults{index}:SEM:CCARrier{carrier_index}:FREQuency:PEAK?").strip(),
            "ipower_abs": self.query(f":FETch:WLAN:RESults{index}:SEM:CCARrier{carrier_index}:IPOWer:ABSolute?").strip(),
            "ipower_rel": self.query(f":FETch:WLAN:RESults{index}:SEM:CCARrier{carrier_index}:IPOWer:RELative?").strip(),
            "power_peak_abs": self.query(f":FETch:WLAN:RESults{index}:SEM:CCARrier{carrier_index}:POWer:PEAK:ABS?").strip(),
        }

    def fetch_sem_offset_margin(self, index: int = 1, offset_index: int = 1) -> Dict[str, str]:
        """Fetches lower/upper offset margin Spectrum Emission Mask (SEM) results for a given offset."""
        return {
            "lower": self.query(f":FETch:WLAN:RESults{index}:SEM:OFFSet:MARGin:LOWer{offset_index}?").strip(),
            "lower_freq": self.query(f":FETch:WLAN:RESults{index}:SEM:OFFSet:MARGin:LOWer{offset_index}:FREQuency?").strip(),
            "lower_margin": self.query(f":FETch:WLAN:RESults{index}:SEM:OFFSet:MARGin:LOWer{offset_index}:MARGin?").strip(),
            "lower_power_abs": self.query(f":FETch:WLAN:RESults{index}:SEM:OFFSet:MARGin:LOWer{offset_index}:POWer:ABSolute?").strip(),
            "lower_power_rel": self.query(f":FETch:WLAN:RESults{index}:SEM:OFFSet:MARGin:LOWer{offset_index}:POWer:RELative?").strip(),
            "lower_status": self.query(f":FETch:WLAN:RESults{index}:SEM:OFFSet:MARGin:LOWer{offset_index}:STATus?").strip(),
            "upper": self.query(f":FETch:WLAN:RESults{index}:SEM:OFFSet:MARGin:UPPer{offset_index}?").strip(),
            "upper_freq": self.query(f":FETch:WLAN:RESults{index}:SEM:OFFSet:MARGin:UPPer{offset_index}:FREQuency?").strip(),
            "upper_margin": self.query(f":FETch:WLAN:RESults{index}:SEM:OFFSet:MARGin:UPPer{offset_index}:MARGin?").strip(),
            "upper_power_abs": self.query(f":FETch:WLAN:RESults{index}:SEM:OFFSet:MARGin:UPPer{offset_index}:POWer:ABSolute?").strip(),
            "upper_power_rel": self.query(f":FETch:WLAN:RESults{index}:SEM:OFFSet:MARGin:UPPer{offset_index}:POWer:RELative?").strip(),
            "upper_status": self.query(f":FETch:WLAN:RESults{index}:SEM:OFFSet:MARGin:UPPer{offset_index}:STATus?").strip(),
        }

    def fetch_sem_offset_power(self, index: int = 1, offset_index: int = 1) -> Dict[str, str]:
        """Fetches lower/upper offset power Spectrum Emission Mask (SEM) results for a given offset."""
        return {
            "lower": self.query(f":FETch:WLAN:RESults{index}:SEM:OFFSet:POWer:LOWer{offset_index}?").strip(),
            "lower_freq": self.query(f":FETch:WLAN:RESults{index}:SEM:OFFSet:POWer:LOWer{offset_index}:FREQuency?").strip(),
            "lower_ipower_abs": self.query(f":FETch:WLAN:RESults{index}:SEM:OFFSet:POWer:LOWer{offset_index}:IPOWer:ABSolute?").strip(),
            "lower_ipower_rel": self.query(f":FETch:WLAN:RESults{index}:SEM:OFFSet:POWer:LOWer{offset_index}:IPOWer:RELative?").strip(),
            "lower_power_abs": self.query(f":FETch:WLAN:RESults{index}:SEM:OFFSet:POWer:LOWer{offset_index}:POWer:ABSolute?").strip(),
            "lower_power_rel": self.query(f":FETch:WLAN:RESults{index}:SEM:OFFSet:POWer:LOWer{offset_index}:POWer:RELative?").strip(),
            "upper": self.query(f":FETch:WLAN:RESults{index}:SEM:OFFSet:POWer:UPPer{offset_index}?").strip(),
            "upper_freq": self.query(f":FETch:WLAN:RESults{index}:SEM:OFFSet:POWer:UPPer{offset_index}:FREQuency?").strip(),
            "upper_ipower_abs": self.query(f":FETch:WLAN:RESults{index}:SEM:OFFSet:POWer:UPPer{offset_index}:IPOWer:ABSolute?").strip(),
            "upper_ipower_rel": self.query(f":FETch:WLAN:RESults{index}:SEM:OFFSet:POWer:UPPer{offset_index}:IPOWer:RELative?").strip(),
            "upper_power_abs": self.query(f":FETch:WLAN:RESults{index}:SEM:OFFSet:POWer:UPPer{offset_index}:POWer:ABSolute?").strip(),
            "upper_power_rel": self.query(f":FETch:WLAN:RESults{index}:SEM:OFFSet:POWer:UPPer{offset_index}:POWer:RELative?").strip(),
        }
    #endregion
