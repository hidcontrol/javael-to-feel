from antlr4 import *

from ANTLR_JavaELParser.JavaELLexer import JavaELLexer
from ANTLR_JavaELParser.JavaELParser import JavaELParser
from loguru import logger

logger = logger.opt(colors=True)


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
    logger.debug(f'<red>context: {id(ctx)} colorized: {dmn_id}</red>')


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


def tree(expression: str):
    input_stream = InputStream(expression)
    lexer = JavaELLexer(input_stream)
    tree_returned = JavaELParser(CommonTokenStream(lexer))
    return tree_returned.ternary()

