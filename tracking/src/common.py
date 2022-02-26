"""This module houses common methods used across the codebase"""

import sys
import os


sys.path.append(f"/Users/{os.environ['USER']}/Documents/tracking/src")
from constants import *
import pandas as pd
from sqlalchemy import create_engine
from datetime import timedelta


def read_dataframe_of_roles():
    """Uses postgres to pull through all members in the team database

    Returns:
        dataframe: Returns two columns, name and role
    """
    engine = create_engine(DATABASE_URI)

    myQuery = "SELECT full_name,company_role FROM team"
    df = pd.read_sql_query(myQuery, engine)
    return df


def change_date_column_in_df_to_datetime(sheet):
    """Takes in a sheet and returns a dataframe of that sheet with a datetime
    columm

    Args:
        sheet (gspread.worksheet): Google sheet with one Date Column as string

    Returns:
        dataframe: Dataframe of the sheet in the input, with Datetime column
    """
    df = pd.DataFrame(sheet.get_all_records())
    df["Date"] = pd.to_datetime(df[df.columns[0]])

    return df


def get_day_list(start_date, end_date):
    """_summary_

    Args:
        start_date (datetime.date): A date lower than the end date
        end_date (datetime.date): A date higher than the start date

    Returns:
        list: List of datetime objects between two dates
    """

    daylist = list()
    delta = end_date - start_date
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        daylist.append(day.strftime("%Y-%m-%d"))

    return daylist
