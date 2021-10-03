grammar feel;

/**************************
 *       EXPRESSIONS
 **************************/
compilation_unit
    : expression EOF
    ;

// #1
expression
    : expr=textualExpression  #expressionTextual
    ;

// #2
textualExpression
    : functionDefinition
    | conditionalOrExpression
    ;

// #41
parameters
    : LPAREN RPAREN                       #parametersEmpty
    | LPAREN namedParameters RPAREN       #parametersNamed
    | LPAREN positionalParameters RPAREN  #parametersPositional
    ;

// #42 #43
namedParameters
    : namedParameter (COMMA namedParameter)*
    ;

namedParameter
    : name=nameDefinition COLON value=expression
    ;

// #44
positionalParameters
    : expression ( COMMA expression )*
    ;

// #46
forExpression
    : FOR iterationContexts RETURN  expression
    ;

iterationContexts
    : iterationContext ( COMMA iterationContext )*
    ;

iterationContext
    : iterationNameDefinition IN expression '..' expression
    | iterationNameDefinition IN expression
    ;

// #47
ifExpression
    : IF c=expression THEN t=expression ELSE e=expression
    ;

// #48
quantifiedExpression
    : SOME iterationContexts SATISFIES  expression    #quantExprSome
    | EVERY iterationContexts SATISFIES expression   #quantExprEvery
    ;

// #54
r_type
    : sk=Identifier LT r_type GT                                                     #listr_type
    | sk=Identifier LT Identifier COLON r_type ( COMMA Identifier COLON r_type )* GT   #contextr_type
    | FUNCTION                                                                     #qnr_type
    | FUNCTION LT r_type ( COMMA r_type )* GT RARROW                                   #functionr_type
    | qualifiedName                                                                #qnr_type
    ;

// #56
r_list
    : LBRACK RBRACK
    | LBRACK expressionList RBRACK
    ;

// #57
functionDefinition
    : FUNCTION LPAREN formalParameters? RPAREN external=EXTERNAL? body=expression
    ;

formalParameters
    : formalParameter ( COMMA formalParameter )*
    ;

// #58
formalParameter
    : nameDefinition COLON r_type
    | nameDefinition
    ;

// #59
context
    : LBRACE RBRACE
    | LBRACE contextEntries RBRACE
    ;

contextEntries
    : contextEntry ( COMMA contextEntry )*
    ;

// #60
contextEntry
    : key
      COLON expression
    ;

// #61
key
    : nameDefinition   #keyName
    | StringLiteral    #keyString
    ;

nameDefinition
    : nameDefinitionTokens
    ;

nameDefinitionWithEOF
    : nameDefinition EOF
    ;

nameDefinitionTokens
    : Identifier
        ( Identifier
        | additionalNameSymbol
        | IntegerLiteral
        | FloatingPointLiteral
        | reusableKeywords
        | IN
        )*
    ;

iterationNameDefinition
    : iterationNameDefinitionTokens
    ;

iterationNameDefinitionTokens
    : Identifier
        ( Identifier
        | additionalNameSymbol
        | IntegerLiteral
        | FloatingPointLiteral
        | reusableKeywords
        )*
    ;


additionalNameSymbol
    : //( '.' | '/' | '-' | '\'' | '+' | '*' )
    DOT | DIV | SUB | ADD | MUL | QUOTE
    ;

conditionalOrExpression
	:	conditionalAndExpression                                                 #condOrAnd
 	|	left=conditionalOrExpression op=OR right=conditionalAndExpression    #condOr
	;

conditionalAndExpression
	:	comparisonExpression                                                   #condAndComp
	|	left=conditionalAndExpression op=AND right=comparisonExpression      #condAnd
	;

comparisonExpression
	:	relationalExpression                                                                   #compExpressionRel
	|   left=comparisonExpression op=(LT |
                                      GT |
                                      LE |
                                      GE |
                                      EQUAL |
                                      NOTEQUAL) right=relationalExpression   #compExpression
	;

relationalExpression
	:	additiveExpression                                                                           #relExpressionAdd
	|	val=relationalExpression BETWEEN start=additiveExpression AND end=additiveExpression   #relExpressionBetween
	|   val=relationalExpression IN LPAREN positiveUnaryTests RPAREN                                     #relExpressionTestList
    |   val=relationalExpression IN expression                                                   #relExpressionValue        // includes simpleUnaryTest
    |   val=relationalExpression INSTANCE OF r_type                                            #relExpressionInstanceOf
	;

expressionList
    :   expression  (COMMA expression)*
    ;

additiveExpression
	:	multiplicativeExpression                            #addExpressionMult
	|	additiveExpression op=ADD multiplicativeExpression  #addExpression
	|	additiveExpression op=SUB multiplicativeExpression  #addExpression
	;

multiplicativeExpression
	:	powerExpression                                              #multExpressionPow
	|	multiplicativeExpression op=( MUL | DIV ) powerExpression    #multExpression
	;

powerExpression
    :   r_filterPathExpression                           #powExpressionUnary
    |   powerExpression op=POW r_filterPathExpression   #powExpression
    ;

r_filterPathExpression
    :   unaryExpression
    |   r_filterPathExpression LBRACK r_filter=expression  RBRACK
    |   r_filterPathExpression DOT  qualifiedName
    ;

unaryExpression
	:	unaryExpression parameters               #fnInvocation
    |	SUB unaryExpression                      #signedUnaryExpressionMinus
	|   unaryExpressionNotPlusMinus              #nonSignedUnaryExpression
    |	ADD unaryExpressionNotPlusMinus          #signedUnaryExpressionPlus
  	;

unaryExpressionNotPlusMinus
	: primary (DOT  qualifiedName parameters?  )?   #uenpmPrimary
	;

primary
    : literal                     #primaryLiteral
    | forExpression               #primaryForExpression
    | quantifiedExpression        #primaryQuantifiedExpression
    | ifExpression                #primaryIfExpression
    | interval                    #primaryInterval
    | r_list                        #primaryList
    | context                     #primaryContext
    | LPAREN expression RPAREN          #primaryParens
    | simplePositiveUnaryTest     #primaryUnaryTest
    | qualifiedName    #primaryName
    ;

// #33 - #39
literal
    :	IntegerLiteral          #numberLiteral
    |	FloatingPointLiteral    #numberLiteral
    |	BooleanLiteral          #boolLiteral
    |   atLiteral               #atLiteralLabel
    |	StringLiteral           #stringLiteral
    |	NULL                #nullLiteral
    ;

atLiteral
    : AT atLiteralValue
    ;

atLiteralValue
    : StringLiteral
    ;

BooleanLiteral
    :   TRUE
    |   FALSE
    ;

/**************************
 *    OTHER CONSTRUCTS
 **************************/

// #7
simplePositiveUnaryTest
    : op=LT    endpoint    #positiveUnaryTestIneqInterval
    | op=GT    endpoint    #positiveUnaryTestIneqInterval
    | op=LE   endpoint    #positiveUnaryTestIneqInterval
    | op=GE   endpoint    #positiveUnaryTestIneqInterval
    | op=EQUAL    endpoint    #positiveUnaryTestIneq
    | op=NOTEQUAL   endpoint    #positiveUnaryTestIneq
    | interval           #positiveUnaryTestInterval
    ;


// #13
simplePositiveUnaryTests
    : simplePositiveUnaryTest ( COMMA simplePositiveUnaryTest )*
    ;


// #14
simpleUnaryTests
    : simplePositiveUnaryTests                     #positiveSimplePositiveUnaryTests
    | NOT LPAREN simplePositiveUnaryTests RPAREN     #negatedSimplePositiveUnaryTests
    | SUB                                          #positiveUnaryTestDash
    ;

// #15
positiveUnaryTest
    : expression
    ;

// #16
positiveUnaryTests
    : positiveUnaryTest ( COMMA positiveUnaryTest )*
    ;


unaryTestsRoot
    : unaryTests EOF
    ;

// #17 (root for decision tables)
unaryTests
    :
    NOT LPAREN positiveUnaryTests RPAREN #unaryTests_negated
    | positiveUnaryTests               #unaryTests_positive
    | SUB                              #unaryTests_empty
    ;

// #18
endpoint
    : additiveExpression
    ;

// #8-#12
interval
    : low=LPAREN start=endpoint ELIPSIS end=endpoint up=RPAREN
    | low=LPAREN start=endpoint ELIPSIS end=endpoint up=LBRACK
    | low=LPAREN start=endpoint ELIPSIS end=endpoint up=RBRACK
    | low=RBRACK start=endpoint ELIPSIS end=endpoint up=RPAREN
    | low=RBRACK start=endpoint ELIPSIS end=endpoint up=LBRACK
    | low=RBRACK start=endpoint ELIPSIS end=endpoint up=RBRACK
    | low=LBRACK start=endpoint ELIPSIS end=endpoint up=RPAREN
    | low=LBRACK start=endpoint ELIPSIS end=endpoint up=LBRACK
    | low=LBRACK start=endpoint ELIPSIS end=endpoint up=RBRACK
    ;

// #20
qualifiedName
    : n1=nameRef
        ( DOT

            n2=nameRef

        )*
    ;

nameRef
    : ( st=Identifier
       | not_st=NOT
       )  nameRefOtherToken*
    ;

nameRefOtherToken
    :
        ~(LPAREN|RPAREN|LBRACK|RBRACK|LBRACE|RBRACE|LT|GT|EQUAL|BANG|COMMA)
    ;

/********************************
 *      KEYWORDS
 ********************************/
reusableKeywords
    : FOR
    | RETURN
    | IF
    | THEN
    | ELSE
    | SOME
    | EVERY
    | SATISFIES
    | INSTANCE
    | OF
    | FUNCTION
    | EXTERNAL
    | OR
    | AND
    | BETWEEN
    | NOT
    | NULL
    | TRUE
    | FALSE
    ;

FOR
    : 'for'
    ;

RETURN
    : 'return'
    ;

// can't be reused
IN
    : 'in'
    ;

IF
    : 'if'
    ;

THEN
    : 'then'
    ;

ELSE
    : 'else'
    ;

SOME
    : 'some'
    ;

EVERY
    : 'every'
    ;

SATISFIES
    : 'satisfies'
    ;

INSTANCE
    : 'instance'
    ;

OF
    : 'of'
    ;

FUNCTION
    : 'function'
    ;

EXTERNAL
    : 'external'
    ;

OR
    : 'or'
    ;

AND
    : 'and'
    ;

BETWEEN
    : 'between'
    ;

NULL
    : 'null'
    ;

TRUE
    : 'true'
    ;

FALSE
    : 'false'
    ;

QUOTE
    :
    '\''
    ;

/********************************
 *      LEXER RULES
 *
 * Include:
 *      - number literals
 *      - boolean literals
 *      - string literals
 *      - null literal
 ********************************/

// Number Literals

// #37
IntegerLiteral
	:	DecimalIntegerLiteral
	|	HexIntegerLiteral
	;

fragment
DecimalIntegerLiteral
	:	DecimalNumeral Integerr_typeSuffix?
	;

fragment
HexIntegerLiteral
	:	HexNumeral Integerr_typeSuffix?
	;

fragment
Integerr_typeSuffix
	:	[lL]
	;

fragment
DecimalNumeral
	:	Digit (Digits? | Underscores Digits)
	;

fragment
Digits
	:	Digit (DigitsAndUnderscores? Digit)?
	;

fragment
Digit
	:	[0-9]
	;

fragment
NonZeroDigit
	:	[1-9]
	;

fragment
DigitsAndUnderscores
	:	DigitOrUnderscore+
	;

fragment
DigitOrUnderscore
	:	Digit
	|	'_'
	;

fragment
Underscores
	:	'_'+
	;

fragment
HexNumeral
	:	'0' [xX] HexDigits
	;

fragment
HexDigits
	:	HexDigit (HexDigitsAndUnderscores? HexDigit)?
	;

fragment
HexDigit
	:	[0-9a-fA-F]
	;

fragment
HexDigitsAndUnderscores
	:	HexDigitOrUnderscore+
	;

fragment
HexDigitOrUnderscore
	:	HexDigit
	|	'_'
	;

// #37
FloatingPointLiteral
	:	DecimalFloatingPointLiteral
	|	HexadecimalFloatingPointLiteral
	;

fragment
DecimalFloatingPointLiteral
	:	Digits '.' Digits ExponentPart? Floatr_typeSuffix?
	|	'.' Digits ExponentPart? Floatr_typeSuffix?
	|	Digits ExponentPart Floatr_typeSuffix?
	|	Digits Floatr_typeSuffix
	;

fragment
ExponentPart
	:	ExponentIndicator SignedInteger
	;

fragment
ExponentIndicator
	:	[eE]
	;

fragment
SignedInteger
	:	Sign? Digits
	;

fragment
Sign
	:	[+-]
	;

fragment
Floatr_typeSuffix
	:	[fFdD]
	;

fragment
HexadecimalFloatingPointLiteral
	:	HexSignificand BinaryExponent Floatr_typeSuffix?
	;

fragment
HexSignificand
	:	HexNumeral '.'?
	|	'0' [xX] HexDigits? '.' HexDigits
	;

fragment
BinaryExponent
	:	BinaryExponentIndicator SignedInteger
	;

fragment
BinaryExponentIndicator
	:	[pP]
	;

// String Literals

StringLiteral
	:	'"' StringCharacters? '"'
	;

fragment
StringCharacters
	:	StringCharacter+
	;

fragment
StringCharacter
	:	~["\\]
	|	EscapeSequence
	;
// Escape Sequences for Character and String Literals
fragment
EscapeSequence
	:	'\\' ~[u]     // required to support FEEL regexps
    |   UnicodeEscape // This is not in the spec but prevents having to preprocess the input
	;
fragment
ZeroToThree
	:	[0-3]
	;
// This is not in the spec but prevents having to preprocess the input
fragment
UnicodeEscape
    :   '\\' 'U' HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit
    |   '\\' 'u' HexDigit HexDigit HexDigit HexDigit
    ;
// The Null Literal
// Separators
LPAREN : '(';
RPAREN : ')';
LBRACE : '{';
RBRACE : '}';
LBRACK : '[';
RBRACK : ']';
COMMA : ',';
ELIPSIS : '..';
DOT : '.';
// Operators
EQUAL : '=';
GT : '>';
LT : '<';
LE : '<=';
GE : '>=';
NOTEQUAL : '!=';
COLON : ':';
RARROW : '->';
POW : '**';
ADD : '+';
SUB : '-';
MUL : '*';
DIV : '/';
BANG
    : '!'
    ;
NOT
    : 'not'
    ;
AT  : '@';
Identifier
    : NameStartChar NameStartCharOrPart*
    ;
fragment
NameStartChar
    : '?' | [A-Z] | '_' | [a-z] | [\u00C0-\u00D6] | [\u00D8-\u00F6] | [\u00F8-\u02FF] | [\u0370-\u037D] | [\u037F-\u1FFF] |
    [\u200C-\u200D] | [\u2070-\u218F] | [\u2C00-\u2FEF] | [\u3001-\uD7FF] | [\uF900-\uFDCF] | [\uFDF0-\uFFFD] |
    [\u{10000}-\u{EFFFF}];
fragment
NameStartCharOrPart
    : '?' | [A-Z] | '_' | [a-z] | [\u00C0-\u00D6] | [\u00D8-\u00F6] | [\u00F8-\u02FF] | [\u0370-\u037D] | [\u037F-\u1FFF] |
    [\u200C-\u200D] | [\u2070-\u218F] | [\u2C00-\u2FEF] | [\u3001-\uD7FF] | [\uF900-\uFDCF] | [\uFDF0-\uFFFD] |
    [\u{10000}-\u{EFFFF}]
    | [0-9] | '\u00B7' | [\u0300-\u036F] | [\u203F-\u2040]
	;
//
// Whitespace and comments
//
WS  :  [ \t\r\n\u000C\u00A0]+ -> skip
    ;
COMMENT
    :   '/*' .*? '*/' -> skip
    ;
LINE_COMMENT
    :   '//' ~[\r\n]* -> skip
    ;
ANY_OTHER_CHAR
    : ~[ \t\r\n\u000c]
    ;