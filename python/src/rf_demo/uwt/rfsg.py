from uwt_visa_instrument import UwtVisaInstrument
from typing import List, Dict, Union, Tuple, Optional

class RfsgClient(UwtVisaInstrument):

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

    def initiate(self) -> None:
        """Starts the generation."""
        self.write(":RFSG:INITiate")

    def abort(self) -> None:
        """Aborts the generation."""
        self.write(":RFSG:ABORt")

    def is_generating(self) -> str:
        """Checks if the generation is ongoing."""
        return self.query(":RFSG:GENerating?").strip()

    def reset(self) -> None:
        """Resets the generator to its default state."""
        self.write(":RFSG:RESet")

    def update_database(self) -> None:
        """Updates the waveform database."""
        self.write(":RFSG:DB:UPDate")

    def validate_database(self) -> str:
        """Checks the data in the waveform database."""
        return self.query(":RFSG:DB:VALidate?").strip()

    #region Configure
    def config_signal(
        self,
        frequency: Optional[float] = None,
        power_level: Optional[float] = None,
        waveform: Optional[str] = None
    ) -> None:
        """Configures the generated RF signal's frequency, power level, and waveform."""
        if frequency is not None:
            self.write(f":CONFigure:RFSG:FREQuency {frequency}")
        if power_level is not None:
            self.write(f":CONFigure:RFSG:POWer {power_level}")
        if waveform is not None:
            self.write(f":CONFigure:RFSG:WAVEform {waveform}")

    def config_repetition(
        self,
        cycles: Optional[int] = None,
        mode: Optional[str] = None
    ) -> None:
        """Configures generation repetition settings."""
        if cycles is not None:
            self.write(f":CONFigure:RFSG:REPetition:CYCLes {cycles}")
        if mode is not None:
            self.write(f":CONFigure:RFSG:REPetition:MODE {mode}")

    def config_script_trigger(
        self,
        digital_edge_slope: Optional[str] = None,
        digital_edge_source: Optional[str] = None,
        digital_level: Optional[str] = None,
        digital_level_source: Optional[str] = None,
        exported_output_terminal: Optional[str] = None,
        trigger_type: Optional[str] = None
    ) -> None:
        """Configures the script trigger source, level/edge behavior, type, and exported output terminal."""
        if digital_edge_slope is not None:
            self.write(f":CONFigure:RFSG:SCRIPt:TRIGger:DIGital:EDGE:SLOPe {digital_edge_slope}")
        if digital_edge_source is not None:
            self.write(f":CONFigure:RFSG:SCRIPt:TRIGger:DIGital:EDGE:SOURce {digital_edge_source}")
        if digital_level is not None:
            self.write(f":CONFigure:RFSG:SCRIPt:TRIGger:DIGital:LEVel {digital_level}")
        if digital_level_source is not None:
            self.write(f":CONFigure:RFSG:SCRIPt:TRIGger:DIGital:LEVel:SOURce {digital_level_source}")
        if exported_output_terminal is not None:
            self.write(f":OUTPut:TRIGger:SCRIPt:OUTPut:TERminal {exported_output_terminal}")
        if trigger_type is not None:
            self.write(f":CONFigure:RFSG:SCRIPt:TRIGger:TYPE {trigger_type}")

    #endregion

    #region Query
    def get_waveforms_folder(self) -> str:
        """Returns the folder the waveforms have been loaded from. Read only."""
        return self.query(":CONFigure:RFSG:WAVEforms:FOLDer?").strip()

    #endregion
