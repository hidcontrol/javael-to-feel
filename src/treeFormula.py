import copy
from loguru import logger
from src.getOperands_01 import toDMN
from collections import namedtuple
import re
import ctypes
from antlr4 import *
from ANTLR_JavaELParser.JavaELParser import JavaELParser
from ANTLR_JavaELParser.JavaELLexer import JavaELLexer
from ANTLR_JavaELParser.JavaELParserVisitor import JavaELParserVisitor

# comment for debug info
logger.disable(__name__)

extract_id_re = re.compile(r'op_(\d+)')

not_re = re.compile(r'~([\d\w_]+)')

new_child_dmn_handler = None

ExpressionZipped = namedtuple('ExpressionZipped', ('expression', 'tree'))


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
        logger.debug("visit Ternary {}: {} with translated {}", ctx.getText(), [i.getText() for i in ctx.getChildren()], self.translated)
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
        logger.debug("visit Relation {}: {} with translated {}", ctx.getText(), [i.getText() for i in ctx.getChildren()], self.translated)
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
        logger.debug("visit Equality {}: {} with translated {}", ctx.getText(), [i.getText() for i in ctx.getChildren()], self.translated)
        if ctx.getChildCount() > 1:
            self.translateEqualityToFEEL(ctx)
        else:
            return self.visitChildren(ctx)

    def visitBase(self, ctx: JavaELParser.BaseContext):
        logger.debug("visit Base {}: {} with translated {}", ctx.getText(), [i.getText() for i in ctx.getChildren()], self.translated)
        if ctx.getChildCount() > 1:
            self.translateUnaryToFEEL(ctx)
        else:
            return self.visitChildren(ctx)

    def visitTerminal(self, node):
        logger.debug("visit Terminal {}", node.getText())
        self.translated.append(node.getText())

    def visitPrimitive(self, ctx: JavaELParser.PrimitiveContext):
        logger.debug("visit Primitive {}: {} with translated {}", ctx.getText(), [i.getText() for i in ctx.getChildren()],
                     self.translated)
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
            self.translated.append('')
            self.translated.append(self.visit(ctx.getChild(2)))

        elif operator == '!=' or operator == 'ne':
            self.translated.append(self.visit(ctx.getChild(0)))
            self.translated.append('not(')
            self.translated.append(self.visit(ctx.getChild(2)))
            self.translated.append(')')


class SubDMNFinder(JavaELParserVisitor):
    def visitBase(self, ctx: JavaELParser.BaseContext):
        if ctx.getChildCount() > 1:
            self.handle_unary(ctx)
        else:
            return self.visitChildren(ctx)

    def visitMember(self, ctx: JavaELParser.MemberContext):
        if ctx.getChildCount() > 1:
            self.handle_binary(ctx)
        else:
            return self.visitChildren(ctx)

    def visitAlgebraic(self, ctx: JavaELParser.AlgebraicContext):
        if ctx.getChildCount() > 1:
            self.handle_binary(ctx)
        else:
            return self.visitChildren(ctx)

    def visitEquality(self, ctx: JavaELParser.EqualityContext):
        if ctx.getChildCount() > 1:
            self.handle_binary(ctx)
        else:
            return self.visitChildren(ctx)

    def visitRelation(self, ctx: JavaELParser.RelationContext):
        if ctx.getChildCount() > 1:
            self.handle_binary(ctx)
        else:
            return self.visitChildren(ctx)

    @staticmethod
    def handle_unary(ctx: ParserRuleContext):
        children_count = ctx.getChildCount()
        if children_count > 1 and not isCtxSimple(ctx.getChild(1)):
            new_child_dmn_handler(ctx.getChild(1), ctx.getChild(0))

    @staticmethod
    def handle_binary(ctx: ParserRuleContext):
        children_count = ctx.getChildCount()
        if children_count > 1:
            if not isCtxSimple(ctx.getChild(0)):
                new_child_dmn_handler(ctx.getChild(0), ctx.getChild(1))
            if not isCtxSimple(ctx.getChild(2)):
                new_child_dmn_handler(ctx.getChild(2), ctx.getChild(1))


class DMNExpression:
    def __init__(self, expr: str, ctx: ParserRuleContext = None, operator: int = None):
        self.expression = expr
        self.operator = operator
        self.root = ctx
        self.children = []

    def find_dependencies(self):
        global new_child_dmn_handler
        new_child_dmn_handler = dmn_tree_handler(self)
        SubDMNFinder().visit(self.root)
        for child in self.children:
            child.find_dependencies()


class DMNTree:
    def __init__(self, ctx: ParserRuleContext):
        self.ctx = ctx
        if ctx:
            self.expr = DMNExpression(ctx.getText(), ctx)
            self.expr.find_dependencies()


class SimpleOperandMarker(JavaELParserVisitor):
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
                        left_operand_parent_with_simple = SimpleOperandMarker._findSimpleOperandAncestor(children[i - 1])
                        if left_operand_parent_with_simple:
                            left_operand_parent_with_simple.is_simple_operand = False
                        children[i - 1].is_simple_operand = True

                    if i + 1 < children_cnt:
                        right_operand_parent_with_simple = SimpleOperandMarker._findSimpleOperandAncestor(children[i + 1])
                        if right_operand_parent_with_simple:
                            right_operand_parent_with_simple.is_simple_operand = False
                        children[i + 1].is_simple_operand = True
        elif isinstance(ctx, JavaELParser.BaseContext):
            for i in range(children_cnt):
                if not(hasattr(children[i], 'symbol') and children[i].symbol.type in [JavaELParser.Not, JavaELParser.Empty, JavaELParser.Minus]):
                    # operand branch
                    operand_marked_parent = SimpleOperandMarker._findSimpleOperandAncestor(children[i])
                    if operand_marked_parent:
                        operand_marked_parent.is_simple_operand = False
                    children[i].is_simple_operand = True
                    return

    def visitTerm(self, ctx: JavaELParser.TermContext):
        self._mark_simple(ctx, JavaELParser.And)
        return self.visitChildren(ctx)

    def visitExpression(self, ctx: JavaELParser.ExpressionContext):
        self._mark_simple(ctx, JavaELParser.Or)
        return self.visitChildren(ctx)

    def visitBase(self, ctx: JavaELParser.BaseContext):
        self._mark_simple(ctx, JavaELParser.Not)
        return self.visitChildren(ctx)


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
            self._zipped.append('op_' + str(id(ctx)) + ' ')
        else:
            return self.visitChildren(ctx)


def dmn_tree_handler(e: DMNExpression):
    def wrapper(ctx, operator):
        e.children.append(DMNExpression(ctx.getText(), ctx, operator))
    return wrapper


def traversFormulaTree(ctx: ParserRuleContext, formula: str):
    logger.debug('formula {} context {}', formula, ctx.getText())
    if not isinstance(ctx, TerminalNode):
        for child in ctx.getChildren():
            formula = traversFormulaTree(child, formula)
    else:
        formula = formula + ctx.getText() + (' ' if ctx.getText() != '.' else '')
    return formula


def tree(expression: str):
    input_stream = InputStream(expression)
    lexer = JavaELLexer(input_stream)
    tree_returned = JavaELParser(CommonTokenStream(lexer))
    return tree_returned.ternary()


def zipFormula(expression: str) -> ExpressionZipped:
    tre = tree(expression)
    SimpleOperandMarker().visit(tre)
    zipper = FormulaZipper()
    zipper.visit(tre)
    return ExpressionZipped(zipper.result, tre)


def unzipOperand(operand_id: str) -> str:
    operand = ctypes.cast(int(operand_id), ctypes.py_object).value
    operand_formula = ''
    operand_formula = traversFormulaTree(operand, operand_formula)
    operand_formula = operand_formula.replace(' .', '.')
    return operand_formula


def unpack(formula: str) -> str:
    # set scopes after not
    for not_m in not_re.findall(formula):
        formula = formula.replace(not_m, '(' + not_m + ')')

    # unzip by id
    for m in extract_id_re.findall(formula):
        formula = formula.replace(m, unzipOperand(m))
    formula = formula.replace('op_', '').replace('_', ' ')

    # java el logical operators form
    formula = formula.replace('~', '!').replace('And', 'and').replace('Or', 'or')
    return formula


def toParentTernaryDist(ctx: ParserRuleContext) -> int:
    dist = 0
    while not isinstance(ctx.parentCtx, JavaELParser.TernaryContext):
        ctx = ctx.parentCtx
        dist += 1
    return dist


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


def isCtxSimple(ctx: ParserRuleContext) -> bool:
    """
    subtree is simple operand if
    max dist to bottom + dist to parent Ternary == 11 (distance to bottom in simple case)
    :param ctx: root of subtree
    :return: bool
    """
    th = treeHeight(ctx)
    tp = toParentTernaryDist(ctx)
    return th + tp == 10
