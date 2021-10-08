import ctypes
import re
from collections import namedtuple
from typing import Set
from antlr4 import ParserRuleContext, TerminalNode
from ANTLR_JavaELParser.JavaELParser import JavaELParser
from ANTLR_JavaELParser.JavaELParserVisitor import JavaELParserVisitor
from loguru import logger

from src.translator.ast_printer import SyntaxTreePrinter

ExpressionZipped = namedtuple('ExpressionZipped', ('expression', 'tree'))

logger = logger.opt(colors=True)

extract_id_re = re.compile(r'op_(\d+)')

not_re = re.compile(r'~([\d\w_]+)')


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
