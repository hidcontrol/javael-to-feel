import unittest
from src.translator.feel_analizer import tree, FEELInputExtractor, FEELRuleExtractor

feel_expr = 'x.call() and y > 5'
rule_extr_binary = 'field.property = null'
rule_extr_function = 'field.function()'
input_braked = 'field["property"]'


class TestFeel(unittest.TestCase):
    def testExtractInputs(self):
        feel_tree = tree(feel_expr)
        self.assertIsNotNone(feel_tree, 'FEEL tree has not created')
        extractor = FEELInputExtractor()
        extractor.visit(feel_tree)
        self.assertTrue(len(extractor.result) > 0, 'FEELInputExtractor found nothing')
        self.assertTrue('x' in extractor.result and 'y' in extractor.result and len(extractor.result) == 2, 'Wrong name found')

    def testRuleExtractor(self):
        feel_tree = tree(rule_extr_binary)
        self.assertIsNotNone(feel_tree, 'FEEL tree has not created')
        extractor = FEELRuleExtractor()
        extractor.visit(feel_tree)
        self.assertEqual(extractor.result, '= null')

        feel_tree = tree(rule_extr_function)
        self.assertIsNotNone(feel_tree, 'FEEL tree has not created')
        extractor = FEELRuleExtractor()
        extractor.visit(feel_tree)
        self.assertEqual(extractor.result, rule_extr_function)

    def testExtractInputBraced(self):
        feel_tree = tree(input_braked)
        self.assertIsNotNone(feel_tree, 'FEEL tree has not created')
        extractor = FEELInputExtractor()
        extractor.visit(feel_tree)
        self.assertTrue(len(extractor.result) > 0, 'FEELInputExtractor found nothing')
        self.assertEqual("field [ \"property\" ]", extractor.result.pop())

if __name__ == '__main__':
    unittest.main()
