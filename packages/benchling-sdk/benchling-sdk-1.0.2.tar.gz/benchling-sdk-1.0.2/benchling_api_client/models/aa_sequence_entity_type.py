from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AaSequenceEntityType(Enums.KnownString):
    AA_SEQUENCE = "aa_sequence"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AaSequenceEntityType":
        if not isinstance(val, str):
            raise ValueError(f"Value of AaSequenceEntityType must be a string (encountered: {val})")
        newcls = Enum("AaSequenceEntityType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AaSequenceEntityType, getattr(newcls, "_UNKNOWN"))
