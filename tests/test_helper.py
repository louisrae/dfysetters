import datetime
from tracking_and_onboarding.helper.roles import *
from tracking_and_onboarding.helper.common import *


def test_canGetDayList():
    start = datetime.date(2022, 2, 20)
    end = datetime.date(2022, 2, 28)
    list = get_day_list(start, end)
    assert "2022-02-21" in list


class TestRoles:
    def setup(self):
        Roles.register_all_members()

    def test_canCreatePerson(self):
        jack = Person("Jack", "Snr Specialist")
        assert jack.name == "Jack" and jack.role == "Snr Specialist"

    def test_canRegisterAllMembers(self):
        df = Databases("team").read_dataframe_of_roles()
        assert len(df.index) == len(Roles.all_team_members_in_company)

    def test_canGetAllSnrSpecialists(self):
        ls = SnrSpecialist().all_members
        assert len(ls) == 12

    def test_canGetAllJnrSpecialists(self):
        ls = JnrSpecialist().all_members
        assert len(ls) == 0

    def test_canGetAllPodLeads(self):
        ls = PodLead().all_members
        assert len(ls) == 5

    def test_canGetAllSetters(self):
        ls = Setter().all_members
        assert len(ls) == 10
