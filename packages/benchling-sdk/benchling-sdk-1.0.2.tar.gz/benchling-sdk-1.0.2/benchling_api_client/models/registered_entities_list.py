from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.aa_sequence import AaSequence
from ..models.custom_entity import CustomEntity
from ..models.dna_oligo import DnaOligo
from ..models.dna_sequence import DnaSequence
from ..models.mixture import Mixture
from ..models.rna_oligo import RnaOligo
from ..types import UNSET, Unset

T = TypeVar("T", bound="RegisteredEntitiesList")


@attr.s(auto_attribs=True, repr=False)
class RegisteredEntitiesList:
    """  """

    _entities: Union[
        Unset, List[Union[DnaSequence, CustomEntity, AaSequence, Mixture, DnaOligo, RnaOligo, UnknownType]]
    ] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("entities={}".format(repr(self._entities)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "RegisteredEntitiesList({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        entities: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._entities, Unset):
            entities = []
            for entities_item_data in self._entities:
                if isinstance(entities_item_data, UnknownType):
                    entities_item = entities_item_data.value
                elif isinstance(entities_item_data, DnaSequence):
                    entities_item = entities_item_data.to_dict()

                elif isinstance(entities_item_data, CustomEntity):
                    entities_item = entities_item_data.to_dict()

                elif isinstance(entities_item_data, AaSequence):
                    entities_item = entities_item_data.to_dict()

                elif isinstance(entities_item_data, Mixture):
                    entities_item = entities_item_data.to_dict()

                elif isinstance(entities_item_data, DnaOligo):
                    entities_item = entities_item_data.to_dict()

                else:
                    entities_item = entities_item_data.to_dict()

                entities.append(entities_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if entities is not UNSET:
            field_dict["entities"] = entities

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entities = []
        _entities = d.pop("entities", UNSET)
        for entities_item_data in _entities or []:

            def _parse_entities_item(
                data: Union[Dict[str, Any]]
            ) -> Union[DnaSequence, CustomEntity, AaSequence, Mixture, DnaOligo, RnaOligo, UnknownType]:
                entities_item: Union[
                    DnaSequence, CustomEntity, AaSequence, Mixture, DnaOligo, RnaOligo, UnknownType
                ]
                discriminator_value: str = cast(str, data.get("entityType"))
                if discriminator_value is not None:
                    if discriminator_value == "dna_sequence":
                        entities_item = DnaSequence.from_dict(data)

                        return entities_item
                    if discriminator_value == "custom_entity":
                        entities_item = CustomEntity.from_dict(data)

                        return entities_item
                    if discriminator_value == "aa_sequence":
                        entities_item = AaSequence.from_dict(data)

                        return entities_item
                    if discriminator_value == "mixture":
                        entities_item = Mixture.from_dict(data)

                        return entities_item
                    if discriminator_value == "dna_oligo":
                        entities_item = DnaOligo.from_dict(data)

                        return entities_item
                    if discriminator_value == "rna_oligo":
                        entities_item = RnaOligo.from_dict(data)

                        return entities_item

                    return UnknownType(value=data)
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    entities_item = DnaSequence.from_dict(data)

                    return entities_item
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    entities_item = CustomEntity.from_dict(data)

                    return entities_item
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    entities_item = AaSequence.from_dict(data)

                    return entities_item
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    entities_item = Mixture.from_dict(data)

                    return entities_item
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    entities_item = DnaOligo.from_dict(data)

                    return entities_item
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    entities_item = RnaOligo.from_dict(data)

                    return entities_item
                except:  # noqa: E722
                    pass
                return UnknownType(data)

            entities_item = _parse_entities_item(entities_item_data)

            entities.append(entities_item)

        registered_entities_list = cls(
            entities=entities,
        )

        registered_entities_list.additional_properties = d
        return registered_entities_list

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def entities(
        self,
    ) -> List[Union[DnaSequence, CustomEntity, AaSequence, Mixture, DnaOligo, RnaOligo, UnknownType]]:
        if isinstance(self._entities, Unset):
            raise NotPresentError(self, "entities")
        return self._entities

    @entities.setter
    def entities(
        self,
        value: List[Union[DnaSequence, CustomEntity, AaSequence, Mixture, DnaOligo, RnaOligo, UnknownType]],
    ) -> None:
        self._entities = value

    @entities.deleter
    def entities(self) -> None:
        self._entities = UNSET
