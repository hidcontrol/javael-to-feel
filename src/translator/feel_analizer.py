from antlr4 import *
from ANTLR_FEELParser.feelParser import feelParser
from ANTLR_FEELParser.feelLexer import feelLexer
from ANTLR_FEELParser.feelVisitor import feelVisitor


def tree(expression: str) -> ParserRuleContext:
    """
    Create AST from expression and return root node
    :param expression:
    :return:
    """
    input_stream = InputStream(expression)
    lexer = feelLexer(input_stream)
    tree_returned = feelParser(CommonTokenStream(lexer))
    return tree_returned.compilation_unit()


class FEELInputExtractor(feelVisitor):
    def __init__(self):
        super(FEELInputExtractor, self).__init__()
        self.identifiers = set()

    @property
    def result(self):
        return self.identifiers

    def visitTerminal(self, node):
        if node.symbol.type == feelLexer.Identifier and isinstance(node.parentCtx, feelParser.NameRefContext):
            self.identifiers.add(node.getText())


class FEELRuleExtractor(feelVisitor):
    def __init__(self):
        super(FEELRuleExtractor, self).__init__()
        self.rule = []

    @property
    def result(self) -> str:
        return ' '.join(self.rule)

    def visitCompExpression(self, ctx:feelParser.CompExpressionRelContext):
        self.rule.extend(
            (
                ctx.getChild(1).getText(),
                ctx.getChild(2).getText()
            )
        )

    def visitFnInvocation(self, ctx:feelParser.FnInvocationContext):
        self.rule.append(
            ctx.getText()
        )
