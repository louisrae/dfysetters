from calendar import calendar
import src_path
from helper.databases import Databases
from tracking_and_onboarding.onboarding_scripts import Slack
from tracking_and_onboarding.onboarding_scripts import GoogleSetup
from gcsa.google_calendar import GoogleCalendar
from slack import WebClient
from helper.credentials.apis import *

client = WebClient(token=SLACK_API)


name_from_db = Databases("teamtest").get_row_of_database_based_on_name()
cal = GoogleCalendar()


class TestOnboarding:
    def test_queryIsCorrect(self):
        query = Databases("team").get_insert_into_query()
        assert "INSERT INTO" in query and "VALUES" in query

    def test_getCorrectMeetingsBasedOnRoleAndPod(self):
        meetings = GoogleSetup(name_from_db, cal).get_events_to_inv()

        assert "Pod Lead Weekly" in meetings

    def test_followUpAddedToCalendar(self):
        message = GoogleSetup(name_from_db, cal).set_follow_up()
        assert "Tylee Groll" in message and "2021-06-29" in message

    def test_getCorrectChannelsBasedOnRoleAndPod(self):
        channel_list = Slack(client, name_from_db).slack_data_setup()
        assert all(
            elem in ["C0199AXJC80", "C01GHC2Q3GC", "C02SXKE5S6R", "C026GHAF3A5"]
            for elem in channel_list[1]
        )

    def test_correctEmailBeingSent(self):
        email_head = "Tylee Groll"
        email = GoogleSetup(name_from_db, cal).email_setup()
        assert email_head in email[2]
