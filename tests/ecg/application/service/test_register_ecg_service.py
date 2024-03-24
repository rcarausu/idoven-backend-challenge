from src.ecg.application.port.in_ports.models.ecg_model import ECGModel, LeadModel
from src.ecg.application.port.in_ports.register_ecg_use_case import RegisterEcgCommand
from src.ecg.application.port.out_ports.save_ecg_port import SaveEcgPort
from src.ecg.application.service.register_ecg_service import RegisterEcgService

from unittest.mock import Mock

from src.ecg.domain.ecg import EcgId


class TestRegisterEcgService:

    mocked_port = Mock(spec=SaveEcgPort)

    service = RegisterEcgService(mocked_port)

    def test_it_should_register_ecg(self):
        # given
        ecg_model = ECGModel(
            leads=[
                LeadModel(
                    name="I",
                    number_of_samples=3,
                    signal=[1, 0, -1]
                )
            ]
        )
        self.mocked_port.save.return_value = EcgId("id")
        # when
        result = self.service.register_ecg(RegisterEcgCommand(ecg_model))
        # then
        assert result == EcgId("id")
