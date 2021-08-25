# Generated from JavaELParser.g4 by ANTLR 4.9
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .JavaELParser import JavaELParser
else:
    from JavaELParser import JavaELParser

# This class defines a complete generic visitor for a parse tree produced by JavaELParser.

class JavaELParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by JavaELParser#ternary.
    def visitTernary(self, ctx:JavaELParser.TernaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaELParser#expression.
    def visitExpression(self, ctx:JavaELParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaELParser#term.
    def visitTerm(self, ctx:JavaELParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaELParser#equality.
    def visitEquality(self, ctx:JavaELParser.EqualityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaELParser#relation.
    def visitRelation(self, ctx:JavaELParser.RelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaELParser#algebraic.
    def visitAlgebraic(self, ctx:JavaELParser.AlgebraicContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaELParser#member.
    def visitMember(self, ctx:JavaELParser.MemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaELParser#base.
    def visitBase(self, ctx:JavaELParser.BaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaELParser#value.
    def visitValue(self, ctx:JavaELParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaELParser#primitive.
    def visitPrimitive(self, ctx:JavaELParser.PrimitiveContext):
        return self.visitChildren(ctx)



del JavaELParser