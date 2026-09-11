import pyvisa
from typing import Optional

class UwtVisaInstrument:
    def _create_vxi_11_str(self) -> str:
        if not self.ip_addr:
            raise RuntimeError("No ip address set for instrument.")
        if not self.rf_port:
            raise RuntimeError("No rf port set for instrument.")
        return f"TCPIP0::{self.ip_addr}::inst{self.rf_port}::INSTR"

    def __init__(
        self, 
        ip_addr: str,
        rf_port: int,
        timeout: int = 5000,
        visa_backend: str = "@py"
        ):
        self._rm = pyvisa.ResourceManager(visa_backend) if visa_backend else pyvisa.ResourceManager()
        self.ip_addr = ip_addr
        self.rf_port = rf_port
        self.resource_name = self._create_vxi_11_str()
        self.timeout = timeout
        self._inst = None

    def open(self) -> None:
        self._inst = self._rm.open_resource(self.resource_name)
        self._inst.timeout = self.timeout

    def write(self, command: str) -> None:
        if not self._inst:
            raise RuntimeError("Instrument session is not open. Call open() first.")
        self._inst.write(command)

    def read(self) -> str:
        if not self._inst:
            raise RuntimeError("Instrument session is not open. Call open() first.")
        return self._inst.read()

    def query(self, command: str) -> str:
        self.write(command)
        return self.read()

    def disconnect(self) -> None:
        if self._inst:
            self._inst.close()
            self._inst = None