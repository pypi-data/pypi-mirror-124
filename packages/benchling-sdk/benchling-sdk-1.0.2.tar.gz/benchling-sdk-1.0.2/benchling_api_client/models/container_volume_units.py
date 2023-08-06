from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class ContainerVolumeUnits(Enums.KnownString):
    PL = "pL"
    NL = "nL"
    UL = "uL"
    ML = "mL"
    L = "L"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "ContainerVolumeUnits":
        if not isinstance(val, str):
            raise ValueError(f"Value of ContainerVolumeUnits must be a string (encountered: {val})")
        newcls = Enum("ContainerVolumeUnits", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(ContainerVolumeUnits, getattr(newcls, "_UNKNOWN"))
