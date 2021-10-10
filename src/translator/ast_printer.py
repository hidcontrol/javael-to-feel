from ANTLR_FEELParser.feelVisitor import feelVisitor
from ANTLR_JavaELParser.JavaELParser import JavaELParser
from ANTLR_JavaELParser.JavaELParserVisitor import JavaELParserVisitor
from loguru import logger

logger = logger.opt(colors=True)
logger.disable(__name__)

keywords = [
    JavaELParser.Not,
    JavaELParser.Empty,
    JavaELParser.Or,
    JavaELParser.And,
    JavaELParser.Minus,
    JavaELParser.Plus,
    JavaELParser.LessEqual,
    JavaELParser.Less,
    JavaELParser.Greater,
    JavaELParser.GreaterEqual,
    JavaELParser.Equality,
    JavaELParser.Mul,
    JavaELParser.Div,
    JavaELParser.DoubleDots,
    JavaELParser.Question,
    JavaELParser.OpenParen,
    JavaELParser.OpenBracket,
    JavaELParser.CloseParen,
    JavaELParser.CloseBracket
]


class JavaELTreePrinter(JavaELParserVisitor):
    def __init__(self):
        super(FEELTreePrinter, self).__init__()
        self.result = []

    def lastContextWasDMN(self):
        return len(self.result) > 0 and 'dmn_' in self.result[-1]

    def passIfNoDMN(self, ctx):
        if hasattr(ctx, 'colors') and len(ctx.colors):
            self.result.append(ctx.colors[-1])
        else:
            return self.visitChildren(ctx)

    def visitTerminal(self, node):
        logger.opt(colors=True).debug(f'terminal: <red>{id(node)}</red> <green>{node.getText()}</green> dmn: {hasattr(node, "colors")}')

        if node.symbol.type in keywords:
            self.result.append(' ')
            self.result.append(node.getText())
            self.result.append(' ')
        else:
            self.result.append(node.getText())

    def visitPrimitive(self, ctx:JavaELParser.PrimitiveContext):
        logger.opt(colors=True).debug(f'primitive: <red>{id(ctx)}</red> <green>{ctx.getText()}</green> dmn: {hasattr(ctx, "colors")}')
        if not self.lastContextWasDMN():
            return self.passIfNoDMN(ctx)

    def visitValue(self, ctx:JavaELParser.ValueContext):
        logger.opt(colors=True).debug(f'value: <red>{id(ctx)}</red> <green>{ctx.getText()}</green> dmn: {hasattr(ctx, "colors")}')
        if not self.lastContextWasDMN():
            return self.passIfNoDMN(ctx)

    def visitBase(self, ctx:JavaELParser.BaseContext):
        logger.opt(colors=True).debug(f'base: <red>{id(ctx)}</red> <green>{ctx.getText()}</green> dmn: {hasattr(ctx, "colors")}')
        if not self.lastContextWasDMN():
            return self.passIfNoDMN(ctx)

    def visitMember(self, ctx:JavaELParser.MemberContext):
        logger.opt(colors=True).debug(f'member: <red>{id(ctx)}</red> <green>{ctx.getText()}</green> dmn: {hasattr(ctx, "colors")}')
        if not self.lastContextWasDMN():
            return self.passIfNoDMN(ctx)

    def visitAlgebraic(self, ctx:JavaELParser.AlgebraicContext):
        logger.opt(colors=True).debug(f'algebraic: <red>{id(ctx)}</red> <green>{ctx.getText()}</green> dmn: {hasattr(ctx, "colors")}')
        if not self.lastContextWasDMN():
            return self.passIfNoDMN(ctx)

    def visitRelation(self, ctx:JavaELParser.RelationContext):
        logger.opt(colors=True).debug(f'relation: <red>{id(ctx)}</red> <green>{ctx.getText()}</green> dmn: {hasattr(ctx, "colors")}')
        if not self.lastContextWasDMN():
            return self.passIfNoDMN(ctx)

    def visitEquality(self, ctx:JavaELParser.EqualityContext):
        logger.opt(colors=True).debug(f'equality: <red>{id(ctx)}</red> <green>{ctx.getText()}</green> dmn: {hasattr(ctx, "colors")}')
        if not self.lastContextWasDMN():
            return self.passIfNoDMN(ctx)

    def visitTerm(self, ctx:JavaELParser.TermContext):
        logger.opt(colors=True).debug(f'term: <red>{id(ctx)}</red> <green>{ctx.getText()}</green> dmn: {hasattr(ctx, "colors")}')
        if not self.lastContextWasDMN():
            return self.passIfNoDMN(ctx)

    def visitExpression(self, ctx:JavaELParser.ExpressionContext):
        logger.opt(colors=True).debug(f'expression: <red>{id(ctx)}</red> <green>{ctx.getText()}</green> dmn: {hasattr(ctx, "colors")}')
        if not self.lastContextWasDMN():
            return self.passIfNoDMN(ctx)

    def visitTernary(self, ctx:JavaELParser.TernaryContext):
        logger.opt(colors=True).debug(f'ternary: <red>{id(ctx)}</red> <green>{ctx.getText()}</green> dmn: {hasattr(ctx, "colors")}')
        if not self.lastContextWasDMN():
            return self.passIfNoDMN(ctx)

    @property
    def tree_expression(self):
        """
        returns stored expression and clear storage
        :return: string representation of expression
        """
        to_return = ''.join(self.result)
        to_return = " ".join(to_return.split())
        self.result.clear()
        return to_return


class FEELTreePrinter(feelVisitor):
    def __init__(self):
        super(FEELTreePrinter, self).__init__()
        self.result = []

    def visitTerminal(self, node):
        self.result.append(node.getText())

    @property
    def tree_expression(self):
        to_return = ' '.join(self.result)
        self.result.clear()
        return to_return
