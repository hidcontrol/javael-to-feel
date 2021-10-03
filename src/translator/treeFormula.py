from typing import List, Set
from lxml import etree

from loguru import logger
from collections import namedtuple
from queue import SimpleQueue
import re
import ctypes
from antlr4 import *
from ANTLR_JavaELParser.JavaELParser import JavaELParser
from ANTLR_JavaELParser.JavaELLexer import JavaELLexer
from ANTLR_JavaELParser.JavaELParserVisitor import JavaELParserVisitor
from src.translator.toKNF import toDMNReady
from src.translator.xmlPacker import DecisionTable, expression_xml

# logger.disable(__name__)

logger = logger.opt(colors=True)

extract_id_re = re.compile(r'op_(\d+)')

not_re = re.compile(r'~([\d\w_]+)')

ExpressionZipped = namedtuple('ExpressionZipped', ('expression', 'tree'))


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
        global new_child_dmn_handler
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
            p = SyntaxTreePrinter()
            p.visit(ctx)
            self.root = ExpressionDMN(p.tree_expression, [ctx])
            self.root.find_dependencies()


def add_color_to_ctx(ctx: ParserRuleContext, dmn_id: str):
    """
    добвать в очередь к ctx новый dmn_id, иначе создать ее
    корневые вершины поддеревьев DMNNode покрашены в одинаковый dmn_id
    :param ctx:
    :param dmn_id:
    :return:
    """
    if hasattr(ctx, 'colors'):
        ctx.colors.append(dmn_id)
    else:
        ctx.colors = []
        ctx.colors.append(dmn_id)
    logger.opt(colors=True).debug(f'<red>context: {id(ctx)} colorized: {dmn_id}</red>')


def tree(expression: str):
    input_stream = InputStream(expression)
    lexer = JavaELLexer(input_stream)
    tree_returned = JavaELParser(CommonTokenStream(lexer))
    return tree_returned.ternary()


def zipFormula(context: ParserRuleContext) -> ExpressionZipped:
    SimpleOperandMarker().visit(context)
    zipper = FormulaZipper()
    zipper.visit(context)
    return ExpressionZipped(zipper.result, context)


def unzipOperand(operand_id: str) -> str:
    operand = ctypes.cast(int(operand_id), ctypes.py_object).value

    logger.opt(colors=True).debug(f'<green>unzip {operand_id}</green>')

    printer = SyntaxTreePrinter()
    printer.visit(operand)
    result = printer.tree_expression
    return result


def concatWithOr(or_operands: Set[str]):
    scoped_or_operands = set()
    for s in or_operands:
        scoped_or_operands.add('(' + s + ')')

    return ' or '.join(scoped_or_operands)


def unpack(formula: str) -> str:
    # set scopes after not
    for not_m in not_re.findall(formula):
        formula = formula.replace(not_m, '(' + not_m + ')')

    # unzip by id
    for m in extract_id_re.findall(formula):
        formula = formula.replace(m, unzipOperand(m))
    formula = formula.replace('op_', ' ')
    formula = re.sub(r'_(..)_', r' \g<1> ', formula)
    formula = formula.replace('_ ', ' ').replace(' _', ' ').replace("\'", "\"")

    # java el logical operators form
    formula = formula.replace('~', '!').replace('And', 'and').replace('Or', 'or')
    return ' '.join(formula.split())


new_child_dmn_handler = None


class SyntaxTreePrinter(JavaELParserVisitor):
    def __init__(self):
        super(SyntaxTreePrinter, self).__init__()
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
        return ' '.join(self.result)


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

        new_expr_node_l = ExpressionDMN(ctx_l.getText(), [ctx_l])
        new_expr_node_r = ExpressionDMN(ctx_r.getText(), [ctx_r])

        new_op_node.children.append(new_expr_node_l)
        new_op_node.children.append(new_expr_node_r)

        self.node.children.append(new_op_node)
        return id(new_op_node)

    def add_unary_children(self, text: str, ctxs: List[ParserRuleContext], operator: int = None):
        """
        Генерирует имя для DMNTreeNode, создает нового ребенка у node,
        в выражении родителя заменяет выражение ребенка на dmn id вида dmn_{int}
        :param ctxs:
        :param text:
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
            if not (isinstance(ctx.getChild(0), TerminalNode) and ctx.getChild(0).symbol.type == JavaELParser.OpenParen) and \
                    not (isinstance(ctx.getChild(2), TerminalNode) and ctx.getChild(2).token.type != JavaELParser.CloseParen):
                self.processBinary(ctx)
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

                # case with chain unary operators
                if isinstance(maybe_operand, TerminalNode):
                    maybe_operator.visited = True

                    new_child_ctxs = []
                    new_child_text = []

                    for j in range(i + 1, children_count):
                        new_child_ctxs.append(ctx.getChild(j))
                        new_child_text.append(ctx.getChild(j).getText())

                    new_child_text = ' '.join(new_child_text)

                    new_child_id = 'dmn' + str(self.add_unary_children(new_child_text, new_child_ctxs, maybe_operator))

                    # редактируем свое выражение
                    self.node.expression = self.node.expression.replace(maybe_operand.getText(),
                                                                        ' ' + new_child_id + ' ')

                    # все следующие пометить как принадлежащие node
                    for j in range(i + 1, children_count):
                        self.node.expression = self.node.expression.replace(ctx.getChild(j).getText(), '')
                        add_color_to_ctx(ctx.getChild(j), new_child_id)
                    break
                else:
                    maybe_operator.visited = True
                    maybe_operand.visited = True
                    new_child_id = 'dmn' + str(
                        self.add_unary_children(maybe_operand.getText(), [maybe_operand], maybe_operator))

                    # редактируем свое выражение
                    self.node.expression = self.node.expression.replace(maybe_operand.getText(),
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


class SimpleOperandMarker(JavaELParserVisitor):
    """
    Find and mark logical operands without other logical operators
    """

    @staticmethod
    def _findSimpleOperandAncestor(ctx: ParserRuleContext) -> ParserRuleContext or None:
        while ctx.parentCtx:
            if hasattr(ctx, 'is_simple_operand') and ctx.is_simple_operand:
                return ctx
            else:
                ctx = ctx.parentCtx
        return None

    @staticmethod
    def _mark_simple(ctx: ParserRuleContext, operator: TerminalNode):
        children = list(ctx.getChildren())
        children_cnt = len(children)

        if isinstance(ctx, (JavaELParser.ExpressionContext, JavaELParser.TermContext)):
            for i in range(children_cnt):
                if hasattr(children[i], 'symbol') and children[i].symbol.type == operator:
                    # убрать is_simple_operand у прямых родителей
                    if i - 1 >= 0:
                        left_operand_parent_with_simple = SimpleOperandMarker._findSimpleOperandAncestor(
                            children[i - 1])
                        if left_operand_parent_with_simple:
                            left_operand_parent_with_simple.is_simple_operand = False
                        children[i - 1].is_simple_operand = True

                    if i + 1 < children_cnt:
                        right_operand_parent_with_simple = SimpleOperandMarker._findSimpleOperandAncestor(
                            children[i + 1])
                        if right_operand_parent_with_simple:
                            right_operand_parent_with_simple.is_simple_operand = False
                        children[i + 1].is_simple_operand = True
        elif isinstance(ctx, JavaELParser.BaseContext):
            for i in range(children_cnt):
                if not (hasattr(children[i], 'symbol') and children[i].symbol.type in [JavaELParser.Not,
                                                                                       JavaELParser.Empty,
                                                                                       JavaELParser.Minus]):
                    # operand branch
                    operand_marked_parent = SimpleOperandMarker._findSimpleOperandAncestor(children[i])
                    if operand_marked_parent:
                        operand_marked_parent.is_simple_operand = False
                    children[i].is_simple_operand = True
                    return

    def visitTerm(self, ctx: JavaELParser.TermContext):

        # если нода помечена как dmn, то она простая
        if hasattr(ctx, 'colors') and len(ctx.colors):
            ctx.is_simple_operand = True
            return
        self._mark_simple(ctx, JavaELParser.And)
        return self.visitChildren(ctx)

    def visitExpression(self, ctx: JavaELParser.ExpressionContext):
        # если нода помечена как dmn, то она простая
        if hasattr(ctx, 'colors') and len(ctx.colors):
            ctx.is_simple_operand = True
            return

        self._mark_simple(ctx, JavaELParser.Or)
        return self.visitChildren(ctx)

    def visitBase(self, ctx: JavaELParser.BaseContext):
        # если нода помечена как dmn, то она простая
        if hasattr(ctx, 'colors') and len(ctx.colors):
            ctx.is_simple_operand = True
            return

        self._mark_simple(ctx, JavaELParser.Not)
        return self.visitChildren(ctx)

    def visitTernary(self, ctx:JavaELParser.TernaryContext):
        # если нода помечена как dmn, то она простая
        if hasattr(ctx, 'colors') and len(ctx.colors):
            ctx.is_simple_operand = True
            return
        else:
            return self.visitChildren(ctx)

    def visitEquality(self, ctx:JavaELParser.EqualityContext):
        # если нода помечена как dmn, то она простая
        if hasattr(ctx, 'colors') and len(ctx.colors):
            ctx.is_simple_operand = True
            return
        else:
            return self.visitChildren(ctx)

    def visitRelation(self, ctx:JavaELParser.RelationContext):
        # если нода помечена как dmn, то она простая
        if hasattr(ctx, 'colors') and len(ctx.colors):
            ctx.is_simple_operand = True
            return
        else:
            return self.visitChildren(ctx)

    def visitAlgebraic(self, ctx:JavaELParser.AlgebraicContext):
        # если нода помечена как dmn, то она простая
        if hasattr(ctx, 'colors') and len(ctx.colors):
            ctx.is_simple_operand = True
            return
        else:
            return self.visitChildren(ctx)

    def visitMember(self, ctx:JavaELParser.MemberContext):
        # если нода помечена как dmn, то она простая
        if hasattr(ctx, 'colors') and len(ctx.colors):
            ctx.is_simple_operand = True
            return
        else:
            return self.visitChildren(ctx)

    def visitTerminal(self, node):
        # если нода помечена как dmn, то она простая
        if hasattr(node, 'colors') and len(node.colors):
            node.is_simple_operand = True
            return
        else:
            return self.visitChildren(node)


class FormulaZipper(JavaELParserVisitor):
    def __init__(self):
        super(FormulaZipper, self).__init__()
        self._zipped = []

    @property
    def result(self):
        to_ret = ''.join([token for token in self._zipped if token is not None]).replace(' . ', '.')
        to_ret = re.sub(r'\s+', ' ', to_ret)
        return to_ret

    def visitTernary(self, ctx: JavaELParser.TernaryContext):
        """
        A ? B : C ==
        (A -> B) and (!A -> C) == (!A or B) and (A or C) ==
        (!A and A) or (!A and С) or (B and A) or (B and С) ==
        (!A and С) or (A and B) or (B and С)
        :param ctx:
        :return:
        """
        if ctx.getChildCount() > 1:  # ternary expression here
            ctx_children = list(ctx.getChildren())
            condition_expression = ctx_children[0]
            true_ternary = ctx_children[2]
            false_ternary = ctx_children[4]

            # (not (A) and C)
            self._zipped.append('(! (')
            self._zipped.append(self.visit(condition_expression))
            self._zipped.append(') and ')
            self._zipped.append(self.visit(false_ternary))
            self._zipped.append(')')
            # or
            self._zipped.append(' or ')
            # (A and B)
            self._zipped.append('(')
            self._zipped.append(self.visit(condition_expression))
            self._zipped.append(' and ')
            self._zipped.append(self.visit(true_ternary))
            self._zipped.append(')')
            # # or
            # self._zipped.append(' or ')
            # # (B and C)
            # self._zipped.append('(')
            # self._zipped.append(self.visit(false_ternary))
            # self._zipped.append(' and ')
            # self._zipped.append(self.visit(true_ternary))
            # self._zipped.append(')')
        else:
            return self.visitChildren(ctx)

    def visitExpression(self, ctx: JavaELParser.ExpressionContext):
        return self.addIdIfSimple(ctx)

    def visitTerm(self, ctx: JavaELParser.TermContext):
        return self.addIdIfSimple(ctx)

    def visitEquality(self, ctx: JavaELParser.EqualityContext):
        return self.addIdIfSimple(ctx)

    def visitRelation(self, ctx: JavaELParser.RelationContext):
        return self.addIdIfSimple(ctx)

    def visitAlgebraic(self, ctx: JavaELParser.AlgebraicContext):
        return self.addIdIfSimple(ctx)

    def visitMember(self, ctx: JavaELParser.MemberContext):
        return self.addIdIfSimple(ctx)

    def visitBase(self, ctx: JavaELParser.BaseContext):
        return self.addIdIfSimple(ctx)

    def visitValue(self, ctx: JavaELParser.ValueContext):
        return self.addIdIfSimple(ctx)

    def visitPrimitive(self, ctx: JavaELParser.PrimitiveContext):
        return self.addIdIfSimple(ctx)

    def visitTerminal(self, node):
        self._zipped.append(node.getText() + ' ')

    def addIdIfSimple(self, ctx: ParserRuleContext):
        if hasattr(ctx, 'is_simple_operand') and ctx.is_simple_operand:
            logger.debug('dmn_id {}', hasattr(ctx, 'dmn_id'))
            self._zipped.append('op_' + str(id(ctx)) + ' ')
        else:
            return self.visitChildren(ctx)


class DMN_XML:
    @classmethod
    def visit(cls, tree: DMNTree) -> etree.Element:
        """
        DFS на возврате
        :return:
        """
        root = tree.root
        decisions = []
        cls._dfs(root, decisions)
        return expression_xml('drd_id', decisions)

    @classmethod
    def _dfs(cls, node: DMNTreeNode, decisions: List[etree.Element]):
        if len(node.children):
            for child in node.children:
                cls._dfs(child, decisions)

        # constraint dmn node
        if isinstance(node, OperatorDMN):
            cls.visitConstraint(node, decisions)
        elif isinstance(node, ExpressionDMN):
            # expression node
            cls.visitExpression(node, decisions)
        else:
            raise ValueError('XML builder got wrong DMN node type')

    @classmethod
    def visitExpression(cls, node: ExpressionDMN, decision_list: List[etree.Element]):
        logger.debug(f'construct DMN xml from <red>expression</red>: <green>{node.expression}</green>')

        dependents = ['dmn' + str(id(c)) for c in node.children]

        new_table = DecisionTable.from_expression(node.expression, 'output_name here', dependents)

        if not new_table:
            logger.error(f'construct DMN xml from <red>expression</red>: <green>{node.expression}</green> failure')
            raise ValueError('DecisionTable is None')

        decision_list.append(new_table)

    @classmethod
    def visitConstraint(cls, node: OperatorDMN, decision_list: List[etree.Element]):
        logger.debug(f'construct DMN xml from <red>constraint</red>: <green>{node.operator}</green>')

        dependents = ['dmn' + str(id(c)) for c in node.children]

        if node.operator.symbol.type in [JavaELParser.Empty, JavaELParser.Not]:
            new_table = DecisionTable.from_constraint(node.operator.symbol.type, dependents, decision_list[-1])

            if new_table is None:
                logger.error(f'construct DMN xml from <red>constraint</red>: <green>{node.operator}</green> failure')
                raise ValueError('DecisionTable is None')

            decision_list.append(new_table)
        else:
            left_op = decision_list[-2]
            right_op = decision_list[-1]

            new_table = DecisionTable.from_constraint(node.operator, dependents, left_op, right_op)

            if new_table is None:
                logger.error(f'construct DMN xml from <red>constraint</red>: <green>{node.operator}</green> failure')
                raise ValueError('DecisionTable is None')

            decision_list.append(new_table)


def treeHeight(ctx: ParserRuleContext) -> int:
    """
    Stuff function for determinate complex operand
    :param ctx: subtree root
    :return: subtree height
    """
    subtree_height = 0
    heightDFS.height = 0
    heightDFS(ctx, subtree_height)
    subtree_height = heightDFS.height
    del heightDFS.height
    return subtree_height


def heightDFS(ctx: ParserRuleContext, cur_h: int):
    cur_h = cur_h + 1
    # logger.debug("{} height {}", ctx.getText(), cur_h)
    if isinstance(ctx, TerminalNode):
        heightDFS.height = max(heightDFS.height, cur_h)
        return cur_h - 1
    for child in ctx.getChildren():
        cur_h = heightDFS(child, cur_h)
    return cur_h - 1


def toParentTernaryDist(ctx: ParserRuleContext) -> int:
    dist = 0
    while not isinstance(ctx.parentCtx, JavaELParser.TernaryContext):
        ctx = ctx.parentCtx
        dist += 1
    return dist


def isCtxSimple(ctx: ParserRuleContext) -> bool:
    """
    subtree is simple operand if
    max dist to bottom + dist to parent Ternary == 10 (distance to bottom in simple case)
    and ctx can be fork, not a TerminalNode
    :param ctx: root of subtree
    :return: bool
    """
    th = treeHeight(ctx)
    tp = toParentTernaryDist(ctx)
    return th + tp == 10 and not isinstance(ctx, TerminalNode)


def translateDMNReadyinDMNTree(dmntree: DMNTree) -> None:
    root_node = dmntree.root
    _translateDMNReadyinDMNTree(root_node)


def _translateDMNReadyinDMNTree(node: DMNTreeNode) -> None:
    # нет оператора -> выражение состоит только из логических операторов,
    # нелогические операторы имеют только простые операнды

    for child in node.children:
        _translateDMNReadyinDMNTree(child)

    if isinstance(node, ExpressionDMN):
        logger.debug(f"translating ExpressionDMN node {node.expression}")
        node.expression = zipFormula(tree(node.expression)).expression
        node.expression = toDMNReady(node.expression)
        node.expression = unpack(concatWithOr(node.expression))
        logger.debug(f"dnf converted: {node.expression}")
        dmn_ready_tree = tree(node.expression)
        conv = ToFEELConverter()
        conv.visit(dmn_ready_tree)
        node.expression = conv.result
    elif isinstance(node, OperatorDMN):
        logger.debug(f"skip OperatorDMN node {node.operator}")


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
