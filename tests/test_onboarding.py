from tracking_and_onboarding.helper.roles import *
from tracking_and_onboarding.helper.common import Databases
from tracking_and_onboarding.onboarding_scripts import Slack
from tracking_and_onboarding.onboarding_scripts import GoogleSetup
from gcsa.google_calendar import GoogleCalendar
from slack_sdk import WebClient

from dotenv import load_dotenv
import os


invite = "https://join.slack.com/t/dfysetters/shared_invite/zt-17uddj711-JK7Nc3RktaB1hz0E4EPBWw"

full_name = "Tylee Groll"
role = "Pod Lead"
email = "tylee@settersandspecialists.com"
pay = "100"
start_date = "2022-01-01"
pod = "Purple"
personal_email = "tyleeann07@gmail.com"


class TestOnboarding:
    load_dotenv("/Users/louisrae/Documents/code/published/dfysetters/.env")
    client = WebClient(token=os.getenv("SLACK_API"))

    name_from_db = Databases(
        "teamtest", "general"
    ).get_row_of_database_based_on_name(email)
    cal = GoogleCalendar()

    def test_queryIsCorrect(self):
        query = Databases("team", "general").get_insert_into_query(
            full_name, role, email, pay, start_date, pod, personal_email
        )
        assert "INSERT INTO" in query and "VALUES" in query

    def test_getCorrectMeetingsBasedOnRoleAndPod(self):
        meetings = GoogleSetup(self.name_from_db, self.cal).get_events_to_inv()

        assert "Pod Lead Weekly" in meetings

    def test_followUpAddedToCalendar(self):
        message = GoogleSetup(self.name_from_db, self.cal).set_follow_up()
        assert "Tylee Groll" in message and "2021-06-29" in message

    def test_getCorrectChannelsBasedOnRoleAndPod(self):
        channel_list = Slack(self.client, self.name_from_db).slack_data_setup()
        assert all(
            elem in ["C0199AXJC80", "C01GHC2Q3GC", "C02SXKE5S6R", "C026GHAF3A5"]
            for elem in channel_list[1]
        )

    def test_correctEmailBeingSent(self):
        email_head = "Tylee Groll"
        email = GoogleSetup(self.name_from_db, self.cal).email_setup(invite)
        assert email_head in email[2]
