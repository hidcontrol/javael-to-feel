# -*- coding: utf-8 -*-

import re
from pyeda.boolalg import expr

# allowed operators and their symbols
OPERATORS = {
    u"¬": "NEG",
    u"&": "AND",
    u"|": "OR",
    u"⇒": "IMP",
    u"⇔": "EQV",
    u"+": "ADD"
}


class Term:
    """A class for representing terms as trees.

    """

    def __init__(self, operands, operator=None):
        """The __init__ method of the `Term` class.
        Args:
                operands (list of (Term or str)): The operands of the term.
                operator (str): The operator ("NEG", "AND", "OR", "IMP", "EQV", or "ADD") connecting the operands.

        """
        self.operands = operands
        self.operator = operator
        if self.operator is None:
            if len(self.operands) > 1:
                raise ValueError("Non-atomic terms must have an operator")
            elif type(self.operands[0]) != str:
                raise ValueError(
                    "Atomic terms must have exactly one string operand")

    def get(self, path):
        """Get the term at a specified position.
        Args:
                path (list of int): Sequence of operands to select.

        Returns:
                Term: The last selected operand.

        """
        t = self
        for p in path:
            t = t.operands[p]
        return t

    def atoms(self, neg=False):
        """Returns the names of the variables in the term.
        Args:
                neg (boolean): Iff true, negated variables are prefixed with "NEG ".

        Returns:
                list of str: List of the variables.

        """
        atms = []
        terms = [self]
        while len(terms) > 0:
            term = terms.pop()
            if term.operator is None:
                atms.append(term.operands[0])
            elif neg and term.operator == "NEG" and term.operands[0].operator is None:
                atms.append("NEG " + term.operands[0].operands[0])
            else:
                terms.extend(term.operands)
        return atms


def find_innermost_brackets(formula):
    """Return the indices of (one of) the innermost bracketed term.
    Args:
            formula (list of str): The formula split at whitespace.

    Returns:
            int: The first index of the first innermost bracketed term.
            int: The last index +1 of the first innermost bracketed term.

    """
    d = 0
    d_max = 0
    i_max = [0, len(formula)-1]
    inside = False
    for i, symb in enumerate(formula):
        if symb == "(":
            d += 1
            if d > d_max:
                d_max = d
                i_max = []
                inside = True
        elif symb == ")":
            d = max(d-1, 0)
            inside = False
        elif inside:
            i_max.append(i)
    return i_max[0], i_max[-1]+1


def parse_formula(formula):
    """Parse a string formula to a term tree.
    Args:
            formula (str): The formula as a usual (in-order) string.

    Returns:
            Term: The formula as a Term object.

    """
    formula = formula.split()
    if len(formula) == 1:
        return Term([formula[0]])
    while len(formula) > 1:
        i1, i2 = find_innermost_brackets(formula)
        b = 1
        if i1 == 0 and i2 == len(formula):
            b = 0
        if i2-i1 == 1:
            if type(formula[i1]) == str:
                formula = formula[:i1-b] + \
                    [Term(formula[i1:i2])] + formula[i2+b:]
            else:
                formula = formula[:i1-b] + formula[i1:i2] + formula[i2+b:]
        elif i2-i1 == 2:
            x = formula[i1:i2][0]
            if x in OPERATORS.keys() and OPERATORS[x] == "NEG":
                x = formula[i1:i2][1]
                if type(x) == str:
                    x = Term([x])
                formula = formula[:i1-b] + [Term([x], "NEG")] + formula[i2+b:]
            else:
                raise ValueError("Invalid formula")
        else:
            operands = []
            operators = set()
            skip_next = False
            for j, x in enumerate(formula[i1:i2]):
                if skip_next:
                    skip_next = False
                    continue
                if x in OPERATORS.keys() and OPERATORS[x] == "NEG":
                    x = formula[i1:i2][j+1]
                    if type(x) == str:
                        x = Term([x])
                    operands.append(Term([x], "NEG"))
                    skip_next = True
                elif x in OPERATORS.keys():
                    operators.add(OPERATORS[x])
                else:
                    if type(x) == str:
                        x = Term([x])
                    operands.append(x)
            if len(operators) > 1:
                raise ValueError("Invalid formula")
            formula = formula[:i1-b] + \
                [Term(operands, list(operators)[0])] + formula[i2+b:]
    return formula[0]


def traverse_preorder(term):
    """Returns a term tree as preorder string.
    Args:
            term (Term): A term object.

    Returns:
            str: The preorder traversal.

    """
    if term.operator is None:
        return term.operands[0]
    order = term.operator + \
        " ( " + " ".join([traverse_preorder(t) for t in term.operands]) + " ) "
    return " ".join(order.strip().split())


def traverse_inorder(term):
    """Returns a term tree as inorder string.
    Args:
            term (Term): A term object.

    Returns:
            str: The inorder traversal.

    """
    if term.operator is None:
        return term.operands[0]
    if len(term.operands) == 1:
        order = " ( " + term.operator + " " + \
            traverse_inorder(term.operands[0]) + " ) "
    else:
        order = " ( " + (" " + term.operator +
                         " ").join([traverse_inorder(t) for t in term.operands]) + " ) "
    return " ".join(order.strip().split())


def traverse_postorder(term):
    """Returns a term tree as postorder string.
    Args:
            term (Term): A term object.

    Returns:
            str: The postorder traversal.

    """
    if term.operator is None:
        return term.operands[0]
    order = " ( " + " ".join([traverse_postorder(t)
                              for t in term.operands]) + " ) " + term.operator
    return " ".join(order.strip().split())


def escape_var_name(var_name):
    """For Pyeda, variable names have to match the expression [a-zA-Z][a-zA-Z0-9_]*.
            This methods escapes special symbols which don't match this expression.

    Args:
            var_name (str): Variable name.

    Returns:
            str: Escaped variable name.

    """
    return var_name.replace("#", "___H___").replace("-", "___D___").replace("+", "___P___").replace(";", "___S___").replace(",", "___C___").replace("[", "___B1___").replace("]", "___B2___")


def unescape_var_name(var_name):
    """Inverse function to `escape_var_name`.

    Args:
            var_name (str): Variable name.

    Returns:
            str: Unescaped variable name.

    """
    return var_name.replace("___H___", "#").replace("___D___", "-").replace("___P___", "+").replace("___S___", ";").replace("___C___", ",").replace("___B1___", "]").replace("___B2___", "]")


def convert_to_pyeda(term):
    """Converts a term object to a PyEDA expression.
    Args:
            term (Term): A term object.

    Returns:
            expr: The corresponding PyEDA expression.

    """
    if term.operator is None:
        return expr.exprvar(escape_var_name(term.operands[0]), None)
    elif term.operator == "NEG":
        return expr.Not(convert_to_pyeda(term.operands[0]), simplify=False)
    elif term.operator == "AND":
        return expr.And(*[convert_to_pyeda(operand) for operand in term.operands], simplify=False)
    elif term.operator == "OR":
        return expr.Or(*[convert_to_pyeda(operand) for operand in term.operands], simplify=False)
    elif term.operator == "IMP":
        return expr.Implies(convert_to_pyeda(term.operands[0]), convert_to_pyeda(term.operands[0]), simplify=False)
    elif term.operator == "EQV":
        return expr.Equal(*[convert_to_pyeda(operand) for operand in term.operands], simplify=False)
    elif term.operator == "ADD":
        return expr.exprvar("___ADD___".join([escape_var_name(operand.operands[0]) for operand in term.operands]), None)


def convert_to_dnf(term):
    """Converts a term into disjunctive normal form (DNF).
    Args:
            term (Term): A term object.

    Returns:
            Term: A term object.

    """
    dnf = str(convert_to_pyeda(term).to_dnf())
    conjuncts = re.findall(r"And\([^\)]+\)", dnf)
    for conjunct in conjuncts:
        dnf = dnf.replace(
            conjunct, "( " + conjunct[4:-1].replace(", ", " & ") + " )")
    if dnf.startswith("Or("):
        dnf = dnf[3:-1].replace(", ", " | ")
    dnf = " ".join(
        [("( " + x.replace("~", "¬ ") + " )" if "~" in x else x) for x in dnf.split()])
    dnf = " ".join([("( " + x.replace("___ADD___", " + ") +
                     " )" if "___ADD___" in x else x) for x in dnf.split()])
    dnf = unescape_var_name(dnf)
    return parse_formula(dnf)


def find_imps(term, path=[]):
    """Finds all implications (and equivalences) in a term.
    Args:
            term (Term): The term to find implications in.

    Returns:
            list of (list of int): List of paths to the implications.
    """
    imps = []
    if term.operator is None:
        return imps
    if term.operator in ["IMP", "EQV"]:
        imps.append(path)
    for i, operand in enumerate(term.operands):
        imps.extend(find_imps(operand, path + [i]))
    return imps


def convert_to_dnf_with_imps(term):
    """Converts a term into disjunctive normal form (DNF), but keeps implications (and equivalences).
    Args:
            term (Term): A term object.

    Returns:
            Term: A term object.

    """
    imps = sorted(find_imps(term), key=lambda x: len(x), reverse=True)
    imp_terms = []
    for i, imp in enumerate(imps):
        imp = term.get(imp)
        imp_terms.append([convert_to_dnf(operand) for operand in imp.operands])
        imp.operands = ["t_"+str(i)+"_"+imp.operator]
        imp.operator = None
    ts = [term]
    while len(ts) > 0:
        t = ts.pop(0)
        if t.operator is None:
            v = t.operands[0].split("_")
            if len(v) == 3 and v[0] == "t":
                t.operator = v[2]
                t.operands = imp_terms[int(v[1])]
        if t.operator is not None:
            ts.extend(t.operands)
    return term


if __name__ == "__main__":
    # test case
    # formula = "( A | ( ¬ ( B & ( E + F + G ) ) ) | E ) & C & D"
    # formula = "A | ¬ B | C | ( D & E & ( ¬ F & G | ¬ H & J ) )"
    formula = "( D & E & ( ¬ F & G | ¬ H & J ) )"
    term = parse_formula(formula)
    print(formula)
    print(traverse_inorder(convert_to_dnf(term)))
