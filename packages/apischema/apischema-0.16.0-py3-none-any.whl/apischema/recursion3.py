from dataclasses import Field, dataclass, field
from enum import Enum
from itertools import chain
from typing import (
    AbstractSet,
    Any,
    Collection,
    Dict,
    List,
    Mapping,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
)

from apischema.cache import cache
from apischema.conversions import AnyConversion
from apischema.conversions.conversions import DefaultConversion
from apischema.conversions.visitor import (
    Conv,
    ConversionsVisitor,
    Deserialization,
    DeserializationVisitor,
    Serialization,
    SerializationVisitor,
)
from apischema.objects import ObjectField
from apischema.objects.visitor import (
    DeserializationObjectVisitor,
    ObjectVisitor,
    SerializationObjectVisitor,
)
from apischema.types import AnyType
from apischema.utils import Lazy
from apischema.visitor import Result

RecursionKey = Tuple[AnyType, Optional[AnyConversion]]


@dataclass
class Shortcut:
    value: bool

    def __hash__(self):
        return hash(None)

    def __eq__(self, other):
        return other is None or isinstance(other, Shortcut)


@cache
def recursion_cache() -> Dict[RecursionKey, bool]:
    return {}


class RecursiveChecker(ConversionsVisitor[Conv, Any], ObjectVisitor[Any]):
    def __init__(self, default_conversion: DefaultConversion):
        super().__init__(default_conversion)
        self._guard: List[RecursionKey] = []
        self._guard_indices: Dict[RecursionKey, int] = {}
        self._not_recursive: Set[RecursionKey] = set()
        self._recursive: Set[RecursionKey] = set()

    def any(self):
        pass

    def collection(self, cls: Type[Collection], value_type: AnyType):
        return self.visit(value_type)

    def enum(self, cls: Type[Enum]):
        pass

    def literal(self, values: Sequence[Any]):
        pass

    def mapping(self, cls: Type[Mapping], key_type: AnyType, value_type: AnyType):
        self.visit(key_type)
        self.visit(value_type)

    def object(self, tp: AnyType, fields: Sequence[ObjectField]):
        global indent
        print(indent * " " + str(tp))
        indent += 4
        for field in fields:
            self.visit_with_conv(field.type, self._field_conversion(field))
        indent -= 4

    def primitive(self, cls: Type):
        pass

    def tuple(self, types: Sequence[AnyType]):
        for tp in types:
            self.visit(tp)

    def _visited_union(self, results: Sequence):
        pass

    def unsupported(self, tp: AnyType):
        pass

    def visit(self, tp: AnyType):
        recursion_key = (tp, self._conversion)
        if recursion_key in self._not_recursive:
            pass
        elif recursion_key in self._guard_indices:
            self._recursive.update(
                key for key in self._guard[self._guard_indices[recursion_key] :]
            )
        else:
            self._guard_indices[recursion_key] = len(self._guard)
            self._guard.append(recursion_key)
            try:
                super().visit(tp)
            finally:
                self._guard.pop()
                self._guard_indices.pop(recursion_key)
            if recursion_key not in self._recursive:
                self._not_recursive.add(recursion_key)


class DeserializationRecursiveChecker(
    DeserializationVisitor,
    DeserializationObjectVisitor,
    RecursiveChecker[Deserialization],
):
    pass


class SerializationRecursiveChecker(
    SerializationVisitor, SerializationObjectVisitor, RecursiveChecker[Serialization]
):
    pass


@cache
def is_recursive(
    tp: AnyType,
    conversion: Optional[AnyConversion],
    default_conversion: DefaultConversion,
    checker_cls: Type[RecursiveChecker],
    shortcut: Optional[Shortcut],
) -> bool:
    cached = recursion_cache()[tp, conversion]
    if cached is not None:
        return cached
    print(f"=========== {tp} ============")
    checker = checker_cls(default_conversion)
    checker.visit_with_conv(tp, conversion)
    for shortcut, keys in [(False, checker._not_recursive), (True, checker._recursive)]:
        for tp_, conv in keys:
            is_recursive(tp_, conv, default_conversion, checker_cls, Shortcut(shortcut))
    print([tp for tp, _ in checker._recursive])
    return (tp, conversion) in checker._recursive


class RecursiveConversionsVisitor(ConversionsVisitor[Conv, Result]):
    def __init__(self, default_conversion: DefaultConversion):
        super().__init__(default_conversion)
        self._cache: Dict[Tuple[AnyType, Optional[AnyConversion]], Result] = {}
        self._first_visit = True

    def _recursive_result(self, lazy: Lazy[Result]) -> Result:
        raise NotImplementedError

    def visit_not_recursive(self, tp: AnyType) -> Result:
        return super().visit(tp)

    def visit(self, tp: AnyType) -> Result:
        if is_recursive(
            tp,
            self._conversion,
            self.default_conversion,
            DeserializationRecursiveChecker  # type: ignore
            if isinstance(self, DeserializationVisitor)
            else SerializationRecursiveChecker,
            None,
        ):
            cache_key = tp, self._conversion
            if cache_key in self._cache:
                return self._cache[cache_key]
            result = None

            def lazy_result():
                assert result is not None
                return result

            self._cache[cache_key] = self._recursive_result(lazy_result)
            try:
                result = super().visit(tp)
            finally:
                del self._cache[cache_key]
            return result
        elif self._first_visit:
            self._first_visit = False
            return super().visit(tp)
        else:
            return self.visit_not_recursive(tp)
