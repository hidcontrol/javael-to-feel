from typing import List

from antlr4 import *

from ANTLR_JavaELParser.JavaELParser import JavaELParser
from ANTLR_JavaELParser.JavaELParserVisitor import JavaELParserVisitor
from src.translator.ast_printer import FEELTreePrinter
from src.translator.node_algorithm import add_color_to_ctx, isCtxSimple
from loguru import logger

logger = logger.opt(colors=True)


class DMNTreeNode:
    def __init__(self):
        self.children = []
        self.contexts = None

    def find_dependencies(self):
        """
        Find dependent sub DMN expressions and replace to id
        example: field.first eq field.second and not (field.third or true) ->
              -> field.first eq field.second and dmn_1
        :return:
        """
        # только один контекст не терминальный
        if isinstance(self, ExpressionDMN):
            for c in self.contexts:
                if not isinstance(c, TerminalNode):
                    DMNTreeBuilder(self).visit(c)

        for child in self.children:
            child.find_dependencies()


class ExpressionDMN(DMNTreeNode):
    def __init__(self, expr: str, ctxs: List[ParserRuleContext]):
        super(ExpressionDMN, self).__init__()
        self.expression = expr
        self.contexts = ctxs
        self.children = []


class OperatorDMN(DMNTreeNode):
    def __init__(self, operator: int):
        super(OperatorDMN, self).__init__()
        self.operator = operator


class DMNTree:
    def __init__(self, ctx: ParserRuleContext):
        self.ctx = ctx
        if ctx:
            p = FEELTreePrinter()
            p.visit(ctx)
            self.root = ExpressionDMN(p.tree_expression, [ctx])
            self.root.find_dependencies()


class DMNTreeBuilder(JavaELParserVisitor):
    """
    Extract to DMN node operands of non-logical operators
    """
    def __init__(self, node: DMNTreeNode):
        super(DMNTreeBuilder, self).__init__()
        self.node = node

    def add_binary_children(self, ctx_l: ParserRuleContext, ctx_r: ParserRuleContext, operator: int):
        # self.node
        #    |
        #    |
        # operator
        #  |    |
        #  |    |
        # left right
        new_op_node = OperatorDMN(operator)

        ast_printer = FEELTreePrinter()

        ast_printer.visit(ctx_l)
        new_expr_node_l = ExpressionDMN(ast_printer.tree_expression, [ctx_l])

        ast_printer.visit(ctx_r)
        new_expr_node_r = ExpressionDMN(ast_printer.tree_expression, [ctx_r])

        new_op_node.children.append(new_expr_node_l)
        new_op_node.children.append(new_expr_node_r)

        self.node.children.append(new_op_node)
        return id(new_op_node)

    def add_unary_children(self, text: str, ctxs: List[ParserRuleContext], operator: int = None):
        """
        Генерирует имя для DMNTreeNode, создает нового ребенка у node,
        в выражении родителя заменяет выражение ребенка на dmn id вида dmn_{int}
        :param ctxs:
        :param text: часть выражения, записанная с пробелами
        :param operator:
        :return:
        """
        # self.node
        #    |
        #    |
        # operator
        #    |
        #    |
        # expression
        if operator:
            new_op_node = OperatorDMN(operator)
            new_expr_node = ExpressionDMN(text, ctxs)
            new_op_node.children.append(new_expr_node)
            self.node.children.append(new_op_node)
            return id(new_op_node)
        else:
            new_node = ExpressionDMN(text, ctxs)
            self.node.children.append(new_node)
            return id(new_node)

    def visitBase(self, ctx: JavaELParser.BaseContext):
        if ctx.getChildCount() > 1:
            self.processUnary(ctx)
        else:
            return self.visitChildren(ctx)

    def visitMember(self, ctx: JavaELParser.MemberContext):
        if ctx.getChildCount() > 1:
            self.processBinary(ctx)
        else:
            return self.visitChildren(ctx)

    def visitAlgebraic(self, ctx: JavaELParser.AlgebraicContext):
        if ctx.getChildCount() > 1:
            self.processBinary(ctx)
        else:
            return self.visitChildren(ctx)

    def visitEquality(self, ctx: JavaELParser.EqualityContext):
        if ctx.getChildCount() > 1:
            self.processBinary(ctx)
        else:
            return self.visitChildren(ctx)

    def visitRelation(self, ctx: JavaELParser.RelationContext):
        if ctx.getChildCount() > 1:
            # пропустить скобки
            if not (isinstance(ctx.getChild(0), TerminalNode) and ctx.getChild(0).symbol.type == JavaELParser.OpenParen) and not (isinstance(ctx.getChild(2), TerminalNode) and ctx.getChild(2).token.type != JavaELParser.CloseParen):
                self.processBinary(ctx)
            else:
                return self.visitChildren(ctx)
        else:
            return self.visitChildren(ctx)

    def processUnary(self, ctx: ParserRuleContext):
        """
        Add DMNNode represents unary operator if operand not simple
        :param ctx:
        :return:
        """
        children_count = ctx.getChildCount()
        for i in range(children_count):

            # pass operated
            if not hasattr(ctx.getChild(i), 'visited') or not ctx.getChild(i).visited:
                maybe_operator = ctx.getChild(i)
                maybe_operand = ctx.getChild(i + 1)

                ast_printer = FEELTreePrinter()
                # case with chain unary operators
                if isinstance(maybe_operand, TerminalNode):
                    maybe_operator.visited = True

                    new_child_ctxs = []
                    new_child_text = []



                    for j in range(i + 1, children_count):
                        new_child_ctxs.append(ctx.getChild(j))
                        ast_printer.visit(ctx.getChild(j))
                        new_child_text.append(ast_printer.tree_expression)

                    new_child_text = ' '.join(new_child_text)

                    new_child_id = 'dmn' + str(self.add_unary_children(new_child_text, new_child_ctxs, maybe_operator))

                    # редактируем свое выражение
                    ast_printer.visit(maybe_operand)
                    self.node.expression = self.node.expression.replace(ast_printer.tree_expression,
                                                                        ' ' + new_child_id + ' ')

                    # все следующие пометить как принадлежащие node
                    for j in range(i + 1, children_count):
                        ast_printer.visit(ctx.getChild(j))
                        self.node.expression = self.node.expression.replace(ast_printer.tree_expression, '')
                        add_color_to_ctx(ctx.getChild(j), new_child_id)
                    break
                else:
                    maybe_operator.visited = True
                    maybe_operand.visited = True

                    ast_printer.visit(maybe_operand)
                    new_child_id = 'dmn' + str(
                        self.add_unary_children(ast_printer.tree_expression, [maybe_operand], maybe_operator))

                    ast_printer.visit(maybe_operand)

                    # редактируем свое выражение
                    self.node.expression = self.node.expression.replace(ast_printer.tree_expression,
                                                                        ' ' + new_child_id + ' ')
                    # пометить операнд как принадлежащий node
                    add_color_to_ctx(maybe_operand, new_child_id)
                    # self.node.expression = self.node.expression.replace(maybe_operand.getText(), ' ' + new_child_id + ' ')

                    break

    def processBinary(self, ctx: ParserRuleContext):
        """
        Add DMNNode if at least one operand not simple
        :param ctx:
        :return:
        """
        children_count = ctx.getChildCount()
        if children_count > 1:
            if not isCtxSimple(ctx.getChild(0)) or not isCtxSimple(ctx.getChild(2)):
                self.add_binary_children(ctx.getChild(0), ctx.getChild(2), ctx.getChild(1).symbol.type)
                # if not isinstance(ctx.getChild(0), TerminalNode):
                #     if not isCtxSimple(ctx.getChild(0)):
                #         self.add_unary_children(ctx.getChild(0), ctx.getChild(1))
                #         add_color_to_ctx(ctx.getChild(0), 'dmn_id' + str(id(self.node)))
                # if not isinstance(ctx.getChild(2), TerminalNode):
                #     if not isCtxSimple(ctx.getChild(2)):
                #         self.add_unary_children(ctx.getChild(2), ctx.getChild(1))
                #         add_color_to_ctx(ctx.getChild(2), 'dmn_id' + str(id(self.node)))


def printDMNTree(dmntree: DMNTree) -> None:
    root_node = dmntree.root
    _printDMNTree(root_node)


def _printDMNTree(node: DMNTreeNode) -> None:
    if isinstance(node, ExpressionDMN):
        logger.debug(
            f"ExpressionDMN node {id(node)} expression: {node.expression}, children: {len(node.children)}")
    elif isinstance(node, OperatorDMN):
        logger.debug(
            f"OperatorDMN node {id(node)} operator: {node.operator}")
    for child in node.children:
        _printDMNTree(child)

