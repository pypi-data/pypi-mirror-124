from dataclasses import Field, dataclass, field
from enum import Enum
from itertools import chain
from typing import (
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
class RecursionGuard:
    keys: List[RecursionKey] = field(default_factory=list)
    key_indices: Dict[RecursionKey, int] = field(default_factory=dict)
    recursive: Set[RecursionKey] = field(default_factory=set)

    def __hash__(self):
        return hash(None)

    def __eq__(self, other):
        return isinstance(other, RecursionGuard)


class RecursiveChecker(ConversionsVisitor[Conv, Any], ObjectVisitor[Any]):
    def __init__(self, default_conversion: DefaultConversion, guard: RecursionGuard):
        super().__init__(default_conversion)
        self.guard = guard
        self._first_visit = True

    def any(self):
        pass

    def collection(self, cls: Type[Collection], value_type: AnyType):
        self.visit(value_type)

    def enum(self, cls: Type[Enum]):
        pass

    def literal(self, values: Sequence[Any]):
        pass

    def mapping(self, cls: Type[Mapping], key_type: AnyType, value_type: AnyType):
        self.visit(key_type)
        self.visit(value_type)

    def object(self, tp: AnyType, fields: Sequence[ObjectField]):
        for field in fields:
            self.visit_with_conv(field.type, self._field_conversion(field))

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
        if self._first_visit:
            self._first_visit = False
            return super().visit(tp)
        is_recursive(
            tp, self.__class__, self._conversion, self.default_conversion, self.guard
        )


class DeserializationRecursiveChecker(
    DeserializationVisitor,
    DeserializationObjectVisitor,
    RecursiveChecker[Deserialization],
):
    pass


class SerializationRecursiveChecker(
    SerializationVisitor,
    SerializationObjectVisitor,
    RecursiveChecker[SerializationVisitor],
):
    pass


@cache
def is_recursive(
    tp: AnyType,
    checker: Type[RecursiveChecker],
    conversion: Optional[AnyConversion],
    default_conversions: DefaultConversion,
    guard: RecursionGuard,
) -> bool:
    recursion_key = tp, conversion
    if recursion_key in guard.keys:
        for key in guard.keys[guard.key_indices[recursion_key] :]:
            guard.recursive.add(key)
        return True
    guard.key_indices[recursion_key] = len(guard.keys)
    guard.keys.append(recursion_key)
    checker(default_conversions, guard).visit_with_conv(tp, conversion)
    try:
        return recursion_key in guard.recursive
    finally:
        guard.keys.pop()
        del guard.key_indices[recursion_key]


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
            DeserializationRecursiveChecker  # type: ignore
            if isinstance(self, DeserializationVisitor)
            else SerializationRecursiveChecker,
            self._conversion,
            self.default_conversion,
            RecursionGuard(),
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
