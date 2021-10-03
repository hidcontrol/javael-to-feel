from src.translator.translate import translate, xml_from_dmntree

EXPRESSION_EXAMPLE = ''
XML_TEST_OUT_PATH = '/out/xml_example_out.xml'


if __name__ == '__main__':
    feel_dmn_tree = translate(EXPRESSION_EXAMPLE)
    xml_from_dmntree(feel_dmn_tree, XML_TEST_OUT_PATH)
