import src_path
from helper.common import generate_variables
from team_onboarding.add_team_member_to_db import get_query
from team_onboarding.slack_setup import slack_data_setup
from team_onboarding.welcome_email import email_setup
from team_onboarding.gcal_setup import get_events_to_inv, set_follow_up


class TestOnboarding:
    def test_queryIsCorrect(self):
        query = get_query()
        assert "INSERT INTO" in query and "VALUES" in query

    def test_getCorrectMeetingsBasedOnRoleAndPod(self):
        name_from_db = generate_variables()
        meetings = get_events_to_inv(name_from_db)
        assert "Pod Lead Weekly" in meetings

    def test_followUpAddedToCalendar(self):
        name_from_db = generate_variables()
        message = set_follow_up(name_from_db)
        assert "Tylee Groll" in message and "2021-06-29" in message

    def test_getCorrectChannelsBasedOnRoleAndPod(self):
        name_from_db = generate_variables()
        channel_list = slack_data_setup(name_from_db)
        assert all(
            elem in ["C0199AXJC80", "C01GHC2Q3GC", "C02SXKE5S6R", "C026GHAF3A5"]
            for elem in channel_list[1]
        )

    def test_correctEmailBeingSent(self):
        name_from_db = generate_variables()
        email_head = "Tylee Groll"
        email = email_setup(name_from_db)
        assert email_head in email[2]
