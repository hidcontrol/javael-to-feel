parser grammar JavaELParser;

options {
    tokenVocab=JavaELLexer;
}

ternary
    : (expression Question ternary DoubleDots ternary)
    | expression
    ;

expression
    : term (Or term)*
    ;

term
    : equality (And equality)*
    ;

equality
    : relation (Equality relation)?
    ;

relation
    : algebraic (Relation algebraic)? |
    OpenParen ternary CloseParen
    ;

algebraic
    : member ((Plus | Minus) member)*
    ;

member
    : base ((Mul | Div | Mod) base)*
    ;

base
    : (Empty | Not | Minus)+ ternary |
      value
    ;

value
    : primitive ((Dot primitive) | (OpenBracket primitive CloseBracket))*
    ;

primitive
    : StringLiteral | BooleanLiteral | NullLiteral| IntegerLiteral | primitive OpenParen (value) CloseParen | primitive OpenParen CloseParen | Identifyer
    ;