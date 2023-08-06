from dataclasses import dataclass
from typing import Dict


@dataclass
class Concepto:
    Descripcion: str
    Cantidad: float
    ValorUnitario: float
    Importe: float
    Impuestos: Dict[str, float]
