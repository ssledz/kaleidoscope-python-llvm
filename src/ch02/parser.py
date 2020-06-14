import sys
from typing import Union, Optional

from ch01.lexer import Lexer, Token
from .ast import *

BinOpPrecedence = {
    '<': 10,
    '+': 20,
    '-': 20,
    '*': 40  # highest
}


class Parser:
    def __init__(self, buffer):
        self.__cur_token = None
        self.__lexer = Lexer(buffer)

    @property
    def current_token(self) -> Union[Token, str]:
        return self.__cur_token

    @property
    def current_token_precedence(self) -> int:
        return BinOpPrecedence.get(self.__cur_token, -1)

    def next_token(self) -> Union[Token, str]:
        self.__cur_token = self.__lexer.gettok()
        return self.__cur_token

    @staticmethod
    def log_error(message: str) -> Union[ExprAST, PrototypeAST, None]:
        print(message, file=sys.stderr)
        return None

    def parse_expression(self) -> Optional[ExprAST]:
        """
        expression
            ::= primary binoprhs
        """
        lhs = self.parse_primary()
        if not lhs:
            return None
        return self.parse_bin_op_rhs(0, lhs)

    def parse_bin_op_rhs(self, expr_prec: int, lhs: ExprAST) -> Optional[ExprAST]:
        """
        binoprhs
            ::= ('+' primary)*
        """
        while True:
            tok_prec = self.current_token_precedence
            if tok_prec < expr_prec:
                return lhs
            bin_op = self.current_token
            self.next_token()
            rhs = self.parse_primary()
            if not rhs:
                return None
            next_prec = self.current_token_precedence
            if tok_prec < next_prec:
                rhs = self.parse_bin_op_rhs(tok_prec + 1, rhs)
                if not rhs:
                    return None
            lhs = BinaryExprAST(op=bin_op, lhs=lhs, rhs=rhs)

    def parse_number_expr(self) -> NumberExprAST:
        """
         numberexpr ::= number
        """
        r = NumberExprAST(self.__lexer.num_val)
        self.next_token()
        return r

    def parse_paren_expr(self) -> Optional[ExprAST]:
        """
        parenexpr ::= '(' expression ')'
        """
        self.next_token()  # consume '('
        expr = self.parse_expression()
        if not expr:
            return None
        if self.current_token != ')':
            return self.log_error("expected ')'")
        self.next_token()  # consume ')'
        return expr

    def parse_identifier_expr(self) -> Optional[ExprAST]:
        """
        identifierexpr
            ::= identifier
            ::= identifier '(' expression* ')'
        """
        id_name = self.__lexer.identifier_str
        self.next_token()  # consume identifier
        if self.current_token != '(':  # simple variable ref
            return VariableExprAST(id_name)
        self.next_token()  # consume '('
        args = []
        if self.current_token != ')':
            while True:
                expr = self.parse_expression()
                if expr:
                    args.append(expr)
                else:
                    return None

                if self.current_token == ')':
                    break
                if self.current_token != ',':
                    return self.log_error("Expected ')' or ',' in argument list")
                self.next_token()
        return CallExprAST(callee=id_name, args=args)

    def parse_primary(self):
        """
        primary
            ::= identifierexpr
            ::= numberexpr
            ::= parenexpr
        """
        return {
            Token.tok_identifier: self.parse_identifier_expr,
            Token.tok_number: self.parse_number_expr,
            '(': self.parse_paren_expr
        }.get(self.current_token, lambda: self.log_error("unknown token when expecting an expression"))()

    def parse_prototype(self) -> Optional[PrototypeAST]:
        """
        prototype
            ::= id '(' id* ')'
        """
        if self.current_token != Token.tok_identifier:
            return self.log_error("Expected function name in prototype")
        fn_name = self.__lexer.identifier_str
        self.next_token()
        if self.current_token != '(':
            return self.log_error("Expected '(' in prototype")
        arg_names = []
        while self.next_token() == Token.tok_identifier:
            arg_names.append(self.__lexer.identifier_str)
        if self.current_token != ')':
            return self.log_error("Expected ')' in prototype")
        self.next_token()  # consume ')'
        return PrototypeAST(name=fn_name, args=arg_names)

    def parse_definition(self) -> Optional[FunctionAST]:
        """
        definition ::= 'def' prototype expression
        """
        self.next_token()  # consume def
        proto = self.parse_prototype()
        if not proto:
            return None
        expr = self.parse_expression()

        if expr:
            return FunctionAST(proto=proto, body=expr)

        return None

    def parse_extern(self) -> PrototypeAST:
        """
        external ::= 'extern' prototype
        """
        self.next_token()  # consume extern
        return self.parse_prototype()

    def parse_top_level_expr(self) -> Optional[FunctionAST]:
        expr = self.parse_expression()
        if expr:
            proto = PrototypeAST(name="", args=[])
            return FunctionAST(proto=proto, body=expr)
        return None
