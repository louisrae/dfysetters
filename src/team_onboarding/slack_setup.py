""" This module will get the channels that the new team member needs to be 
invited to"""
import src_path
from slack import WebClient
from helper.constants import *


client = WebClient(token=SLACK_TOKEN)


def slack_data_setup(df):
    """Gives us a list of channels to invite a Slack Id to

    Args:
        df (dataframe): Single row dataframe with the data of the employee who
        needs to be followed up with

    Returns:
        tuple: slack_id of the desired team member, channels to invite them to
    """
    pod = df["pod"][0]
    role = df["company_role"][0]
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

    pod = df["pod"][0]
    role = df["company_role"][0]
    user_id = df["slack_id"][0]

    return user_id, channels
