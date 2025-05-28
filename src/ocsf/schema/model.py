"""This module contains the dataclasses that represent the OCSF schema."""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, TypeVar


class OcsfModel: ...


# TODO: is this used?
@dataclass
class OcsfVersion(OcsfModel):
    version: str


@dataclass
class OcsfEnumMember(OcsfModel):
    """An enum member. Enums are dictionaries of str: OcsfEnumMember."""

    caption: str
    description: str | None = None
    notes: str | None = None


@dataclass
class OcsfDeprecationInfo(OcsfModel):
    """Deprecation information for an object, event, or attribute."""

    message: str
    since: str


@dataclass
class OcsfType(OcsfModel):
    """A data type definition."""

    caption: str
    description: str | None = None
    is_array: bool = False
    deprecated: OcsfDeprecationInfo | None = None
    max_len: int | None = None
    observable: int | None = None
    range: list[int] | None = None
    regex: str | None = None
    type: str | None = None
    type_name: str | None = None
    values: list[Any] | None = None


@dataclass
class OcsfAttr(OcsfModel):
    """An attribute definition."""

    caption: str
    type: str
    requirement: str = "optional"
    description: str | None = None
    is_array: bool = False
    deprecated: OcsfDeprecationInfo | None = None
    enum: dict[str, OcsfEnumMember] | None = None
    group: str | None = None
    observable: int | None = None
    profile: str | list[str] | None = None
    sibling: str | None = None
    object_type: str | None = None
    object_name: str | None = None
    type_name: str | None = None

    def is_object(self) -> bool:
        return self.type[-2:] != "_t"

    def is_primitive(self) -> bool:
        return not self.is_object()


@dataclass
class OcsfObject(OcsfModel):
    """An object definition."""

    caption: str
    name: str
    description: str | None = None
    attributes: dict[str, OcsfAttr] = field(default_factory=dict)
    extends: str | None = None
    observable: int | None = None
    profiles: list[str] | None = None
    constraints: dict[str, list[str]] | None = None
    deprecated: OcsfDeprecationInfo | None = None


@dataclass
class OcsfEvent(OcsfModel):
    """An event definition."""

    caption: str
    name: str
    attributes: dict[str, OcsfAttr] = field(default_factory=dict)
    description: str | None = None
    uid: int | None = None
    category: str | None = None
    extends: str | None = None
    profiles: list[str] | None = None
    associations: dict[str, list[str]] | None = None
    constraints: dict[str, list[str]] | None = None
    deprecated: OcsfDeprecationInfo | None = None


@dataclass
class OcsfProfile(OcsfModel):
    """A profile definition."""

    caption: str
    name: str
    meta: str = "profile"
    description: str | None = None
    attributes: dict[str, OcsfAttr] = field(default_factory=dict)
    deprecated: OcsfDeprecationInfo | None = None
    annotations: dict[str, str] | None = None


@dataclass
class OcsfExtension(OcsfModel):
    """An extension definition."""

    name: str
    uid: int
    caption: str
    version: str | None = None
    description: str | None = None
    deprecated: OcsfDeprecationInfo | None = None


@dataclass
class OcsfCategory(OcsfModel):
    """A category definition."""

    name: str
    uid: int
    caption: str
    description: str | None = None
    deprecated: OcsfDeprecationInfo | None = None
    classes: dict[str, OcsfEvent] | None = None


@dataclass
class OcsfSchema(OcsfModel):
    """An OCSF schema as represented in the OCSF server's export endpoint."""

    version: str
    classes: dict[str, OcsfEvent] = field(default_factory=dict)
    objects: dict[str, OcsfObject] = field(default_factory=dict)
    types: dict[str, OcsfType] = field(default_factory=dict)
    base_event: OcsfEvent | None = None
    profiles: dict[str, OcsfProfile] | None = None
    extensions: dict[str, OcsfExtension] | None = None
    categories: dict[str, OcsfCategory] | None = None


# A type variable constrained to OCSF models.
OcsfT = TypeVar("OcsfT", bound=OcsfModel, covariant=True)
WithAttributes = OcsfEvent | OcsfObject | OcsfProfile


class OcsfElementType(StrEnum):
    EVENT = "event"
    OBJECT = "object"
    ENUM_MEMBER = "enum"
    ATTRIBUTE = "attribute"
    TYPE = "type"
