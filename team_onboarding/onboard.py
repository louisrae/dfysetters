"""This module takes the files from the src repo and 
gives a full onboarding flow"""

from src.add_team_member_to_db import *
from src.slack_setup import *
from src.gcal_setup import *
from src.welcome_email import email_setup
from src.common import *
import ezgmail


ezgmail.init(
    tokenFile="/Users/louisrae/Documents/code (parent)/credentials/token.json",
    credentialsFile="/Users/louisrae/Documents/code (parent)/credentials/credentials.json",
)


def main():
    """Will add a member to the team database, send the welcome email, set the
    follow up task and get the company meetings that need to be invited to.
    Then it will prompt the user to add the team member to Asana"""

    # query = get_query()
    # add_member(query)

    df = generate_variables()

    address, subject, body = email_setup(df)
    print(body)
    to_send = input("Do you want to send the above email? (y or n): ").lower()
    if to_send == "n":
        pass
    elif to_send == "y":
        ezgmail.send(address, subject, body)
        print("Email Sent")

    set_follow_up(df)
    print("Follow Up Set")

    meetings = get_events_to_inv(df)
    print(f"Meetings to add to are {meetings}")

    input(
        "Have you added this email to Asana and invited to Company Wiki and Onboarding?"
    )


def get_slack_channels():
    """Will add a given member to the correct slack channels
    based on their Slack_ID"""

    df = generate_variables()
    user_id, channels = slack_data_setup(df)
    print(channels)
    to_invite = input(
        "Do you want to invite to the above channels? (y or n): "
    ).lower()
    if to_invite == "n":
        pass
    elif to_invite == "y":
        for channel in channels:
            try:
                client.conversations_invite(channel=channel, users=user_id)
                print(f"{user_id} added to {channel}")
            except Exception as e:
                print()
                print(f"{user_id} could not be added to {channel}")


main()
get_slack_channels()
