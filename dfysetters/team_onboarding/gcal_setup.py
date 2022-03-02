"""This module works with Google Calendar to set follow up events and invite 
new team members to the relevant meetings"""

import src_path
from datetime import timedelta
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event
from helper.constants import *


def set_follow_up(row_of_df):
    """Will put a follow up event on louisrae@settersandspecialists.com calendar

    Args:
        df (dataframe): Single row dataframe with the data of the employee who
        needs to be followed up with"""

    calendar = GoogleCalendar(
        GCAL_EMAIL_LOUISRAE,
        credentials_path=GCAL_CREDENTIALS_PATH,
        token_path=GCAL_TOKEN_PICKLE_PATH,
    )

    name = row_of_df["full_name"][0]
    start = row_of_df["start_date"][0] + timedelta(14)
    end = start + timedelta(1)
    event = Event(f"End of trial for {name}", start=start, end=end)
    calendar.add_event(event)

    return f"{name} added to calendar for {start}"


def get_events_to_inv(row_of_df):
    """Gives a list of events based on the team member that they need to be
    invited to

    Args:
        row_of_df (dataframe): Single row dataframe with the data of the employee who
        needs to be followed up with

    Returns:
        _type_: _description_
    """
    role = row_of_df["company_role"][0]
    pod = row_of_df["pod"][0]
    meetings = []

    if role == "Pod Lead":
        meetings.append("Pod Lead Monthly")
        meetings.append("Pod Lead Weekly")
        meetings.append("Pod Lead Daily")
        meetings.append("Pod Lead Review")
    elif role == "Snr Specialist":
        meetings.append("Specialist Training")
    elif role == "Setter":
        meetings.append("Setters Training")

    if pod == "Purple":
        meetings.append("Purple Weekly")
        meetings.append("Purple Daily")
    elif pod == "Girls":
        meetings.append("Girls Weekly")
        meetings.append("Girls Daily")

    meetings.append("Monthly Town hall")

    return meetings