from typing import Dict, Set

from src.dependencyTable.checkBrackets import *
import re
from pyeda.boolalg import expr

# strn = "word hereword word, there word"
# search = "word"
# print(re.findall(r"\b" + search + r"\b", strn))

# result = re.sub(r"\s+"," ", text, flags = re.I) # Удаление несколькиз пробелов
# result = re.sub(r"^\s+", "", text) # Удаление пробелов сначал и с конца
# result = re.sub(r"\s+[a-zA-Z]\s+", " ", text) # Удаление остатков спецсимволов
# result = re.split(r"\s+", text) # Разделение строки на элементы
dirty_operands_01 = []


def toDMNReady(el: str) -> Set[str]:
    if check_brackets(el):
        # Форматируем выражение: добавляем отступы, заменяем операнды на совместимые с билиотекой EDA
        el = el.replace('!', ' ~ ')
        el = el.replace(' not ', ' ~ ')
        el = el.replace(' and ', ' & ')
        el = el.replace(')and', ') & ')
        el = el.replace('and(', '& (')
        el = el.replace('&&', ' & ')
        el = el.replace(' or ', ' | ')
        el = el.replace(')or', ') | ')
        el = el.replace('or(', '| (')
        el = el.replace('||', ' | ')
        el = el.replace(' eq ', '_eq_')
        el = el.replace(' == ', '_eq_')
        el = el.replace(' empty ', ' empty_')
        # null склеить с операндом
        el = el.replace(' null', '_null')
        el = re.sub(r"^empty ", "empty_", el)
        el = el.replace('\'', '')
        el = el.replace('[', '_')
        el = el.replace(']', '_')
        el = el.replace('.', '_')
        el = re.sub(' +', ' ', el)  # Замена нескольких пробелов одним
        # el = el.replace('(', ' ( ')
        # el = el.replace(')', ' ) ')
        el = el.replace('_ ', ' ')
        el = el.replace(' _', ' ')
        el = re.sub(r"([^\s\)]+)\((.+?)\)(?=[^()]*(\(|$))", r"\1_\2_", el)
        # print("\r\n------------------------------------------------------")
        # print("................................................[ OK ] \rПодготовка формулы")
        # print(el)
        #
        dirty_operands_01 = re.split(r"(?:\s\&\s|\s\|\s)", el)  # Разделение на операнды
        dirty_operands_02 = set(dirty_operands_01)
        dirty_operands_03 = set()
        for op in dirty_operands_02:
            dirty_operands_03.add(op.replace('(', '').replace(')', '').strip())

        # print("\r\n------------------------------------------------------")
        # print("................................................[ OK ] \rЭлементы формулы")
        # print("Всего . . : {}",format(dirty_operands_01.__len__()))
        # print("Уникальных: {}",format(dirty_operands_03.__len__()))
        # print("----------------------")
        #
        formula = el  # .replace(" eq '", '_eq_').replace("'", '').replace("empty ", "empty_").replace(".", "_")
        # print(*dirty_operands_03, sep = "\n")
        formulaDnf = expr.expr(formula).to_dnf()
        # print("\r\n------------------------------------------------------")
        # print("................................................[ OK ] \rПриведение к ДНФ")
        # print(formulaDnf)
        #
        x = re.findall(r"And\([^\)]+\)", str(formulaDnf))  # <===
        t = re.sub(r"And\([^\)]+\)", "", str(formulaDnf))
        t = t.replace(' ,', '')
        m = re.split(r"(?:Or\(|\,)", t)  # <===
        dmn_01 = x+m
        dmn_02 = set()
        for op in dmn_01:
            if len(op.strip()) > 1:
                op = re.sub(r"^And\(", '', op)
                op = re.sub(r"\)$", '', op)
                op = re.sub(r",", ' and ', op)
                dmn_02.add(op.strip())

        return dmn_02

        # print("\r\n------------------------------------------------------")
        # print("................................................[ OK ] \rПриведение к DMN")
        # print(*dmn_02, sep="\n")
        # return 'Or(' + ', '.join(dmn_02) + ')'

    else:
        raise ValueError("Invalid brackets")
