import string
import random
import re
from lxml import etree
from enum import Enum
from collections import namedtuple
from src.translator.toKNF import toDMNReady
from typing import Dict, Iterable, Set, List, Collection
from loguru import logger
from src.translator.feel_analizer import tree, FEELInputExtractor, FEELRuleExtractor
from ANTLR_JavaELParser.JavaELParser import JavaELParser

xmlns = 'https://www.omg.org/spec/DMN/20191111/MODEL/'
dmndi = 'https://www.omg.org/spec/DMN/20191111/DMNDI/'
biodi = 'http://bpmn.io/schema/dmn/biodi/2.0'
dc = 'http://www.omg.org/spec/DMN/20180521/DC/'
di = 'http://www.omg.org/spec/DMN/20180521/DI/'
namespace = 'http://camunda.org/schema/1.0/dmn'
exporter = 'Camunda Modeler'
exporterVersion = '4.9.0'


RuleTag = namedtuple('RuleTag', ('inputEntries', 'outputEntry'))

logger = logger.opt(colors=True)


class TypeRef(Enum):
    STRING = 1,
    INTEGER = 2


class DmnElementsExtracter:
    AND_OPERANDS_RE = re.compile(r'^and\((.*)\)$')
    WITH_BOOLEAN_METHOD = re.compile(r'^(.+?)\..+?\(\)$')

    @classmethod
    def _getInput(cls, expr: str):
        """
        Suggesting that only one identifier in expression
        :param expr:
        :return:
        """
        feel_expr_tree = tree(expr)
        extractor = FEELInputExtractor()
        extractor.visit(feel_expr_tree)
        if len(extractor.result) > 1:
            raise ValueError(f"Expected only one input in {expr}")

        return extractor.result.pop()

    @classmethod
    def _getOutput(cls, expr: str):
        tokens = expr.split()
        if len(tokens) == 1 and cls.WITH_BOOLEAN_METHOD.findall(tokens[0]) is None:
            return tokens[0]

    @staticmethod
    def _getRule(expr: str):
        """
        operand op value -> op value
        operand.field op value -> op value
        operand.field[] op value-> operand.field[] op value
        operand[val] = null -> operand[val] = null

        :param expr: FEEL expression without logical
        :return:
        """
        expr_tree = tree(expr)
        rule_extr = FEELRuleExtractor()
        rule_extr.visit(expr_tree)
        return rule_extr.result

    @classmethod
    def _split_by_or_by_and(cls, operands_FEEL: str) -> List[List[str]]:
        """
        (... and ... and ...) or (... and ... and ...) -> [ [and operands]]
        :param operands_FEEL: {'... and ...',..}
        :return: [[operands], ..]
        """
        or_splited = []
        for or_ops in operands_FEEL.split('or'):
            and_ops = or_ops.split('and')
            and_splited = []
            for e in and_ops:
                e = e.replace('empty_', 'empty ').replace('_null', ' null').strip()
                and_splited.append(e)
            or_splited.append(and_splited)
        return or_splited

    @classmethod
    def getInputs(cls, expr: str) -> Set[str]:  # lvalue во всех операндах or
        """
        operands can be 'lvalue op rvalue' or 'input.boolean_function'
        inputs are lvalue or input without boolean_function
        :param expr: simple dmn expression
        :return: Set[str]
        """
        feel_expr_tree = tree(expr)
        extractor = FEELInputExtractor()
        extractor.visit(feel_expr_tree)
        return extractor.result

    @classmethod
    def getRulesOrdered(cls, expr: str, inputs) -> Iterable[RuleTag]:  # rvalue c оператором
        """
        :param inputs: order of rules
        :param expr:
        :return:
        """
        rules = dict().fromkeys(inputs)
        used_inputs = []
        to_return = []
        is_none_row_needs = False

        # TODO: remove _prepare()
        for row in cls._split_by_or_by_and(expr):
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
    def newTable(cls, inputs: Collection, output_name: str, rules_rows: Iterable[RuleTag], dependentDMNs: List[str]):
        decision_tag = cls.decision(cls._constructDecisionId(), 'test_name')

        for dependence in dependentDMNs:
            # TODO: add href to inforeq
            info_requirement_tag = cls.informationRequirement(cls._constructInformationRequirementId())
            req_input_tag = cls.requiredInput(dependence)

            info_requirement_tag.append(req_input_tag)

            decision_tag.append(info_requirement_tag)

        decisionTable = cls.decisionTable(cls._constructDecisionTableId())

        decision_tag.append(decisionTable)

        # construct input tag branch
        for inputVar in inputs:

            input_tag = cls.input(cls._constructInputId(), inputVar)
            # TODO: TypeRef.STRING всегда?
            input_tag.append(cls.inputExpression(cls._constructInputExpressionId(), TypeRef.STRING, inputVar))

            decisionTable.append(
                input_tag
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
        return decision_tag

    @classmethod
    def from_expression(cls, expression: str, output_name: str, dependentDMNs: List[str]) -> etree.Element:
        inputs = DmnElementsExtracter.getInputs(expression)
        return cls.newTable(
                inputs,
                output_name,
            DmnElementsExtracter.getRulesOrdered(expression, inputs),
                dependentDMNs
            )

    @classmethod
    def from_constraint(cls, operator: int, dependentDMNs: List[str], left_operand, right_operand=None):

        if operator == JavaELParser.Equal:

            return cls._constructEqual(left_operand, right_operand, dependentDMNs)

        elif operator == JavaELParser.NotEqual:

            return cls._constructNotEqual(left_operand, right_operand, dependentDMNs)

        elif operator == JavaELParser.Greater:

            return cls._constructGreater(left_operand, right_operand, dependentDMNs)

        elif operator == JavaELParser.GreaterEqual:

            return cls._constructGreaterEqual(left_operand, right_operand, dependentDMNs)

        elif operator == JavaELParser.Less:

            return cls._constructLess(left_operand, right_operand, dependentDMNs)

        elif operator == JavaELParser.LessEqual:

            return cls._constructLessEqual(left_operand, right_operand, dependentDMNs)

        elif operator == JavaELParser.Not:

            return cls._constructNot(left_operand, dependentDMNs)

        elif operator == JavaELParser.Empty:

            return cls._constructEmpty(left_operand, dependentDMNs)

    @classmethod
    def _constructEqual(cls, left_op: etree.Element, right_op: etree.Element, dependentDMNs: List[str]):

        logger.debug(f'creating <green>equal</green> xml tree left_op: <red>{left_op}</red>, right_op: <red>{right_op}</red>')

        rules = (
            RuleTag(
                inputEntries=('', f'not( {0} )'.format(left_op.get('id'))),
                outputEntry='false'
            ),
            RuleTag(
                inputEntries=('', ''),
                outputEntry='true'
            )
        )
        return cls.newTable(
            (left_op.get('id'), right_op.get('id')),
            cls.OPERATION_RESULT_LABEL,
            rules,
            dependentDMNs
        )

    @classmethod
    def _constructNotEqual(cls, left_op, right_op, dependentDMNs: List[str]):

        logger.debug(f'creating <green>not equal</green> xml tree left_op: <red>{left_op}</red>, right_op: <red>{right_op}</red>')

        rules = (
            RuleTag(
                inputEntries=('', f'not( {0} )'.format(left_op.get('id'))),
                outputEntry='true'
            ),
            RuleTag(
                inputEntries=('', ''),
                outputEntry='false'
            )
        )
        return cls.newTable(
            (left_op.get('id'), right_op.get('id')),
            cls.OPERATION_RESULT_LABEL,
            rules,
            dependentDMNs
        )

    @classmethod
    def _constructLess(cls, left_op, right_op, dependentDMNs: List[str]):

        logger.debug(
            f'creating <green>less</green> xml tree left_op: <red>{left_op}</red>, right_op: <red>{right_op}</red>')

        rules = (
            RuleTag(
                inputEntries=('', f'< {0}'.format(left_op.get('id'))),
                outputEntry='true'
            ),
            RuleTag(
                inputEntries=('', ''),
                outputEntry='false'
            )
        )
        return cls.newTable(
            (left_op.get('id'), right_op.get('id')),
            cls.OPERATION_RESULT_LABEL,
            rules,
            dependentDMNs
        )

    @classmethod
    def _constructLessEqual(cls, left_op, right_op, dependentDMNs: List[str]):

        logger.debug(
            f'creating <green>less equal</green> xml tree left_op: <red>{left_op}</red>, right_op: <red>{right_op}</red>')

        rules = (
            RuleTag(
                inputEntries=('', f'<= {0}'.format(left_op.get('id'))),
                outputEntry='true'
            ),
            RuleTag(
                inputEntries=('', ''),
                outputEntry='false'
            )
        )
        return cls.newTable(
            (left_op.get('id'), right_op.get('id')),
            cls.OPERATION_RESULT_LABEL,
            rules,
            dependentDMNs
        )

    @classmethod
    def _constructGreater(cls, left_op, right_op, dependentDMNs: List[str]):

        logger.debug(
            f'creating <green>greater</green> xml tree left_op: <red>{left_op}</red>, right_op: <red>{right_op}</red>')

        rules = (
            RuleTag(
                inputEntries=('', f'< {0}'.format(left_op.get('id'))),
                outputEntry='false'
            ),
            RuleTag(
                inputEntries=('', ''),
                outputEntry='true'
            )
        )
        return cls.newTable(
            (left_op.get('id'), right_op.get('id')),
            cls.OPERATION_RESULT_LABEL,
            rules,
            dependentDMNs
        )

    @classmethod
    def _constructGreaterEqual(cls, left_op, right_op, dependentDMNs: List[str]):

        logger.debug(f'creating <green>greater equal</green> xml tree left_op: <red>{left_op}</red>, right_op: <red>{right_op}</red>')

        rules = (
            RuleTag(
                inputEntries=('', f'<= {0}'.format(left_op.get('id'))),
                outputEntry='false'
            ),
            RuleTag(
                inputEntries=('', ''),
                outputEntry='true'
            )
        )
        return cls.newTable(
            (left_op.get('id'), right_op.get('id')),
            cls.OPERATION_RESULT_LABEL,
            rules,
            dependentDMNs
        )

    @classmethod
    def _constructNot(cls, op, dependentDMNs: List[str]):

        logger.debug(
            f'creating <green>not</green> xml tree op: <red>{op}</red>')

        rules = (
            RuleTag(
                inputEntries=(f"{op.get('id')}", 'true'),
                outputEntry='false'
            ),
            RuleTag(
                inputEntries=('', ''),
                outputEntry='true'
            )
        )
        return cls.newTable(
            [op.get('id')],
            cls.OPERATION_RESULT_LABEL,
            rules,
            dependentDMNs
        )

    @classmethod
    def _constructEmpty(cls, op, dependentDMNs: List[str]):

        logger.debug(
            f'creating <green>empty</green> xml tree op: <red>{op}</red>')

        rules = (
            RuleTag(
                inputEntries=(f"{op.get('id')}", 'null'),
                outputEntry='true'
            ),
            RuleTag(
                inputEntries=('', ''),
                outputEntry='false'
            )
        )
        return cls.newTable(
            (op.get('id')),
            cls.OPERATION_RESULT_LABEL,
            rules,
            dependentDMNs
        )

    @classmethod
    def decision(cls, id_attr: str, name_attr: str):
        return etree.Element('decision', id=id_attr, name=name_attr)

    @staticmethod
    def decisionTable(id_attr: str):
        logger.debug(
            f'new <green>decisionTable</green> xml tag, id: <red>{id_attr}</red>')

        return etree.Element('decisionTable', id=id_attr)

    @staticmethod
    def input(id_attr: str, label_attr: str):
        logger.debug(
            f'new <green>input</green> xml tag, id: <red>{id_attr}</red>, label: <red>{label_attr}</red>')

        if not label_attr:
            label_attr = ''

        return etree.Element('input', id=id_attr, label=label_attr)

    @staticmethod
    def inputExpression(id_attr: str, typeRef_attr: TypeRef, text_val: str):

        logger.debug(
            f'new <green>inputExpression</green> xml tag, id: <red>{id_attr}</red>, typeRef: <red>{typeRef_attr}</red>, text: <red>{text_val}</red>')

        to_return = None

        if typeRef_attr == TypeRef.STRING:
            to_return = etree.Element('inputExpression', id=id_attr, typeRef='string')
        elif typeRef_attr == TypeRef.INTEGER:
            to_return = etree.Element('inputExpression', id=id_attr, typeRef='integer')

        to_return.append(DecisionTable.text(text_val))
        return to_return

    @staticmethod
    def output(id_attr: str, label_attr: str, name_attr: str, typeRef_attr: TypeRef):

        logger.debug(
            f'new <green>output</green> xml tag, id: <red>{id_attr}</red>, typeRef: <red>{typeRef_attr}</red>, label: <red>{label_attr}</red>, name: <red>{name_attr}</red>')

        if typeRef_attr == TypeRef.STRING:
            return etree.Element('output', id=id_attr, label=label_attr, name=name_attr, typeRef='string')
        elif typeRef_attr == TypeRef.INTEGER:
            return etree.Element('output', id=id_attr, label=label_attr, name=name_attr, typeRef='integer')

    @staticmethod
    def rule(id_attr: str, description_tag_text: str = None):

        logger.debug(
            f'new <green>rule</green> xml tag, id: <red>{id_attr}</red>, description: <red>{description_tag_text}</red>')

        to_return = etree.Element('rule', id=id_attr)

        description = etree.Element('description')
        description.text = description_tag_text

        to_return.append(description)
        return to_return

    @staticmethod
    def text(text_value):

        to_return = etree.Element('text')
        to_return.text = text_value
        return to_return

    @staticmethod
    def inputEntry(id_attr: str, text_val: str):
        logger.debug(
            f'new <green>inputEntry</green> xml tag, id: <red>{id_attr}</red>, text: <red>{text_val}</red>')

        if not text_val:
            text_val = ''

        to_return = etree.Element('inputEntry', id=id_attr)
        to_return.append(DecisionTable.text(text_val))
        return to_return

    @staticmethod
    def outputEntry(id_attr: str, text_val: str):

        if not text_val:
            text_val = ''

        logger.debug(
            f'new <green>outputEntry</green> xml tag, id: <red>{id_attr}</red>, text: <red>{text_val}</red>')

        to_return = etree.Element('outputEntry', id=id_attr)
        to_return.append(DecisionTable.text(text_val))
        return to_return

    @staticmethod
    def informationRequirement(id_attr: str):
        logger.debug(
            f'new <green>informationRequirement</green> xml tag, id: <red>{id_attr}</red>')

        return etree.Element('informationRequirement', id=id_attr)

    @staticmethod
    def requiredInput(href_attr: str):
        logger.debug(
            f'new <green>requiredInput</green> xml tag, href: <red>{href_attr}</red>')

        return etree.Element('requiredInput', href=href_attr)

    @staticmethod
    def requiredDecision(href_attr: str):
        logger.debug(
            f'new <green>requiredDecision</green> xml tag, href: <red>{href_attr}</red>')

        return etree.Element('requiredDecision', href=href_attr)

    @staticmethod
    def authorityRequirement(id_attr: str):
        logger.debug(
            f'new <green>authorityRequirement</green> xml tag, id: <red>{id_attr}</red>')

        return etree.Element('authorityRequirement', id=id_attr)

    @staticmethod
    def requiredAuthority(href_attr: str):
        logger.debug(
            f'new <green>requiredAuthority</green> xml tag, href: <red>{href_attr}</red>')

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

    @staticmethod
    def _constructDecisionId() -> str:
        return 'Decision_' + DecisionTable._constructIdSuffix()

    @staticmethod
    def _constructInformationRequirementId() -> str:
        return 'InformationRequirement_' + DecisionTable._constructIdSuffix()


def expression_xml(drd_id: str, decisions: List[etree.Element]):
    NSMAP = {'dmndi': dmndi, 'dc': dc, 'biodi': biodi, 'di': di, }
    root = etree.Element('definitions', xmlns=xmlns, nsmap=NSMAP)
    attributes = root.attrib
    attributes['name'] = 'DRD'
    attributes['namespace'] = namespace
    attributes['exporter'] = exporter
    attributes['exporterVersion'] = exporterVersion
    for d in decisions:
        root.append(d)
    # TODO: добавить inputData
    return root
