import unittest

from src.translator.knf_converter import toDMNReady
from src.translator.treeFormula import tree, DMNTree, zipFormula, FormulaZipper, SimpleOperandMarker, unpack, concatWithOr
from src.translator.treeFormula import treeHeight, ToFEELConverter, printDMNTree

simple_operand = "value.property"
simplify_with_ternary = "fields.ApplicantType.value.fields.Code eq 'UL' ? 'Юридический адрес' : 'Адрес места регистрации'"
simple_operand_or = "fields['SignFL'] eq true or fields['SignUL'] eq true"
sub_dmn_equality = "(first and second) == third"
sub_dmn_empty = "empty (first and second)"
sub_dmn_not_empty = "! empty (first and second)"
sub_dmn_complex = "fields.p_ContractTransferType.Code eq '7185643' and !empty fields.ScanNotificationLetterSO"
translate_with_ternary = "a ? b : c"
translate_with_equality = "(a == b) and (c ne d)"
translate_with_complex_value = "value.property == 12"
translate_with_empty = "empty (some_big_expression)"
translate_with_not = "! (a and b)"
translate_with_complex_unary = "not empty (a and b or c)"
translate_complex = "view.viewId.contains('portal.xhtml') and value.contains(fields.ApplicantType.Code) and !empty fields.wiringDiagram and fields.p_ContractTransferType.Code eq '7185643' and (!empty fields.id or (dataObjectController.instance.objectStatus.status.code eq 'ta03_Paused' and fields.SendDate))"
translate_complex_ternary = "value.property ? (first_var and second_var or ! third_var) : 'xexe'"


simple_operand_tree_h = 11


class TestTreeTraverses(unittest.TestCase):
    def test_height(self):
        t = tree(simple_operand)
        self.assertEqual(simple_operand_tree_h, treeHeight(t))

    def assertTranslation(self, java_el, feel):
        t = tree(java_el)
        converter = ToFEELConverter()
        converter.visit(t)
        self.assertEqual(feel, converter.result)

    def test_find_sub_dmn_equality(self):
        t = tree(sub_dmn_equality)
        dmntree = DMNTree(t)
        self.assertEqual(1, len(dmntree.root.children))
        self.assertEqual('(firstandsecond)', dmntree.root.children[0].expression)
        self.assertEqual('==', dmntree.root.children[0].operator.getText())

    def test_find_sub_dmn_empty(self):
        t = tree(sub_dmn_empty)
        dmntree = DMNTree(t)
        self.assertEqual(1, len(dmntree.root.children))
        self.assertEqual('(firstandsecond)', dmntree.root.children[0].expression)
        self.assertEqual('empty', dmntree.root.children[0].operator.getText())

    def test_find_sub_dmn_empty(self):
        t = tree(sub_dmn_not_empty)
        dmntree = DMNTree(t)

        printDMNTree(dmntree)

        self.assertEqual(1, len(dmntree.root.children))

        self.assertEqual('!empty(firstandsecond)', dmntree.root.children[0].expression)
        self.assertEqual('!', dmntree.root.children[0].operator.getText())

        self.assertEqual('(firstandsecond)', dmntree.root.children[0].children[0].expression)
        self.assertEqual('empty', dmntree.root.children[0].children[0].operator.getText())

    def test_find_sub_dmn_complex(self):
        t = tree(sub_dmn_complex)
        dmntree = DMNTree(t)
        printDMNTree(dmntree)

    def test_translate_ternary(self):
        self.assertTranslation(translate_with_ternary, 'if a then b else c')

    def test_translate_equality(self):
        self.assertTranslation(translate_with_equality, '( a b ) and ( c not( d ) )')

    def test_translate_complex_value(self):
        self.assertTranslation(translate_with_complex_value, 'value.property 12')

    def test_translate_empty(self):
        self.assertTranslation(translate_with_empty, '( some_big_expression ) null')

    def test_translate_not(self):
        self.assertTranslation(translate_with_not, 'not( ( a and b ) )')

    def test_translate_not(self):
        self.assertTranslation(translate_with_complex_unary, 'not( ( a and b or c ) null )')

    def test_translate_complex(self):
        self.assertTranslation(translate_complex, "view.viewId.contains('portal.xhtml') and value.contains(fields.ApplicantType.Code) and not( fields.wiringDiagram and fields.p_ContractTransferType.Code '7185643' and ( not( fields.id or ( dataObjectController.instance.objectStatus.status.code 'ta03_Paused' and fields.SendDate ) null ) ) null )")

    def test_complex_ternary(self):
        self.assertTranslation(translate_complex_ternary, "if value.property then ( first_var and second_var or not( third_var ) ) else 'xexe'")

    def test_simplify(self):
        prepared = zipFormula(tree(simplify_with_ternary)).expression
        prepared = toDMNReady(prepared)
        prepared = unpack(concatWithOr(prepared))
        prepared = prepared.replace(' ', '')
        self.assertTrue(
            prepared in [
            '((fields.ApplicantType.value.fields.Codeeq\"UL\")and\"Юридическийадрес\")or(!(fields.ApplicantType.value.fields.Codeeq\"UL\")and\"Адресместарегистрации\")',
            '(!(fields.ApplicantType.value.fields.Codeeq\"UL\")and\"Адресместарегистрации\")or((fields.ApplicantType.value.fields.Codeeq\"UL\")and\"Юридическийадрес\")',
            '(!(fields.ApplicantType.value.fields.Codeeq"UL")and"Адресместарегистрации")or((fields.ApplicantType.value.fields.Codeeq"UL")and"Юридическийадрес")'
                ]
            , "Unpack has error"
        )

    def testZipper(self):
        t = tree(simplify_with_ternary)
        SimpleOperandMarker().visit(t)
        zipper = FormulaZipper()
        zipper.visit(t)
        self.assertEqual(8, len(zipper.result.split(' ')))

    def test_or(self):
        prepared = zipFormula(tree(simple_operand_or)).expression
        prepared = toDMNReady(prepared)
        prepared = unpack(concatWithOr(prepared))
        self.assertTrue(
            prepared in [
                "( fields [ 'SignUL' ] eq true) or ( fields [ 'SignFL' ] eq true)",
                "( fields [ 'SignFL' ] eq true) or ( fields [ 'SignUL' ] eq true)"
            ],
            "Unpack broken"
        )

if __name__ == '__main__':
    unittest.main()
