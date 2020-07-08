from abc import ABC, abstractmethod
from typing import List

from dataclasses import dataclass


class ExprAST(ABC):

    @abstractmethod
    def accept(self, visitor: 'AstVisitor'):
        pass


@dataclass
class NumberExprAST(ExprAST):
    val: float

    def accept(self, visitor: 'AstVisitor'):
        visitor.visit_number_expr(self)


@dataclass
class VariableExprAST(ExprAST):
    name: str

    def accept(self, visitor: 'AstVisitor'):
        visitor.visit_variable_expr(self)


@dataclass
class BinaryExprAST(ExprAST):
    op: str
    lhs: ExprAST
    rhs: ExprAST

    def accept(self, visitor: 'AstVisitor'):
        visitor.visit_binary_expr(self)


@dataclass
class CallExprAST(ExprAST):
    callee: str
    args: List[ExprAST]

    def accept(self, visitor: 'AstVisitor'):
        visitor.visit_call_expr(self)


@dataclass
class PrototypeAST:
    name: str
    args: List[str]

    def accept(self, visitor: 'AstVisitor'):
        visitor.visit_prototype(self)


@dataclass
class FunctionAST:
    proto: PrototypeAST
    body: ExprAST

    def accept(self, visitor: 'AstVisitor'):
        visitor.visit_function(self)


class AstVisitor(ABC):

    @abstractmethod
    def visit_number_expr(self, expr: NumberExprAST):
        pass

    @abstractmethod
    def visit_variable_expr(self, expr: VariableExprAST):
        pass

    @abstractmethod
    def visit_binary_expr(self, expr: BinaryExprAST):
        pass

    @abstractmethod
    def visit_call_expr(self, expr: CallExprAST):
        pass

    @abstractmethod
    def visit_prototype(self, expr: PrototypeAST):
        pass

    @abstractmethod
    def visit_function(self, expr: FunctionAST):
        pass
