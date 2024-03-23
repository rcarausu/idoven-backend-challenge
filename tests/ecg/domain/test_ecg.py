from datetime import datetime, timezone

from freezegun import freeze_time

from ecg.domain.ecg import Lead, ECG


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

    def test_it_counts_number_of_zero_crossings_for_signal(self):
        # given
        lead = Lead('V1', signal=[1, -2, 0, 3, -4, 0, 0, 5, 6, -7])
        # then
        assert lead.number_of_zero_crossings() == 5


class TestECG:

    @freeze_time("2024-01-01")
    def test_it_creates_ecg_with_default_values(self):
        # given
        ecg = ECG()
        # then
        assert type(ecg.ecg_id) is str
        assert ecg.create_date == datetime(2024, 1, 1, tzinfo=timezone.utc)
        assert len(ecg.leads) == 0

    def test_it_creates_ecg_from_constructor(self):
        # given
        ecg = ECG(ecg_id="id", create_date=datetime.fromisoformat("2024-01-01T00:00:00"),
                  leads=[Lead("V1", [-1, 0, 1])])
        # then
        assert ecg.ecg_id == "id"
        assert ecg.create_date == datetime(2024, 1, 1)
        assert ecg.leads == [Lead("V1", [-1, 0, 1])]
