import string
import random
import typing
import re
from lxml import etree
from enum import Enum
from collections import namedtuple
from src.getOperands_01 import toDMN
from typing import Dict, Iterable, Set, List

from ANTLR_JavaELParser.JavaELParser import JavaELParser
from antlr4 import ParserRuleContext


xmlns = 'https://www.omg.org/spec/DMN/20191111/MODEL/'
dmndi = 'https://www.omg.org/spec/DMN/20191111/DMNDI/'
biodi = 'http://bpmn.io/schema/dmn/biodi/2.0'
dc = 'http://www.omg.org/spec/DMN/20180521/DC/'
di = 'http://www.omg.org/spec/DMN/20180521/DI/'
namespace = 'http://camunda.org/schema/1.0/dmn'
exporter = 'Camunda Modeler'
exporterVersion = '4.9.0'


RuleTag = namedtuple('RuleTag', ('inputEntries', 'outputEntry'))


class TypeRef(Enum):
    STRING = 1,
    INTEGER = 2


class DmnElementsExtracter:
    AND_OPERANDS_RE = re.compile(r'^and\((.*)\)$')
    WITH_BOOLEAN_METHOD = re.compile(r'^(.+?)\..+?\(\)$')

    @classmethod
    def _getInput(cls, expr: str):
        tokens = expr.split()
        if len(tokens) > 1:  # binary operator with operands
            return tokens[0]
        else:  # property.function()
            with_method = cls.WITH_BOOLEAN_METHOD.findall(tokens[0])
            if with_method:
                return with_method[0]

    @classmethod
    def _getOutput(cls, expr: str):
        tokens = expr.split()
        if len(tokens) == 1 and cls.WITH_BOOLEAN_METHOD.findall(tokens[0]) is None:
            return tokens[0]

    @staticmethod
    def _getRule(expr: str):
        tokens = expr.split()
        if len(tokens) > 1:  # binary operator with operands
            return ' '.join(tokens[1:])
        else:  # property.function()
            primitives = tokens[0].split('.')
            # cut '.function()' and return
            return primitives[len(primitives) - 1]

    @classmethod
    def _prepare(cls, operands_FEEL: Dict[str]):
        """
        :param operands_FEEL: {'and(....)',..}
        :return: [[operands], ..]
        """
        or_concatenated = []
        for operand in operands_FEEL:
            in_and = cls.AND_OPERANDS_RE.findall(operand)
            if in_and:
                splited = in_and[0].split(',').strip()  # list of strings
                # splited.join(' and ')
                or_concatenated.append(splited)
        return or_concatenated

    @classmethod
    def getInputs(cls, expr: str) -> Set[str]:  # lvalue во всех операндах or
        """
        operands can be 'lvalue op rvalue' or 'input.boolean_function'
        inputs are lvalue or input without boolean_function
        :param expr: simple dmn expression
        :return: Set[str]
        """
        inputs = set()
        for row in cls._prepare(toDMN(expr)):
            for cell in row:
                inputs.add(cls._getInput(cell))
        return inputs

    @classmethod
    def getRulesOrdered(cls, expr_tree: str, inputs) -> Iterable[RuleTag]:  # rvalue c оператором
        """
        :param inputs: order of rules
        :param expr_tree:
        :return:
        """
        rules = dict().fromkeys(inputs)
        used_inputs = []
        to_return = []
        is_none_row_needs = False

        for row in cls._prepare(toDMN(expr_tree)):
            output = []

            for cell in row:
                inputName, ruleExpr = cls._getInput(cell), cls._getRule(cell)

                out = cls._getOutput(cell)
                if out:
                    output.append(out)

                used_inputs.append(inputName)

                if rules[inputName]:
                    rules[inputName].append(ruleExpr)
                else:
                    rules[inputName] = [ruleExpr]

            # rule of missed input is None
            for key in rules.keys():
                if key not in used_inputs:
                    if rules[key]:
                        rules[key].append(None)
                    else:
                        rules[key] = [None]
            used_inputs.clear()
            # или все outputEntries это rvalue, или все outputEntries это boolean вида:
            # inputEntry, inputEntry, ... : true
            # inputEntry, inputEntry, ... : true
            # ...
            # None      , None      , ... : false
            row_input_entries = []
            for key in inputs:
                # get last rule ordered to inputs arg
                row_input_entries.append(rules[key][-1])

            if len(output) == 1:
                # случай с rvalue
                to_return.append(RuleTag(inputEntries=row_input_entries, outputEntry=output[0]))

            elif len(output) == 0:
                # случай с bool, необходимо добавить строку с None и false
                to_return.append(RuleTag(inputEntries=row_input_entries, outputEntry='true'))
                is_none_row_needs = True
            else:
                raise ValueError('Rule must have only 1 output')

        if is_none_row_needs:
            none_row = []
            for _ in inputs:
                # get last rule ordered to inputs arg
                none_row.append(None)
            to_return.append(RuleTag(inputEntries=none_row, outputEntry='false'))
        
        return to_return


class DecisionTable:
    RANDOM_ID_LEN = 7
    OPERATION_RESULT_LABEL = 'operation_result'

    @classmethod
    def newTable(cls, inputs: Iterable, output_name: str, rules_rows: Iterable[RuleTag]):
        decisionTable = cls.decisionTable(cls._constructDecisionTableId())

        # construct input tag branch
        for inputVar in inputs:
            decisionTable.append(
                cls.input(cls._constructInputId(), inputVar).append(
                    # TODO: TypeRef.STRING всегда?
                    cls.inputExpression(cls._constructInputExpressionId(), TypeRef.STRING, inputVar)
                )
            )

        # construct output tag
        # TODO: тип output?
        decisionTable.append(
            cls.output(cls._constructOutputId(), output_name, output_name, TypeRef.STRING)
        )

        # construct rule tag branch
        for rulePack in rules_rows:
            rule = cls.rule(cls._constructRuleId())

            for singleInput in rulePack.inputEntries:
                rule.append(cls.inputEntry(cls._constructInputEntryId(), singleInput))

            rule.append(cls.outputEntry(cls._constructOutputId(), rulePack.outputEntry))
            decisionTable.append(rule)
        return decisionTable

    @classmethod
    def from_expression(cls, expression: str, output_name: str) -> etree.Element:
        inputs = DmnElementsExtracter.getInputs(expression)
        return cls.newTable(
            inputs,
            output_name,
            DmnElementsExtracter.getRulesOrdered(expression, inputs)
        )

    @classmethod
    def from_constraint(cls, operator: int, left_operand, right_operand):
        if operator == JavaELParser.Equal:

            return cls._constructEqual(left_operand, right_operand)

        elif operator == JavaELParser.NotEqual:

            return cls._constructNotEqual(left_operand, right_operand)

        elif operator == JavaELParser.Greater:

            return cls._constructGreater(left_operand, right_operand)

        elif operator == JavaELParser.GreaterEqual:

            return cls._constructGreaterEqual(left_operand, right_operand)

        elif operator == JavaELParser.Less:

            return cls._constructLess(left_operand, right_operand)

        elif operator == JavaELParser.LessEqual:

            return cls._constructLessEqual(left_operand, right_operand)

    @classmethod
    def _constructEqual(cls, left_op: etree.Element, right_op: etree.Element):
        rules = (
            RuleTag(
                inputEntries=('', f'not( {0} )'.format(left_op['id'])),
                outputEntry='false'
            ),
            RuleTag(
                inputEntries=('', ''),
                outputEntry='true'
            )
        )
        return cls.newTable(
            (left_op['id'], right_op['id']),
            cls.OPERATION_RESULT_LABEL,
            rules,
        )

    @classmethod
    def _constructNotEqual(cls, left_op, right_op):
        rules = (
            RuleTag(
                inputEntries=('', f'not( {0} )'.format(left_op['id'])),
                outputEntry='true'
            ),
            RuleTag(
                inputEntries=('', ''),
                outputEntry='false'
            )
        )
        return cls.newTable(
            (left_op['id'], right_op['id']),
            cls.OPERATION_RESULT_LABEL,
            rules,
        )

    @classmethod
    def _constructLess(cls, left_op, right_op):
        rules = (
            RuleTag(
                inputEntries=('', f'< {0}'.format(left_op['id'])),
                outputEntry='true'
            ),
            RuleTag(
                inputEntries=('', ''),
                outputEntry='false'
            )
        )
        return cls.newTable(
            (left_op['id'], right_op['id']),
            cls.OPERATION_RESULT_LABEL,
            rules,
        )

    @classmethod
    def _constructLessEqual(cls, left_op, right_op):
        rules = (
            RuleTag(
                inputEntries=('', f'<= {0}'.format(left_op['id'])),
                outputEntry='true'
            ),
            RuleTag(
                inputEntries=('', ''),
                outputEntry='false'
            )
        )
        return cls.newTable(
            (left_op['id'], right_op['id']),
            cls.OPERATION_RESULT_LABEL,
            rules,
        )

    @classmethod
    def _constructGreater(cls, left_op, right_op):
        rules = (
            RuleTag(
                inputEntries=('', f'< {0}'.format(left_op['id'])),
                outputEntry='false'
            ),
            RuleTag(
                inputEntries=('', ''),
                outputEntry='true'
            )
        )
        return cls.newTable(
            (left_op['id'], right_op['id']),
            cls.OPERATION_RESULT_LABEL,
            rules,
        )

    @classmethod
    def _constructGreaterEqual(cls, left_op, right_op):
        rules = (
            RuleTag(
                inputEntries=('', f'<= {0}'.format(left_op['id'])),
                outputEntry='false'
            ),
            RuleTag(
                inputEntries=('', ''),
                outputEntry='true'
            )
        )
        return cls.newTable(
            (left_op['id'], right_op['id']),
            cls.OPERATION_RESULT_LABEL,
            rules,
        )

    @staticmethod
    def decisionTable(id_attr: str):
        return etree.Element('decisionTable', id=id_attr)

    @staticmethod
    def input(id_attr: str, label_attr: str):
        return etree.Element('input', id=id_attr, label=label_attr)

    @staticmethod
    def inputExpression(id_attr: str, typeRef_attr: TypeRef, text_val: str):
        to_return = None

        if typeRef_attr == TypeRef.STRING:
            to_return = etree.Element('inputExpression', id=id_attr, typeRef='string')
        elif typeRef_attr == TypeRef.INTEGER:
            to_return = etree.Element('inputExpression', id=id_attr, typeRef='integer')

        return to_return.append(DecisionTable.text(text_val))

    @staticmethod
    def output(id_attr: str, label_attr: str, name_attr: str, typeRef_attr: TypeRef):
        if typeRef_attr == TypeRef.STRING:
            return etree.Element('output', id=id_attr, label=label_attr, name=name_attr, typeRef='string')
        elif typeRef_attr == TypeRef.INTEGER:
            return etree.Element('output', id=id_attr, label=label_attr, name=name_attr, typeRef='integer')

    @staticmethod
    def rule(id_attr: str, description_tag_text: str = None):
        to_return = etree.Element('rule', id=id_attr)

        description = etree.Element('description')
        description.text = description_tag_text

        return to_return.append(description)

    @staticmethod
    def text(text_value):
        to_return = etree.Element('text')
        to_return.text = text_value
        return to_return

    @staticmethod
    def inputEntry(id_attr: str, text_val: str):
        return etree.Element('inputEntry', id=id_attr).append(DecisionTable.text(text_val))

    @staticmethod
    def outputEntry(id_attr: str, text_val: str):
        return etree.Element('outputEntry', id=id_attr).append(DecisionTable.text(text_val))

    @staticmethod
    def informationRequirement(id_attr: str):
        return etree.Element('informationRequirement', id=id_attr)

    @staticmethod
    def requiredInput(href_attr: str):
        return etree.Element('requiredInput', href=href_attr)

    @staticmethod
    def requiredDecision(href_attr: str):
        return etree.Element('requiredDecision', href=href_attr)

    @staticmethod
    def authorityRequirement(id_attr: str):
        return etree.Element('authorityRequirement', id=id_attr)

    @staticmethod
    def requiredAuthority(href_attr: str):
        return etree.Element('requiredAuthority', href=href_attr)

    @staticmethod
    def definitions(id_attr: str, name_attr: str):
        pass

    @staticmethod
    def _constructDecisionTableId():
        return 'DecisionTable_' + DecisionTable._constructIdSuffix()

    @staticmethod
    def _constructInputId():
        return 'Input_' + DecisionTable._constructIdSuffix()

    @staticmethod
    def _constructInputExpressionId():
        return 'InputExpression_' + DecisionTable._constructIdSuffix()

    @staticmethod
    def _constructOutputId():
        return 'Output_' + DecisionTable._constructIdSuffix()

    @staticmethod
    def _constructRuleId():
        return 'DecisionRule_' + DecisionTable._constructIdSuffix()

    @staticmethod
    def _constructInputEntryId():
        return 'UnaryTest_' + DecisionTable._constructIdSuffix()

    @staticmethod
    def _constructOutputEntryId():
        return 'LiteralExpression_' + DecisionTable._constructIdSuffix()

    @staticmethod
    def _constructIdSuffix() -> str:
        return ''.join(
            random.choice(string.ascii_uppercase + string.digits)
            for _ in range(DecisionTable.RANDOM_ID_LEN)
        )


def expression_xml(drd_id: str, decisions: List[etree.Element]):
    root = etree.Element('definitions')
    root['xmlns:dmndi'] = dmndi
    root['xmlns'] = xmlns
    root['xmlns:dc'] = dc
    root['xmlns:biodi'] = biodi
    root['xmlns:di'] = di
    root['id'] = drd_id
    root['name'] = 'DRD'
    root['namespace'] = namespace
    root['exporter'] = exporter
    root['exporterVersion'] = exporterVersion
    for d in decisions:
        root.append(d)
    # TODO: добавить inputData
    return root
