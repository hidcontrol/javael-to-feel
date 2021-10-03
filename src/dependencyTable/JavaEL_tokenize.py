import re
from enum import Enum
from collections import namedtuple
from typing import List

value_re = re.compile(r'^[\d\w.\'-]*(?:\(\'\w*\'\))?')
empty_re = re.compile(r'^empty')
true_re = re.compile(r'^true')
false_re = re.compile(r'^false')


class JavaELTokenType(Enum):
    ROUNDED_SCOPE_OPEN = 1
    ROUNDED_SCOPE_CLOSE = 2
    LVALUE = 3
    RVALUE = 4
    NOT = 5
    AND = 6
    OR = 7
    EMPTY = 8
    EQUAL = 9
    TERNAR_QUEST = 10
    TERNAR_DOTS = 11
    NOT_EQUAL = 12
    SQUARED_SCOPE_OPEN = 13
    SQUARED_SCOPE_CLOSE = 14
    COMMA = 15
    LESS = 16,
    GREATER = 17,
    LESS_EQUAL = 18,
    GREATER_EQUAL = 19,
    PLUS = 20,
    MINUS = 21,
    MUL = 22,
    DIV = 23,
    MOD = 24,
    TRUE = 25,
    FALSE = 26,


class JavaELToken(namedtuple('JavaELToken', ('token_type', 'token_value'))):
    def __eq__(self, other):
        return self.token_type == other.token_type


# reserved symbols and words
EL_ONE_SYMBOL_OPERATORS = [
    JavaELToken(token_type=JavaELTokenType.ROUNDED_SCOPE_OPEN, token_value='('),
    JavaELToken(token_type=JavaELTokenType.ROUNDED_SCOPE_CLOSE, token_value=')'),
    JavaELToken(token_type=JavaELTokenType.SQUARED_SCOPE_OPEN, token_value='['),
    JavaELToken(token_type=JavaELTokenType.SQUARED_SCOPE_CLOSE, token_value=']'),
    JavaELToken(token_type=JavaELTokenType.NOT, token_value='!'),
    JavaELToken(token_type=JavaELTokenType.COMMA, token_value=','),
    JavaELToken(token_type=JavaELTokenType.TERNAR_DOTS, token_value=':'),
    JavaELToken(token_type=JavaELTokenType.TERNAR_QUEST, token_value='?'),
    JavaELToken(token_type=JavaELTokenType.PLUS, token_value='+'),
    JavaELToken(token_type=JavaELTokenType.MINUS, token_value='-'),
    JavaELToken(token_type=JavaELTokenType.DIV, token_value='/'),
    JavaELToken(token_type=JavaELTokenType.MOD, token_value='%'),
    JavaELToken(token_type=JavaELTokenType.MUL, token_value='*'),

]

EL_TWO_SYMBOL_OPERATORS = [
    JavaELToken(token_type=JavaELTokenType.EQUAL, token_value='eq'),
    JavaELToken(token_type=JavaELTokenType.EQUAL, token_value='=='),
    JavaELToken(token_type=JavaELTokenType.NOT_EQUAL, token_value='ne'),
    JavaELToken(token_type=JavaELTokenType.NOT_EQUAL, token_value='!='),
    JavaELToken(token_type=JavaELTokenType.GREATER, token_value='gt'),
    JavaELToken(token_type=JavaELTokenType.GREATER, token_value='>'),
    JavaELToken(token_type=JavaELTokenType.LESS, token_value='lt'),
    JavaELToken(token_type=JavaELTokenType.LESS, token_value='<'),
    JavaELToken(token_type=JavaELTokenType.GREATER_EQUAL, token_value='ge'),
    JavaELToken(token_type=JavaELTokenType.GREATER_EQUAL, token_value='>='),
    JavaELToken(token_type=JavaELTokenType.LESS_EQUAL, token_value='le'),
    JavaELToken(token_type=JavaELTokenType.LESS_EQUAL, token_value='<='),
    JavaELToken(token_type=JavaELTokenType.AND, token_value='&&'),
    JavaELToken(token_type=JavaELTokenType.OR, token_value='||'),
    JavaELToken(token_type=JavaELTokenType.OR, token_value='or'),

]

EL_TREE_SYMBOLS_OPERATORS = [
    JavaELToken(token_type=JavaELTokenType.AND, token_value='and'),
    JavaELToken(token_type=JavaELTokenType.DIV, token_value='div'),
    JavaELToken(token_type=JavaELTokenType.MOD, token_value='mod'),
]


EL_TRUE = JavaELToken(token_type=JavaELTokenType.TRUE, token_value='true')
EL_FALSE = JavaELToken(token_type=JavaELTokenType.FALSE, token_value='false')
EL_EMPTY = JavaELToken(token_type=JavaELTokenType.EMPTY, token_value='empty')


def recognize_token(expression: str, offset: int) -> JavaELToken:
    one_symbol_op = expression[offset]

    if one_symbol_op == ' ':
        return None

    for token in EL_ONE_SYMBOL_OPERATORS:
        if token.token_value == one_symbol_op:
            return token

    two_symbol_op = expression[offset:offset + 2]

    for token in EL_TWO_SYMBOL_OPERATORS:
        if token.token_value == two_symbol_op:
            return token

    tree_symbol_op = expression[offset:offset + 3]

    for token in EL_TREE_SYMBOLS_OPERATORS:
        if token.token_value == tree_symbol_op:
            return token

    true_val = true_re.search(expression[offset])
    if true_val:
        return EL_TRUE

    false_val = false_re.search(expression[offset])
    if false_val:
        return EL_FALSE

    empty_op = empty_re.search(expression[offset])
    if empty_op:
        return EL_EMPTY

    value = value_re.search(expression[offset:])
    if value and value[0]:
        if ('(' in value[0] and ')' in value[0]) or '\'' in value[0]:
            return JavaELToken(token_type=JavaELTokenType.RVALUE, token_value=value[0])
        else:
            return JavaELToken(token_type=JavaELTokenType.LVALUE, token_value=value[0])

    raise ValueError(f'Unexpected token {expression[offset]}')


def tokenize_expression(expression: str) -> List[JavaELToken]:
    """
    Parse JavaEL expression by tokens
    :param expression:
    :return: List[JavaELToken]
    """
    offset = 0
    tokenized = []

    while offset < len(expression):
        token = recognize_token(expression, offset)
        if token:
            offset += len(token.token_value)
            tokenized.append(token)
        else:
            # space found
            offset += 1

    return tokenized
