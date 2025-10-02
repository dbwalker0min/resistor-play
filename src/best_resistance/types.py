from __future__ import annotations

from dataclasses import dataclass
from typing import overload
from numbers import Real

@dataclass
class Resistor:
    sym: str
    value: float

    # --- Overloads for a / b ---
    @overload
    def __truediv__(self, other: Resistor) -> float: ...
    @overload
    def __truediv__(self, other: Real) -> float: ...

    def __truediv__(self, other: Real | Resistor) -> float:
        if isinstance(other, Resistor):
            denom = other.value
        elif isinstance(other, Real):
            denom = float(other)
        else:
            return NotImplemented  # lets other's __rtruediv__ run
        if denom == 0:
            raise ZeroDivisionError("division by zero")
        return self.value / denom

    # --- Overloads for x / a ---
    @overload
    def __rtruediv__(self, other: Real) -> float: ...
    @overload
    def __rtruediv__(self, other: Resistor) -> float: ...

    def __rtruediv__(self, other: Real | Resistor) -> float:
        if isinstance(other, Resistor):
            num = other.value
        elif isinstance(other, Real):
            num = float(other)
        else:
            return NotImplemented
        if self.value == 0:
            raise ZeroDivisionError("division by zero")
        return num / self.value
