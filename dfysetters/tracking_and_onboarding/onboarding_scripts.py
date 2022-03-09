"""This module works with Google Calendar to set follow up events and invite 
new team members to the relevant meetings"""

import src_path
from datetime import timedelta
from gcsa.event import Event
from helper.constants import *


class GoogleSetup:
    def __init__(self, row_of_df, calendar):
        self.row_of_df = row_of_df
        self.calendar = calendar

    def set_follow_up(self):
        """Will put a follow up event on louisrae@settersandspecialists.com calendar

        Args:
            df (dataframe): Single row dataframe with the data of the employee who
            needs to be followed up with"""

        name = self.row_of_df["full_name"][0]
        start = self.row_of_df["start_date"][0] + timedelta(14)
        end = start + timedelta(1)
        event = Event(f"End of trial for {name}", start=start, end=end)
        self.calendar.add_event(event)

        return f"{name} added to calendar for {start}"

    def get_events_to_inv(self):
        """Gives a list of events based on the team member that they need to be
        invited to

        Args:
            row_of_df (dataframe): Single row dataframe with the data of the employee who
            needs to be followed up with

        Returns:
            _type_: _description_
        """
        role = self.row_of_df["company_role"][0]
        pod = self.row_of_df["pod"][0]
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

    def email_setup(self):
        """Generates the email to be sent

        Args:
            row_of_df (dataframe): Single row dataframe with the data of the employee who
            needs to be followed up with

        Returns:
            tuple: email address to send to, subject line of email, body of email
        """

        email_address = self.row_of_df["company_email"][0]

        slack_link = input("What is the manual invite link you generated? ")

        subject = "Congratulations!"

        body = f"""{self.row_of_df["full_name"][0]},

        Congratulations and welcome to Setters&Specialists! We've decided to bring you on board as our new {self.row_of_df["company_role"][0]}. We're excited to have you and can't wait for you to start!

        As discussed, here are the terms of your employment:

        Rate: {self.row_of_df["pay_per_client"][0]} USD per client (OTE: 3k)

        Hours: 9-5 CST but performance is more important

        Working days: Monday - Friday

        Before we move to the onboarding process, please complete the following right away:

        Join Our Asana Workspace (Link In Email)

        Join our Slack channel ({slack_link})

        Watch Asana Initial Video (In Onboarding Project in Asana)

        An Asana and Slack Invite have been sent to {self.row_of_df["company_email"][0]}, please confirm once you have this.

        We cannot move forward until the above 2 tasks are complete. :)

        We're looking at about three days for general onboarding. After that, you'll move to your department, where you'll start role-specific training.

        Please let me know if you have any questions.

        Again, Welcome to Setters&Specialists! :)

        Setters & Specialists Ltd"""

        return email_address, subject, body


class Slack:
    def __init__(self, slack_webclient, row_of_df):
        self.slack_webclient = slack_webclient
        self.row_of_df = row_of_df

    def slack_data_setup(self):
        """Gives us a list of channels to invite a Slack Id to

        Args:
            row_of_df (dataframe): Single row dataframe with the data of the employee who
            needs to be followed up with

        Returns:
            tuple: slack_id of the desired team member, channels to invite them to
        """
        pod = self.row_of_df["pod"][0]
        role = self.row_of_df["company_role"][0]
        user_id = self.row_of_df["slack_id"][0]

        channels = []
        if pod == "Girls":
            channels.append(GIRLS_ID)
        elif pod == "Purple":
            channels.append(PURPLE_ID)
        elif pod == "Ops":
            channels.append(SCRUMTEAM_ID)
        elif pod == "SFU":
            channels.append(SFU_ID)

        if "Specialist" in role:
            channels.append(SPECIALISTS_ID)
        elif "Setter" in role:
            channels.append(SETTERS_ID)
        elif "Pod Lead" in role:
            channels.append(LEVEL_5_ID)

        channels.append(SETTERS_TEAM_ID)
        channels.append(CLIENT_REPORTS_ID)

        return user_id, channels
