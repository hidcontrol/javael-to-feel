import re
import copy
import click
import sys
import xmldict
import networkx as nx
import pandas as pd
import xml.etree.ElementTree as ET
from loguru import logger
from matplotlib import pyplot as plt
from loguru import logger
from collections import namedtuple
from enum import Enum
from typing import List, Set
from JavaEL_tokenize import JavaELTokenType, tokenize_expression

ExpressionDependencyBase = namedtuple('ExpressionDependencyBase', ('property', 'expression', 'condition_type', 'form'))


class ExpressionDependency(ExpressionDependencyBase):
    pass
    # def __hash__(self):
    #     return hash(self.property)
    #
    # def __eq__(self, other):
    #     return self.property == other.property


logger.remove()
logger.add(sys.stdout, colorize=True, level='DEBUG', format='{level} {message}')

# find <key>(...)</key><value(...)>
property_expression_re = re.compile(r'(?<=<key>)(.*?)(?=</key>\s*<value(.*?)>)')
# find JavaEL expression
expression_re = re.compile(r'(\w+)=\"#{(.*?)}\"')
# file extension regexp
extract_filetype_re = re.compile(r'\w+\.(xml)')
# find form name
form_name_re = re.compile(r'objectForm name=\"(.+?)\"')


# compiled dataframe columns names
DATAFRAME_SRC_FORM_NAME = 'srcFormName'
DATAFRAME_SRC_FIELD_NAME = 'srcFieldName'
DATAFRAME_DST_FIELD_NAME = 'dstFieldNames'
DATAFRAME_DMN_NAME = 'DMN_name'
DATAFRAME_EXPRESSION = 'expression'


def extract_prop_dependency_from_file(xml_file_path):
    """
    get Java EL expressions from xml file with <form> tags
    :param xml_file_path: path to form xml file
    :return: dict {
                    'formName1': [ExpressionsDependency ...],
                    'formName2': [ExpressionsDependency ...],
                    ...
                    }
    """
    if extract_filetype_re.findall(xml_file_path)[0] != 'xml':
        raise ValueError('Invalid xml file')
    forms_exprs_props = {}

    xml_tree = ET.parse(xml_file_path)
    root = xml_tree.getroot()
    forms = list(root.iter('forms'))

    for form in forms:
        props_exprs = re.findall(property_expression_re, form.text)
        form_name = form_name_re.findall(form.text)[0]

        if props_exprs:
            forms_exprs_props[form_name] = []

            for match in props_exprs:
                exprs = re.findall(expression_re, match[1])
                if exprs:
                    for e in exprs:
                        forms_exprs_props[form_name].append(
                            ExpressionDependency(
                                property=match[0], condition_type=e[0], expression=e[1], form=form_name
                            )
                        )

    return forms_exprs_props


def extract_props_from_expression(expr_dep: str) -> Set[str]:
    """
    From all lvalues remove "fields." prefix and properties or rvalue like prop.attr
    :param expr_dep: ExpressionDependency
    :return: List[str]
    """
    tokens = tokenize_expression(expr_dep)
    dependents = set()

    for token in tokens:
        if token.token_type == JavaELTokenType.LVALUE:
            val = copy.deepcopy(token.token_value)
            val = re.sub(r'^fields.', '', val)
            val = re.search(r'\w+', val)
            if val:
                dependents.add(val[0])
            else:
                logger.debug(f'Syntax error during extract dependent property from {token.token_value}')
        elif token.token_type == JavaELTokenType.RVALUE:
            val = copy.deepcopy(token.token_value)
            val = re.findall(r'^(\w+)\.', val)
            if val:
                dependents.add(val[0])

    return dependents


class JavaELExpression:
    """
    Class represents common Java EL expression
    Every JavaELExpression consists of JavaELSimpleExpressions and logical operators
    """

    def __init__(self, expression: ExpressionDependency):
        self.expression = expression

    def __str__(self):
        return self.expression


class JavaELSimpleExpression(JavaELExpression):
    """
    Class represents simple expression with only one operator or boolean
    """

    def __init__(self, *args, **kwargs):
        super(JavaELSimpleExpression, self).__init__(*args, **kwargs)


@click.command()
@click.argument('path')
@click.argument('out')
def main(path, out):
    user_input_file_path = path

    javael_exprs_from_file = extract_prop_dependency_from_file(xml_file_path=path)

    adjacency = {}  # str: List[str]

    for form in javael_exprs_from_file.keys():
        for expr in javael_exprs_from_file[form]:
            logger.debug(expr.expression)
            # find dependent expressions here
            try:
                adjacency[expr] = extract_props_from_expression(expr.expression)
            except ValueError:
                # TODO: error handler
                pass
            # commented for writing just unique related properties
            # if expr in adjacency.keys():
            #     adjacency[expr].update(extract_props_from_expression(expr.expression))
            # else:
            #     adjacency[expr] = extract_props_from_expression(expr.expression)

    dataframe = pd.DataFrame(
        columns=[
            DATAFRAME_SRC_FORM_NAME,
            DATAFRAME_SRC_FIELD_NAME,
            DATAFRAME_DST_FIELD_NAME,
            DATAFRAME_DMN_NAME,
            DATAFRAME_EXPRESSION
        ]
    )

    dataframe_rows = []

    for key in adjacency.keys():
        dataframe_rows.append(
            {
                DATAFRAME_SRC_FORM_NAME: key.form,
                DATAFRAME_SRC_FIELD_NAME: key.property,
                DATAFRAME_DST_FIELD_NAME: adjacency[key] if len(adjacency[key]) else None,
                DATAFRAME_EXPRESSION: key.expression
            }
        )
    dataframe = dataframe.append(pd.DataFrame(dataframe_rows))

    dataframe.to_csv(out, index=False)


if __name__ == '__main__':
    main()
