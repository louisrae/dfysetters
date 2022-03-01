import src_path
import pytest
from tracking.roles import *
from helper.databases import Databases


class TestRoles:
    def setup(self):
        Roles.register_all_members()

    def test_canCreatePerson(self):
        jack = Person("Jack", "Snr Specialist")
        assert jack.name == "Jack" and jack.role == "Snr Specialist"

    def test_canRegisterAllMembers(self):
        df = Databases("teamtest").read_dataframe_of_roles()
        assert len(df.index) == len(Roles.all_team_members_in_company)

    def test_canGetAllSnrSpecialists(self):
        ls = SnrSpecialist().all_members
        assert len(ls) == 10

    def test_canGetAllJnrSpecialists(self):
        ls = JnrSpecialist().all_members
        assert len(ls) == 0

    def test_canGetAllPodLeads(self):
        ls = PodLead().all_members
        assert len(ls) == 5

    def test_canGetAllSetters(self):
        ls = Setter().all_members
        assert len(ls) == 9
