"""A collection of data classes representing the metaschema of the OCSF."""

from dataclasses import dataclass
from typing import Any, TypeVar

IncludeTarget = str | list[str]


class DefinitionPart: ...


class DefinitionData(DefinitionPart): ...


@dataclass
class VersionDefn(DefinitionData):
    version: str | None = None


@dataclass
class EnumMemberDefn(DefinitionPart):
    """An enum member. Enums are dictionaries of str: EnumMemberDefn."""

    caption: str | None = None
    description: str | None = None
    notes: str | None = None


@dataclass
class DeprecationInfoDefn(DefinitionPart):
    """Deprecation information for an object, event, or attribute."""

    message: str | None = None
    since: str | None = None


@dataclass
class TypeDefn(DefinitionPart):
    """A data type definition."""

    caption: str | None = None
    description: str | None = None
    is_array: bool | None = None
    deprecated: DeprecationInfoDefn | None = None
    max_len: int | None = None
    observable: int | None = None
    range: list[int] | None = None
    regex: str | None = None
    type: str | None = None
    type_name: str | None = None
    values: list[Any] | None = None


@dataclass
class DictionaryTypesDefn(DefinitionPart):
    attributes: dict[str, TypeDefn | IncludeTarget] | None = None
    caption: str | None = None
    description: str | None = None


@dataclass
class AttrDefn(DefinitionPart):
    """An attribute definition."""

    caption: str | None = None
    requirement: str | None = None
    type: str | None = None
    description: str | None = None
    is_array: bool | None = None
    deprecated: DeprecationInfoDefn | None = None
    enum: dict[str, EnumMemberDefn] | None = None
    group: str | None = None
    observable: int | None = None
    profile: str | list[str] | None = None
    sibling: str | None = None
    object_type: str | None = None
    object_name: str | None = None


@dataclass
class DictionaryDefn(DefinitionData):
    """A dictionary definition."""

    name: str | None = None
    caption: str | None = None
    description: str | None = None
    attributes: dict[str, AttrDefn | IncludeTarget] | None = None
    types: DictionaryTypesDefn | None = None


@dataclass
class ObjectDefn(DefinitionData):
    """An object definition."""

    caption: str | None = None
    name: str | None = None
    description: str | None = None
    attributes: dict[str, AttrDefn | IncludeTarget] | None = None
    extends: str | None = None
    observable: int | None = None
    profiles: list[str] | None = None
    constraints: dict[str, list[str]] | None = None
    deprecated: DeprecationInfoDefn | None = None
    include_: IncludeTarget | None = None
    src_extension: str | None = None
    key: str | None = None

    def get_key(self) -> str | None:
        """Return the key for the object definition with the extension prefix when appropriate."""
        if self.key is None:
            return self.name
        else:
            return self.key


@dataclass
class EventDefn(DefinitionData):
    """An event definition."""

    caption: str | None = None
    name: str | None = None
    attributes: dict[str, AttrDefn | IncludeTarget] | None = None
    description: str | None = None
    uid: int | None = None
    category: str | None = None
    extends: str | None = None
    profiles: list[str] | None = None
    associations: dict[str, list[str]] | None = None
    constraints: dict[str, list[str]] | None = None
    deprecated: DeprecationInfoDefn | None = None
    include_: IncludeTarget | None = None
    src_extension: str | None = None
    key: str | None = None

    def get_key(self) -> str | None:
        """Return the key for the object definition with the extension prefix when appropriate."""
        if self.key is None:
            return self.name
        else:
            return self.key


@dataclass
class IncludeDefn(DefinitionData):
    """An include definition."""

    caption: str | None = None
    description: str | None = None
    attributes: dict[str, AttrDefn | IncludeTarget] | None = None
    annotations: AttrDefn | None = None


@dataclass
class ProfileDefn(DefinitionData):
    """A profile definition."""

    caption: str | None = None
    name: str | None = None
    meta: str | None = None
    description: str | None = None
    attributes: dict[str, AttrDefn | IncludeTarget] | None = None
    deprecated: DeprecationInfoDefn | None = None
    annotations: AttrDefn | None = None
    src_extension: str | None = None
    key: str | None = None

    def get_key(self) -> str | None:
        """Return the key for the object definition with the extension prefix when appropriate."""
        if self.key is None:
            return self.name
        else:
            return self.key


@dataclass
class ExtensionDefn(DefinitionData):
    """An extension definition."""

    name: str | None = None
    uid: int | None = None
    caption: str | None = None
    version: str | None = None
    description: str | None = None
    deprecated: DeprecationInfoDefn | None = None


@dataclass
class CategoryDefn(DefinitionPart):
    """A category definition."""

    caption: str | None = None
    description: str | None = None
    uid: int | None = None
    type: str | None = None
    classes: dict[str, EventDefn] | None = None


@dataclass
class CategoriesDefn(DefinitionData):
    """A list of categories."""

    attributes: dict[str, CategoryDefn | IncludeTarget] | None = None
    caption: str | None = None
    description: str | None = None
    name: str | None = None


DefinitionT = TypeVar("DefinitionT", bound=DefinitionData, covariant=True)

AnyDefinition = (
    ObjectDefn | EventDefn | ProfileDefn | ExtensionDefn | DictionaryDefn | IncludeDefn | CategoriesDefn | VersionDefn
)

DefnWithName = ObjectDefn | EventDefn | ExtensionDefn | ProfileDefn
"""Definitions with a name property."""

DefnWithAttrs = ObjectDefn | EventDefn | ProfileDefn | DictionaryDefn | IncludeDefn
"""Definitions with attributes of type dict[str, AttrDefn]."""

DefnWithInclude = ObjectDefn | EventDefn
"""Definitions that support include directives at their root."""

DefnWithAnnotations = ProfileDefn | IncludeDefn
"""Definitions that support annotations."""

DefnWithExtn = ObjectDefn | EventDefn | ProfileDefn
"""Definitions that can be introduced to the core schema by an extension.

This is only used for definitions that create new record types in the core schema. `dictionary.json` is exempt.
"""

DefnWithExtends = ObjectDefn | EventDefn
