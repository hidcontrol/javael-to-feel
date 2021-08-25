import unittest
from src.getOperands_01 import toDMN

test_el = "empty fields.id or !securityDataProvider.hasRole('tehprisEE_User')or\
    (dataObjectController.instance.objectStatus.status.code eq 'ta03_Paused')or\
    (dataObjectController.instance.objectStatus.status.code eq 'ta05_ContractOnReviewApplicant' and \
    fields.p_ContractTransferType.Code eq '7185643' and (!empty fields['ScanDogovor'] and \
    empty fields['ScanDogovorCL'] or !empty fields['ScanDopDogovor'] and \
    empty fields['ScanDopDogovorUser']))or(dataObjectController.instance.objectStatus.status.code eq 'ta06_ContractSigned' and \
    fields.p_ContractTransferType.Code eq '7185643' and !empty fields['DateCompTechnical_Company'] and \
    empty fields['DateCompTechnical_applicant'])or(dataObjectController.instance.objectStatus.status.code eq 'ta07_TUImplementationCheck' and \
    fields.p_ContractTransferType.Code eq '7185643' and !empty fields['ScanActTU'] and empty fields['ScanActTU_User'])or\
    (dataObjectController.instance.objectStatus.status.code eq 'ta09_ActsSigning' and fields.p_ContractTransferType.Code eq '7185643' and \
    !empty fields['ScanActTP'] and empty fields['ScanActTP_User'])"

test_el_expected = "Or(~securityDataProvider_hasRole_tehprisEE_User_, And(fields_p_ContractTransferType_Code_eq_7185643, dataObjectController_instance_objectStatus_status_code_eq_ta09_ActsSigning, ~empty_fields_ScanActTP, empty_fields_ScanActTP_User_), dataObjectController_instance_objectStatus_status_code_eq_ta03_Paused, empty_fields_id, And(dataObjectController_instance_objectStatus_status_code_eq_ta05_ContractOnReviewApplicant, fields_p_ContractTransferType_Code_eq_7185643, ~empty_fields_ScanDopDogovor, empty_fields_ScanDopDogovorUser_), And(fields_p_ContractTransferType_Code_eq_7185643, dataObjectController_instance_objectStatus_status_code_eq_ta06_ContractSigned, ~empty_fields_DateCompTechnical_Company, empty_fields_DateCompTechnical_applicant_), And(dataObjectController_instance_objectStatus_status_code_eq_ta05_ContractOnReviewApplicant, fields_p_ContractTransferType_Code_eq_7185643, ~empty_fields_ScanDogovor, empty_fields_ScanDogovorCL), And(fields_p_ContractTransferType_Code_eq_7185643, dataObjectController_instance_objectStatus_status_code_eq_ta07_TUImplementationCheck, ~empty_fields_ScanActTU, empty_fields_ScanActTU_User_))"


class TestToDMN(unittest.TestCase):
    def test_to_dmn(self):
        result = toDMN(test_el)
        self.assertEqual(test_el_expected, result)


if __name__ == '__main__':
    unittest.main()
