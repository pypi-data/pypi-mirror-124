from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class DnaSequenceEntityType(Enums.KnownString):
    DNA_SEQUENCE = "dna_sequence"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "DnaSequenceEntityType":
        if not isinstance(val, str):
            raise ValueError(f"Value of DnaSequenceEntityType must be a string (encountered: {val})")
        newcls = Enum("DnaSequenceEntityType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(DnaSequenceEntityType, getattr(newcls, "_UNKNOWN"))
