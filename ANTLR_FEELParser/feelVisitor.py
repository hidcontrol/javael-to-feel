# Generated from feel.g4 by ANTLR 4.9
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .feelParser import feelParser
else:
    from feelParser import feelParser

# This class defines a complete generic visitor for a parse tree produced by feelParser.

class feelVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by feelParser#compilation_unit.
    def visitCompilation_unit(self, ctx:feelParser.Compilation_unitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#expressionTextual.
    def visitExpressionTextual(self, ctx:feelParser.ExpressionTextualContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#textualExpression.
    def visitTextualExpression(self, ctx:feelParser.TextualExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#parametersEmpty.
    def visitParametersEmpty(self, ctx:feelParser.ParametersEmptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#parametersNamed.
    def visitParametersNamed(self, ctx:feelParser.ParametersNamedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#parametersPositional.
    def visitParametersPositional(self, ctx:feelParser.ParametersPositionalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#namedParameters.
    def visitNamedParameters(self, ctx:feelParser.NamedParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#namedParameter.
    def visitNamedParameter(self, ctx:feelParser.NamedParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#positionalParameters.
    def visitPositionalParameters(self, ctx:feelParser.PositionalParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#forExpression.
    def visitForExpression(self, ctx:feelParser.ForExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#iterationContexts.
    def visitIterationContexts(self, ctx:feelParser.IterationContextsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#iterationContext.
    def visitIterationContext(self, ctx:feelParser.IterationContextContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#ifExpression.
    def visitIfExpression(self, ctx:feelParser.IfExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#quantExprSome.
    def visitQuantExprSome(self, ctx:feelParser.QuantExprSomeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#quantExprEvery.
    def visitQuantExprEvery(self, ctx:feelParser.QuantExprEveryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#listr_type.
    def visitListr_type(self, ctx:feelParser.Listr_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#contextr_type.
    def visitContextr_type(self, ctx:feelParser.Contextr_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#qnr_type.
    def visitQnr_type(self, ctx:feelParser.Qnr_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#functionr_type.
    def visitFunctionr_type(self, ctx:feelParser.Functionr_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#r_list.
    def visitR_list(self, ctx:feelParser.R_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#functionDefinition.
    def visitFunctionDefinition(self, ctx:feelParser.FunctionDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#formalParameters.
    def visitFormalParameters(self, ctx:feelParser.FormalParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#formalParameter.
    def visitFormalParameter(self, ctx:feelParser.FormalParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#context.
    def visitContext(self, ctx:feelParser.ContextContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#contextEntries.
    def visitContextEntries(self, ctx:feelParser.ContextEntriesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#contextEntry.
    def visitContextEntry(self, ctx:feelParser.ContextEntryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#keyName.
    def visitKeyName(self, ctx:feelParser.KeyNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#keyString.
    def visitKeyString(self, ctx:feelParser.KeyStringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#nameDefinition.
    def visitNameDefinition(self, ctx:feelParser.NameDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#nameDefinitionWithEOF.
    def visitNameDefinitionWithEOF(self, ctx:feelParser.NameDefinitionWithEOFContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#nameDefinitionTokens.
    def visitNameDefinitionTokens(self, ctx:feelParser.NameDefinitionTokensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#iterationNameDefinition.
    def visitIterationNameDefinition(self, ctx:feelParser.IterationNameDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#iterationNameDefinitionTokens.
    def visitIterationNameDefinitionTokens(self, ctx:feelParser.IterationNameDefinitionTokensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#additionalNameSymbol.
    def visitAdditionalNameSymbol(self, ctx:feelParser.AdditionalNameSymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#condOr.
    def visitCondOr(self, ctx:feelParser.CondOrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#condOrAnd.
    def visitCondOrAnd(self, ctx:feelParser.CondOrAndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#condAndComp.
    def visitCondAndComp(self, ctx:feelParser.CondAndCompContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#condAnd.
    def visitCondAnd(self, ctx:feelParser.CondAndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#compExpression.
    def visitCompExpression(self, ctx:feelParser.CompExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#compExpressionRel.
    def visitCompExpressionRel(self, ctx:feelParser.CompExpressionRelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#relExpressionBetween.
    def visitRelExpressionBetween(self, ctx:feelParser.RelExpressionBetweenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#relExpressionValue.
    def visitRelExpressionValue(self, ctx:feelParser.RelExpressionValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#relExpressionTestList.
    def visitRelExpressionTestList(self, ctx:feelParser.RelExpressionTestListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#relExpressionAdd.
    def visitRelExpressionAdd(self, ctx:feelParser.RelExpressionAddContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#relExpressionInstanceOf.
    def visitRelExpressionInstanceOf(self, ctx:feelParser.RelExpressionInstanceOfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#expressionList.
    def visitExpressionList(self, ctx:feelParser.ExpressionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#addExpressionMult.
    def visitAddExpressionMult(self, ctx:feelParser.AddExpressionMultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#addExpression.
    def visitAddExpression(self, ctx:feelParser.AddExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#multExpressionPow.
    def visitMultExpressionPow(self, ctx:feelParser.MultExpressionPowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#multExpression.
    def visitMultExpression(self, ctx:feelParser.MultExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#powExpressionUnary.
    def visitPowExpressionUnary(self, ctx:feelParser.PowExpressionUnaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#powExpression.
    def visitPowExpression(self, ctx:feelParser.PowExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#r_filterPathExpression.
    def visitR_filterPathExpression(self, ctx:feelParser.R_filterPathExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#signedUnaryExpressionPlus.
    def visitSignedUnaryExpressionPlus(self, ctx:feelParser.SignedUnaryExpressionPlusContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#signedUnaryExpressionMinus.
    def visitSignedUnaryExpressionMinus(self, ctx:feelParser.SignedUnaryExpressionMinusContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#fnInvocation.
    def visitFnInvocation(self, ctx:feelParser.FnInvocationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#nonSignedUnaryExpression.
    def visitNonSignedUnaryExpression(self, ctx:feelParser.NonSignedUnaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#uenpmPrimary.
    def visitUenpmPrimary(self, ctx:feelParser.UenpmPrimaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#primaryLiteral.
    def visitPrimaryLiteral(self, ctx:feelParser.PrimaryLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#primaryForExpression.
    def visitPrimaryForExpression(self, ctx:feelParser.PrimaryForExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#primaryQuantifiedExpression.
    def visitPrimaryQuantifiedExpression(self, ctx:feelParser.PrimaryQuantifiedExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#primaryIfExpression.
    def visitPrimaryIfExpression(self, ctx:feelParser.PrimaryIfExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#primaryInterval.
    def visitPrimaryInterval(self, ctx:feelParser.PrimaryIntervalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#primaryList.
    def visitPrimaryList(self, ctx:feelParser.PrimaryListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#primaryContext.
    def visitPrimaryContext(self, ctx:feelParser.PrimaryContextContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#primaryParens.
    def visitPrimaryParens(self, ctx:feelParser.PrimaryParensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#primaryUnaryTest.
    def visitPrimaryUnaryTest(self, ctx:feelParser.PrimaryUnaryTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#primaryName.
    def visitPrimaryName(self, ctx:feelParser.PrimaryNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#numberLiteral.
    def visitNumberLiteral(self, ctx:feelParser.NumberLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#boolLiteral.
    def visitBoolLiteral(self, ctx:feelParser.BoolLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#atLiteralLabel.
    def visitAtLiteralLabel(self, ctx:feelParser.AtLiteralLabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#stringLiteral.
    def visitStringLiteral(self, ctx:feelParser.StringLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#nullLiteral.
    def visitNullLiteral(self, ctx:feelParser.NullLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#atLiteral.
    def visitAtLiteral(self, ctx:feelParser.AtLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#atLiteralValue.
    def visitAtLiteralValue(self, ctx:feelParser.AtLiteralValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#positiveUnaryTestIneqInterval.
    def visitPositiveUnaryTestIneqInterval(self, ctx:feelParser.PositiveUnaryTestIneqIntervalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#positiveUnaryTestIneq.
    def visitPositiveUnaryTestIneq(self, ctx:feelParser.PositiveUnaryTestIneqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#positiveUnaryTestInterval.
    def visitPositiveUnaryTestInterval(self, ctx:feelParser.PositiveUnaryTestIntervalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#simplePositiveUnaryTests.
    def visitSimplePositiveUnaryTests(self, ctx:feelParser.SimplePositiveUnaryTestsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#positiveSimplePositiveUnaryTests.
    def visitPositiveSimplePositiveUnaryTests(self, ctx:feelParser.PositiveSimplePositiveUnaryTestsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#negatedSimplePositiveUnaryTests.
    def visitNegatedSimplePositiveUnaryTests(self, ctx:feelParser.NegatedSimplePositiveUnaryTestsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#positiveUnaryTestDash.
    def visitPositiveUnaryTestDash(self, ctx:feelParser.PositiveUnaryTestDashContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#positiveUnaryTest.
    def visitPositiveUnaryTest(self, ctx:feelParser.PositiveUnaryTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#positiveUnaryTests.
    def visitPositiveUnaryTests(self, ctx:feelParser.PositiveUnaryTestsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#unaryTestsRoot.
    def visitUnaryTestsRoot(self, ctx:feelParser.UnaryTestsRootContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#unaryTests_negated.
    def visitUnaryTests_negated(self, ctx:feelParser.UnaryTests_negatedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#unaryTests_positive.
    def visitUnaryTests_positive(self, ctx:feelParser.UnaryTests_positiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#unaryTests_empty.
    def visitUnaryTests_empty(self, ctx:feelParser.UnaryTests_emptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#endpoint.
    def visitEndpoint(self, ctx:feelParser.EndpointContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#interval.
    def visitInterval(self, ctx:feelParser.IntervalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#qualifiedName.
    def visitQualifiedName(self, ctx:feelParser.QualifiedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#nameRef.
    def visitNameRef(self, ctx:feelParser.NameRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#nameRefOtherToken.
    def visitNameRefOtherToken(self, ctx:feelParser.NameRefOtherTokenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by feelParser#reusableKeywords.
    def visitReusableKeywords(self, ctx:feelParser.ReusableKeywordsContext):
        return self.visitChildren(ctx)



del feelParser