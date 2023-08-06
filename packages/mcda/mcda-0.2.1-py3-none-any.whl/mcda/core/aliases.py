from typing import Callable, List, NamedTuple, TypeVar, Union

T = TypeVar("T")  # Generic type

NumericValue = Union[int, float]
Value = Union[NumericValue, str]
Id = str
Name = str
Active = bool
Real = bool

Matrix = List[List[T]]

Alternative = Id
Criterion = Id
Category = Id

PerformanceTable = Matrix[Value]
NumericPerformanceTable = Matrix[NumericValue]

Function = Callable[[Value], Value]
NumericFunction = Callable[[NumericValue], NumericValue]


class CategoriesInterval(NamedTuple):
    lower_bound: Category
    upper_bound: Category


Assignment = Union[Category, List[Category], CategoriesInterval]

# Threshold = AffineFunction
