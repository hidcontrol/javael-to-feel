# Generated from feel.g4 by ANTLR 4.9
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .feelParser import feelParser
else:
    from feelParser import feelParser

# This class defines a complete listener for a parse tree produced by feelParser.
class feelListener(ParseTreeListener):

    # Enter a parse tree produced by feelParser#compilation_unit.
    def enterCompilation_unit(self, ctx:feelParser.Compilation_unitContext):
        pass

    # Exit a parse tree produced by feelParser#compilation_unit.
    def exitCompilation_unit(self, ctx:feelParser.Compilation_unitContext):
        pass


    # Enter a parse tree produced by feelParser#expressionTextual.
    def enterExpressionTextual(self, ctx:feelParser.ExpressionTextualContext):
        pass

    # Exit a parse tree produced by feelParser#expressionTextual.
    def exitExpressionTextual(self, ctx:feelParser.ExpressionTextualContext):
        pass


    # Enter a parse tree produced by feelParser#textualExpression.
    def enterTextualExpression(self, ctx:feelParser.TextualExpressionContext):
        pass

    # Exit a parse tree produced by feelParser#textualExpression.
    def exitTextualExpression(self, ctx:feelParser.TextualExpressionContext):
        pass


    # Enter a parse tree produced by feelParser#parametersEmpty.
    def enterParametersEmpty(self, ctx:feelParser.ParametersEmptyContext):
        pass

    # Exit a parse tree produced by feelParser#parametersEmpty.
    def exitParametersEmpty(self, ctx:feelParser.ParametersEmptyContext):
        pass


    # Enter a parse tree produced by feelParser#parametersNamed.
    def enterParametersNamed(self, ctx:feelParser.ParametersNamedContext):
        pass

    # Exit a parse tree produced by feelParser#parametersNamed.
    def exitParametersNamed(self, ctx:feelParser.ParametersNamedContext):
        pass


    # Enter a parse tree produced by feelParser#parametersPositional.
    def enterParametersPositional(self, ctx:feelParser.ParametersPositionalContext):
        pass

    # Exit a parse tree produced by feelParser#parametersPositional.
    def exitParametersPositional(self, ctx:feelParser.ParametersPositionalContext):
        pass


    # Enter a parse tree produced by feelParser#namedParameters.
    def enterNamedParameters(self, ctx:feelParser.NamedParametersContext):
        pass

    # Exit a parse tree produced by feelParser#namedParameters.
    def exitNamedParameters(self, ctx:feelParser.NamedParametersContext):
        pass


    # Enter a parse tree produced by feelParser#namedParameter.
    def enterNamedParameter(self, ctx:feelParser.NamedParameterContext):
        pass

    # Exit a parse tree produced by feelParser#namedParameter.
    def exitNamedParameter(self, ctx:feelParser.NamedParameterContext):
        pass


    # Enter a parse tree produced by feelParser#positionalParameters.
    def enterPositionalParameters(self, ctx:feelParser.PositionalParametersContext):
        pass

    # Exit a parse tree produced by feelParser#positionalParameters.
    def exitPositionalParameters(self, ctx:feelParser.PositionalParametersContext):
        pass


    # Enter a parse tree produced by feelParser#forExpression.
    def enterForExpression(self, ctx:feelParser.ForExpressionContext):
        pass

    # Exit a parse tree produced by feelParser#forExpression.
    def exitForExpression(self, ctx:feelParser.ForExpressionContext):
        pass


    # Enter a parse tree produced by feelParser#iterationContexts.
    def enterIterationContexts(self, ctx:feelParser.IterationContextsContext):
        pass

    # Exit a parse tree produced by feelParser#iterationContexts.
    def exitIterationContexts(self, ctx:feelParser.IterationContextsContext):
        pass


    # Enter a parse tree produced by feelParser#iterationContext.
    def enterIterationContext(self, ctx:feelParser.IterationContextContext):
        pass

    # Exit a parse tree produced by feelParser#iterationContext.
    def exitIterationContext(self, ctx:feelParser.IterationContextContext):
        pass


    # Enter a parse tree produced by feelParser#ifExpression.
    def enterIfExpression(self, ctx:feelParser.IfExpressionContext):
        pass

    # Exit a parse tree produced by feelParser#ifExpression.
    def exitIfExpression(self, ctx:feelParser.IfExpressionContext):
        pass


    # Enter a parse tree produced by feelParser#quantExprSome.
    def enterQuantExprSome(self, ctx:feelParser.QuantExprSomeContext):
        pass

    # Exit a parse tree produced by feelParser#quantExprSome.
    def exitQuantExprSome(self, ctx:feelParser.QuantExprSomeContext):
        pass


    # Enter a parse tree produced by feelParser#quantExprEvery.
    def enterQuantExprEvery(self, ctx:feelParser.QuantExprEveryContext):
        pass

    # Exit a parse tree produced by feelParser#quantExprEvery.
    def exitQuantExprEvery(self, ctx:feelParser.QuantExprEveryContext):
        pass


    # Enter a parse tree produced by feelParser#listr_type.
    def enterListr_type(self, ctx:feelParser.Listr_typeContext):
        pass

    # Exit a parse tree produced by feelParser#listr_type.
    def exitListr_type(self, ctx:feelParser.Listr_typeContext):
        pass


    # Enter a parse tree produced by feelParser#contextr_type.
    def enterContextr_type(self, ctx:feelParser.Contextr_typeContext):
        pass

    # Exit a parse tree produced by feelParser#contextr_type.
    def exitContextr_type(self, ctx:feelParser.Contextr_typeContext):
        pass


    # Enter a parse tree produced by feelParser#qnr_type.
    def enterQnr_type(self, ctx:feelParser.Qnr_typeContext):
        pass

    # Exit a parse tree produced by feelParser#qnr_type.
    def exitQnr_type(self, ctx:feelParser.Qnr_typeContext):
        pass


    # Enter a parse tree produced by feelParser#functionr_type.
    def enterFunctionr_type(self, ctx:feelParser.Functionr_typeContext):
        pass

    # Exit a parse tree produced by feelParser#functionr_type.
    def exitFunctionr_type(self, ctx:feelParser.Functionr_typeContext):
        pass


    # Enter a parse tree produced by feelParser#r_list.
    def enterR_list(self, ctx:feelParser.R_listContext):
        pass

    # Exit a parse tree produced by feelParser#r_list.
    def exitR_list(self, ctx:feelParser.R_listContext):
        pass


    # Enter a parse tree produced by feelParser#functionDefinition.
    def enterFunctionDefinition(self, ctx:feelParser.FunctionDefinitionContext):
        pass

    # Exit a parse tree produced by feelParser#functionDefinition.
    def exitFunctionDefinition(self, ctx:feelParser.FunctionDefinitionContext):
        pass


    # Enter a parse tree produced by feelParser#formalParameters.
    def enterFormalParameters(self, ctx:feelParser.FormalParametersContext):
        pass

    # Exit a parse tree produced by feelParser#formalParameters.
    def exitFormalParameters(self, ctx:feelParser.FormalParametersContext):
        pass


    # Enter a parse tree produced by feelParser#formalParameter.
    def enterFormalParameter(self, ctx:feelParser.FormalParameterContext):
        pass

    # Exit a parse tree produced by feelParser#formalParameter.
    def exitFormalParameter(self, ctx:feelParser.FormalParameterContext):
        pass


    # Enter a parse tree produced by feelParser#context.
    def enterContext(self, ctx:feelParser.ContextContext):
        pass

    # Exit a parse tree produced by feelParser#context.
    def exitContext(self, ctx:feelParser.ContextContext):
        pass


    # Enter a parse tree produced by feelParser#contextEntries.
    def enterContextEntries(self, ctx:feelParser.ContextEntriesContext):
        pass

    # Exit a parse tree produced by feelParser#contextEntries.
    def exitContextEntries(self, ctx:feelParser.ContextEntriesContext):
        pass


    # Enter a parse tree produced by feelParser#contextEntry.
    def enterContextEntry(self, ctx:feelParser.ContextEntryContext):
        pass

    # Exit a parse tree produced by feelParser#contextEntry.
    def exitContextEntry(self, ctx:feelParser.ContextEntryContext):
        pass


    # Enter a parse tree produced by feelParser#keyName.
    def enterKeyName(self, ctx:feelParser.KeyNameContext):
        pass

    # Exit a parse tree produced by feelParser#keyName.
    def exitKeyName(self, ctx:feelParser.KeyNameContext):
        pass


    # Enter a parse tree produced by feelParser#keyString.
    def enterKeyString(self, ctx:feelParser.KeyStringContext):
        pass

    # Exit a parse tree produced by feelParser#keyString.
    def exitKeyString(self, ctx:feelParser.KeyStringContext):
        pass


    # Enter a parse tree produced by feelParser#nameDefinition.
    def enterNameDefinition(self, ctx:feelParser.NameDefinitionContext):
        pass

    # Exit a parse tree produced by feelParser#nameDefinition.
    def exitNameDefinition(self, ctx:feelParser.NameDefinitionContext):
        pass


    # Enter a parse tree produced by feelParser#nameDefinitionWithEOF.
    def enterNameDefinitionWithEOF(self, ctx:feelParser.NameDefinitionWithEOFContext):
        pass

    # Exit a parse tree produced by feelParser#nameDefinitionWithEOF.
    def exitNameDefinitionWithEOF(self, ctx:feelParser.NameDefinitionWithEOFContext):
        pass


    # Enter a parse tree produced by feelParser#nameDefinitionTokens.
    def enterNameDefinitionTokens(self, ctx:feelParser.NameDefinitionTokensContext):
        pass

    # Exit a parse tree produced by feelParser#nameDefinitionTokens.
    def exitNameDefinitionTokens(self, ctx:feelParser.NameDefinitionTokensContext):
        pass


    # Enter a parse tree produced by feelParser#iterationNameDefinition.
    def enterIterationNameDefinition(self, ctx:feelParser.IterationNameDefinitionContext):
        pass

    # Exit a parse tree produced by feelParser#iterationNameDefinition.
    def exitIterationNameDefinition(self, ctx:feelParser.IterationNameDefinitionContext):
        pass


    # Enter a parse tree produced by feelParser#iterationNameDefinitionTokens.
    def enterIterationNameDefinitionTokens(self, ctx:feelParser.IterationNameDefinitionTokensContext):
        pass

    # Exit a parse tree produced by feelParser#iterationNameDefinitionTokens.
    def exitIterationNameDefinitionTokens(self, ctx:feelParser.IterationNameDefinitionTokensContext):
        pass


    # Enter a parse tree produced by feelParser#additionalNameSymbol.
    def enterAdditionalNameSymbol(self, ctx:feelParser.AdditionalNameSymbolContext):
        pass

    # Exit a parse tree produced by feelParser#additionalNameSymbol.
    def exitAdditionalNameSymbol(self, ctx:feelParser.AdditionalNameSymbolContext):
        pass


    # Enter a parse tree produced by feelParser#condOr.
    def enterCondOr(self, ctx:feelParser.CondOrContext):
        pass

    # Exit a parse tree produced by feelParser#condOr.
    def exitCondOr(self, ctx:feelParser.CondOrContext):
        pass


    # Enter a parse tree produced by feelParser#condOrAnd.
    def enterCondOrAnd(self, ctx:feelParser.CondOrAndContext):
        pass

    # Exit a parse tree produced by feelParser#condOrAnd.
    def exitCondOrAnd(self, ctx:feelParser.CondOrAndContext):
        pass


    # Enter a parse tree produced by feelParser#condAndComp.
    def enterCondAndComp(self, ctx:feelParser.CondAndCompContext):
        pass

    # Exit a parse tree produced by feelParser#condAndComp.
    def exitCondAndComp(self, ctx:feelParser.CondAndCompContext):
        pass


    # Enter a parse tree produced by feelParser#condAnd.
    def enterCondAnd(self, ctx:feelParser.CondAndContext):
        pass

    # Exit a parse tree produced by feelParser#condAnd.
    def exitCondAnd(self, ctx:feelParser.CondAndContext):
        pass


    # Enter a parse tree produced by feelParser#compExpression.
    def enterCompExpression(self, ctx:feelParser.CompExpressionContext):
        pass

    # Exit a parse tree produced by feelParser#compExpression.
    def exitCompExpression(self, ctx:feelParser.CompExpressionContext):
        pass


    # Enter a parse tree produced by feelParser#compExpressionRel.
    def enterCompExpressionRel(self, ctx:feelParser.CompExpressionRelContext):
        pass

    # Exit a parse tree produced by feelParser#compExpressionRel.
    def exitCompExpressionRel(self, ctx:feelParser.CompExpressionRelContext):
        pass


    # Enter a parse tree produced by feelParser#relExpressionBetween.
    def enterRelExpressionBetween(self, ctx:feelParser.RelExpressionBetweenContext):
        pass

    # Exit a parse tree produced by feelParser#relExpressionBetween.
    def exitRelExpressionBetween(self, ctx:feelParser.RelExpressionBetweenContext):
        pass


    # Enter a parse tree produced by feelParser#relExpressionValue.
    def enterRelExpressionValue(self, ctx:feelParser.RelExpressionValueContext):
        pass

    # Exit a parse tree produced by feelParser#relExpressionValue.
    def exitRelExpressionValue(self, ctx:feelParser.RelExpressionValueContext):
        pass


    # Enter a parse tree produced by feelParser#relExpressionTestList.
    def enterRelExpressionTestList(self, ctx:feelParser.RelExpressionTestListContext):
        pass

    # Exit a parse tree produced by feelParser#relExpressionTestList.
    def exitRelExpressionTestList(self, ctx:feelParser.RelExpressionTestListContext):
        pass


    # Enter a parse tree produced by feelParser#relExpressionAdd.
    def enterRelExpressionAdd(self, ctx:feelParser.RelExpressionAddContext):
        pass

    # Exit a parse tree produced by feelParser#relExpressionAdd.
    def exitRelExpressionAdd(self, ctx:feelParser.RelExpressionAddContext):
        pass


    # Enter a parse tree produced by feelParser#relExpressionInstanceOf.
    def enterRelExpressionInstanceOf(self, ctx:feelParser.RelExpressionInstanceOfContext):
        pass

    # Exit a parse tree produced by feelParser#relExpressionInstanceOf.
    def exitRelExpressionInstanceOf(self, ctx:feelParser.RelExpressionInstanceOfContext):
        pass


    # Enter a parse tree produced by feelParser#expressionList.
    def enterExpressionList(self, ctx:feelParser.ExpressionListContext):
        pass

    # Exit a parse tree produced by feelParser#expressionList.
    def exitExpressionList(self, ctx:feelParser.ExpressionListContext):
        pass


    # Enter a parse tree produced by feelParser#addExpressionMult.
    def enterAddExpressionMult(self, ctx:feelParser.AddExpressionMultContext):
        pass

    # Exit a parse tree produced by feelParser#addExpressionMult.
    def exitAddExpressionMult(self, ctx:feelParser.AddExpressionMultContext):
        pass


    # Enter a parse tree produced by feelParser#addExpression.
    def enterAddExpression(self, ctx:feelParser.AddExpressionContext):
        pass

    # Exit a parse tree produced by feelParser#addExpression.
    def exitAddExpression(self, ctx:feelParser.AddExpressionContext):
        pass


    # Enter a parse tree produced by feelParser#multExpressionPow.
    def enterMultExpressionPow(self, ctx:feelParser.MultExpressionPowContext):
        pass

    # Exit a parse tree produced by feelParser#multExpressionPow.
    def exitMultExpressionPow(self, ctx:feelParser.MultExpressionPowContext):
        pass


    # Enter a parse tree produced by feelParser#multExpression.
    def enterMultExpression(self, ctx:feelParser.MultExpressionContext):
        pass

    # Exit a parse tree produced by feelParser#multExpression.
    def exitMultExpression(self, ctx:feelParser.MultExpressionContext):
        pass


    # Enter a parse tree produced by feelParser#powExpressionUnary.
    def enterPowExpressionUnary(self, ctx:feelParser.PowExpressionUnaryContext):
        pass

    # Exit a parse tree produced by feelParser#powExpressionUnary.
    def exitPowExpressionUnary(self, ctx:feelParser.PowExpressionUnaryContext):
        pass


    # Enter a parse tree produced by feelParser#powExpression.
    def enterPowExpression(self, ctx:feelParser.PowExpressionContext):
        pass

    # Exit a parse tree produced by feelParser#powExpression.
    def exitPowExpression(self, ctx:feelParser.PowExpressionContext):
        pass


    # Enter a parse tree produced by feelParser#r_filterPathExpression.
    def enterR_filterPathExpression(self, ctx:feelParser.R_filterPathExpressionContext):
        pass

    # Exit a parse tree produced by feelParser#r_filterPathExpression.
    def exitR_filterPathExpression(self, ctx:feelParser.R_filterPathExpressionContext):
        pass


    # Enter a parse tree produced by feelParser#signedUnaryExpressionPlus.
    def enterSignedUnaryExpressionPlus(self, ctx:feelParser.SignedUnaryExpressionPlusContext):
        pass

    # Exit a parse tree produced by feelParser#signedUnaryExpressionPlus.
    def exitSignedUnaryExpressionPlus(self, ctx:feelParser.SignedUnaryExpressionPlusContext):
        pass


    # Enter a parse tree produced by feelParser#signedUnaryExpressionMinus.
    def enterSignedUnaryExpressionMinus(self, ctx:feelParser.SignedUnaryExpressionMinusContext):
        pass

    # Exit a parse tree produced by feelParser#signedUnaryExpressionMinus.
    def exitSignedUnaryExpressionMinus(self, ctx:feelParser.SignedUnaryExpressionMinusContext):
        pass


    # Enter a parse tree produced by feelParser#fnInvocation.
    def enterFnInvocation(self, ctx:feelParser.FnInvocationContext):
        pass

    # Exit a parse tree produced by feelParser#fnInvocation.
    def exitFnInvocation(self, ctx:feelParser.FnInvocationContext):
        pass


    # Enter a parse tree produced by feelParser#nonSignedUnaryExpression.
    def enterNonSignedUnaryExpression(self, ctx:feelParser.NonSignedUnaryExpressionContext):
        pass

    # Exit a parse tree produced by feelParser#nonSignedUnaryExpression.
    def exitNonSignedUnaryExpression(self, ctx:feelParser.NonSignedUnaryExpressionContext):
        pass


    # Enter a parse tree produced by feelParser#uenpmPrimary.
    def enterUenpmPrimary(self, ctx:feelParser.UenpmPrimaryContext):
        pass

    # Exit a parse tree produced by feelParser#uenpmPrimary.
    def exitUenpmPrimary(self, ctx:feelParser.UenpmPrimaryContext):
        pass


    # Enter a parse tree produced by feelParser#primaryLiteral.
    def enterPrimaryLiteral(self, ctx:feelParser.PrimaryLiteralContext):
        pass

    # Exit a parse tree produced by feelParser#primaryLiteral.
    def exitPrimaryLiteral(self, ctx:feelParser.PrimaryLiteralContext):
        pass


    # Enter a parse tree produced by feelParser#primaryForExpression.
    def enterPrimaryForExpression(self, ctx:feelParser.PrimaryForExpressionContext):
        pass

    # Exit a parse tree produced by feelParser#primaryForExpression.
    def exitPrimaryForExpression(self, ctx:feelParser.PrimaryForExpressionContext):
        pass


    # Enter a parse tree produced by feelParser#primaryQuantifiedExpression.
    def enterPrimaryQuantifiedExpression(self, ctx:feelParser.PrimaryQuantifiedExpressionContext):
        pass

    # Exit a parse tree produced by feelParser#primaryQuantifiedExpression.
    def exitPrimaryQuantifiedExpression(self, ctx:feelParser.PrimaryQuantifiedExpressionContext):
        pass


    # Enter a parse tree produced by feelParser#primaryIfExpression.
    def enterPrimaryIfExpression(self, ctx:feelParser.PrimaryIfExpressionContext):
        pass

    # Exit a parse tree produced by feelParser#primaryIfExpression.
    def exitPrimaryIfExpression(self, ctx:feelParser.PrimaryIfExpressionContext):
        pass


    # Enter a parse tree produced by feelParser#primaryInterval.
    def enterPrimaryInterval(self, ctx:feelParser.PrimaryIntervalContext):
        pass

    # Exit a parse tree produced by feelParser#primaryInterval.
    def exitPrimaryInterval(self, ctx:feelParser.PrimaryIntervalContext):
        pass


    # Enter a parse tree produced by feelParser#primaryList.
    def enterPrimaryList(self, ctx:feelParser.PrimaryListContext):
        pass

    # Exit a parse tree produced by feelParser#primaryList.
    def exitPrimaryList(self, ctx:feelParser.PrimaryListContext):
        pass


    # Enter a parse tree produced by feelParser#primaryContext.
    def enterPrimaryContext(self, ctx:feelParser.PrimaryContextContext):
        pass

    # Exit a parse tree produced by feelParser#primaryContext.
    def exitPrimaryContext(self, ctx:feelParser.PrimaryContextContext):
        pass


    # Enter a parse tree produced by feelParser#primaryParens.
    def enterPrimaryParens(self, ctx:feelParser.PrimaryParensContext):
        pass

    # Exit a parse tree produced by feelParser#primaryParens.
    def exitPrimaryParens(self, ctx:feelParser.PrimaryParensContext):
        pass


    # Enter a parse tree produced by feelParser#primaryUnaryTest.
    def enterPrimaryUnaryTest(self, ctx:feelParser.PrimaryUnaryTestContext):
        pass

    # Exit a parse tree produced by feelParser#primaryUnaryTest.
    def exitPrimaryUnaryTest(self, ctx:feelParser.PrimaryUnaryTestContext):
        pass


    # Enter a parse tree produced by feelParser#primaryName.
    def enterPrimaryName(self, ctx:feelParser.PrimaryNameContext):
        pass

    # Exit a parse tree produced by feelParser#primaryName.
    def exitPrimaryName(self, ctx:feelParser.PrimaryNameContext):
        pass


    # Enter a parse tree produced by feelParser#numberLiteral.
    def enterNumberLiteral(self, ctx:feelParser.NumberLiteralContext):
        pass

    # Exit a parse tree produced by feelParser#numberLiteral.
    def exitNumberLiteral(self, ctx:feelParser.NumberLiteralContext):
        pass


    # Enter a parse tree produced by feelParser#boolLiteral.
    def enterBoolLiteral(self, ctx:feelParser.BoolLiteralContext):
        pass

    # Exit a parse tree produced by feelParser#boolLiteral.
    def exitBoolLiteral(self, ctx:feelParser.BoolLiteralContext):
        pass


    # Enter a parse tree produced by feelParser#atLiteralLabel.
    def enterAtLiteralLabel(self, ctx:feelParser.AtLiteralLabelContext):
        pass

    # Exit a parse tree produced by feelParser#atLiteralLabel.
    def exitAtLiteralLabel(self, ctx:feelParser.AtLiteralLabelContext):
        pass


    # Enter a parse tree produced by feelParser#stringLiteral.
    def enterStringLiteral(self, ctx:feelParser.StringLiteralContext):
        pass

    # Exit a parse tree produced by feelParser#stringLiteral.
    def exitStringLiteral(self, ctx:feelParser.StringLiteralContext):
        pass


    # Enter a parse tree produced by feelParser#nullLiteral.
    def enterNullLiteral(self, ctx:feelParser.NullLiteralContext):
        pass

    # Exit a parse tree produced by feelParser#nullLiteral.
    def exitNullLiteral(self, ctx:feelParser.NullLiteralContext):
        pass


    # Enter a parse tree produced by feelParser#atLiteral.
    def enterAtLiteral(self, ctx:feelParser.AtLiteralContext):
        pass

    # Exit a parse tree produced by feelParser#atLiteral.
    def exitAtLiteral(self, ctx:feelParser.AtLiteralContext):
        pass


    # Enter a parse tree produced by feelParser#atLiteralValue.
    def enterAtLiteralValue(self, ctx:feelParser.AtLiteralValueContext):
        pass

    # Exit a parse tree produced by feelParser#atLiteralValue.
    def exitAtLiteralValue(self, ctx:feelParser.AtLiteralValueContext):
        pass


    # Enter a parse tree produced by feelParser#positiveUnaryTestIneqInterval.
    def enterPositiveUnaryTestIneqInterval(self, ctx:feelParser.PositiveUnaryTestIneqIntervalContext):
        pass

    # Exit a parse tree produced by feelParser#positiveUnaryTestIneqInterval.
    def exitPositiveUnaryTestIneqInterval(self, ctx:feelParser.PositiveUnaryTestIneqIntervalContext):
        pass


    # Enter a parse tree produced by feelParser#positiveUnaryTestIneq.
    def enterPositiveUnaryTestIneq(self, ctx:feelParser.PositiveUnaryTestIneqContext):
        pass

    # Exit a parse tree produced by feelParser#positiveUnaryTestIneq.
    def exitPositiveUnaryTestIneq(self, ctx:feelParser.PositiveUnaryTestIneqContext):
        pass


    # Enter a parse tree produced by feelParser#positiveUnaryTestInterval.
    def enterPositiveUnaryTestInterval(self, ctx:feelParser.PositiveUnaryTestIntervalContext):
        pass

    # Exit a parse tree produced by feelParser#positiveUnaryTestInterval.
    def exitPositiveUnaryTestInterval(self, ctx:feelParser.PositiveUnaryTestIntervalContext):
        pass


    # Enter a parse tree produced by feelParser#simplePositiveUnaryTests.
    def enterSimplePositiveUnaryTests(self, ctx:feelParser.SimplePositiveUnaryTestsContext):
        pass

    # Exit a parse tree produced by feelParser#simplePositiveUnaryTests.
    def exitSimplePositiveUnaryTests(self, ctx:feelParser.SimplePositiveUnaryTestsContext):
        pass


    # Enter a parse tree produced by feelParser#positiveSimplePositiveUnaryTests.
    def enterPositiveSimplePositiveUnaryTests(self, ctx:feelParser.PositiveSimplePositiveUnaryTestsContext):
        pass

    # Exit a parse tree produced by feelParser#positiveSimplePositiveUnaryTests.
    def exitPositiveSimplePositiveUnaryTests(self, ctx:feelParser.PositiveSimplePositiveUnaryTestsContext):
        pass


    # Enter a parse tree produced by feelParser#negatedSimplePositiveUnaryTests.
    def enterNegatedSimplePositiveUnaryTests(self, ctx:feelParser.NegatedSimplePositiveUnaryTestsContext):
        pass

    # Exit a parse tree produced by feelParser#negatedSimplePositiveUnaryTests.
    def exitNegatedSimplePositiveUnaryTests(self, ctx:feelParser.NegatedSimplePositiveUnaryTestsContext):
        pass


    # Enter a parse tree produced by feelParser#positiveUnaryTestDash.
    def enterPositiveUnaryTestDash(self, ctx:feelParser.PositiveUnaryTestDashContext):
        pass

    # Exit a parse tree produced by feelParser#positiveUnaryTestDash.
    def exitPositiveUnaryTestDash(self, ctx:feelParser.PositiveUnaryTestDashContext):
        pass


    # Enter a parse tree produced by feelParser#positiveUnaryTest.
    def enterPositiveUnaryTest(self, ctx:feelParser.PositiveUnaryTestContext):
        pass

    # Exit a parse tree produced by feelParser#positiveUnaryTest.
    def exitPositiveUnaryTest(self, ctx:feelParser.PositiveUnaryTestContext):
        pass


    # Enter a parse tree produced by feelParser#positiveUnaryTests.
    def enterPositiveUnaryTests(self, ctx:feelParser.PositiveUnaryTestsContext):
        pass

    # Exit a parse tree produced by feelParser#positiveUnaryTests.
    def exitPositiveUnaryTests(self, ctx:feelParser.PositiveUnaryTestsContext):
        pass


    # Enter a parse tree produced by feelParser#unaryTestsRoot.
    def enterUnaryTestsRoot(self, ctx:feelParser.UnaryTestsRootContext):
        pass

    # Exit a parse tree produced by feelParser#unaryTestsRoot.
    def exitUnaryTestsRoot(self, ctx:feelParser.UnaryTestsRootContext):
        pass


    # Enter a parse tree produced by feelParser#unaryTests_negated.
    def enterUnaryTests_negated(self, ctx:feelParser.UnaryTests_negatedContext):
        pass

    # Exit a parse tree produced by feelParser#unaryTests_negated.
    def exitUnaryTests_negated(self, ctx:feelParser.UnaryTests_negatedContext):
        pass


    # Enter a parse tree produced by feelParser#unaryTests_positive.
    def enterUnaryTests_positive(self, ctx:feelParser.UnaryTests_positiveContext):
        pass

    # Exit a parse tree produced by feelParser#unaryTests_positive.
    def exitUnaryTests_positive(self, ctx:feelParser.UnaryTests_positiveContext):
        pass


    # Enter a parse tree produced by feelParser#unaryTests_empty.
    def enterUnaryTests_empty(self, ctx:feelParser.UnaryTests_emptyContext):
        pass

    # Exit a parse tree produced by feelParser#unaryTests_empty.
    def exitUnaryTests_empty(self, ctx:feelParser.UnaryTests_emptyContext):
        pass


    # Enter a parse tree produced by feelParser#endpoint.
    def enterEndpoint(self, ctx:feelParser.EndpointContext):
        pass

    # Exit a parse tree produced by feelParser#endpoint.
    def exitEndpoint(self, ctx:feelParser.EndpointContext):
        pass


    # Enter a parse tree produced by feelParser#interval.
    def enterInterval(self, ctx:feelParser.IntervalContext):
        pass

    # Exit a parse tree produced by feelParser#interval.
    def exitInterval(self, ctx:feelParser.IntervalContext):
        pass


    # Enter a parse tree produced by feelParser#qualifiedName.
    def enterQualifiedName(self, ctx:feelParser.QualifiedNameContext):
        pass

    # Exit a parse tree produced by feelParser#qualifiedName.
    def exitQualifiedName(self, ctx:feelParser.QualifiedNameContext):
        pass


    # Enter a parse tree produced by feelParser#nameRef.
    def enterNameRef(self, ctx:feelParser.NameRefContext):
        pass

    # Exit a parse tree produced by feelParser#nameRef.
    def exitNameRef(self, ctx:feelParser.NameRefContext):
        pass


    # Enter a parse tree produced by feelParser#nameRefOtherToken.
    def enterNameRefOtherToken(self, ctx:feelParser.NameRefOtherTokenContext):
        pass

    # Exit a parse tree produced by feelParser#nameRefOtherToken.
    def exitNameRefOtherToken(self, ctx:feelParser.NameRefOtherTokenContext):
        pass


    # Enter a parse tree produced by feelParser#reusableKeywords.
    def enterReusableKeywords(self, ctx:feelParser.ReusableKeywordsContext):
        pass

    # Exit a parse tree produced by feelParser#reusableKeywords.
    def exitReusableKeywords(self, ctx:feelParser.ReusableKeywordsContext):
        pass



del feelParser