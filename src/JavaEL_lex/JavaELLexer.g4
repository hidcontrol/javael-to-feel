lexer grammar JavaELLexer;

OpenParen:          '(';
CloseParen:         ')';
OpenBracket:        '[';
CloseBracket:       ']';

And:                'and' | '&&';
Or:                 'or' | '||';
Not:                'not' | '!';

Equality:           Equal | NotEqual;
Relation:           Greater | Less | GreaterEqual | LessEqual;
Logical:            And | Or | Not;

Equal:              '==' | 'eq';
NotEqual:           '!=' | 'ne';
Greater:            'gt' | '>';
Less:               'lt' | '<';
GreaterEqual:       'ge' | '>=';
LessEqual:          'le' | '<=';

Dot:                '.';
Comma:              ',';
Question:           '?';
DoubleDots:         ':';

Plus:               '+';
Minus:              '-';
Mul:                '*';
Div:                '/' | 'div';
Mod:                '%' | 'mod';

Empty:              'empty';

BooleanLiteral:     'true' | 'false';
NullLiteral:        'null';
StringLiteral:      ('"' DoubleStringCharacter* '"'
             |       '\'' SingleStringCharacter* '\'');
IntegerLiteral:     DecimalIntegerLiteral;
WS:                 [ \n\t\r]+ -> skip;
Identifyer : [a-zA-Z_]+DecimalIntegerLiteral*[a-zA-Z_]*;

fragment DecimalIntegerLiteral
    : '0'
    | [1-9] [0-9]*
    ;

fragment DoubleStringCharacter
    : ~["\\\r\n]
    | '\\' EscapeSequence
    | LineContinuation
    ;

fragment SingleStringCharacter
    : ~['\\\r\n]
    | '\\' EscapeSequence
    | LineContinuation
    ;

fragment EscapeSequence
    : CharacterEscapeSequence
    | '0' // no digit ahead! TODO
    | HexEscapeSequence
    | UnicodeEscapeSequence
    | ExtendedUnicodeEscapeSequence
    ;
fragment CharacterEscapeSequence
    : SingleEscapeCharacter
    | NonEscapeCharacter
    ;
fragment HexEscapeSequence
    : 'x' HexDigit HexDigit
    ;
fragment UnicodeEscapeSequence
    : 'u' HexDigit HexDigit HexDigit HexDigit
    | 'u' '{' HexDigit HexDigit+ '}'
    ;
fragment ExtendedUnicodeEscapeSequence
    : 'u' '{' HexDigit+ '}'
    ;
fragment SingleEscapeCharacter
    : ['"\\bfnrtv]
    ;

fragment NonEscapeCharacter
    : ~['"\\bfnrtv0-9xu\r\n]
    ;
fragment EscapeCharacter
    : SingleEscapeCharacter
    | [0-9]
    | [xu]
    ;
fragment LineContinuation
    : '\\' [\r\n\u2028\u2029]
    ;

fragment HexDigit
    : [_0-9a-fA-F]
    ;
