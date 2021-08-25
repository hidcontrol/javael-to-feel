import unittest
from src.JavaEL_tokenize import JavaELTokenType, JavaELToken, tokenize_expression


class TestTokenize(unittest.TestCase):
    def test_lvalue(self):
        tokens = tokenize_expression('securityDataProvider.loggedInUser')
        self.assertEqual(tokens[0].token_value, 'securityDataProvider.loggedInUser')
        self.assertEqual(tokens[0].token_type, JavaELTokenType.LVALUE)

        tokens = None

        tokens = tokenize_expression('fields.ApplicantType.Code')
        self.assertEqual(tokens[0].token_value, 'fields.ApplicantType.Code')

    def test_rvalue(self):
        tokens = tokenize_expression("\'1234\'")
        self.assertEqual(tokens, [JavaELToken(JavaELTokenType.RVALUE, '\'1234\'')])

        tokens = None

        tokens = tokenize_expression("\'PU522_04_ApprovalInspectionTime\'")
        self.assertEqual(tokens, [JavaELToken(JavaELTokenType.RVALUE, '\'PU522_04_ApprovalInspectionTime\'')])

        tokens = None

        tokens = tokenize_expression("securityDataProvider.hasRole('tehprisEE_portalUserRegistrator')")
        self.assertEqual(tokens[0].token_value, "securityDataProvider.hasRole('tehprisEE_portalUserRegistrator')")
        self.assertEqual(tokens[0].token_type, JavaELTokenType.RVALUE)

        tokens = None

        tokens = tokenize_expression("'PU522_09_Non-admission'")
        self.assertEqual(tokens[0].token_value, "'PU522_09_Non-admission'")
        self.assertEqual(tokens[0].token_type, JavaELTokenType.RVALUE)

    def test_and(self):
        tokens = tokenize_expression("securityDataProvider.hasRole('tehprisEE_portalUserRegistrator') and !securityDataProvider.hasRole('admin')")
        self.assertEqual(tokens[1].token_type, JavaELTokenType.AND)

        tokens = tokenize_expression("!empty fields and fields.RepeatedNonadmission eq true and fields.CommunicationMethod.Code eq '57518'")
        self.assertEqual(tokens[3].token_type, JavaELTokenType.AND)
        self.assertEqual(tokens[7].token_type, JavaELTokenType.AND)

    def test_data_series(self):
        tokens = tokenize_expression("['956','957'].contains(fields.p_ReasonTP.Code) and (view.viewId.contains('portal.xhtml') or (securityDataProvider.hasRole('tehprisEE_portalUserRegistrator')))")
        self.assertEqual(tokens[0].token_type, JavaELTokenType.SQUARED_SCOPE_OPEN)
        self.assertEqual(tokens[4].token_type, JavaELTokenType.SQUARED_SCOPE_CLOSE)
        self.assertEqual(tokens[2].token_type, JavaELTokenType.COMMA)
