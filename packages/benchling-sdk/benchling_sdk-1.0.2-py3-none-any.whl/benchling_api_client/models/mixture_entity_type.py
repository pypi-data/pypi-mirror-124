from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class MixtureEntityType(Enums.KnownString):
    MIXTURE = "mixture"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "MixtureEntityType":
        if not isinstance(val, str):
            raise ValueError(f"Value of MixtureEntityType must be a string (encountered: {val})")
        newcls = Enum("MixtureEntityType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(MixtureEntityType, getattr(newcls, "_UNKNOWN"))
