import re


class JavaELExpressionParser:
    def __init__(self, expression):
        self._prepared_dmn = expression
        self._expression = expression  # copy here?
        self._operands = None

    def _extract_vars(self):
        # only variables and binary operators needed
        prepared = self._expression.replace('(', '')
        prepared = prepared.replace(')', '')
        prepared = prepared.replace('!', '')
        prepared = prepared.replace('empty', '')

        operands = set(re.split(r"(?:\sand\s|\sor\s)", prepared))
        for op in operands:
            op = op.replace('fields.', '')
            op = op.strip()

    def _prepare_for_pyeda(self):
        # Форматируем выражение: добавляем отступы, заменяем операнды на совместимые с билиотекой EDA
        self._prepared_dmn = self._prepared_dmn.replace('!', ' ~ ')
        self._prepared_dmn = self._prepared_dmn.replace(' not ', ' ~ ')
        self._prepared_dmn = self._prepared_dmn.replace(' and ', ' & ')
        self._prepared_dmn = self._prepared_dmn.replace(')and', ') & ')
        self._prepared_dmn = self._prepared_dmn.replace('and(', '& (')
        self._prepared_dmn = self._prepared_dmn.replace('&&', ' & ')
        self._prepared_dmn = self._prepared_dmn.replace(' or ', ' | ')
        self._prepared_dmn = self._prepared_dmn.replace(')or', ') | ')
        self._prepared_dmn = self._prepared_dmn.replace('or(', '| (')
        self._prepared_dmn = self._prepared_dmn.replace('||', ' | ')
        self._prepared_dmn = self._prepared_dmn.replace(' eq ', '_eq_')
        self._prepared_dmn = self._prepared_dmn.replace(' empty ', ' empty_')
        self._prepared_dmn = re.sub(r"^empty ", "empty_", self._prepared_dmn)
        self._prepared_dmn = self._prepared_dmn.replace('\'', '')
        self._prepared_dmn = self._prepared_dmn.replace('[', '_')
        self._prepared_dmn = self._prepared_dmn.replace(']', '_')
        self._prepared_dmn = self._prepared_dmn.replace('.', '_')
        self._prepared_dmn = re.sub(' +', ' ', self._prepared_dmn)  # Замена нескольких пробелов одним
        self._prepared_dmn = re.sub(r"([^\s\)]+)\((.+?)\)(?=[^()]*(\(|$))", r"\1_\2_", self._prepared_dmn)
        self._prepared_dmn = self._prepared_dmn.replace('(', ' ( ')
        self._prepared_dmn = self._prepared_dmn.replace(')', ' ) ')
        self._prepared_dmn = self._prepared_dmn.replace('_ ', ' ')
        self._prepared_dmn = self._prepared_dmn.replace(' _', ' ')

    def _split_pyeda_operands(self):
        operands = set(re.split(r"(?:\s\&\s|\s\|\s)", self._prepared_dmn))  # Разделение на операнды
        for op in operands:
            op = op.replace('(', '').replace(')', '').strip()

    def prepare_to_dmn(self):
        self._prepare_for_pyeda()
        self._split_pyeda_operands()
        return self._prepared_dmn
