import src_path
from helper.databases import Databases
from team_onboarding.slack_setup import slack_data_setup
from team_onboarding.welcome_email import email_setup
from team_onboarding.gcal_setup import get_events_to_inv, set_follow_up


class TestOnboarding:

    name_from_db = None

    def setup(cls):
        cls.name_from_db = Databases(
            "teamtest"
        ).get_row_of_database_based_on_name()

    def test_queryIsCorrect(self):
        query = Databases("team").get_insert_into_query()
        assert "INSERT INTO" in query and "VALUES" in query

    def test_getCorrectMeetingsBasedOnRoleAndPod(self):
        meetings = get_events_to_inv(self.name_from_db)
        assert "Pod Lead Weekly" in meetings

    def test_followUpAddedToCalendar(self):
        message = set_follow_up(self.name_from_db)
        assert "Tylee Groll" in message and "2021-06-29" in message

    def test_getCorrectChannelsBasedOnRoleAndPod(self):
        channel_list = slack_data_setup(self.name_from_db)
        assert all(
            elem in ["C0199AXJC80", "C01GHC2Q3GC", "C02SXKE5S6R", "C026GHAF3A5"]
            for elem in channel_list[1]
        )

    def test_correctEmailBeingSent(self):
        email_head = "Tylee Groll"
        email = email_setup(self.name_from_db)
        assert email_head in email[2]
