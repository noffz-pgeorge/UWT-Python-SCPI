from noffz_uwt.instrument import UwtVisaInstrument
from typing import List, Dict, Union, Tuple, Optional

class LteClient(UwtVisaInstrument):
    """SCPI client for the UWT LTE analyzer.

    Subblock/carrier-indexed commands use the ``:CONFigure:LTE:SBLock<i>:...`` form of the
    manual's two equivalent spellings (the other being ``:CONFigure:LTE<i>:...``).
    All index arguments are 1-based and default to 1.
    """

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
        self.write(f":LTE:INITiate {result_space}")

    def get_measurement_state(self) -> str:
        """Returns the current state (READY, PROCESSING, OFF, PENDING, ACTIVE)."""
        return self.query(":LTE:MEASurement:STATe?").strip()

    def reset(self) -> None:
        """Resets the analyzer to its default state."""
        self.write(":LTE:RESet")

    def fetch(self, result_space: str) -> None:
        """Fetches LTE results into the given result space."""
        self.write(f":LTE:FETch {result_space}")

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
        """Configures LTE trigger settings."""
        if trigger_delay_sec is not None:
            self.write(f":TRIGger:LTE:DELay {trigger_delay_sec}")
        if trigger_edge is not None:
            self.write(f":TRIGger:LTE:EDGE {trigger_edge}")
        if trigger_min_quiet_duration_sec is not None:
            self.write(f":TRIGger:LTE:MQTime {trigger_min_quiet_duration_sec}")
        if trigger_source is not None:
            self.write(f":TRIGger:LTE:SOURce {trigger_source}")
        if trigger_threshold is not None:
            self.write(f":TRIGger:LTE:THReshold {trigger_threshold}")
        if trigger_timeout_sec is not None:
            self.write(f":TRIGger:LTE:TOUT {trigger_timeout_sec}")

    def config_signal(
        self,
        auto_npusch_channel_detection_enabled: Optional[bool] = None,
        cyclic_prefix: Optional[str] = None,
        duplex_scheme: Optional[str] = None,
        enodeb_category: Optional[str] = None,
        link_direction: Optional[str] = None,
        lte_cell_specific_ratio: Optional[str] = None,
        mod_interval_count: Optional[int] = None,
        mod_interval_offset: Optional[int] = None,
        number_of_dut_antennas: Optional[int] = None,
        rb_auto_detection: Optional[bool] = None,
        subcarrier_spacing: Optional[str] = None,
        trace_enable: Optional[bool] = None,
        transmit_antenna_to_analyze: Optional[int] = None,
        uldl_configuration: Optional[int] = None
    ) -> None:
        """Configures link direction, duplexing, frame structure, antennas, and auto-detection settings."""
        if auto_npusch_channel_detection_enabled is not None:
            self.write(f":CONFigure:LTE:NPUSch:CDETection:AUTO:ENABle {1 if auto_npusch_channel_detection_enabled else 0}")
        if cyclic_prefix is not None:
            self.write(f":CONFigure:LTE:CP {cyclic_prefix}")
        if duplex_scheme is not None:
            self.write(f":CONFigure:LTE:DUPLlex {duplex_scheme}")
        if enodeb_category is not None:
            self.write(f":CONFigure:LTE:ENB:CATegory {enodeb_category}")
        if link_direction is not None:
            self.write(f":CONFigure:LTE:LINK:DIRection {link_direction}")
        if lte_cell_specific_ratio is not None:
            self.write(f":CONFigure:LTE:CSRatio {lte_cell_specific_ratio}")
        if mod_interval_count is not None:
            self.write(f":CONFigure:LTE:MODInt:COUNt {mod_interval_count}")
        if mod_interval_offset is not None:
            self.write(f":CONFigure:LTE:MIDInt:OFFSet {mod_interval_offset}")
        if number_of_dut_antennas is not None:
            self.write(f":CONFigure:LTE:NDUT {number_of_dut_antennas}")
        if rb_auto_detection is not None:
            self.write(f":CONFigure:LTE:RB:DETection:AUTO {1 if rb_auto_detection else 0}")
        if subcarrier_spacing is not None:
            self.write(f":CONFigure:LTE:SCSpacing {subcarrier_spacing}")
        if trace_enable is not None:
            self.write(f":CONFigure:LTE:TRACe:ENABle {1 if trace_enable else 0}")
        if transmit_antenna_to_analyze is not None:
            self.write(f":CONFigure:LTE:AANTenna {transmit_antenna_to_analyze}")
        if uldl_configuration is not None:
            self.write(f":CONFigure:LTE:ULDL {uldl_configuration}")

    def config_subblock(
        self,
        subblock_index: int = 1,
        center_frequency_hz: Optional[float] = None,
        component_carrier_at_center_frequency: Optional[int] = None,
        component_carrier_spacing_type: Optional[str] = None,
        frequency_definition: Optional[str] = None,
        max_input_power_dbm: Optional[float] = None,
        user_margin_db: Optional[float] = None
    ) -> None:
        """Configures subblock center frequency, power, spacing, and margin settings."""
        if center_frequency_hz is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:FREQuency:CENTer {center_frequency_hz}")
        if component_carrier_at_center_frequency is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CENTer:INDex {component_carrier_at_center_frequency}")
        if component_carrier_spacing_type is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:SType {component_carrier_spacing_type}")
        if frequency_definition is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:FREQuency:DEFinition {frequency_definition}")
        if max_input_power_dbm is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:POWer:MAX {max_input_power_dbm}")
        if user_margin_db is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:UMARgin {user_margin_db}")

    def config_carrier(
        self,
        subblock_index: int = 1,
        carrier_index: int = 1,
        base_sequence_mode: Optional[bool] = None,
        carrier_cell_id: Optional[int] = None,
        carrier_channel_bandwidth: Optional[str] = None,
        group_hopping_enable: Optional[bool] = None,
        n_cell_ids: Optional[int] = None,
        nbiot_uplink_subcarrier_spacing: Optional[str] = None,
        pcfich_cfis: Optional[int] = None,
        pcfich_power_db: Optional[float] = None
    ) -> None:
        """Configures component carrier bandwidth, cell ID, and NB-IoT/PCFICH settings."""
        if base_sequence_mode is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:BSMOde {1 if base_sequence_mode else 0}")
        if carrier_cell_id is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:CID {carrier_cell_id}")
        if carrier_channel_bandwidth is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:BW {carrier_channel_bandwidth}")
        if group_hopping_enable is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:GHOPping:ENABle {1 if group_hopping_enable else 0}")
        if n_cell_ids is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:NCID {n_cell_ids}")
        if nbiot_uplink_subcarrier_spacing is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:NBIOt:UPLInk:SCSpacing {nbiot_uplink_subcarrier_spacing}")
        if pcfich_cfis is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:PCFICH:CFIS {pcfich_cfis}")
        if pcfich_power_db is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:PCFICH:POWer {pcfich_power_db}")

    def config_carrier_npusch(
        self,
        subblock_index: int = 1,
        carrier_index: int = 1,
        npusch_dmrs_base_sequence_index: Optional[int] = None,
        npusch_dmrs_cyclic_shift: Optional[int] = None,
        npusch_dmrs_delta_ss: Optional[int] = None,
        npusch_format: Optional[int] = None,
        npusch_modulation_type: Optional[str] = None,
        npusch_number_of_tones: Optional[int] = None,
        npusch_starting_slot: Optional[int] = None,
        npusch_tone_offsets: Optional[int] = None
    ) -> None:
        """Configures component carrier NPUSCH (NB-IoT uplink) settings."""
        if npusch_dmrs_base_sequence_index is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:NPUSch:DMRSignal:BSIndex {npusch_dmrs_base_sequence_index}")
        if npusch_dmrs_cyclic_shift is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:NPUSch:DMRSignal:CSHIft {npusch_dmrs_cyclic_shift}")
        if npusch_dmrs_delta_ss is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:NPUSch:DMRSignal:DSS {npusch_dmrs_delta_ss}")
        if npusch_format is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:NPUSch:FORMat {npusch_format}")
        if npusch_modulation_type is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:NPUSch:MODulation:TYPE {npusch_modulation_type}")
        if npusch_number_of_tones is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:NPUSch:NTONes {npusch_number_of_tones}")
        if npusch_starting_slot is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:NPUSch:SSLOt {npusch_starting_slot}")
        if npusch_tone_offsets is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:NPUSch:TOFFsets {npusch_tone_offsets}")

    def config_carrier_pusch(
        self,
        subblock_index: int = 1,
        carrier_index: int = 1,
        auto_dmrs_detection_enable: Optional[bool] = None,
        delta_sequence_shift: Optional[int] = None,
        downlink_test_model: Optional[str] = None,
        emtc_analysis_enable: Optional[bool] = None,
        pbch_power_db: Optional[float] = None,
        pdcch_power_db: Optional[float] = None,
        pss_power_db: Optional[float] = None,
        pusch_dmrs_n1: Optional[int] = None,
        pusch_dmrs_n2: Optional[int] = None,
        pusch_modulation_type: Optional[str] = None,
        sss_power_db: Optional[float] = None
    ) -> None:
        """Configures component carrier PUSCH, DMRS, test model, and downlink channel power settings."""
        if auto_dmrs_detection_enable is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:PUSCh:DMRS:AUTO:ENABle {1 if auto_dmrs_detection_enable else 0}")
        if delta_sequence_shift is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:PUSCh:DMRSignal:DSS {delta_sequence_shift}")
        if downlink_test_model is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:PUSCh:DOWNlink:TMODel {downlink_test_model}")
        if emtc_analysis_enable is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:PUSCh:EMTC:ENABle {1 if emtc_analysis_enable else 0}")
        if pbch_power_db is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:PUSCh:POWer:PBCH {pbch_power_db}")
        if pdcch_power_db is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:PUSCh:POWer:PDCCH {pdcch_power_db}")
        if pss_power_db is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:PUSCh:POWer:PSS {pss_power_db}")
        if pusch_dmrs_n1 is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:PUSCh:DMRSignal:ONE {pusch_dmrs_n1}")
        if pusch_dmrs_n2 is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:PUSCh:DMRSignal:TWO {pusch_dmrs_n2}")
        if pusch_modulation_type is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:PUSCh:MODulation:TYPE {pusch_modulation_type}")
        if sss_power_db is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:PUSCh:POWer:SSS {sss_power_db}")

    def config_carrier_pusch_cluster(
        self,
        subblock_index: int = 1,
        carrier_index: int = 1,
        cluster_index: int = 1,
        rb_count: Optional[int] = None
    ) -> None:
        """Configures the resource block count for a PUSCH RB cluster."""
        if rb_count is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:PUSCh:RBCLuster{cluster_index}:NRB {rb_count}")

    def config_carrier_subframe(
        self,
        subblock_index: int = 1,
        carrier_index: int = 1,
        subframe_index: int = 1,
        number_of_pdsch_channels: Optional[int] = None,
        pdsch_modulation_type: Optional[str] = None,
        pdsch_power_db: Optional[float] = None,
        pdsch_resource_block_allocation: Optional[str] = None,
        phich_duration: Optional[str] = None,
        phich_power_db: Optional[float] = None,
        phich_resource_ng: Optional[str] = None
    ) -> None:
        """Configures per-subframe PDSCH and PHICH settings for a component carrier."""
        if number_of_pdsch_channels is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:SUBFrame{subframe_index}:PDSCH:NCH {number_of_pdsch_channels}")
        if pdsch_modulation_type is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:SUBFrame{subframe_index}:PDSCH:MODulation:TYPE {pdsch_modulation_type}")
        if pdsch_power_db is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:SUBFrame{subframe_index}:PDSCH:POWer {pdsch_power_db}")
        if pdsch_resource_block_allocation is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:SUBFrame{subframe_index}:PDSCH:RBLOck {pdsch_resource_block_allocation}")
        if phich_duration is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:SUBFrame{subframe_index}:PHICH:DURation {phich_duration}")
        if phich_power_db is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:SUBFrame{subframe_index}:PHICH:POWer {phich_power_db}")
        if phich_resource_ng is not None:
            self.write(f":CONFigure:LTE:SBLock{subblock_index}:CCARrier{carrier_index}:SUBFrame{subframe_index}:PHICH:RESOurce {phich_resource_ng}")

    def config_acp(
        self,
        acp_all_traces_enable: Optional[bool] = None,
        acp_amplitude_correction_type: Optional[str] = None,
        acp_averaging_count: Optional[int] = None,
        acp_averaging_enable: Optional[bool] = None,
        acp_averaging_type: Optional[str] = None,
        acp_enable: Optional[bool] = None,
        acp_enable_configurable_number_of_offsets: Optional[bool] = None,
        acp_eutra_offset_definition: Optional[str] = None,
        acp_far_if_output_power_offset_db: Optional[float] = None,
        acp_if_output_power_offset_auto: Optional[bool] = None,
        acp_measurement_method: Optional[str] = None,
        acp_measurement_mode: Optional[str] = None,
        acp_near_if_output_power_offset_db: Optional[float] = None,
        acp_noise_compensation_enable: Optional[bool] = None,
        acp_number_of_analysis_threads: Optional[int] = None,
        acp_number_of_eutra_offsets: Optional[int] = None,
        acp_number_of_gsm_offsets: Optional[int] = None,
        acp_number_of_utra_offsets: Optional[int] = None,
        acp_power_units: Optional[str] = None,
        acp_rbw_auto_bandwidth: Optional[bool] = None,
        acp_rbw_bandwidth_hz: Optional[float] = None,
        acp_rbw_filter_type: Optional[str] = None,
        acp_sequential_fft_size: Optional[int] = None,
        acp_sweep_time_auto: Optional[bool] = None,
        acp_sweep_time_interval_s: Optional[float] = None
    ) -> None:
        """Configures Adjacent Channel Power (ACP) measurement settings."""
        if acp_all_traces_enable is not None:
            self.write(f":CONFigure:LTE:ACP:TRACe:ENABle {1 if acp_all_traces_enable else 0}")
        if acp_amplitude_correction_type is not None:
            self.write(f":CONFigure:LTE:ACP:ACTYpe {acp_amplitude_correction_type}")
        if acp_averaging_count is not None:
            self.write(f":CONFigure:LTE:ACP:AVG:COUNt {acp_averaging_count}")
        if acp_averaging_enable is not None:
            self.write(f":CONFigure:LTE:ACP:AVG:ENABle {1 if acp_averaging_enable else 0}")
        if acp_averaging_type is not None:
            self.write(f":CONFigure:LTE:ACP:AVG:TYPE {acp_averaging_type}")
        if acp_enable is not None:
            self.write(f":CONFigure:LTE:ACP:ENABle {1 if acp_enable else 0}")
        if acp_enable_configurable_number_of_offsets is not None:
            self.write(f":CONFigure:LTE:ACP:NOFFsets:ENABle {1 if acp_enable_configurable_number_of_offsets else 0}")
        if acp_eutra_offset_definition is not None:
            self.write(f":CONFigure:LTE:ACP:OFFSet:EUTRa:DEFInition {acp_eutra_offset_definition}")
        if acp_far_if_output_power_offset_db is not None:
            self.write(f":CONFigure:LTE:ACP:ACP:IF:OPOWer:FAR:OFFSet {acp_far_if_output_power_offset_db}")
        if acp_if_output_power_offset_auto is not None:
            self.write(f":CONFigure:LTE:ACP:IF:OPOWer:FAR:AUTO {1 if acp_if_output_power_offset_auto else 0}")
        if acp_measurement_method is not None:
            self.write(f":CONFigure:LTE:ACP:MEASurement:METHod {acp_measurement_method}")
        if acp_measurement_mode is not None:
            self.write(f":CONFigure:LTE:ACP:MEASurement:MODE {acp_measurement_mode}")
        if acp_near_if_output_power_offset_db is not None:
            self.write(f":CONFigure:LTE:ACP:IF:OPOWer:NEAR:OFFSet {acp_near_if_output_power_offset_db}")
        if acp_noise_compensation_enable is not None:
            self.write(f":CONFigure:LTE:ACP:NCOMp:ENABle {1 if acp_noise_compensation_enable else 0}")
        if acp_number_of_analysis_threads is not None:
            self.write(f":CONFigure:LTE:ACP:NTHReads {acp_number_of_analysis_threads}")
        if acp_number_of_eutra_offsets is not None:
            self.write(f":CONFigure:LTE:ACP:NOFFsets:EUTRa {acp_number_of_eutra_offsets}")
        if acp_number_of_gsm_offsets is not None:
            self.write(f":CONFigure:LTE:ACP:NOFFsets:GSM {acp_number_of_gsm_offsets}")
        if acp_number_of_utra_offsets is not None:
            self.write(f":CONFigure:LTE:ACP:NOFFsets:UTRa {acp_number_of_utra_offsets}")
        if acp_power_units is not None:
            self.write(f":CONFigure:LTE:ACP:POWer:UNITs {acp_power_units}")
        if acp_rbw_auto_bandwidth is not None:
            self.write(f":CONFigure:LTE:ACP:RBW:BWAuto {1 if acp_rbw_auto_bandwidth else 0}")
        if acp_rbw_bandwidth_hz is not None:
            self.write(f":CONFigure:LTE:ACP:RBW:BW {acp_rbw_bandwidth_hz}")
        if acp_rbw_filter_type is not None:
            self.write(f":CONFigure:LTE:ACP:RBW:FILTer {acp_rbw_filter_type}")
        if acp_sequential_fft_size is not None:
            self.write(f":CONFigure:LTE:ACP:SFFT:SIZE {acp_sequential_fft_size}")
        if acp_sweep_time_auto is not None:
            self.write(f":CONFigure:LTE:ACP:SWEep:AUTO {1 if acp_sweep_time_auto else 0}")
        if acp_sweep_time_interval_s is not None:
            self.write(f":CONFigure:LTE:ACP:SWEep:INTerval {acp_sweep_time_interval_s}")

    def config_chp(
        self,
        chp_all_traces_enable: Optional[bool] = None,
        chp_amplitude_correction_type: Optional[str] = None,
        chp_averaging_count: Optional[int] = None,
        chp_averaging_enable: Optional[bool] = None,
        chp_averaging_type: Optional[str] = None,
        chp_enable: Optional[bool] = None,
        chp_integration_bandwidth_type: Optional[str] = None,
        chp_measurement_mode: Optional[str] = None,
        chp_number_of_analysis_threads: Optional[int] = None,
        chp_rbw_auto_bandwidth: Optional[bool] = None,
        chp_rbw_bandwidth_hz: Optional[float] = None,
        chp_rbw_filter_type: Optional[str] = None,
        chp_sweep_time_auto: Optional[bool] = None,
        chp_sweep_time_interval_s: Optional[float] = None
    ) -> None:
        """Configures Channel Power (CHP) measurement settings."""
        if chp_all_traces_enable is not None:
            self.write(f":CONFigure:LTE:CHP:TRACe:ENABle {1 if chp_all_traces_enable else 0}")
        if chp_amplitude_correction_type is not None:
            self.write(f":CONFigure:LTE:CHP:ACType {chp_amplitude_correction_type}")
        if chp_averaging_count is not None:
            self.write(f":CONFigure:LTE:CHP:AVG:COUNt {chp_averaging_count}")
        if chp_averaging_enable is not None:
            self.write(f":CONFigure:LTE:CHP:AVG:ENABle {1 if chp_averaging_enable else 0}")
        if chp_averaging_type is not None:
            self.write(f":CONFigure:LTE:CHP:AVG:TYPE {chp_averaging_type}")
        if chp_enable is not None:
            self.write(f":CONFigure:LTE:CHP:ENABle {1 if chp_enable else 0}")
        if chp_integration_bandwidth_type is not None:
            self.write(f":CONFigure:LTE:CHP:INTegration:BWType {chp_integration_bandwidth_type}")
        if chp_measurement_mode is not None:
            self.write(f":CONFigure:LTE:CHP:MEASurement:MODE {chp_measurement_mode}")
        if chp_number_of_analysis_threads is not None:
            self.write(f":CONFigure:LTE:CHP:NTHReads {chp_number_of_analysis_threads}")
        if chp_rbw_auto_bandwidth is not None:
            self.write(f":CONFigure:LTE:CHP:RBW:BWAuto {1 if chp_rbw_auto_bandwidth else 0}")
        if chp_rbw_bandwidth_hz is not None:
            self.write(f":CONFigure:LTE:CHP:RBW:BWIDth {chp_rbw_bandwidth_hz}")
        if chp_rbw_filter_type is not None:
            self.write(f":CONFigure:LTE:CHP:RBW:FILTer {chp_rbw_filter_type}")
        if chp_sweep_time_auto is not None:
            self.write(f":CONFigure:LTE:CHP:SWEep:AUTO {1 if chp_sweep_time_auto else 0}")
        if chp_sweep_time_interval_s is not None:
            self.write(f":CONFigure:LTE:CHP:SWEep:INTerval {chp_sweep_time_interval_s}")

    def config_modacc(
        self,
        mod_acc_all_traces_enable: Optional[bool] = None,
        mod_acc_averaging_count: Optional[int] = None,
        mod_acc_averaging_enable: Optional[bool] = None,
        mod_acc_channel_estimation_type: Optional[str] = None,
        mod_acc_common_clock_source_enable: Optional[bool] = None,
        mod_acc_condition: Optional[str] = None,
        mod_acc_enable: Optional[bool] = None,
        mod_acc_evm_exclusion_period_enable: Optional[bool] = None,
        mod_acc_evm_unit: Optional[str] = None,
        mod_acc_fft_window_length_pct: Optional[float] = None,
        mod_acc_fft_window_offset_pct: Optional[float] = None,
        mod_acc_fft_window_type: Optional[str] = None,
        mod_acc_in_band_emission_mask_type: Optional[str] = None,
        mod_acc_iq_gain_imbalance_correction_enabled: Optional[bool] = None,
        mod_acc_iq_mismatch_estimations_enabled: Optional[bool] = None,
        mod_acc_iq_origin_offset_estimation_enabled: Optional[bool] = None,
        mod_acc_iq_quadrature_error_correction_enabled: Optional[bool] = None,
        mod_acc_iq_timing_skew_correction_enabled: Optional[bool] = None,
        mod_acc_meas_mode: Optional[str] = None,
        mod_acc_multicarrier_filter_enable: Optional[bool] = None,
        mod_acc_number_of_analysis_threads: Optional[int] = None,
        mod_acc_spectrum_inverted: Optional[bool] = None,
        mod_acc_sync_mode: Optional[str] = None
    ) -> None:
        """Configures Modulation Accuracy (ModAcc) settings."""
        if mod_acc_all_traces_enable is not None:
            self.write(f":CONFigure:LTE:MODacc:TRACe:ENABle {1 if mod_acc_all_traces_enable else 0}")
        if mod_acc_averaging_count is not None:
            self.write(f":CONFigure:LTE:MODacc:AVG:COUNt {mod_acc_averaging_count}")
        if mod_acc_averaging_enable is not None:
            self.write(f":CONFigure:LTE:MODacc:AVG:ENABle {1 if mod_acc_averaging_enable else 0}")
        if mod_acc_channel_estimation_type is not None:
            self.write(f":CONFigure:LTE:MODacc:CETYpe {mod_acc_channel_estimation_type}")
        if mod_acc_common_clock_source_enable is not None:
            self.write(f":CONFigure:LTE:MODacc:CCLock:ENABle {1 if mod_acc_common_clock_source_enable else 0}")
        if mod_acc_condition is not None:
            self.write(f":CONFigure:LTE:MODacc:CONDition {mod_acc_condition}")
        if mod_acc_enable is not None:
            self.write(f":CONFigure:LTE:MODacc:ENABle {1 if mod_acc_enable else 0}")
        if mod_acc_evm_exclusion_period_enable is not None:
            self.write(f":CONFigure:LTE:MODacc:EVM:EPERiod:ENABle {1 if mod_acc_evm_exclusion_period_enable else 0}")
        if mod_acc_evm_unit is not None:
            self.write(f":CONFigure:LTE:MODacc:EVM:UNIT {mod_acc_evm_unit}")
        if mod_acc_fft_window_length_pct is not None:
            self.write(f":CONFigure:LTE:MODacc:FFT:WINdow:LENgth {mod_acc_fft_window_length_pct}")
        if mod_acc_fft_window_offset_pct is not None:
            self.write(f":CONFigure:LTE:MODacc:FFT:WINdow:OFFSet {mod_acc_fft_window_offset_pct}")
        if mod_acc_fft_window_type is not None:
            self.write(f":CONFigure:LTE:MODacc:FFT:WINdow:TYPE {mod_acc_fft_window_type}")
        if mod_acc_in_band_emission_mask_type is not None:
            self.write(f":CONFigure:LTE:MODacc:IBE:MASK:TYPE {mod_acc_in_band_emission_mask_type}")
        if mod_acc_iq_gain_imbalance_correction_enabled is not None:
            self.write(f":CONFigure:LTE:MODacc:IQ:GAINimbalance:CORRection:ENABle {1 if mod_acc_iq_gain_imbalance_correction_enabled else 0}")
        if mod_acc_iq_mismatch_estimations_enabled is not None:
            self.write(f":CONFigure:LTE:MODacc:IQ:MISMatch:ESTimation:ENABle {1 if mod_acc_iq_mismatch_estimations_enabled else 0}")
        if mod_acc_iq_origin_offset_estimation_enabled is not None:
            self.write(f":CONFigure:LTE:MODacc:IQ:ORIGin:OFFSet:ESTimation:ENABle {1 if mod_acc_iq_origin_offset_estimation_enabled else 0}")
        if mod_acc_iq_quadrature_error_correction_enabled is not None:
            self.write(f":CONFigure:LTE:MODacc:IQ:QERRor:CORRection:ENABle {1 if mod_acc_iq_quadrature_error_correction_enabled else 0}")
        if mod_acc_iq_timing_skew_correction_enabled is not None:
            self.write(f":CONFigure:LTE:MODacc:IQ:TIMingskew:CORRection:ENABle {1 if mod_acc_iq_timing_skew_correction_enabled else 0}")
        if mod_acc_meas_mode is not None:
            self.write(f":CONFigure:LTE:MODacc:MMODe {mod_acc_meas_mode}")
        if mod_acc_multicarrier_filter_enable is not None:
            self.write(f":CONFigure:LTE:MODacc:MCFilter:ENABle {1 if mod_acc_multicarrier_filter_enable else 0}")
        if mod_acc_number_of_analysis_threads is not None:
            self.write(f":CONFigure:LTE:MODacc:NTHReads {mod_acc_number_of_analysis_threads}")
        if mod_acc_spectrum_inverted is not None:
            self.write(f":CONFigure:LTE:MODacc:SINVerted {1 if mod_acc_spectrum_inverted else 0}")
        if mod_acc_sync_mode is not None:
            self.write(f":CONFigure:LTE:MODacc:SYNC {mod_acc_sync_mode}")

    def config_obw(
        self,
        obw_all_traces_enable: Optional[bool] = None,
        obw_amplitude_correction_type: Optional[str] = None,
        obw_averaging_count: Optional[int] = None,
        obw_averaging_enable: Optional[bool] = None,
        obw_averaging_type: Optional[str] = None,
        obw_enable: Optional[bool] = None,
        obw_number_of_analysis_threads: Optional[int] = None,
        obw_rbw_auto_bandwidth: Optional[bool] = None,
        obw_rbw_bandwidth_hz: Optional[float] = None,
        obw_rbw_filter_type: Optional[str] = None,
        obw_sweep_time_auto: Optional[bool] = None,
        obw_sweep_time_interval_s: Optional[float] = None
    ) -> None:
        """Configures Occupied Bandwidth (OBW) measurement settings."""
        if obw_all_traces_enable is not None:
            self.write(f":CONFigure:LTE:OBW:TRACe:ENABle {1 if obw_all_traces_enable else 0}")
        if obw_amplitude_correction_type is not None:
            self.write(f":CONFigure:LTE:OBW:ACTYpe {obw_amplitude_correction_type}")
        if obw_averaging_count is not None:
            self.write(f":CONFigure:LTE:OBW:AVG:COUNt {obw_averaging_count}")
        if obw_averaging_enable is not None:
            self.write(f":CONFigure:LTE:OBW:AVG:ENABle {1 if obw_averaging_enable else 0}")
        if obw_averaging_type is not None:
            self.write(f":CONFigure:LTE:OBW:AVG:TYPE {obw_averaging_type}")
        if obw_enable is not None:
            self.write(f":CONFigure:LTE:OBW:ENABle {1 if obw_enable else 0}")
        if obw_number_of_analysis_threads is not None:
            self.write(f":CONFigure:LTE:OBW:NTHReads {obw_number_of_analysis_threads}")
        if obw_rbw_auto_bandwidth is not None:
            self.write(f":CONFigure:LTE:OBW:RBW:BWAuto {1 if obw_rbw_auto_bandwidth else 0}")
        if obw_rbw_bandwidth_hz is not None:
            self.write(f":CONFigure:LTE:OBW:RBW:BW {obw_rbw_bandwidth_hz}")
        if obw_rbw_filter_type is not None:
            self.write(f":CONFigure:LTE:OBW:RBW:FILTer {obw_rbw_filter_type}")
        if obw_sweep_time_auto is not None:
            self.write(f":CONFigure:LTE:OBW:SWEep:AUTO {1 if obw_sweep_time_auto else 0}")
        if obw_sweep_time_interval_s is not None:
            self.write(f":CONFigure:LTE:OBW:SWEep:INTerval {obw_sweep_time_interval_s}")

    def config_pvt(
        self,
        pvt_all_traces_enable: Optional[bool] = None,
        pvt_averaging_count: Optional[int] = None,
        pvt_averaging_enable: Optional[bool] = None,
        pvt_averaging_type: Optional[str] = None,
        pvt_enable: Optional[bool] = None,
        pvt_measurement_mode: Optional[str] = None,
        pvt_number_of_analysis_threads: Optional[int] = None,
        pvt_off_power_exclusion_after_s: Optional[float] = None,
        pvt_off_power_exclusion_before_s: Optional[float] = None
    ) -> None:
        """Configures Power vs Time (PVT) measurement settings."""
        if pvt_all_traces_enable is not None:
            self.write(f":CONFigure:LTE:PVT:TRACe:ENABle {1 if pvt_all_traces_enable else 0}")
        if pvt_averaging_count is not None:
            self.write(f":CONFigure:LTE:PVT:AVG:COUNt {pvt_averaging_count}")
        if pvt_averaging_enable is not None:
            self.write(f":CONFigure:LTE:PVT:AVG:ENABle {1 if pvt_averaging_enable else 0}")
        if pvt_averaging_type is not None:
            self.write(f":CONFigure:LTE:PVT:AVG:TYPE {pvt_averaging_type}")
        if pvt_enable is not None:
            self.write(f":CONFigure:LTE:PVT:ENABle {1 if pvt_enable else 0}")
        if pvt_measurement_mode is not None:
            self.write(f":CONFigure:LTE:PVT:METHod {pvt_measurement_mode}")
        if pvt_number_of_analysis_threads is not None:
            self.write(f":CONFigure:LTE:PVT:NTHReads {pvt_number_of_analysis_threads}")
        if pvt_off_power_exclusion_after_s is not None:
            self.write(f":CONFigure:LTE:PVT:POWer:OFF:EXCLusion:AFTer {pvt_off_power_exclusion_after_s}")
        if pvt_off_power_exclusion_before_s is not None:
            self.write(f":CONFigure:LTE:PVT:POWer:OFF:EXCLusion:BEFore {pvt_off_power_exclusion_before_s}")

    def config_sem(
        self,
        sem_aggregated_maximum_power_dbm: Optional[float] = None,
        sem_all_traces_enable: Optional[bool] = None,
        sem_amplitude_correction_type: Optional[str] = None,
        sem_averaging_count: Optional[int] = None,
        sem_averaging_enable: Optional[bool] = None,
        sem_averaging_type: Optional[str] = None,
        sem_delta_f_maximum_hz: Optional[float] = None,
        sem_downlink_mask_type: Optional[str] = None,
        sem_enable: Optional[bool] = None,
        sem_number_of_analysis_threads: Optional[int] = None,
        sem_number_of_offsets: Optional[int] = None,
        sem_offset_absolute_limit_start_dbm: Optional[float] = None,
        sem_offset_absolute_limit_stop_dbm: Optional[float] = None,
        sem_offset_bandwidth_integral: Optional[int] = None,
        sem_offset_limit_fail_mask: Optional[str] = None,
        sem_offset_relative_limit_start_dbm: Optional[float] = None,
        sem_offset_relative_limit_stop_dbm: Optional[float] = None,
        sem_offset_sideband: Optional[str] = None,
        sem_offset_start_frequency_hz: Optional[float] = None,
        sem_offset_stop_frequency_hz: Optional[float] = None,
        sem_rbw_bandwidth_hz: Optional[float] = None,
        sem_rbw_filter_type: Optional[str] = None,
        sem_standard_mask_type: Optional[str] = None,
        sem_sweep_time_auto: Optional[bool] = None,
        sem_sweep_time_interval_s: Optional[float] = None,
        sem_uplink_mask_type: Optional[str] = None
    ) -> None:
        """Configures Spectrum Emission Mask (SEM) settings."""
        if sem_aggregated_maximum_power_dbm is not None:
            self.write(f":CONFigure:LTE:SEM:POWer:MAX:AGGRegated {sem_aggregated_maximum_power_dbm}")
        if sem_all_traces_enable is not None:
            self.write(f":CONFigure:LTE:SEM:TRACe:ENABle {1 if sem_all_traces_enable else 0}")
        if sem_amplitude_correction_type is not None:
            self.write(f":CONFigure:LTE:SEM:ACType {sem_amplitude_correction_type}")
        if sem_averaging_count is not None:
            self.write(f":CONFigure:LTE:SEM:AVG:COUNt {sem_averaging_count}")
        if sem_averaging_enable is not None:
            self.write(f":CONFigure:LTE:SEM:AVG:ENABle {1 if sem_averaging_enable else 0}")
        if sem_averaging_type is not None:
            self.write(f":CONFigure:LTE:SEM:AVG:TYPE {sem_averaging_type}")
        if sem_delta_f_maximum_hz is not None:
            self.write(f":CONFigure:LTE:SEM:DFREquency:MAXimum {sem_delta_f_maximum_hz}")
        if sem_downlink_mask_type is not None:
            self.write(f":CONFigure:LTE:SEM:DLInk:MTYPe {sem_downlink_mask_type}")
        if sem_enable is not None:
            self.write(f":CONFigure:LTE:SEM:ENABle {1 if sem_enable else 0}")
        if sem_number_of_analysis_threads is not None:
            self.write(f":CONFigure:LTE:SEM:NTHReads {sem_number_of_analysis_threads}")
        if sem_number_of_offsets is not None:
            self.write(f":CONFigure:LTE:SEM:NOFFset {sem_number_of_offsets}")
        if sem_offset_absolute_limit_start_dbm is not None:
            self.write(f":CONFigure:LTE:SEM:OFFSet:LIMit:ABSoulte:STARt {sem_offset_absolute_limit_start_dbm}")
        if sem_offset_absolute_limit_stop_dbm is not None:
            self.write(f":CONFigure:LTE:SEM:OFFSet:LIMit:ABSoulte:STOP {sem_offset_absolute_limit_stop_dbm}")
        if sem_offset_bandwidth_integral is not None:
            self.write(f":CONFigure:LTE:SEM:OFFSet:BW:INTegral {sem_offset_bandwidth_integral}")
        if sem_offset_limit_fail_mask is not None:
            self.write(f":CONFigure:LTE:SEM:OFFSet:LIMit:FMASk {sem_offset_limit_fail_mask}")
        if sem_offset_relative_limit_start_dbm is not None:
            self.write(f":CONFigure:LTE:SEM:OFFSet:LIMit:RELative:STARt {sem_offset_relative_limit_start_dbm}")
        if sem_offset_relative_limit_stop_dbm is not None:
            self.write(f":CONFigure:LTE:SEM:OFFSet:LIMit:RELative:STOP {sem_offset_relative_limit_stop_dbm}")
        if sem_offset_sideband is not None:
            self.write(f":CONFigure:LTE:SEM:OFFSet:SBANd {sem_offset_sideband}")
        if sem_offset_start_frequency_hz is not None:
            self.write(f":CONFigure:LTE:SEM:OFFSet:FREQuency:STARt {sem_offset_start_frequency_hz}")
        if sem_offset_stop_frequency_hz is not None:
            self.write(f":CONFigure:LTE:SEM:OFFSet:FREQuency:STOP {sem_offset_stop_frequency_hz}")
        if sem_rbw_bandwidth_hz is not None:
            self.write(f":CONFigure:LTE:SEM:RBW:BW {sem_rbw_bandwidth_hz}")
        if sem_rbw_filter_type is not None:
            self.write(f":CONFigure:LTE:SEM:RBW:TYPE {sem_rbw_filter_type}")
        if sem_standard_mask_type is not None:
            self.write(f":CONFigure:LTE:SEM:MTYPe:STD {sem_standard_mask_type}")
        if sem_sweep_time_auto is not None:
            self.write(f":CONFigure:LTE:SEM:SWEep:AUTO {1 if sem_sweep_time_auto else 0}")
        if sem_sweep_time_interval_s is not None:
            self.write(f":CONFigure:LTE:SEM:SWEep:INTerval {sem_sweep_time_interval_s}")
        if sem_uplink_mask_type is not None:
            self.write(f":CONFigure:LTE:SEM:ULInk:MTYPe {sem_uplink_mask_type}")

    def config_slot_phase(
        self,
        slot_phase_all_traces_enable: Optional[bool] = None,
        slot_phase_common_clock_source_enabled: Optional[bool] = None,
        slot_phase_exclusion_period_enabled: Optional[bool] = None,
        slot_phase_measurement_enabled: Optional[bool] = None,
        slot_phase_measurement_length: Optional[int] = None,
        slot_phase_measurement_offset: Optional[int] = None,
        slot_phase_spectrum_inverted: Optional[bool] = None,
        slot_phase_synchronization_mode: Optional[str] = None
    ) -> None:
        """Configures Slot Phase measurement settings."""
        if slot_phase_all_traces_enable is not None:
            self.write(f":CONFigure:LTE:SLOT:PHASe:TRACe:ENABle {1 if slot_phase_all_traces_enable else 0}")
        if slot_phase_common_clock_source_enabled is not None:
            self.write(f":CONFigure:LTE:SLOT:PHASe:CClock:ENABle {1 if slot_phase_common_clock_source_enabled else 0}")
        if slot_phase_exclusion_period_enabled is not None:
            self.write(f":CONFigure:LTE:SLOT:PHASe:EPERiod:ENABle {1 if slot_phase_exclusion_period_enabled else 0}")
        if slot_phase_measurement_enabled is not None:
            self.write(f":CONFigure:LTE:SLOT:PHASe:MEASurement:ENABle {1 if slot_phase_measurement_enabled else 0}")
        if slot_phase_measurement_length is not None:
            self.write(f":CONFigure:LTE:SLOT:PHASe:MEASurement:LENgth {slot_phase_measurement_length}")
        if slot_phase_measurement_offset is not None:
            self.write(f":CONFigure:LTE:SLOT:PHASe:MEASurement:OFFSet {slot_phase_measurement_offset}")
        if slot_phase_spectrum_inverted is not None:
            self.write(f":CONFigure:LTE:SLOT:PHASe:SPECtrum:INVerted {1 if slot_phase_spectrum_inverted else 0}")
        if slot_phase_synchronization_mode is not None:
            self.write(f":CONFigure:LTE:SLOT:PHASe:SYNC {slot_phase_synchronization_mode}")

    def config_slot_power(
        self,
        slot_power_all_traces_enable: Optional[bool] = None,
        slot_power_common_clock_source_enabled: Optional[bool] = None,
        slot_power_measurement_enabled: Optional[bool] = None,
        slot_power_measurement_length: Optional[int] = None,
        slot_power_measurement_offset: Optional[int] = None,
        slot_power_spectrum_inverted: Optional[bool] = None
    ) -> None:
        """Configures Slot Power measurement settings."""
        if slot_power_all_traces_enable is not None:
            self.write(f":CONFigure:LTE:SLOT:POWer:TRACe:ENABle {1 if slot_power_all_traces_enable else 0}")
        if slot_power_common_clock_source_enabled is not None:
            self.write(f":CONFigure:LTE:SLOT:POWer:CClock:ENABle {1 if slot_power_common_clock_source_enabled else 0}")
        if slot_power_measurement_enabled is not None:
            self.write(f":CONFigure:LTE:SLOT:POWer:MEASurement:ENABle {1 if slot_power_measurement_enabled else 0}")
        if slot_power_measurement_length is not None:
            self.write(f":CONFigure:LTE:SLOT:POWer:MEASurement:LENgth {slot_power_measurement_length}")
        if slot_power_measurement_offset is not None:
            self.write(f":CONFigure:LTE:SLOT:POWer:MEASurement:OFFSet {slot_power_measurement_offset}")
        if slot_power_spectrum_inverted is not None:
            self.write(f":CONFigure:LTE:SLOT:POWer:SPECtrum:INVerted {1 if slot_power_spectrum_inverted else 0}")

    #endregion

    #region Fetch
    def fetch_acp(self, index: int = 1, subblock_index: int = 1) -> Dict[str, str]:
        """Fetches ACP subblock results (total power, offset count, measurement freq/bandwidth/power)."""
        return {
            "meas_freq": self.query(f":FETch:LTE:RESults{index}:ACP:SBlock{subblock_index}:MEAS:FREQuency?").strip(),
            "meas_ibandwidth": self.query(f":FETch:LTE:RESults{index}:ACP:SBlock{subblock_index}:MEAS:IBANDwidth?").strip(),
            "meas_power": self.query(f":FETch:LTE:RESults{index}:ACP:SBlock{subblock_index}:MEAS:POWer?").strip(),
            "offset_count": self.query(f":FETch:LTE:RESults{index}:ACP:SBlock{subblock_index}:OFFSet:COUNt?").strip(),
            "power_total": self.query(f":FETch:LTE:RESults{index}:ACP:SBlock{subblock_index}:POWer:TOTal?").strip(),
        }

    def fetch_acp_carrier(self, index: int = 1, subblock_index: int = 1, carrier_index: int = 1) -> Dict[str, str]:
        """Fetches ACP component carrier power results."""
        return {
            "power_abs": self.query(f":FETch:LTE:RESults{index}:ACP:SBlock{subblock_index}:CCARrier{carrier_index}:POWer:ABSolute?").strip(),
            "power_rel": self.query(f":FETch:LTE:RESults{index}:ACP:SBlock{subblock_index}:CCARrier{carrier_index}:POWer:RELative?").strip(),
        }

    def fetch_acp_offset(self, index: int = 1, subblock_index: int = 1, offset_index: int = 1) -> Dict[str, str]:
        """Fetches ACP lower/upper offset channel power results."""
        return {
            "lower_power_abs": self.query(f":FETch:LTE:RESults{index}:ACP:SBlock{subblock_index}:OFFSet{offset_index}:LOWer:POWer:ABSolute?").strip(),
            "lower_power_rel": self.query(f":FETch:LTE:RESults{index}:ACP:SBlock{subblock_index}:OFFSet{offset_index}:LOWer:POWer:RELative?").strip(),
            "upper_power_abs": self.query(f":FETch:LTE:RESults{index}:ACP:SBlock{subblock_index}:OFFSet{offset_index}:UPPer:POWer:ABSolute?").strip(),
            "upper_power_rel": self.query(f":FETch:LTE:RESults{index}:ACP:SBlock{subblock_index}:OFFSet{offset_index}:UPPer:POWer:RELative?").strip(),
        }

    def fetch_acp_results(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches the combined ACP results string (total power, subblock, carriers, offsets)."""
        return self.query(f":FETch:LTE:RESults{index}:ACP:SBlock{subblock_index}?").strip()

    def fetch_acp_results_all(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches the combined ACP results string (ALL form)."""
        return self.query(f":FETch:LTE:RESults{index}:ACP:SBlock{subblock_index}:ALL?").strip()

    def fetch_acp_meas_results(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches the ACP subblock measurement results string."""
        return self.query(f":FETch:LTE:RESults{index}:ACP:SBlock{subblock_index}:MEAS?").strip()

    def fetch_acp_meas_results_all(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches the ACP subblock measurement results string (ALL form)."""
        return self.query(f":FETch:LTE:RESults{index}:ACP:SBlock{subblock_index}:MEAS:ALL?").strip()

    def fetch_acp_carrier_results(self, index: int = 1, subblock_index: int = 1, carrier_index: int = 1) -> str:
        """Fetches the ACP carrier measurement results string."""
        return self.query(f":FETch:LTE:RESults{index}:ACP:SBlock{subblock_index}:CCARrier{carrier_index}?").strip()

    def fetch_acp_offset_results(self, index: int = 1, subblock_index: int = 1, offset_index: int = 1) -> str:
        """Fetches the ACP offset channel measurement results string."""
        return self.query(f":FETch:LTE:RESults{index}:ACP:SBlock{subblock_index}:OFFSet{offset_index}?").strip()

    def fetch_chp(self, index: int = 1, subblock_index: int = 1) -> Dict[str, str]:
        """Fetches CHP subblock results (total power, measurement freq/bandwidth/power)."""
        return {
            "meas_freq": self.query(f":FETch:LTE:RESults{index}:CHP:SBlock{subblock_index}:MEAS:FREQuency?").strip(),
            "meas_ibandwidth": self.query(f":FETch:LTE:RESults{index}:CHP:SBlock{subblock_index}:MEAS:IBANDwidth?").strip(),
            "meas_power": self.query(f":FETch:LTE:RESults{index}:CHP:SBlock{subblock_index}:MEAS:POWer?").strip(),
            "power_total": self.query(f":FETch:LTE:RESults{index}:CHP:SBlock{subblock_index}:POWer:TOTal?").strip(),
        }

    def fetch_chp_carrier(self, index: int = 1, subblock_index: int = 1, carrier_index: int = 1) -> Dict[str, str]:
        """Fetches CHP component carrier power results."""
        return {
            "power_abs": self.query(f":FETch:LTE:RESults{index}:CHP:SBlock{subblock_index}:CCARrier{carrier_index}:POWer:ABSolute?").strip(),
            "power_rel": self.query(f":FETch:LTE:RESults{index}:CHP:SBlock{subblock_index}:CCARrier{carrier_index}:POWer:RELative?").strip(),
        }

    def fetch_chp_results(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches the combined CHP results string (total power, subblock, carriers)."""
        return self.query(f":FETch:LTE:RESults{index}:CHP:SBlock{subblock_index}?").strip()

    def fetch_chp_results_all(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches the combined CHP results string (ALL form)."""
        return self.query(f":FETch:LTE:RESults{index}:CHP:SBlock{subblock_index}:ALL?").strip()

    def fetch_chp_meas_results(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches the CHP subblock measurement results string."""
        return self.query(f":FETch:LTE:RESults{index}:CHP:SBlock{subblock_index}:MEAS?").strip()

    def fetch_chp_meas_results_all(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches the CHP subblock measurement results string (ALL form)."""
        return self.query(f":FETch:LTE:RESults{index}:CHP:SBlock{subblock_index}:MEAS:ALL?").strip()

    def fetch_chp_carrier_results(self, index: int = 1, subblock_index: int = 1, carrier_index: int = 1) -> str:
        """Fetches the CHP carrier measurement results string."""
        return self.query(f":FETch:LTE:RESults{index}:CHP:SBlock{subblock_index}:CCARrier{carrier_index}?").strip()

    def fetch_modacc(self, index: int = 1, subblock_index: int = 1) -> Dict[str, str]:
        """Fetches ModAcc subblock results (IBE margin, IQ impairments, number of subblocks)."""
        return {
            "ibe_margin": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:IBE:MARGin?").strip(),
            "iq_mean_gain_imbalances": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:IQ:MEAN:GAIN:IMBalances?").strip(),
            "iq_mean_origin_offsets": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:IQ:MEAN:ORIGin:OFFSets?").strip(),
            "iq_mean_quadrature_errors": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:IQ:MEAN:QUADrature:ERRors?").strip(),
            "number": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:NUMber?").strip(),
        }

    def fetch_modacc_carrier_npusch(self, index: int = 1, subblock_index: int = 1, carrier_index: int = 1) -> Dict[str, str]:
        """Fetches ModAcc NPUSCH (NB-IoT uplink) EVM and power results."""
        return {
            "npusch_evm_dmrs_peak_max": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:NPUSch:EVM:DMRS:PEAK:MAX?").strip(),
            "npusch_evm_peak_max": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:NPUSch:EVM:PEAK:MAX?").strip(),
            "npusch_evm_rms_dmrs_mean": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:NPUSch:EVM:RMS:DMRS:MEAN?").strip(),
            "npusch_evm_rms_mean": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:NPUSch:EVM:RMS:MEAN?").strip(),
            "npusch_power_dmrs_mean": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:NPUSch:POWer:DMRS:MEAN?").strip(),
            "npusch_power_mean": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:NPUSch:POWer:MEAN?").strip(),
        }

    def fetch_modacc_carrier_pusch(self, index: int = 1, subblock_index: int = 1, carrier_index: int = 1) -> Dict[str, str]:
        """Fetches ModAcc PUSCH EVM and power results."""
        return {
            "pusch_evm_dmr_peak_max": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:PUSCh:EVM:DMR:PEAK:MAX?").strip(),
            "pusch_evm_peak_max": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:PUSCh:EVM:PEAK:MAX?").strip(),
            "pusch_power_dmrs_mean": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:PUSCh:POWer:DMRS:MEAN?").strip(),
            "pusch_power_mean": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:PUSCh:POWer:MEAN?").strip(),
            "pusch_rms_evm_dmr_mean": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:PUSCh:RMS:EVM:DMR:MEAN?").strip(),
            "pusch_rms_evm_mean": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:PUSCh:RMS:EVM:MEAN?").strip(),
        }

    def fetch_modacc_carrier_pdsch(self, index: int = 1, subblock_index: int = 1, carrier_index: int = 1) -> Dict[str, str]:
        """Fetches ModAcc PDSCH EVM results per modulation type."""
        return {
            "pdsch_evm_rms_mean": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:PDSCh:EVM:RMS:MEAN?").strip(),
            "pdsch_evm_rms_qam_1024_mean": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:PDSCh:EVM:RMS:QAM:1024:MEAN?").strip(),
            "pdsch_evm_rms_qam_16_mean": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:PDSCh:EVM:RMS:QAM:16:MEAN?").strip(),
            "pdsch_evm_rms_qam_256_mean": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:PDSCh:EVM:RMS:QAM:256:MEAN?").strip(),
            "pdsch_evm_rms_qam_64_mean": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:PDSCh:EVM:RMS:QAM:64:MEAN?").strip(),
            "pdsch_evm_rms_qpsk_mean": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:PDSCh:EVM:RMS:QPSK:MEAN?").strip(),
        }

    def fetch_modacc_carrier(self, index: int = 1, subblock_index: int = 1, carrier_index: int = 1) -> Dict[str, str]:
        """Fetches ModAcc component carrier results (EVM, frequency error, IQ impairments, magnitude/phase errors, SRS/RS power)."""
        return {
            "detected_cid": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:DETected:CID?").strip(),
            "evm_peak_index_scarrier": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:EVM:PEAK:INDex:SCARrier?").strip(),
            "evm_peak_index_slot": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:EVM:PEAK:INDex:SLOT?").strip(),
            "evm_peak_index_symbol": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:EVM:PEAK:INDex:SYMBol?").strip(),
            "evm_peak_max": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:EVM:PEAK:MAX?").strip(),
            "evm_rms_csrs_mean": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:EVM:RMS:CSRS:MEAN?").strip(),
            "evm_rms_mean": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:EVM:RMS:MEAN?").strip(),
            "evm_rms_pss_mean": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:EVM:RMS:PSS:MEAN?").strip(),
            "evm_rms_srs_mean": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:EVM:RMS:SRS:MEAN?").strip(),
            "evm_rms_sss_mean": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:EVM:RMS:SSS:MEAN?").strip(),
            "ibe_margin": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:IBE:MARGin?").strip(),
            "iq_mean_gain_imbalances": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:IQ:MEAN:GAIN:IMBalances?").strip(),
            "iq_mean_origin_offsets": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:IQ:MEAN:ORIGin:OFFSets?").strip(),
            "iq_mean_quadrature_errors": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:IQ:MEAN:QUADrature:ERRors?").strip(),
            "mean_freq_error": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:MEAN:FREQuency:ERRor?").strip(),
            "mean_iq_timingskew": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:MEAN:IQ:TIMingskew?").strip(),
            "mean_toffsets": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:MEAN:TOFFsets?").strip(),
            "ofdm_symbol_tpower": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:OFDM:SYMBol:TPOWer?").strip(),
            "peak_magnitude_errors_max": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:PEAK:MAGNitude:ERRors:MAX?").strip(),
            "peak_phase_errors_max": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:PEAK:PHASe:ERRors:MAX?").strip(),
            "power_srs_mean": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:POWer:SRS:MEAN?").strip(),
            "r1max_r1min": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:R1MAX:R1MIN?").strip(),
            "r1max_r2min": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:R1MAX:R2MIN?").strip(),
            "r2max_r1min": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:R2MAX:R1MIN?").strip(),
            "r2max_r2min": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:R2MAX:R2MIN?").strip(),
            "reserved_1": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:REServed:1?").strip(),
            "reserved_2": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:REServed:2?").strip(),
            "rms_mean_magnitude_errors": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:RMS:MEAN:MAGNitude:ERRors?").strip(),
            "rms_mean_phase_errors": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:RMS:MEAN:PHASe:ERRors?").strip(),
            "rs_tpower": self.query(f":FETch:LTE:RESults{index}:MODacc:SBlock{subblock_index}:CCARrier{carrier_index}:RS:TPOWer?").strip(),
        }

    def fetch_obw(self, index: int = 1, subblock_index: int = 1) -> Dict[str, str]:
        """Fetches Occupied Bandwidth (OBW) results."""
        return {
            "bandwidth": self.query(f":FETch:LTE:RESults{index}:OBW:SBlock{subblock_index}:BANDwidth?").strip(),
            "freq_start": self.query(f":FETch:LTE:RESults{index}:OBW:SBlock{subblock_index}:FREQuency:STARt?").strip(),
            "freq_stop": self.query(f":FETch:LTE:RESults{index}:OBW:SBlock{subblock_index}:FREQuency:STOP?").strip(),
            "power_abs": self.query(f":FETch:LTE:RESults{index}:OBW:SBlock{subblock_index}:POWer:ABSolute?").strip(),
        }

    def fetch_obw_results(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches the combined OBW results string."""
        return self.query(f":FETch:LTE:RESults{index}:OBW:SBlock{subblock_index}?").strip()

    def fetch_obw_results_all(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches the combined OBW results string (ALL form)."""
        return self.query(f":FETch:LTE:RESults{index}:OBW:SBlock{subblock_index}:ALL?").strip()

    def fetch_pvt(self, index: int = 1, subblock_index: int = 1) -> Dict[str, str]:
        """Fetches Power vs Time (PVT) subblock results."""
        return {
            "sbnumber": self.query(f":FETch:LTE:RESults{index}:PVT:SBlock{subblock_index}:SBNumber?").strip(),
        }

    def fetch_pvt_carrier(self, index: int = 1, subblock_index: int = 1, carrier_index: int = 1) -> Dict[str, str]:
        """Fetches Power vs Time (PVT) carrier results (burst width, on/off power, status)."""
        return {
            "burst_width": self.query(f":FETch:LTE:RESults{index}:PVT:SBlock{subblock_index}:CARRier{carrier_index}:BURSt:WIDth?").strip(),
            "power_off_abs_mean_after": self.query(f":FETch:LTE:RESults{index}:PVT:SBlock{subblock_index}:CARRier{carrier_index}:POWer:OFF:ABSolute:MEAN:AFTer?").strip(),
            "power_off_abs_mean_before": self.query(f":FETch:LTE:RESults{index}:PVT:SBlock{subblock_index}:CARRier{carrier_index}:POWer:OFF:ABSolute:MEAN:BEFore?").strip(),
            "power_on_abs_mean": self.query(f":FETch:LTE:RESults{index}:PVT:SBlock{subblock_index}:CARRier{carrier_index}:POWer:ON:ABSolute:MEAN?").strip(),
            "status": self.query(f":FETch:LTE:RESults{index}:PVT:SBlock{subblock_index}:CARRier{carrier_index}:STATus?").strip(),
        }

    def fetch_sem(self, index: int = 1, subblock_index: int = 1) -> Dict[str, str]:
        """Fetches SEM subblock results (total power, status, measurement freq/bandwidth/power)."""
        return {
            "meas_freq": self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:MEAS:FREQuency?").strip(),
            "meas_ibandwidth": self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:MEAS:IBANDwidth?").strip(),
            "meas_power": self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:MEAS:POWer?").strip(),
            "power_total": self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:POWer:TOTal?").strip(),
            "status": self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:STATus?").strip(),
        }

    def fetch_sem_carrier(self, index: int = 1, subblock_index: int = 1, carrier_index: int = 1) -> Dict[str, str]:
        """Fetches SEM component carrier results."""
        return {
            "freq_peak": self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:CCARrier{carrier_index}:FREQuency:PEAK?").strip(),
            "ipower_abs": self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:CCARrier{carrier_index}:IPOWer:ABSolute?").strip(),
            "ipower_rel": self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:CCARrier{carrier_index}:IPOWer:RELative?").strip(),
            "power_peak_abs": self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:CCARrier{carrier_index}:POWer:PEAK:ABS?").strip(),
        }

    def fetch_sem_offset_margin(self, index: int = 1, subblock_index: int = 1, offset_index: int = 1) -> Dict[str, str]:
        """Fetches SEM lower/upper offset margin results at a given offset index."""
        return {
            "lower_freq": self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:OFFSet:MARGin:LOWer{offset_index}:FREQuency?").strip(),
            "lower_margin": self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:OFFSet:MARGin:LOWer{offset_index}:MARGin?").strip(),
            "lower_power_abs": self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:OFFSet:MARGin:LOWer{offset_index}:POWer:ABSolute?").strip(),
            "lower_power_rel": self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:OFFSet:MARGin:LOWer{offset_index}:POWer:RELative?").strip(),
            "lower_status": self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:OFFSet:MARGin:LOWer{offset_index}:STATus?").strip(),
            "upper_freq": self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:OFFSet:MARGin:UPPer{offset_index}:FREQuency?").strip(),
            "upper_margin": self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:OFFSet:MARGin:UPPer{offset_index}:MARGin?").strip(),
            "upper_power_abs": self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:OFFSet:MARGin:UPPer{offset_index}:POWer:ABSolute?").strip(),
            "upper_power_rel": self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:OFFSet:MARGin:UPPer{offset_index}:POWer:RELative?").strip(),
            "upper_status": self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:OFFSet:MARGin:UPPer{offset_index}:STATus?").strip(),
        }

    def fetch_sem_offset_power(self, index: int = 1, subblock_index: int = 1, offset_index: int = 1) -> Dict[str, str]:
        """Fetches SEM lower/upper offset power results at a given offset index."""
        return {
            "lower_freq": self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:OFFSet:POWer:LOWer{offset_index}:FREQuency?").strip(),
            "lower_ipower_abs": self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:OFFSet:POWer:LOWer{offset_index}:IPOWer:ABSolute?").strip(),
            "lower_ipower_rel": self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:OFFSet:POWer:LOWer{offset_index}:IPOWer:RELative?").strip(),
            "lower_power_abs": self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:OFFSet:POWer:LOWer{offset_index}:POWer:ABSolute?").strip(),
            "lower_power_rel": self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:OFFSet:POWer:LOWer{offset_index}:POWer:RELative?").strip(),
            "upper_freq": self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:OFFSet:POWer:UPPer{offset_index}:FREQuency?").strip(),
            "upper_ipower_abs": self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:OFFSet:POWer:UPPer{offset_index}:IPOWer:ABSolute?").strip(),
            "upper_ipower_rel": self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:OFFSet:POWer:UPPer{offset_index}:IPOWer:RELative?").strip(),
            "upper_power_abs": self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:OFFSet:POWer:UPPer{offset_index}:POWer:ABSolute?").strip(),
            "upper_power_rel": self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:OFFSet:POWer:UPPer{offset_index}:POWer:RELative?").strip(),
        }

    def fetch_sem_results_all(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches the combined SEM results string."""
        return self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:ALL?").strip()

    def fetch_sem_meas_results(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches the SEM subblock measurement results string."""
        return self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:MEAS?").strip()

    def fetch_sem_meas_results_all(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches the SEM subblock measurement results string (ALL form)."""
        return self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:MEAS:ALL?").strip()

    def fetch_sem_carrier_results(self, index: int = 1, subblock_index: int = 1, carrier_index: int = 1) -> str:
        """Fetches the SEM carrier measurement results string."""
        return self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:CCARrier{carrier_index}?").strip()

    def fetch_sem_offset_margin_results(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches all lower and upper SEM offset margins."""
        return self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:OFFSet:MARGin?").strip()

    def fetch_sem_offset_margin_lower_results(self, index: int = 1, subblock_index: int = 1, offset_index: int = 1) -> str:
        """Fetches lower offset margin results (margin, freq, abs/rel power)."""
        return self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:OFFSet:MARGin:LOWer{offset_index}?").strip()

    def fetch_sem_offset_margin_upper_results(self, index: int = 1, subblock_index: int = 1, offset_index: int = 1) -> str:
        """Fetches upper offset margin results (margin, freq, abs/rel power)."""
        return self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:OFFSet:MARGin:UPPer{offset_index}?").strip()

    def fetch_sem_offset_power_results(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches all lower and upper SEM offset powers."""
        return self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:OFFSet:POWer?").strip()

    def fetch_sem_offset_power_lower_results(self, index: int = 1, subblock_index: int = 1, offset_index: int = 1) -> str:
        """Fetches lower offset power results (peak freq, peak/integrated powers)."""
        return self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:OFFSet:POWer:LOWer{offset_index}?").strip()

    def fetch_sem_offset_power_upper_results(self, index: int = 1, subblock_index: int = 1, offset_index: int = 1) -> str:
        """Fetches upper offset power results (peak freq, peak/integrated powers)."""
        return self.query(f":FETch:LTE:RESults{index}:SEM:SBlock{subblock_index}:OFFSet:POWer:UPPer{offset_index}?").strip()

    def fetch_slot_phase(self, index: int = 1, subblock_index: int = 1) -> Dict[str, str]:
        """Fetches Slot Phase results (maximum phase discontinuity)."""
        return {
            "phase_discontinuity_max": self.query(f":FETch:LTE:RESults{index}:SLOT:PHASe:SBlock{subblock_index}:PHASe:DISContinuity:MAX?").strip(),
        }

    def fetch_slot_phase_discontinuity(self, index: int = 1, subblock_index: int = 1, slot_index: int = 1) -> str:
        """Fetches the phase difference at a given slot boundary."""
        return self.query(f":FETch:LTE:RESults{index}:SLOT:PHASe:SBlock{subblock_index}:PHASe:DISContinuity{slot_index}?").strip()

    def fetch_slot_power_subframe_power(self, index: int = 1, subblock_index: int = 1, subframe_index: int = 1) -> str:
        """Fetches the subframe power (dBm) at a given subframe."""
        return self.query(f":FETch:LTE:RESults{index}:SLOT:POWer:SBlock{subblock_index}:SFRame:POWer{subframe_index}?").strip()

    def fetch_slot_power_subframe_power_delta(self, index: int = 1, subblock_index: int = 1, subframe_index: int = 1) -> str:
        """Fetches the subframe power delta (dB) at a given subframe."""
        return self.query(f":FETch:LTE:RESults{index}:SLOT:POWer:SBlock{subblock_index}:SFRame:POWer:DELTa{subframe_index}?").strip()

    #endregion
