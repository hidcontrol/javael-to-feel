from unittest import TestCase
from src.buildPropDependency import extract_props_from_expression


class TestExtractJavaELDependents(TestCase):
    def setUp(self) -> None:
        self.test_expression = ''

    def tearDown(self) -> None:
        self.test_expression = ''

    def test_rvalue_with_attribute(self):
        self.test_expression = "securityDataProvider.hasRole('tehprisEE_portalUserRegistrator')"
        self.assertEqual({'securityDataProvider'}, extract_props_from_expression(self.test_expression))

    def test_lvalue_fields_test_attribute(self):
        self.test_expression = "fields.ApplicantType.value.fields.Code"
        self.assertEqual({'ApplicantType'}, extract_props_from_expression(self.test_expression))

    def test_rvalue_no_property(self):
        self.test_expression = "'tehprisEE_portalUserRegistrator'"
        self.assertEqual(set(), extract_props_from_expression(self.test_expression))

        self.test_expression = "'СНИЛС'"
        self.assertEqual(set(), extract_props_from_expression(self.test_expression))

        self.test_expression = "true"
        self.assertEqual(set(), extract_props_from_expression(self.test_expression))

        self.test_expression = "false"
        self.assertEqual(set(), extract_props_from_expression(self.test_expression))

        self.test_expression = "'tehprisEE_Zayavki_view'"
        self.assertEqual(set(), extract_props_from_expression(self.test_expression))

