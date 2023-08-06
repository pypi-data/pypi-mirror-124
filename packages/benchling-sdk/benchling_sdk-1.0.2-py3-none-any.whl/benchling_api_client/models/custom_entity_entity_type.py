from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class CustomEntityEntityType(Enums.KnownString):
    CUSTOM_ENTITY = "custom_entity"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "CustomEntityEntityType":
        if not isinstance(val, str):
            raise ValueError(f"Value of CustomEntityEntityType must be a string (encountered: {val})")
        newcls = Enum("CustomEntityEntityType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(CustomEntityEntityType, getattr(newcls, "_UNKNOWN"))
