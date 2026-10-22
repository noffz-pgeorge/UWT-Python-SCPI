from uwt.instrument import UwtVisaInstrument
from typing import List, Dict, Union, Tuple, Optional

class NrClient(UwtVisaInstrument):

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
        self.write(f":NR:INITiate {result_space}")

    def get_measurement_state(self) -> str:
        """Returns the current state (READY, PROCESSING, OFF, PENDING, ACTIVE)."""
        return self.query(":NR:MEASurement:STATe?").strip()

    def reset(self) -> None:
        """Resets the analyzer to its default state."""
        self.write(":NR:RESet")

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
        """Configures NR trigger settings."""
        if trigger_delay_sec is not None:
            self.write(f":TRIGger:NR:DELay {trigger_delay_sec}")
        if trigger_edge is not None:
            self.write(f":TRIGger:NR:EDGE {trigger_edge}")
        if trigger_min_quiet_duration_sec is not None:
            self.write(f":TRIGger:NR:MQTime {trigger_min_quiet_duration_sec}")
        if trigger_source is not None:
            self.write(f":TRIGger:NR:SOURce {trigger_source}")
        if trigger_threshold is not None:
            self.write(f":TRIGger:NR:THReshold {trigger_threshold}")
        if trigger_timeout_sec is not None:
            self.write(f":TRIGger:NR:TOUT {trigger_timeout_sec}")

    def config_signal(
        self,
        auto_resource_block_detection_enabled: Optional[bool] = None,
        gnodeb_category: Optional[str] = None,
        gnodeb_type: Optional[str] = None,
        grid_size_mode: Optional[str] = None,
        link_direction: Optional[str] = None,
        phase_compensation: Optional[str] = None,
        power_class: Optional[str] = None,
        trace_enable: Optional[bool] = None,
        transmit_antenna_to_analyze: Optional[int] = None
    ) -> None:
        """Configures link direction, gNodeB type/category, power class, grid, phase compensation, and auto-detection settings."""
        if auto_resource_block_detection_enabled is not None:
            self.write(f":CONFigure:NR:RBAuto:ENABle {1 if auto_resource_block_detection_enabled else 0}")
        if gnodeb_category is not None:
            self.write(f":CONFigure:NR:GNB:CATegory {gnodeb_category}")
        if gnodeb_type is not None:
            self.write(f":CONFigure:NR:GNODeb:TYPE {gnodeb_type}")
        if grid_size_mode is not None:
            self.write(f":CONFigure:NR:GRId:SIZE:MODE {grid_size_mode}")
        if link_direction is not None:
            self.write(f":CONFigure:NR:LINK:DIRection {link_direction}")
        if phase_compensation is not None:
            self.write(f":CONFigure:NR:COMPensation:PHASe {phase_compensation}")
        if power_class is not None:
            self.write(f":CONFigure:NR:POWClass {power_class}")
        if trace_enable is not None:
            self.write(f":CONFigure:NR:TRACe:ENABle {1 if trace_enable else 0}")
        if transmit_antenna_to_analyze is not None:
            self.write(f":CONFigure:NR:ANTenna {transmit_antenna_to_analyze}")

    def config_subblock(
        self,
        subblock_index: int = 1,
        cc_at_center_frequency: Optional[int] = None,
        cc_spacing_type: Optional[str] = None,
        center_frequency_hz: Optional[float] = None,
        channel_raster: Optional[str] = None,
        frequency_definition: Optional[str] = None,
        frequency_range: Optional[str] = None,
        max_input_power_dbm: Optional[float] = None,
        nr_band: Optional[int] = None,
        phase_compensation_frequency_hz: Optional[float] = None,
        tx_lo_frequency_hz: Optional[float] = None,
        user_margin_db: Optional[float] = None
    ) -> None:
        """Configures subblock band, frequency range, center/LO frequency, raster, power, and margin settings."""
        if cc_at_center_frequency is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CENTer:INDex {cc_at_center_frequency}")
        if cc_spacing_type is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCSType {cc_spacing_type}")
        if center_frequency_hz is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:FREQuency:CENTer {center_frequency_hz}")
        if channel_raster is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CHRaster {channel_raster}")
        if frequency_definition is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:FREQuency:DEFinition {frequency_definition}")
        if frequency_range is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:FRANge {frequency_range}")
        if max_input_power_dbm is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:POWer:MAX {max_input_power_dbm}")
        if nr_band is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:BAND {nr_band}")
        if phase_compensation_frequency_hz is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:FREQuency:PHASecomp {phase_compensation_frequency_hz}")
        if tx_lo_frequency_hz is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:FREQuency:TXLO {tx_lo_frequency_hz}")
        if user_margin_db is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:UMARgin {user_margin_db}")

    def config_carrier(
        self,
        subblock_index: int = 1,
        carrier_index: int = 1,
        carrier_cell_id: Optional[int] = None,
        carrier_channel_bandwidth: Optional[str] = None,
        frequency_hz: Optional[float] = None,
        number_of_bandwidth_parts: Optional[int] = None,
        reference_grid_start: Optional[int] = None,
        reference_grid_subcarrier_spacing: Optional[str] = None
    ) -> None:
        """Configures component carrier bandwidth, frequency, cell ID, BWP count, and RB alignment."""
        if carrier_cell_id is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:CID {carrier_cell_id}")
        if carrier_channel_bandwidth is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BW {carrier_channel_bandwidth}")
        if frequency_hz is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:FREQuency {frequency_hz}")
        if number_of_bandwidth_parts is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP:NUMber {number_of_bandwidth_parts}")
        if reference_grid_start is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:RBALignment:GRID:STARt {reference_grid_start}")
        if reference_grid_subcarrier_spacing is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:RBALignment:GRID:SCSPacing {reference_grid_subcarrier_spacing}")

    def config_bwp(
        self,
        subblock_index: int = 1,
        carrier_index: int = 1,
        bwp_index: int = 1,
        cyclic_prefix_mode: Optional[str] = None,
        grid_start: Optional[int] = None,
        number_of_rbs: Optional[int] = None,
        number_of_users: Optional[int] = None,
        rb_offset: Optional[int] = None,
        subcarrier_spacing: Optional[str] = None
    ) -> None:
        """Configures bandwidth part (BWP) numerology, RB allocation, grid start, and user count."""
        if cyclic_prefix_mode is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:CPMode {cyclic_prefix_mode}")
        if grid_start is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:GRID:STARt {grid_start}")
        if number_of_rbs is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:RBNum {number_of_rbs}")
        if number_of_users is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER:NUMber {number_of_users}")
        if rb_offset is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:RBOffset {rb_offset}")
        if subcarrier_spacing is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:SCSPacing {subcarrier_spacing}")

    def config_user(
        self,
        subblock_index: int = 1,
        carrier_index: int = 1,
        bwp_index: int = 1,
        user_index: int = 1,
        number_of_pdsch_configuration: Optional[int] = None,
        number_of_pusch_configuration: Optional[int] = None,
        rnti: Optional[int] = None
    ) -> None:
        """Configures BWP user RNTI and PDSCH/PUSCH configuration counts."""
        if number_of_pdsch_configuration is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PDSCh:NUMber {number_of_pdsch_configuration}")
        if number_of_pusch_configuration is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PUSCh:NUMber {number_of_pusch_configuration}")
        if rnti is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:RNTI {rnti}")

    def config_pdsch_cluster(
        self,
        subblock_index: int = 1,
        carrier_index: int = 1,
        bwp_index: int = 1,
        user_index: int = 1,
        pdsch_index: int = 1,
        cluster_index: int = 1,
        number_of_rbs: Optional[int] = None,
        rb_offset: Optional[int] = None
    ) -> None:
        """Configures a PDSCH RB cluster (RB count and offset)."""
        if number_of_rbs is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PDSCh{pdsch_index}:CLUSter{cluster_index}:RBNum {number_of_rbs}")
        if rb_offset is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PDSCh{pdsch_index}:CLUSter{cluster_index}:RBOffset {rb_offset}")

    def config_pdsch(
        self,
        subblock_index: int = 1,
        carrier_index: int = 1,
        bwp_index: int = 1,
        user_index: int = 1,
        pdsch_index: int = 1,
        dmrs_additional_positions: Optional[int] = None,
        dmrs_antenna_ports: Optional[str] = None,
        dmrs_configuration_type: Optional[str] = None,
        dmrs_duration: Optional[str] = None,
        dmrs_number_of_cdm_groups: Optional[int] = None,
        dmrs_power_db: Optional[float] = None,
        dmrs_power_mode: Optional[str] = None,
        dmrs_scrambling_id_mode: Optional[str] = None,
        dmrs_type_a_position: Optional[int] = None,
        mapping_type: Optional[str] = None,
        modulation_type: Optional[str] = None,
        present_in_ssb_rb: Optional[bool] = None,
        ptrs_enabled: Optional[bool] = None,
        slot_allocation: Optional[str] = None,
        symbol_allocation: Optional[str] = None
    ) -> None:
        """Configures PDSCH allocation, modulation, DMRS, and PTRS settings."""
        if dmrs_additional_positions is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PDSCh{pdsch_index}:DMRS:MAPPing:APOSition {dmrs_additional_positions}")
        if dmrs_antenna_ports is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PDSCh{pdsch_index}:DMRS:ANTenna:PORT {dmrs_antenna_ports}")
        if dmrs_configuration_type is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PDSCh{pdsch_index}:DMRS:CFG:TYPE {dmrs_configuration_type}")
        if dmrs_duration is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PDSCh{pdsch_index}:DMRS:MAPPing:DURation {dmrs_duration}")
        if dmrs_number_of_cdm_groups is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PDSCh{pdsch_index}:DMRS:NCDMgroups {dmrs_number_of_cdm_groups}")
        if dmrs_power_db is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PDSCh{pdsch_index}:DMRS:POWer {dmrs_power_db}")
        if dmrs_power_mode is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PDSCh{pdsch_index}:DMRS:POWer:MODE {dmrs_power_mode}")
        if dmrs_scrambling_id_mode is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PDSCh{pdsch_index}:DMRS:NSCid {dmrs_scrambling_id_mode}")
        if dmrs_type_a_position is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PDSCh{pdsch_index}:DMRS:MAPPing:TYPE:A:PO {dmrs_type_a_position}")
        if mapping_type is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PDSCh{pdsch_index}:DMRS:MAPPing:TYPE {mapping_type}")
        if modulation_type is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PDSCh{pdsch_index}:MODulation:TYPE {modulation_type}")
        if present_in_ssb_rb is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PDSCh{pdsch_index}:SSB {1 if present_in_ssb_rb else 0}")
        if ptrs_enabled is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PDSCh{pdsch_index}:PTRS:ENABle {1 if ptrs_enabled else 0}")
        if slot_allocation is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PDSCh{pdsch_index}:ALLocation:SLOT {slot_allocation}")
        if symbol_allocation is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PDSCh{pdsch_index}:ALLocation:SYMBol {symbol_allocation}")

    def config_pusch(
        self,
        subblock_index: int = 1,
        carrier_index: int = 1,
        bwp_index: int = 1,
        user_index: int = 1,
        pusch_index: int = 1,
        dmrs_additional_positions: Optional[int] = None,
        dmrs_antenna_ports: Optional[str] = None,
        dmrs_configuration_type: Optional[str] = None,
        dmrs_duration: Optional[str] = None,
        dmrs_number_of_cdm_groups: Optional[int] = None,
        dmrs_power_db: Optional[float] = None,
        dmrs_power_mode: Optional[str] = None,
        dmrs_scrambling_id_mode: Optional[str] = None,
        dmrs_type_a_position: Optional[int] = None,
        mapping_type: Optional[str] = None,
        modulation_type: Optional[str] = None,
        ptrs_enabled: Optional[bool] = None,
        slot_allocation: Optional[str] = None,
        symbol_allocation: Optional[str] = None,
        transform_precoding_enabled: Optional[bool] = None
    ) -> None:
        """Configures PUSCH allocation, modulation, DMRS, PTRS, and transform precoding settings."""
        if dmrs_additional_positions is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PUSCh{pusch_index}:DMRS:MAPPing:APOSition {dmrs_additional_positions}")
        if dmrs_antenna_ports is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PUSCh{pusch_index}:DMRS:ANTenna:PORT {dmrs_antenna_ports}")
        if dmrs_configuration_type is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PUSCh{pusch_index}:DMRS:CFG:TYPE {dmrs_configuration_type}")
        if dmrs_duration is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PUSCh{pusch_index}:DMRS:MAPPing:DURation {dmrs_duration}")
        if dmrs_number_of_cdm_groups is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PUSCh{pusch_index}:DMRS:NCDMgroups {dmrs_number_of_cdm_groups}")
        if dmrs_power_db is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PUSCh{pusch_index}:DMRS:POWer {dmrs_power_db}")
        if dmrs_power_mode is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PUSCh{pusch_index}:DMRS:POWer:MODE {dmrs_power_mode}")
        if dmrs_scrambling_id_mode is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PUSCh{pusch_index}:DMRS:NSCid {dmrs_scrambling_id_mode}")
        if dmrs_type_a_position is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PUSCh{pusch_index}:DMRS:MAPPing:TYPE:A:PO {dmrs_type_a_position}")
        if mapping_type is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PUSCh{pusch_index}:DMRS:MAPPing:TYPE {mapping_type}")
        if modulation_type is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PUSCh{pusch_index}:MODulation:TYPE {modulation_type}")
        if ptrs_enabled is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PUSCh{pusch_index}:PTRS:ENABle {1 if ptrs_enabled else 0}")
        if slot_allocation is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PUSCh{pusch_index}:ALLocation:SLOT {slot_allocation}")
        if symbol_allocation is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PUSCh{pusch_index}:ALLocation:SYMBol {symbol_allocation}")
        if transform_precoding_enabled is not None:
            self.write(f":CONFigure:NR:SBLock{subblock_index}:CCARrier{carrier_index}:BWP{bwp_index}:USER{user_index}:PUSCh{pusch_index}:TRPCoding:ENABle {1 if transform_precoding_enabled else 0}")

    def config_acp(
        self,
        acp_all_traces_enable: Optional[bool] = None,
        acp_amplitude_correction_type: Optional[str] = None,
        acp_averaging_count: Optional[int] = None,
        acp_averaging_enable: Optional[bool] = None,
        acp_averaging_type: Optional[str] = None,
        acp_enable: Optional[bool] = None,
        acp_far_if_output_power_offset_db: Optional[float] = None,
        acp_if_output_power_offset_auto: Optional[bool] = None,
        acp_measurement_method: Optional[str] = None,
        acp_near_if_output_power_offset_db: Optional[float] = None,
        acp_noise_compensation_enable: Optional[bool] = None,
        acp_number_of_analysis_threads: Optional[int] = None,
        acp_number_of_eutra_offsets: Optional[int] = None,
        acp_number_of_nr_offsets: Optional[int] = None,
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
            self.write(f":CONFigure:NR:ACP:TRACe:ENABle {1 if acp_all_traces_enable else 0}")
        if acp_amplitude_correction_type is not None:
            self.write(f":CONFigure:NR:ACP:ACTYpe {acp_amplitude_correction_type}")
        if acp_averaging_count is not None:
            self.write(f":CONFigure:NR:ACP:AVG:COUNt {acp_averaging_count}")
        if acp_averaging_enable is not None:
            self.write(f":CONFigure:NR:ACP:AVG:ENABle {1 if acp_averaging_enable else 0}")
        if acp_averaging_type is not None:
            self.write(f":CONFigure:NR:ACP:AVG:TYPE {acp_averaging_type}")
        if acp_enable is not None:
            self.write(f":CONFigure:NR:ACP:ENABle {1 if acp_enable else 0}")
        if acp_far_if_output_power_offset_db is not None:
            self.write(f":CONFigure:NR:ACP:IF:OPOWer:FAR:OFFSet {acp_far_if_output_power_offset_db}")
        if acp_if_output_power_offset_auto is not None:
            self.write(f":CONFigure:NR:ACP:IF:OPOWer:FAR:AUTO {1 if acp_if_output_power_offset_auto else 0}")
        if acp_measurement_method is not None:
            self.write(f":CONFigure:NR:ACP:METHod {acp_measurement_method}")
        if acp_near_if_output_power_offset_db is not None:
            self.write(f":CONFigure:NR:ACP:IF:OPOWer:NEAR:OFFSet {acp_near_if_output_power_offset_db}")
        if acp_noise_compensation_enable is not None:
            self.write(f":CONFigure:NR:ACP:NCOMp:ENABle {1 if acp_noise_compensation_enable else 0}")
        if acp_number_of_analysis_threads is not None:
            self.write(f":CONFigure:NR:ACP:NTHReads {acp_number_of_analysis_threads}")
        if acp_number_of_eutra_offsets is not None:
            self.write(f":CONFigure:NR:ACP:NOFFsets:EUTRa {acp_number_of_eutra_offsets}")
        if acp_number_of_nr_offsets is not None:
            self.write(f":CONFigure:NR:ACP:NR {acp_number_of_nr_offsets}")
        if acp_number_of_utra_offsets is not None:
            self.write(f":CONFigure:NR:ACP:NOFFsets:UTRa {acp_number_of_utra_offsets}")
        if acp_power_units is not None:
            self.write(f":CONFigure:NR:ACP:POWer:UNITs {acp_power_units}")
        if acp_rbw_auto_bandwidth is not None:
            self.write(f":CONFigure:NR:ACP:RBW:BWAuto {1 if acp_rbw_auto_bandwidth else 0}")
        if acp_rbw_bandwidth_hz is not None:
            self.write(f":CONFigure:NR:ACP:RBW:BW {acp_rbw_bandwidth_hz}")
        if acp_rbw_filter_type is not None:
            self.write(f":CONFigure:NR:ACP:RBW:FILTer {acp_rbw_filter_type}")
        if acp_sequential_fft_size is not None:
            self.write(f":CONFigure:NR:ACP:SFFT:SIZE {acp_sequential_fft_size}")
        if acp_sweep_time_auto is not None:
            self.write(f":CONFigure:NR:ACP:SWEep:AUTO {1 if acp_sweep_time_auto else 0}")
        if acp_sweep_time_interval_s is not None:
            self.write(f":CONFigure:NR:ACP:SWEep:INTerval {acp_sweep_time_interval_s}")

    def config_chp(
        self,
        chp_all_traces_enable: Optional[bool] = None,
        chp_amplitude_correction_type: Optional[str] = None,
        chp_averaging_count: Optional[int] = None,
        chp_averaging_enable: Optional[bool] = None,
        chp_averaging_type: Optional[str] = None,
        chp_enable: Optional[bool] = None,
        chp_number_of_analysis_threads: Optional[int] = None,
        chp_rbw_auto_bandwidth: Optional[bool] = None,
        chp_rbw_bandwidth_hz: Optional[float] = None,
        chp_rbw_filter_type: Optional[str] = None,
        chp_sweep_time_auto: Optional[bool] = None,
        chp_sweep_time_interval_s: Optional[float] = None
    ) -> None:
        """Configures Channel Power (CHP) measurement settings."""
        if chp_all_traces_enable is not None:
            self.write(f":CONFigure:NR:CHP:TRACe:ENABle {1 if chp_all_traces_enable else 0}")
        if chp_amplitude_correction_type is not None:
            self.write(f":CONFigure:NR:CHP:ACTYpe {chp_amplitude_correction_type}")
        if chp_averaging_count is not None:
            self.write(f":CONFigure:NR:CHP:AVG:COUNt {chp_averaging_count}")
        if chp_averaging_enable is not None:
            self.write(f":CONFigure:NR:CHP:AVG:ENABle {1 if chp_averaging_enable else 0}")
        if chp_averaging_type is not None:
            self.write(f":CONFigure:NR:CHP:AVG:TYPE {chp_averaging_type}")
        if chp_enable is not None:
            self.write(f":CONFigure:NR:CHP:ENABle {1 if chp_enable else 0}")
        if chp_number_of_analysis_threads is not None:
            self.write(f":CONFigure:NR:CHP:NTHReads {chp_number_of_analysis_threads}")
        if chp_rbw_auto_bandwidth is not None:
            self.write(f":CONFigure:NR:CHP:RBW:BWAuto {1 if chp_rbw_auto_bandwidth else 0}")
        if chp_rbw_bandwidth_hz is not None:
            self.write(f":CONFigure:NR:CHP:RBW:BW {chp_rbw_bandwidth_hz}")
        if chp_rbw_filter_type is not None:
            self.write(f":CONFigure:NR:CHP:RBW:FILTer {chp_rbw_filter_type}")
        if chp_sweep_time_auto is not None:
            self.write(f":CONFigure:NR:CHP:SWEep:AUTO {1 if chp_sweep_time_auto else 0}")
        if chp_sweep_time_interval_s is not None:
            self.write(f":CONFigure:NR:CHP:SWEep:INTerval {chp_sweep_time_interval_s}")

    def config_modacc(
        self,
        mod_acc_all_traces_enable: Optional[bool] = None,
        mod_acc_averaging_count: Optional[int] = None,
        mod_acc_averaging_enable: Optional[bool] = None,
        mod_acc_channel_estimation_type: Optional[str] = None,
        mod_acc_common_clock_source_enable: Optional[bool] = None,
        mod_acc_dc_subcarrier_removal_enable: Optional[bool] = None,
        mod_acc_enable: Optional[bool] = None,
        mod_acc_evm_reference_data_symbols_mode: Optional[str] = None,
        mod_acc_evm_unit: Optional[str] = None,
        mod_acc_fft_window_length_pct: Optional[float] = None,
        mod_acc_fft_window_offset_pct: Optional[float] = None,
        mod_acc_fft_window_type: Optional[str] = None,
        mod_acc_frequency_error_estimation: Optional[str] = None,
        mod_acc_iq_gain_imbalance_correction_enabled: Optional[bool] = None,
        mod_acc_iq_impairments_estimation_enabled: Optional[bool] = None,
        mod_acc_iq_impairments_model: Optional[str] = None,
        mod_acc_iq_impairments_per_subcarrier_enabled: Optional[bool] = None,
        mod_acc_iq_mismatch_estimation_enabled: Optional[bool] = None,
        mod_acc_iq_origin_offset_estimation_enabled: Optional[bool] = None,
        mod_acc_iq_quadrature_error_correction_enabled: Optional[bool] = None,
        mod_acc_iq_timing_skew_correction_enabled: Optional[bool] = None,
        mod_acc_magnitude_and_phase_error_enabled: Optional[bool] = None,
        mod_acc_meas_length: Optional[float] = None,
        mod_acc_meas_length_unit: Optional[str] = None,
        mod_acc_meas_offset: Optional[float] = None,
        mod_acc_measurement_mode: Optional[str] = None,
        mod_acc_multicarrier_filter_enable: Optional[bool] = None,
        mod_acc_number_of_analysis_threads: Optional[int] = None,
        mod_acc_phase_tracking_enabled: Optional[bool] = None,
        mod_acc_spectral_flatness: Optional[str] = None,
        mod_acc_spectrum_inverted: Optional[bool] = None,
        mod_acc_symbol_clock_error_estimation_enabled: Optional[bool] = None,
        mod_acc_sync_mode: Optional[str] = None,
        mod_acc_timing_tracking_enabled: Optional[bool] = None
    ) -> None:
        """Configures Modulation Accuracy (ModAcc) settings."""
        if mod_acc_all_traces_enable is not None:
            self.write(f":CONFigure:NR:MODacc:TRACe:ENABle {1 if mod_acc_all_traces_enable else 0}")
        if mod_acc_averaging_count is not None:
            self.write(f":CONFigure:NR:MODacc:AVG:COUNt {mod_acc_averaging_count}")
        if mod_acc_averaging_enable is not None:
            self.write(f":CONFigure:NR:MODacc:AVG:ENABle {1 if mod_acc_averaging_enable else 0}")
        if mod_acc_channel_estimation_type is not None:
            self.write(f":CONFigure:NR:MODacc:CETYpe {mod_acc_channel_estimation_type}")
        if mod_acc_common_clock_source_enable is not None:
            self.write(f":CONFigure:NR:MODacc:CCLock:ENABle {1 if mod_acc_common_clock_source_enable else 0}")
        if mod_acc_dc_subcarrier_removal_enable is not None:
            self.write(f":CONFigure:NR:MODacc:DC:SCRemoval:ENABle {1 if mod_acc_dc_subcarrier_removal_enable else 0}")
        if mod_acc_enable is not None:
            self.write(f":CONFigure:NR:MODacc:ENABle {1 if mod_acc_enable else 0}")
        if mod_acc_evm_reference_data_symbols_mode is not None:
            self.write(f":CONFigure:NR:MODacc:Evm:REFerence:DATA:SYMBols:MODE {mod_acc_evm_reference_data_symbols_mode}")
        if mod_acc_evm_unit is not None:
            self.write(f":CONFigure:NR:MODacc:EVM:UNIT {mod_acc_evm_unit}")
        if mod_acc_fft_window_length_pct is not None:
            self.write(f":CONFigure:NR:MODacc:FFT:WINdow:LENgth {mod_acc_fft_window_length_pct}")
        if mod_acc_fft_window_offset_pct is not None:
            self.write(f":CONFigure:NR:MODacc:FFT:WINdow:OFFSet {mod_acc_fft_window_offset_pct}")
        if mod_acc_fft_window_type is not None:
            self.write(f":CONFigure:NR:MODacc:FFT:WINdow:TYPE {mod_acc_fft_window_type}")
        if mod_acc_frequency_error_estimation is not None:
            self.write(f":CONFigure:NR:MODacc:FERR:ESTimation {mod_acc_frequency_error_estimation}")
        if mod_acc_iq_gain_imbalance_correction_enabled is not None:
            self.write(f":CONFigure:NR:MODacc:IQ:GAINimbalance:CORRection:ENABle {1 if mod_acc_iq_gain_imbalance_correction_enabled else 0}")
        if mod_acc_iq_impairments_estimation_enabled is not None:
            self.write(f":CONFigure:NR:MODacc:IQ:IMPairments:ESTimation:ENABle {1 if mod_acc_iq_impairments_estimation_enabled else 0}")
        if mod_acc_iq_impairments_model is not None:
            self.write(f":CONFigure:NR:MODacc:IQ:IMPairments:MODel {mod_acc_iq_impairments_model}")
        if mod_acc_iq_impairments_per_subcarrier_enabled is not None:
            self.write(f":CONFigure:NR:MODacc:IQ:IMPairmentsersubcarrier:ENABle {1 if mod_acc_iq_impairments_per_subcarrier_enabled else 0}")
        if mod_acc_iq_mismatch_estimation_enabled is not None:
            self.write(f":CONFigure:NR:MODacc:IQ:MISMatch:ESTimation:ENABle {1 if mod_acc_iq_mismatch_estimation_enabled else 0}")
        if mod_acc_iq_origin_offset_estimation_enabled is not None:
            self.write(f":CONFigure:NR:MODacc:IQ:ORIGin:OFFSet:ESTimation:ENABle {1 if mod_acc_iq_origin_offset_estimation_enabled else 0}")
        if mod_acc_iq_quadrature_error_correction_enabled is not None:
            self.write(f":CONFigure:NR:MODacc:IQ:QERRor:CORRection:ENABle {1 if mod_acc_iq_quadrature_error_correction_enabled else 0}")
        if mod_acc_iq_timing_skew_correction_enabled is not None:
            self.write(f":CONFigure:NR:MODacc:IQ:TIMingskew:CORRection:ENABle {1 if mod_acc_iq_timing_skew_correction_enabled else 0}")
        if mod_acc_magnitude_and_phase_error_enabled is not None:
            self.write(f":CONFigure:NR:MODacc:MAGNitudeandphase:ERRor:ENABle {1 if mod_acc_magnitude_and_phase_error_enabled else 0}")
        if mod_acc_meas_length is not None:
            self.write(f":CONFigure:NR:MODacc:MEASurement:LENgth {mod_acc_meas_length}")
        if mod_acc_meas_length_unit is not None:
            self.write(f":CONFigure:NR:MODacc:MEASurement:UNIT {mod_acc_meas_length_unit}")
        if mod_acc_meas_offset is not None:
            self.write(f":CONFigure:NR:MODacc:MEASurement:OFFSet {mod_acc_meas_offset}")
        if mod_acc_measurement_mode is not None:
            self.write(f":CONFigure:NR:MODacc:MEASurement:MODE {mod_acc_measurement_mode}")
        if mod_acc_multicarrier_filter_enable is not None:
            self.write(f":CONFigure:NR:MODacc:MCFilter:ENABle {1 if mod_acc_multicarrier_filter_enable else 0}")
        if mod_acc_number_of_analysis_threads is not None:
            self.write(f":CONFigure:NR:ModAcc:NTHReads {mod_acc_number_of_analysis_threads}")
        if mod_acc_phase_tracking_enabled is not None:
            self.write(f":CONFigure:NR:MODacc:TRACking:PHASe {1 if mod_acc_phase_tracking_enabled else 0}")
        if mod_acc_spectral_flatness is not None:
            self.write(f":CONFigure:NR:MODacc:SFCondition {mod_acc_spectral_flatness}")
        if mod_acc_spectrum_inverted is not None:
            self.write(f":CONFigure:NR:MODacc:SINVerted {1 if mod_acc_spectrum_inverted else 0}")
        if mod_acc_symbol_clock_error_estimation_enabled is not None:
            self.write(f":CONFigure:NR:MODacc:SYMBol:CERRor:ESTimation:ENABle {1 if mod_acc_symbol_clock_error_estimation_enabled else 0}")
        if mod_acc_sync_mode is not None:
            self.write(f":CONFigure:NR:MODacc:SYNC {mod_acc_sync_mode}")
        if mod_acc_timing_tracking_enabled is not None:
            self.write(f":CONFigure:NR:MODacc:TRACking:TIME {1 if mod_acc_timing_tracking_enabled else 0}")

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
            self.write(f":CONFigure:NR:OBW:TRACe:ENABle {1 if obw_all_traces_enable else 0}")
        if obw_amplitude_correction_type is not None:
            self.write(f":CONFigure:NR:OBW:ACTYpe {obw_amplitude_correction_type}")
        if obw_averaging_count is not None:
            self.write(f":CONFigure:NR:OBW:AVG:COUNt {obw_averaging_count}")
        if obw_averaging_enable is not None:
            self.write(f":CONFigure:NR:OBW:AVG:ENABle {1 if obw_averaging_enable else 0}")
        if obw_averaging_type is not None:
            self.write(f":CONFigure:NR:OBW:AVG:TYPE {obw_averaging_type}")
        if obw_enable is not None:
            self.write(f":CONFigure:NR:OBW:ENABle {1 if obw_enable else 0}")
        if obw_number_of_analysis_threads is not None:
            self.write(f":CONFigure:NR:OBW:NTHReads {obw_number_of_analysis_threads}")
        if obw_rbw_auto_bandwidth is not None:
            self.write(f":CONFigure:NR:OBW:RBW:BWAuto {1 if obw_rbw_auto_bandwidth else 0}")
        if obw_rbw_bandwidth_hz is not None:
            self.write(f":CONFigure:NR:OBW:RBW:BW {obw_rbw_bandwidth_hz}")
        if obw_rbw_filter_type is not None:
            self.write(f":CONFigure:NR:OBW:RBW:TYPE {obw_rbw_filter_type}")
        if obw_sweep_time_auto is not None:
            self.write(f":CONFigure:NR:OBW:SWEep:AUTO {1 if obw_sweep_time_auto else 0}")
        if obw_sweep_time_interval_s is not None:
            self.write(f":CONFigure:NR:OBW:SWEep:INTerval {obw_sweep_time_interval_s}")

    def config_sem(
        self,
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
        sem_sweep_time_auto: Optional[bool] = None,
        sem_sweep_time_interval_s: Optional[float] = None,
        sem_uplink_mask_type: Optional[str] = None
    ) -> None:
        """Configures Spectrum Emission Mask (SEM) settings."""
        if sem_all_traces_enable is not None:
            self.write(f":CONFigure:NR:SEM:TRACe:ENABle {1 if sem_all_traces_enable else 0}")
        if sem_amplitude_correction_type is not None:
            self.write(f":CONFigure:NR:SEM:ACTYpe {sem_amplitude_correction_type}")
        if sem_averaging_count is not None:
            self.write(f":CONFigure:NR:SEM:AVG:COUNt {sem_averaging_count}")
        if sem_averaging_enable is not None:
            self.write(f":CONFigure:NR:SEM:AVG:ENABle {1 if sem_averaging_enable else 0}")
        if sem_averaging_type is not None:
            self.write(f":CONFigure:NR:SEM:AVG:TYPE {sem_averaging_type}")
        if sem_delta_f_maximum_hz is not None:
            self.write(f":CONFigure:NR:SEM:DFREquency:MAXimum {sem_delta_f_maximum_hz}")
        if sem_downlink_mask_type is not None:
            self.write(f":CONFigure:NR:SEM:DLInk:MTYPe {sem_downlink_mask_type}")
        if sem_enable is not None:
            self.write(f":CONFigure:NR:SEM:ENABle {1 if sem_enable else 0}")
        if sem_number_of_analysis_threads is not None:
            self.write(f":CONFigure:NR:SEM:NTHReads {sem_number_of_analysis_threads}")
        if sem_number_of_offsets is not None:
            self.write(f":CONFigure:NR:SEM:NOFFset {sem_number_of_offsets}")
        if sem_offset_absolute_limit_start_dbm is not None:
            self.write(f":CONFigure:NR:SEM:OFFSet:LIMit:ABSolute:STARt {sem_offset_absolute_limit_start_dbm}")
        if sem_offset_absolute_limit_stop_dbm is not None:
            self.write(f":CONFigure:NR:SEM:OFFSet:LIMit:ABSolute:STOP {sem_offset_absolute_limit_stop_dbm}")
        if sem_offset_bandwidth_integral is not None:
            self.write(f":CONFigure:NR:SEM:RBW:INTegral {sem_offset_bandwidth_integral}")
        if sem_offset_limit_fail_mask is not None:
            self.write(f":CONFigure:NR:SEM:OFFSet:LIMit:MASK {sem_offset_limit_fail_mask}")
        if sem_offset_relative_limit_start_dbm is not None:
            self.write(f":CONFigure:NR:SEM:OFFSet:LIMit:RELative:STARt {sem_offset_relative_limit_start_dbm}")
        if sem_offset_relative_limit_stop_dbm is not None:
            self.write(f":CONFigure:NR:SEM:OFFSet:LIMit:RELative:STOP {sem_offset_relative_limit_stop_dbm}")
        if sem_offset_sideband is not None:
            self.write(f":CONFigure:NR:SEM:OFFSet:SBANd {sem_offset_sideband}")
        if sem_offset_start_frequency_hz is not None:
            self.write(f":CONFigure:NR:SEM:OFFSet:FREQuency:STARt {sem_offset_start_frequency_hz}")
        if sem_offset_stop_frequency_hz is not None:
            self.write(f":CONFigure:NR:SEM:OFFSet:FREQuency:STOP {sem_offset_stop_frequency_hz}")
        if sem_rbw_bandwidth_hz is not None:
            self.write(f":CONFigure:NR:SEM:RBW:BW {sem_rbw_bandwidth_hz}")
        if sem_rbw_filter_type is not None:
            self.write(f":CONFigure:NR:SEM:RBW:TYPE {sem_rbw_filter_type}")
        if sem_sweep_time_auto is not None:
            self.write(f":CONFigure:NR:SEM:SWEep:AUTO {1 if sem_sweep_time_auto else 0}")
        if sem_sweep_time_interval_s is not None:
            self.write(f":CONFigure:NR:SEM:SWEep:INTerval {sem_sweep_time_interval_s}")
        if sem_uplink_mask_type is not None:
            self.write(f":CONFigure:NR:SEM:ULInk:MTYPe {sem_uplink_mask_type}")

    def config_txp(
        self,
        txp_all_traces_enable: Optional[bool] = None,
        txp_averaging_count: Optional[int] = None,
        txp_averaging_enable: Optional[bool] = None,
        txp_enable: Optional[bool] = None,
        txp_measurement_interval_sec: Optional[float] = None,
        txp_measurement_offset_sec: Optional[float] = None,
        txp_number_of_analysis_threads: Optional[int] = None
    ) -> None:
        """Configures TX Power (TXP) measurement settings."""
        if txp_all_traces_enable is not None:
            self.write(f":CONFigure:NR:TXP:TRACe:ENABle {1 if txp_all_traces_enable else 0}")
        if txp_averaging_count is not None:
            self.write(f":CONFigure:NR:TXP:AVG:COUNt {txp_averaging_count}")
        if txp_averaging_enable is not None:
            self.write(f":CONFigure:NR:TXP:AVG:ENABle {1 if txp_averaging_enable else 0}")
        if txp_enable is not None:
            self.write(f":CONFigure:NR:TXP:ENABle {1 if txp_enable else 0}")
        if txp_measurement_interval_sec is not None:
            self.write(f":CONFigure:NR:TXP:MEASurement:INTerval {txp_measurement_interval_sec}")
        if txp_measurement_offset_sec is not None:
            self.write(f":CONFigure:NR:TXP:MEASurement:OFFSet {txp_measurement_offset_sec}")
        if txp_number_of_analysis_threads is not None:
            self.write(f":CONFigure:NR:TXP:NTHReads {txp_number_of_analysis_threads}")

    #endregion

    #region Fetch
    def fetch_acp(self, index: int = 1, subblock_index: int = 1) -> Dict[str, str]:
        """Fetches ACP subblock results (total power, offset count, measurement freq/bandwidth/power)."""
        return {
            "meas_freq": self.query(f":FETch:NR:RESults{index}:ACP:SBLock{subblock_index}:MEAS:FREQuency?").strip(),
            "meas_ibandwidth": self.query(f":FETch:NR:RESults{index}:ACP:SBLock{subblock_index}:MEAS:IBANDwidth?").strip(),
            "meas_power": self.query(f":FETch:NR:RESults{index}:ACP:SBLock{subblock_index}:MEAS:POWer?").strip(),
            "offset_count": self.query(f":FETch:NR:RESults{index}:ACP:SBLock{subblock_index}:OFFSet:COUNt?").strip(),
            "power_total": self.query(f":FETch:NR:RESults{index}:ACP:SBLock{subblock_index}:POWer:TOTal?").strip(),
        }

    def fetch_acp_carrier(self, index: int = 1, subblock_index: int = 1, carrier_index: int = 1) -> Dict[str, str]:
        """Fetches ACP component carrier power results."""
        return {
            "power_abs": self.query(f":FETch:NR:RESults{index}:ACP:SBLock{subblock_index}:CCARrier{carrier_index}:POWer:ABSolute?").strip(),
            "power_rel": self.query(f":FETch:NR:RESults{index}:ACP:SBLock{subblock_index}:CCARrier{carrier_index}:POWer:RELative?").strip(),
        }

    def fetch_acp_offset(self, index: int = 1, subblock_index: int = 1, offset_index: int = 1) -> Dict[str, str]:
        """Fetches ACP lower/upper offset channel power results."""
        return {
            "lower_power_abs": self.query(f":FETch:NR:RESults{index}:ACP:SBLock{subblock_index}:OFFSet{offset_index}:LOWer:POWer:ABSolute?").strip(),
            "lower_power_rel": self.query(f":FETch:NR:RESults{index}:ACP:SBLock{subblock_index}:OFFSet{offset_index}:LOWer:POWer:RELative?").strip(),
            "upper_power_abs": self.query(f":FETch:NR:RESults{index}:ACP:SBLock{subblock_index}:OFFSet{offset_index}:UPPer:POWer:ABSolute?").strip(),
            "upper_power_rel": self.query(f":FETch:NR:RESults{index}:ACP:SBLock{subblock_index}:OFFSet{offset_index}:UPPer:POWer:RELative?").strip(),
        }

    def fetch_acp_results(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches the combined ACP results string (total power, subblock, carriers, offsets)."""
        return self.query(f":FETch:NR:RESults{index}:ACP:SBLock{subblock_index}?").strip()

    def fetch_acp_results_all(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches the combined ACP results string (ALL form)."""
        return self.query(f":FETch:NR:RESults{index}:ACP:SBLock{subblock_index}:ALL?").strip()

    def fetch_acp_meas_results(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches the ACP subblock measurement results string."""
        return self.query(f":FETch:NR:RESults{index}:ACP:SBLock{subblock_index}:MEAS?").strip()

    def fetch_acp_meas_results_all(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches the ACP subblock measurement results string (ALL form)."""
        return self.query(f":FETch:NR:RESults{index}:ACP:SBLock{subblock_index}:MEAS:ALL?").strip()

    def fetch_acp_carrier_results(self, index: int = 1, subblock_index: int = 1, carrier_index: int = 1) -> str:
        """Fetches the ACP carrier measurement results string."""
        return self.query(f":FETch:NR:RESults{index}:ACP:SBLock{subblock_index}:CCARrier{carrier_index}?").strip()

    def fetch_acp_offset_results(self, index: int = 1, subblock_index: int = 1, offset_index: int = 1) -> str:
        """Fetches the ACP offset channel measurement results string."""
        return self.query(f":FETch:NR:RESults{index}:ACP:SBLock{subblock_index}:OFFSet{offset_index}?").strip()

    def fetch_chp(self, index: int = 1, subblock_index: int = 1) -> Dict[str, str]:
        """Fetches CHP subblock results (total power, measurement freq/bandwidth/power)."""
        return {
            "meas_freq": self.query(f":FETch:NR:RESults{index}:CHP:SBLock{subblock_index}:MEAS:FREQuency?").strip(),
            "meas_ibandwidth": self.query(f":FETch:NR:RESults{index}:CHP:SBLock{subblock_index}:MEAS:IBANDwidth?").strip(),
            "meas_power": self.query(f":FETch:NR:RESults{index}:CHP:SBLock{subblock_index}:MEAS:POWer?").strip(),
            "power_total": self.query(f":FETch:NR:RESults{index}:CHP:SBLock{subblock_index}:POWer:TOTal?").strip(),
        }

    def fetch_chp_carrier(self, index: int = 1, subblock_index: int = 1, carrier_index: int = 1) -> Dict[str, str]:
        """Fetches CHP component carrier power results."""
        return {
            "power_abs": self.query(f":FETch:NR:RESults{index}:CHP:SBLock{subblock_index}:CCARrier{carrier_index}:POWer:ABSolute?").strip(),
            "power_rel": self.query(f":FETch:NR:RESults{index}:CHP:SBLock{subblock_index}:CCARrier{carrier_index}:POWer:RELative?").strip(),
        }

    def fetch_chp_results(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches the combined CHP results string (total power, subblock, carriers)."""
        return self.query(f":FETch:NR:RESults{index}:CHP:SBLock{subblock_index}?").strip()

    def fetch_chp_results_all(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches the combined CHP results string (ALL form)."""
        return self.query(f":FETch:NR:RESults{index}:CHP:SBLock{subblock_index}:ALL?").strip()

    def fetch_chp_meas_results(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches the CHP subblock measurement results string."""
        return self.query(f":FETch:NR:RESults{index}:CHP:SBLock{subblock_index}:MEAS?").strip()

    def fetch_chp_meas_results_all(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches the CHP subblock measurement results string (ALL form)."""
        return self.query(f":FETch:NR:RESults{index}:CHP:SBLock{subblock_index}:MEAS:ALL?").strip()

    def fetch_chp_carrier_results(self, index: int = 1, subblock_index: int = 1, carrier_index: int = 1) -> str:
        """Fetches the CHP carrier measurement results string."""
        return self.query(f":FETch:NR:RESults{index}:CHP:SBLock{subblock_index}:CCARrier{carrier_index}?").strip()

    def fetch_modacc_carrier_pdsch(self, index: int = 1, subblock_index: int = 1, carrier_index: int = 1) -> Dict[str, str]:
        """Fetches ModAcc PDSCH EVM (data/DMRS/PTRS) and power results."""
        return {
            "pdsch_evm_data_peak_max": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:PDSCh:EVM:DATA:PEAK:MAXimum?").strip(),
            "pdsch_evm_data_rms_mean": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:PDSCh:EVM:DATA:RMS:MEAN?").strip(),
            "pdsch_evm_dmrs_peak_max": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:PDSCh:EVM:DMRS:PEAK:MAXimum?").strip(),
            "pdsch_evm_dmrs_rms_mean": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:PDSCh:EVM:DMRS:RMS:MEAN?").strip(),
            "pdsch_evm_ptrs_rms_mean": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:PDSCh:EVM:PTRS:RMS:MEAN?").strip(),
            "pdsch_powers_data_mean": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:PDSCh:POWers:DATA:MEAN?").strip(),
            "pdsch_powers_dmrs_mean": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:PDSCh:POWers:DMRS:MEAN?").strip(),
            "pdsch_powers_ptrs_mean": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:PDSCh:POWers:PTRS:MEAN?").strip(),
        }

    def fetch_modacc_carrier_pusch(self, index: int = 1, subblock_index: int = 1, carrier_index: int = 1) -> Dict[str, str]:
        """Fetches ModAcc PUSCH EVM (data/DMRS/PTRS) and power results."""
        return {
            "pusch_evm_data_peak_max": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:PUSCh:EVM:DATA:PEAK:MAXimum?").strip(),
            "pusch_evm_data_rms_mean": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:PUSCh:EVM:DATA:RMS:MEAN?").strip(),
            "pusch_evm_dmrs_peak_max": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:PUSCh:EVM:DMRS:PEAK:MAXimum?").strip(),
            "pusch_evm_dmrs_rms_mean": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:PUSCh:EVM:DMRS:RMS:MEAN?").strip(),
            "pusch_evm_ptrs_peak_max": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:PUSCh:EVM:PTRS:PEAK:MAXimum?").strip(),
            "pusch_evm_ptrs_rms_mean": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:PUSCh:EVM:PTRS:RMS:MEAN?").strip(),
            "pusch_powers_data_mean": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:PUSCh:POWers:DATA:MEAN?").strip(),
            "pusch_powers_dmrs_mean": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:PUSCh:POWers:DMRS:MEAN?").strip(),
            "pusch_powers_ptrs_mean": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:PUSCh:POWers:PTRS:MEAN?").strip(),
        }

    def fetch_modacc_carrier_spectral_flatness(self, index: int = 1, subblock_index: int = 1, carrier_index: int = 1) -> Dict[str, str]:
        """Fetches ModAcc spectral flatness results (range 1/2 min/max and subcarrier indices)."""
        return {
            "fmargin_slot_index": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:SPECtral:FMARgin:SLOT:INDex?").strip(),
            "frange1_max": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:SPECtral:FRANge1:MAXimum?").strip(),
            "frange1_max_subcarrier_index": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:SPECtral:FRANge1:MAXimum:SUBCarrier:INDex?").strip(),
            "frange1_min": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:SPECtral:FRANge1:MINimum?").strip(),
            "frange1_min_subcarrier_index": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:SPECtral:FRANge1:MINimum:SUBCarrier:INDex?").strip(),
            "frange2_max": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:SPECtral:FRANge2:MAXimum?").strip(),
            "frange2_max_subcarrier_index": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:SPECtral:FRANge2:MAXimum:SUBCarrier:INDex?").strip(),
            "frange2_min": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:SPECtral:FRANge2:MINimum?").strip(),
            "frange2_min_subcarrier_index": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:SPECtral:FRANge2:MINimum:SUBCarrier:INDex?").strip(),
        }

    def fetch_modacc_carrier(self, index: int = 1, subblock_index: int = 1, carrier_index: int = 1) -> Dict[str, str]:
        """Fetches ModAcc component carrier results (EVM, impairments, magnitude/phase errors, PBCH/PSS/SSS EVM, IBE margin)."""
        return {
            "evm_peak_bw_index": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:EVM:PEAK:BW:INDex?").strip(),
            "evm_peak_max": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:EVM:PEAK:MAXimum?").strip(),
            "evm_peak_slot_index": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:EVM:PEAK:SLOT:INDex?").strip(),
            "evm_peak_subcarrier_index": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:EVM:PEAK:SUBCarrier:INDex?").strip(),
            "evm_peak_symbol_index": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:EVM:PEAK:SYMbol:INDex?").strip(),
            "evm_rms_mean": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:EVM:RMS:MEAN?").strip(),
            "ibe_margin": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:IBE:MARGin?").strip(),
            "impairments_ferror_mean": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:IMPairments:FERRor:MEAN?").strip(),
            "impairments_iqgain_imbalance": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:IMPairments:IQGain:IMBalance?").strip(),
            "impairments_iqorigin_offset": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:IMPairments:IQOrigin:OFFSet?").strip(),
            "impairments_iqquadrature": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:IMPairments:IQQuadrature?").strip(),
            "iq_timingskew_mean": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:IQ:TIMingskew:MEAN?").strip(),
            "magnitude_peak_max": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:MAGNitude:PEAK:MAXimum?").strip(),
            "magnitude_rms_mean": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:MAGNitude:RMS:MEAN?").strip(),
            "noise_compensation_applied": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:NOISe:COMPensation:APPLied?").strip(),
            "pbch_data_peak_evm_max": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:PBCH:DATA:PEAK:EVM:MAXimum?").strip(),
            "pbch_data_rms_evm_mean": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:PBCH:DATA:RMS:EVM:MEAN?").strip(),
            "pbch_dmrs_peak_evm_maxium": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:PBCH:DMRS:PEAK:EVM:MAXium?").strip(),
            "pbch_dmrs_rms_evm_mean": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:PBCH:DMRS:RMS:EVM:MEAN?").strip(),
            "phase_peak_max": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:PHASe:PEAK:MAXimum?").strip(),
            "phase_rms_mean": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:PHASe:RMS:MEAN?").strip(),
            "pss_peak_evm_max": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:PSS:PEAK:EVM:MAXimum?").strip(),
            "pss_rms_evm_mean": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:PSS:RMS:EVM:MEAN?").strip(),
            "sss_peak_evm_max": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:SSS:PEAK:EVM:MAXimum?").strip(),
            "sss_rms_evm_mean": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:SSS:RMS:EVM:MEAN?").strip(),
            "toffset_mean": self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:TOFFset:MEAN?").strip(),
        }

    def fetch_modacc_results_all(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches the combined ModAcc results string for the subblock."""
        return self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:ALL?").strip()

    def fetch_modacc_carrier_results_all(self, index: int = 1, subblock_index: int = 1, carrier_index: int = 1) -> str:
        """Fetches the combined ModAcc carrier results string."""
        return self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:ALL?").strip()

    def fetch_modacc_carrier_evm_results_all(self, index: int = 1, subblock_index: int = 1, carrier_index: int = 1) -> str:
        """Fetches the combined ModAcc carrier EVM results string."""
        return self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:EVM:ALL?").strip()

    def fetch_modacc_carrier_impairments_results(self, index: int = 1, subblock_index: int = 1, carrier_index: int = 1) -> str:
        """Fetches the combined ModAcc carrier impairments results string."""
        return self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:IMPairments?").strip()

    def fetch_modacc_carrier_pdsch_results(self, index: int = 1, subblock_index: int = 1, carrier_index: int = 1) -> str:
        """Fetches the combined ModAcc PDSCH results string."""
        return self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:PDSCh?").strip()

    def fetch_modacc_carrier_pusch_results(self, index: int = 1, subblock_index: int = 1, carrier_index: int = 1) -> str:
        """Fetches the combined ModAcc PUSCH results string."""
        return self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:PUSCh?").strip()

    def fetch_modacc_carrier_spectral_flatness_results(self, index: int = 1, subblock_index: int = 1, carrier_index: int = 1) -> str:
        """Fetches the combined ModAcc spectral flatness results string."""
        return self.query(f":FETch:NR:RESults{index}:MODacc{subblock_index}:CCARrier{carrier_index}:SFLatness?").strip()

    def fetch_obw(self, index: int = 1, subblock_index: int = 1) -> Dict[str, str]:
        """Fetches Occupied Bandwidth (OBW) results."""
        return {
            "bandwidth": self.query(f":FETch:NR:RESults{index}:OBW:SBLock{subblock_index}:BANDwidth?").strip(),
            "freq_start": self.query(f":FETch:NR:RESults{index}:OBW:SBLock{subblock_index}:FREQuency:STARt?").strip(),
            "freq_stop": self.query(f":FETch:NR:RESults{index}:OBW:SBLock{subblock_index}:FREQuency:STOP?").strip(),
            "power_abs": self.query(f":FETch:NR:RESults{index}:OBW:SBLock{subblock_index}:POWer:ABSolute?").strip(),
        }

    def fetch_obw_results(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches the combined OBW results string."""
        return self.query(f":FETch:NR:RESults{index}:OBW:SBLock{subblock_index}?").strip()

    def fetch_obw_results_all(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches the combined OBW results string (ALL form)."""
        return self.query(f":FETch:NR:RESults{index}:OBW:SBLock{subblock_index}:ALL?").strip()

    def fetch_sem(self, index: int = 1, subblock_index: int = 1) -> Dict[str, str]:
        """Fetches SEM subblock results (total power, status, measurement freq/bandwidth/power)."""
        return {
            "meas_freq": self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:MEAS:FREQuency?").strip(),
            "meas_ibandwidth": self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:MEAS:IBANDwidth?").strip(),
            "meas_power": self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:MEAS:POWer?").strip(),
            "power_total": self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:POWer:TOTal?").strip(),
            "status": self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:STATus?").strip(),
        }

    def fetch_sem_carrier(self, index: int = 1, subblock_index: int = 1, carrier_index: int = 1) -> Dict[str, str]:
        """Fetches SEM component carrier results."""
        return {
            "freq_peak": self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:CCARrier{carrier_index}:FREQuency:PEAK?").strip(),
            "ipower_abs": self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:CCARrier{carrier_index}:IPOWer:ABSolute?").strip(),
            "ipower_rel": self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:CCARrier{carrier_index}:IPOWer:RELative?").strip(),
            "power_peak_abs": self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:CCARrier{carrier_index}:POWer:PEAK:ABS?").strip(),
        }

    def fetch_sem_offset_margin(self, index: int = 1, subblock_index: int = 1, offset_index: int = 1) -> Dict[str, str]:
        """Fetches SEM lower/upper offset margin results at a given offset index."""
        return {
            "lower_freq": self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:OFFSet:MARGin:LOWer{offset_index}:FREQuency?").strip(),
            "lower_margin": self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:OFFSet:MARGin:LOWer{offset_index}:MARGin?").strip(),
            "lower_power_abs": self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:OFFSet:MARGin:LOWer{offset_index}:POWer:ABSolute?").strip(),
            "lower_power_rel": self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:OFFSet:MARGin:LOWer{offset_index}:POWer:RELative?").strip(),
            "lower_status": self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:OFFSet:MARGin:LOWer{offset_index}:STATus?").strip(),
            "upper_freq": self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:OFFSet:MARGin:UPPer{offset_index}:FREQuency?").strip(),
            "upper_margin": self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:OFFSet:MARGin:UPPer{offset_index}:MARGin?").strip(),
            "upper_power_abs": self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:OFFSet:MARGin:UPPer{offset_index}:POWer:ABSolute?").strip(),
            "upper_power_rel": self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:OFFSet:MARGin:UPPer{offset_index}:POWer:RELative?").strip(),
            "upper_status": self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:OFFSet:MARGin:UPPer{offset_index}:STATus?").strip(),
        }

    def fetch_sem_offset_power(self, index: int = 1, subblock_index: int = 1, offset_index: int = 1) -> Dict[str, str]:
        """Fetches SEM lower/upper offset power results at a given offset index."""
        return {
            "lower_freq": self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:OFFSet:POWer:LOWer{offset_index}:FREQuency?").strip(),
            "lower_ipower_abs": self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:OFFSet:POWer:LOWer{offset_index}:IPOWer:ABSolute?").strip(),
            "lower_ipower_rel": self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:OFFSet:POWer:LOWer{offset_index}:IPOWer:RELative?").strip(),
            "lower_power_abs": self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:OFFSet:POWer:LOWer{offset_index}:POWer:ABSolute?").strip(),
            "lower_power_rel": self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:OFFSet:POWer:LOWer{offset_index}:POWer:RELative?").strip(),
            "upper_freq": self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:OFFSet:POWer:UPPer{offset_index}:FREQuency?").strip(),
            "upper_ipower_abs": self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:OFFSet:POWer:UPPer{offset_index}:IPOWer:ABSolute?").strip(),
            "upper_ipower_rel": self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:OFFSet:POWer:UPPer{offset_index}:IPOWer:RELative?").strip(),
            "upper_power_abs": self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:OFFSet:POWer:UPPer{offset_index}:POWer:ABSolute?").strip(),
            "upper_power_rel": self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:OFFSet:POWer:UPPer{offset_index}:POWer:RELative?").strip(),
        }

    def fetch_sem_results_all(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches the combined SEM results string."""
        return self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:ALL?").strip()

    def fetch_sem_meas_results(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches the SEM subblock measurement results string."""
        return self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:MEAS?").strip()

    def fetch_sem_meas_results_all(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches the SEM subblock measurement results string (ALL form)."""
        return self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:MEAS:ALL?").strip()

    def fetch_sem_carrier_results(self, index: int = 1, subblock_index: int = 1, carrier_index: int = 1) -> str:
        """Fetches the SEM carrier measurement results string."""
        return self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:CCARrier{carrier_index}?").strip()

    def fetch_sem_offset_margin_results(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches all lower and upper SEM offset margins."""
        return self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:OFFSet:MARGin?").strip()

    def fetch_sem_offset_margin_lower_results(self, index: int = 1, subblock_index: int = 1, offset_index: int = 1) -> str:
        """Fetches lower offset margin results (margin, freq, abs/rel power)."""
        return self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:OFFSet:MARGin:LOWer{offset_index}?").strip()

    def fetch_sem_offset_margin_upper_results(self, index: int = 1, subblock_index: int = 1, offset_index: int = 1) -> str:
        """Fetches upper offset margin results (margin, freq, abs/rel power)."""
        return self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:OFFSet:MARGin:UPPer{offset_index}?").strip()

    def fetch_sem_offset_power_results(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches all lower and upper SEM offset powers."""
        return self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:OFFSet:POWer?").strip()

    def fetch_sem_offset_power_lower_results(self, index: int = 1, subblock_index: int = 1, offset_index: int = 1) -> str:
        """Fetches lower offset power results (peak freq, peak/integrated powers)."""
        return self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:OFFSet:POWer:LOWer{offset_index}?").strip()

    def fetch_sem_offset_power_upper_results(self, index: int = 1, subblock_index: int = 1, offset_index: int = 1) -> str:
        """Fetches upper offset power results (peak freq, peak/integrated powers)."""
        return self.query(f":FETch:NR:RESults{index}:SEM:SBLock{subblock_index}:OFFSet:POWer:UPPer{offset_index}?").strip()

    def fetch_txp(self, index: int = 1, subblock_index: int = 1) -> Dict[str, str]:
        """Fetches TX Power (TXP) results (average/peak power, subblock count)."""
        return {
            "avg_power_mean": self.query(f":FETch:NR:RESults{index}:TXP:SBLock{subblock_index}:AVG:POWer:MEAN?").strip(),
            "number": self.query(f":FETch:NR:RESults{index}:TXP:SBLock{subblock_index}:NUMber?").strip(),
            "peak_power_max": self.query(f":FETch:NR:RESults{index}:TXP:SBLock{subblock_index}:PEAK:POWer:MAXimum?").strip(),
        }

    def fetch_txp_results_all(self, index: int = 1, subblock_index: int = 1) -> str:
        """Fetches the combined TXP results string."""
        return self.query(f":FETch:NR:RESults{index}:TXP:SBLock{subblock_index}:ALL?").strip()

    #endregion
