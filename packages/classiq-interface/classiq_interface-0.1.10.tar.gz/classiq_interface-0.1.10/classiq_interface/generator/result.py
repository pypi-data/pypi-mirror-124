import base64
import enum
import io
from typing import Union, List, Optional

import pydantic
from PIL import Image
from classiq_interface.generator.generation_metadata import GenerationMetadata


class QuantumFormat(str, enum.Enum):
    QASM = "qasm"
    QSHARP = "qs"
    QIR = "ll"
    IONQ = "ionq"
    CIRQ = "cirq"


class GenerationStatus(str, enum.Enum):
    NONE = "none"
    SUCCESS = "success"
    UNSAT = "unsat"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"
    ERROR = "error"


# TODO: Merge all output formats to single field (dictionary?) to avoid clutter
class GeneratedCircuit(pydantic.BaseModel):
    qubit_count: Optional[int]
    depth: Optional[int]
    qasm: Optional[str]
    qsharp: Optional[str]
    qir: Optional[str]
    ionq: Optional[str]
    cirq: Optional[str]
    output_format: List[QuantumFormat]
    image_raw: str
    qviz_html: Optional[str]
    metadata: GenerationMetadata

    def show(self) -> None:
        image = Image.open(io.BytesIO(base64.b64decode(self.image_raw)))
        image.show()

    @property
    def image(self):
        return Image.open(io.BytesIO(base64.b64decode(self.image_raw)))


class GenerationResult(pydantic.BaseModel):
    status: GenerationStatus
    details: Union[GeneratedCircuit, str]
