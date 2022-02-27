import src_path
from helper.common import generate_variables
from team_onboarding.add_team_member_to_db import get_query
from team_onboarding.slack_setup import slack_data_setup
from team_onboarding.welcome_email import email_setup
from team_onboarding.gcal_setup import get_events_to_inv, set_follow_up

df = generate_variables()  # Use Tylee Groll As Name


def test_queryIsCorrect():
    query = get_query()
    assert "INSERT INTO" in query and "VALUES" in query


def test_getCorrectMeetingsBasedOnRoleAndPod():
    meetings = get_events_to_inv(df)
    assert "Pod Lead Weekly" in meetings


def test_followUpAddedToCalendar():
    message = set_follow_up(df)
    assert "Tylee Groll" in message and "2021-06-29" in message


def test_getCorrectChannelsBasedOnRoleAndPod():
    channel_list = slack_data_setup(df)
    assert all(
        elem in ["C0199AXJC80", "C01GHC2Q3GC", "C02SXKE5S6R", "C026GHAF3A5"]
        for elem in channel_list[1]
    )


def test_correctEmailBeingSent():
    email_head = """Tylee Groll,

    Congratulations and welcome to Setters&Specialists! We've decided to bring you on board as our new Pod Lead. We're excited to have you and can't wait for you to start!"""
    email = email_setup(df)
    assert email_head in email[2]
