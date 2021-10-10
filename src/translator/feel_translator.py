import re

from antlr4 import TerminalNode, ParserRuleContext

from ANTLR_JavaELParser.JavaELParser import JavaELParser
from ANTLR_JavaELParser.JavaELParserVisitor import JavaELParserVisitor


class ToFEELConverter(JavaELParserVisitor):
    def __init__(self):
        super(ToFEELConverter, self).__init__()
        self.translated = []
        self.visited = []

    @property
    def result(self):
        to_ret = ''
        for i in self.translated:
            if i is not None:
                to_ret += i + ' '
        to_ret = to_ret.replace(' .', '.').replace('. ', '.').strip()
        to_ret = re.sub(r'\s+', ' ', to_ret)
        return to_ret

    def visitTernary(self, ctx: JavaELParser.TernaryContext):
        # logger.debug("visit Ternary {}: {} with translated {}", ctx.getText(), [i.getText() for i in ctx.getChildren()],
        #              self.translated)
        if ctx.getChildCount() > 1:  # ternary expression
            ctx_children = list(ctx.getChildren())
            condition_expression = ctx_children[0]
            true_ternary = ctx_children[2]
            false_ternary = ctx_children[4]

            self.translated.append('if')
            self.translated.append(self.visit(condition_expression))
            self.translated.append('then')
            self.translated.append(self.visit(true_ternary))
            self.translated.append('else')
            self.translated.append(self.visit(false_ternary))
        else:
            return self.visitChildren(ctx)

    def visitRelation(self, ctx: JavaELParser.RelationContext):
        # logger.debug("visit Relation {}: {} with translated {}", ctx.getText(),
        #              [i.getText() for i in ctx.getChildren()], self.translated)
        if ctx.getChildCount() > 1 and isinstance(ctx.getChild(1), TerminalNode):
            left_algebraic = ctx.getChild(0)
            right_algebraic = ctx.getChild(2)
            ctx_operator = ctx.getChild(1)

            self.translated.append(self.visit(left_algebraic))
            self.translated.append(self.translateRelationalToFEEL(ctx_operator))
            self.translated.append(self.visit(right_algebraic))

        else:
            return self.visitChildren(ctx)

    def visitEquality(self, ctx: JavaELParser.EqualityContext):
        # logger.debug("visit Equality {}: {} with translated {}", ctx.getText(),
        #              [i.getText() for i in ctx.getChildren()], self.translated)
        if ctx.getChildCount() > 1:
            self.translateEqualityToFEEL(ctx)
        else:
            return self.visitChildren(ctx)

    def visitBase(self, ctx: JavaELParser.BaseContext):
        # logger.debug("visit Base {}: {} with translated {}", ctx.getText(), [i.getText() for i in ctx.getChildren()],
        #              self.translated)
        if ctx.getChildCount() > 1:
            self.translateUnaryToFEEL(ctx)
        else:
            return self.visitChildren(ctx)

    def visitTerminal(self, node):
        # logger.debug("visit Terminal {}", node.getText())
        self.translated.append(node.getText())

    def visitPrimitive(self, ctx: JavaELParser.PrimitiveContext):
        # logger.debug("visit Primitive {}: {} with translated {}", ctx.getText(),
        #              [i.getText() for i in ctx.getChildren()],
        #              self.translated)
        self.translated.append(ctx.getText())

    def translateUnaryToFEEL(self, ctx: ParserRuleContext):
        child_cht = ctx.getChildCount()
        for i in range(child_cht):
            child = ctx.getChild(i)
            if child not in self.visited:
                if isinstance(child, TerminalNode):
                    operator = child.symbol.type
                    self.visited.append(child)

                    if operator == JavaELParser.Not:
                        self.translated.append('not(')
                        self.translateUnaryToFEEL(ctx)
                        self.translated.append(')')

                    elif operator == JavaELParser.Empty:
                        self.translateUnaryToFEEL(ctx)
                        self.translated.append(' ')
                        self.translated.append(' = ')
                        self.translated.append('null')
                else:
                    self.visit(child)
                    self.visited.append(child)

    def visitChildren(self, node):
        result = self.defaultResult()
        n = node.getChildCount()
        for i in range(n):
            if not self.shouldVisitNextChild(node, result):
                return result

            c = node.getChild(i)
            childResult = None
            if c not in self.visited:
                childResult = c.accept(self)
            result = self.aggregateResult(result, childResult)

        return result

    @staticmethod
    def translateRelationalToFEEL(operator: str) -> str:
        if operator == 'gt':
            return '>'
        elif operator == 'lt':
            return '<'
        elif operator == 'ge':
            return '>='
        elif operator == 'le':
            return '<='

    def translateEqualityToFEEL(self, ctx: ParserRuleContext):
        operator = ctx.getChild(1).getText()
        if operator == '==' or operator == 'eq':
            self.translated.append(self.visit(ctx.getChild(0)))
            self.translated.append('=')
            self.translated.append(self.visit(ctx.getChild(2)))

        elif operator == '!=' or operator == 'ne':
            self.translated.append(self.visit(ctx.getChild(0)))
            self.translated.append('not(')
            self.translated.append(self.visit(ctx.getChild(2)))
            self.translated.append(')')
