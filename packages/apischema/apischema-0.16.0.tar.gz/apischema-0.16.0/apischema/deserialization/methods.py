import cython
from typing import Any, Callable, Collection, Tuple

from apischema.validation.errors import ValidationError
from apischema.json_schema.types import bad_type
from apischema.schemas.constraints import Check
from apischema.types import NoneType



# def primitive_factory(
#     cls: type, checks: Collection[Tuple[Check, Any, str]]
# ) -> Callable[[Any], Any]:
#     is_float = cls is float
#     is_none = cls is NoneType
#
#     def method(data: object):
#         if data is None if is_none else not isinstance(data, cls):
#             if is_float and isinstance(data, int):
#                 data = float(data)
#             else:
#                 raise bad_type(data, cls)
#         if checks:
#             errors = [err for check, attr, err in checks if check(data, attr)]
#             if errors:
#                 raise ValidationError(errors)
#         return data
#
#     return method

# @cython.cclass
# class primitive_factory:
#     is_float: bool
#     is_none: bool
#     cls: type
#     checks: Collection[Tuple[Check, Any, str]]
#
#     def __init__(self, cls: type, checks: Collection[Tuple[Check, Any, str]]):
#         self.cls = cls
#         self.checks = checks
#         self.is_float = cls is float
#         self.is_none = cls is NoneType
#
#     def __call__(self, data: object):
#         if data is None if self.is_none else not isinstance(data, self.cls):
#             if self.is_float and isinstance(data, int):
#                 data = float(data)
#             else:
#                 raise bad_type(data, self.cls)
#         if self.checks:
#             errors = [err for check, attr, err in self.checks if check(data, attr)]
#             if errors:
#                 raise ValidationError(errors)
#         return data

# @cython.ccall
# def plop(a: cython.int, b: cython.int) -> cython.int:
#     while b > 0:
#         b -= 1
#         a += b
#     return identity(a)

def identity(x):
    return x