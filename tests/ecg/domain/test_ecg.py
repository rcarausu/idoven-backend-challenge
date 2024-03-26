from datetime import datetime, timezone
from unittest.mock import patch

from freezegun import freeze_time

from src.user.domain.user import UserId
from src.ecg.domain.ecg import Lead, ECG, EcgId


class TestLead:

    def test_it_creates_lead_without_number_of_samples(self):
        # given
        lead = Lead('V1', signal=[-1, 0, 1])
        # then
        assert lead.name == 'V1'
        assert lead.number_of_samples is None
        assert lead.signal == [-1, 0, 1]

    def test_it_creates_lead_with_number_of_samples(self):
        # given
        lead = Lead('V1', number_of_samples=3, signal=[-1, 0, 1])
        # then
        assert lead.name == 'V1'
        assert lead.number_of_samples == 3
        assert lead.signal == [-1, 0, 1]


class TestECG:

    @patch('src.ecg.domain.ecg.uuid.uuid4', return_value="uuid4_generated_id")
    @freeze_time("2024-01-01")
    def test_it_creates_ecg_with_default_values(self, mocker):
        # when
        ecg = ECG(user_id=UserId())
        # then
        assert ecg.id == EcgId("uuid4_generated_id")
        assert ecg.user_id == UserId("uuid4_generated_id")
        assert ecg.create_date == datetime(2024, 1, 1, tzinfo=timezone.utc)
        assert len(ecg.leads) == 0

    def test_it_creates_ecg_from_constructor(self):
        # when
        ecg = ECG(
            id=EcgId("id"),
            user_id=UserId("id"),
            create_date=datetime.fromisoformat("2024-01-01T00:00:00"),
            leads=[Lead("V1", [-1, 0, 1])]
        )
        # then
        assert ecg.id == EcgId("id")
        assert ecg.user_id == UserId("id")
        assert ecg.create_date == datetime(2024, 1, 1)
        assert ecg.leads == [Lead("V1", [-1, 0, 1])]
