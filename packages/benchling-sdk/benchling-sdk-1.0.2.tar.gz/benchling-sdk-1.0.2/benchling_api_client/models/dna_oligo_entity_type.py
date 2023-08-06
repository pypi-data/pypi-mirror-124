from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class DnaOligoEntityType(Enums.KnownString):
    DNA_OLIGO = "dna_oligo"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "DnaOligoEntityType":
        if not isinstance(val, str):
            raise ValueError(f"Value of DnaOligoEntityType must be a string (encountered: {val})")
        newcls = Enum("DnaOligoEntityType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(DnaOligoEntityType, getattr(newcls, "_UNKNOWN"))
