import unittest
from src.translator.translate import translate, xml_from_dmntree
from lxml import etree

XML_TEST_OUT_PATH = 'res/out/test_xml_out'
XSD_PATH = 'res/xsd/dmn.xsd'


class TestIntegration(unittest.TestCase):
    def setUp(self) -> None:
        self.java_el_expressions = [
            # "!empty second",
            "fields['SignFL'] eq true or fields['SignUL'] eq true"
        ]
        # self.xmlschema = etree.XMLSchema(etree.parse(XSD_PATH))

    def test_integration(self):
        for expr in self.java_el_expressions:
            dmn_tree = translate(expr)
            xml_from_dmntree(dmn_tree, XML_TEST_OUT_PATH)
            # self.assertTrue(self.xmlschema.validate(etree.parse(XML_TEST_OUT_PATH)))


if __name__ == '__main__':
    unittest.main()
