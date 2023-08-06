from dataclasses import dataclass, field
from typing import AbstractSet, Any, Callable, Optional, Tuple, cast

from apischema.fields import FIELDS_SET_ATTR
from apischema.types import AnyType, Undefined
from apischema.utils import Lazy, OptimizedFunc

Method = OptimizedFunc


class IdentityMethod(Method):
    def call(self, arg: Any) -> Any:
        return arg


class ListMethod(Method):
    call = staticmethod(list)


class DictMethod(Method):
    call = staticmethod(dict)


class StrMethod(Method):
    call = staticmethod(str)


class IntMethod(Method):
    call = staticmethod(int)


class BoolMethod(Method):
    call = staticmethod(bool)


class FloatMethod(Method):
    call = staticmethod(float)


@dataclass
class AttrGetter(OptimizedFunc):
    name: str

    def call(self, arg: Any) -> Any:
        return getattr(arg, self.name)


@dataclass
class ItemGetter(OptimizedFunc):
    key: str

    def call(self, arg: Any) -> Any:
        return arg[self.key]


@dataclass
class RecMethod(Method):
    lazy: Lazy[Method]
    method: Optional[Method] = field(init=False)

    def __post_init__(self):
        self.method = None

    def call(self, arg: Any) -> Any:
        if self.method is None:
            self.method = self.lazy()
        return self.method.call(arg)


@dataclass
class AnyMethod(Method):
    factory: Callable[[AnyType], Method]

    def call(self, arg: Any) -> Any:
        return self.factory(arg.__class__).call(arg)


@dataclass
class CollectionMethod(Method):
    elt_method: Method

    def call(self, arg: Any) -> Any:
        return [self.elt_method.call(elt) for elt in arg]


class ValueMethod(Method):
    def call(self, arg: Any) -> Any:
        return arg.value


@dataclass
class EnumMethod(Method):
    any_method: AnyMethod

    def call(self, arg: Any) -> Any:
        return self.any_method.call(arg.value)


@dataclass
class MappingMethod(Method):
    key_method: Method
    value_method: Method

    def call(self, arg: Any) -> Any:
        return {
            self.key_method.call(key): self.value_method.call(value)
            for key, value in arg.items()
        }


@dataclass
class FieldInfo:
    name: str
    alias: Optional[str]
    getter: Optional[Callable[[Any], Any]]
    required: bool
    skip_if: Optional[Callable]
    undefined: bool
    skip_none: bool
    skip_default: bool
    field_default: Any  # https://github.com/cython/cython/issues/4383
    method: Method
    skippable: bool = field(init=False)

    def __post_init__(self):
        self.skippable = (
            self.skip_if or self.undefined or self.skip_none or self.skip_default
        )

    def update_result(self, result: dict, value: Any):
        if not self.skippable or not (
            (self.skip_if is not None and self.skip_if(value))
            or (self.undefined and value is Undefined)
            or (self.skip_none and value is None)
            or (self.skip_default and value == self.field_default)
        ):
            if self.alias is not None:
                result[self.alias] = self.method.call(value)
            else:
                result.update(self.method.call(value))


@dataclass
class SerializedInfo:
    alias: str
    func: Callable[[Any], Any]
    undefined: bool
    skip_none: bool
    method: Method

    def update_result(self, result: dict, value: Any):
        if not (self.undefined and value is Undefined) and not (
            self.skip_none and value is None
        ):
            result[self.alias] = self.method.call(value)


@dataclass
class ObjectMethod(Method):
    fields: Tuple[FieldInfo, ...]
    nb_fields: int = field(init=False)

    def __post_init__(self):
        self.nb_fields = len(self.fields)


@dataclass
class ClassMethod(ObjectMethod):
    exclude_unset: bool

    def call(self, arg: Any) -> Any:
        result: dict = {}
        for i in range(self.nb_fields):
            field: FieldInfo = self.fields[i]
            if not self.exclude_unset or field.name not in getattr(
                arg, FIELDS_SET_ATTR
            ):
                field.update_result(
                    result,
                    getattr(arg, field.name)
                    if field.getter is None
                    else field.getter(arg),
                )


@dataclass
class TypedDictMethod(ObjectMethod):
    additional_properties: bool
    field_names: AbstractSet[str]
    any_method: Method

    def call(self, arg: Any) -> Any:
        result: dict = {}
        for i in range(self.nb_fields):
            field: FieldInfo = self.fields[i]
            if field.required or field.name in arg:
                field.update_result(
                    result,
                    arg[field.name] if field.getter is None else field.getter(arg),
                )
        if self.additional_properties:
            for key, value in arg.items():
                if key not in self.field_names and isinstance(key, str):
                    result[str(key)] = self.any_method.call(value)


@dataclass
class TupleMethod(Method):
    elt_methods: Tuple[Method, ...]

    def call(self, arg: Any) -> Any:
        return [method.call(arg[i]) for i, method in enumerate(self.elt_methods)]


@dataclass
class OptionalMethod(Method):
    value_method: Method

    def call(self, arg: Any) -> Any:
        return self.value_method.call(arg) if arg is not None else None


@dataclass
class UnionAlternative:
    check: Callable[[Any, Any], bool]
    check_arg: Any
    method: Method


@dataclass
class UnionMethod(Method):
    alternatives: Tuple[UnionAlternative, ...]
    fallback: Callable[[Any], Any]

    def call(self, arg: Any) -> Any:
        for alternative in self.alternatives:
            if alternative.check(arg, alternative.check_arg):
                try:
                    return alternative.method.call(arg)
                except Exception:
                    pass
        return self.fallback(arg)


@dataclass
class WrapperMethod(Method):
    wrapped: Callable[[Any], Any]

    def call(self, arg: Any) -> Any:
        return self.wrapped(arg)


@dataclass
class ConversionMethod(Method):
    converter: Callable[[Any], Any]
    method: Method

    def call(self, arg: Any) -> Any:
        return self.method.call(self.converter(arg))
