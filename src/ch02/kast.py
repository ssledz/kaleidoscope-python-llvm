from abc import ABC
from typing import List

from dataclasses import dataclass


class ExprAST(ABC):
    pass


@dataclass
class NumberExprAST(ExprAST):
    val: float


@dataclass
class VariableExprAST(ExprAST):
    name: str


@dataclass
class BinaryExprAST(ExprAST):
    op: str
    lhs: ExprAST
    rhs: ExprAST


@dataclass
class CallExprAST(ExprAST):
    callee: str
    args: List[ExprAST]


@dataclass
class PrototypeAST:
    name: str
    args: List[str]


@dataclass
class FunctionAST:
    proto: PrototypeAST
    body: ExprAST
