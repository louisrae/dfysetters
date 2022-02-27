import src_path
import pytest
from tracking.roles import (
    Roles,
    Person,
    SnrSpecialist,
    JnrSpecialist,
    Setter,
    Operations,
    PodLead,
)
from helper.common import read_dataframe_of_roles


class TestRoles:
    @pytest.fixture
    def register(self):
        register = Roles.register_all_members()
        return register

    def test_canCreatePerson(self):
        jack = Person("Jack", "Snr Specialist")
        assert jack.name == "Jack" and jack.role == "Snr Specialist"

    def test_canRegisterAllMembers(self, register):
        df = read_dataframe_of_roles()
        assert len(df.index) == len(Roles.all_team_members_in_company)

    def test_canGetAllSnrSpecialists(self, register):
        ls = SnrSpecialist().all_members
        assert len(ls) == 10

    def test_canGetAllJnrSpecialists(register):
        ls = JnrSpecialist().all_members
        assert len(ls) == 0

    def test_canGetAllPodLeads(register):
        ls = PodLead().all_members
        assert len(ls) == 5

    def test_canGetAllSetters(register):
        ls = Setter().all_members
        assert len(ls) == 9
