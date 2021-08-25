# Generated from JavaELParser.g4 by ANTLR 4.9
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .JavaELParser import JavaELParser
else:
    from JavaELParser import JavaELParser

# This class defines a complete listener for a parse tree produced by JavaELParser.
class JavaELParserListener(ParseTreeListener):

    # Enter a parse tree produced by JavaELParser#ternary.
    def enterTernary(self, ctx:JavaELParser.TernaryContext):
        pass

    # Exit a parse tree produced by JavaELParser#ternary.
    def exitTernary(self, ctx:JavaELParser.TernaryContext):
        pass


    # Enter a parse tree produced by JavaELParser#expression.
    def enterExpression(self, ctx:JavaELParser.ExpressionContext):
        pass

    # Exit a parse tree produced by JavaELParser#expression.
    def exitExpression(self, ctx:JavaELParser.ExpressionContext):
        pass


    # Enter a parse tree produced by JavaELParser#term.
    def enterTerm(self, ctx:JavaELParser.TermContext):
        pass

    # Exit a parse tree produced by JavaELParser#term.
    def exitTerm(self, ctx:JavaELParser.TermContext):
        pass


    # Enter a parse tree produced by JavaELParser#equality.
    def enterEquality(self, ctx:JavaELParser.EqualityContext):
        pass

    # Exit a parse tree produced by JavaELParser#equality.
    def exitEquality(self, ctx:JavaELParser.EqualityContext):
        pass


    # Enter a parse tree produced by JavaELParser#relation.
    def enterRelation(self, ctx:JavaELParser.RelationContext):
        pass

    # Exit a parse tree produced by JavaELParser#relation.
    def exitRelation(self, ctx:JavaELParser.RelationContext):
        pass


    # Enter a parse tree produced by JavaELParser#algebraic.
    def enterAlgebraic(self, ctx:JavaELParser.AlgebraicContext):
        pass

    # Exit a parse tree produced by JavaELParser#algebraic.
    def exitAlgebraic(self, ctx:JavaELParser.AlgebraicContext):
        pass


    # Enter a parse tree produced by JavaELParser#member.
    def enterMember(self, ctx:JavaELParser.MemberContext):
        pass

    # Exit a parse tree produced by JavaELParser#member.
    def exitMember(self, ctx:JavaELParser.MemberContext):
        pass


    # Enter a parse tree produced by JavaELParser#base.
    def enterBase(self, ctx:JavaELParser.BaseContext):
        pass

    # Exit a parse tree produced by JavaELParser#base.
    def exitBase(self, ctx:JavaELParser.BaseContext):
        pass


    # Enter a parse tree produced by JavaELParser#value.
    def enterValue(self, ctx:JavaELParser.ValueContext):
        pass

    # Exit a parse tree produced by JavaELParser#value.
    def exitValue(self, ctx:JavaELParser.ValueContext):
        pass


    # Enter a parse tree produced by JavaELParser#primitive.
    def enterPrimitive(self, ctx:JavaELParser.PrimitiveContext):
        pass

    # Exit a parse tree produced by JavaELParser#primitive.
    def exitPrimitive(self, ctx:JavaELParser.PrimitiveContext):
        pass



del JavaELParser