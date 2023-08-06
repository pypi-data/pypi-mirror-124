from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class RnaOligoEntityType(Enums.KnownString):
    RNA_OLIGO = "rna_oligo"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "RnaOligoEntityType":
        if not isinstance(val, str):
            raise ValueError(f"Value of RnaOligoEntityType must be a string (encountered: {val})")
        newcls = Enum("RnaOligoEntityType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(RnaOligoEntityType, getattr(newcls, "_UNKNOWN"))
