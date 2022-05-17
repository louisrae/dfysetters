"""This module houses common methods used across the codebase"""
from datetime import timedelta
from matplotlib import use
import pandas as pd
import datetime
from dotenv import load_dotenv
import os


def change_date_column_in_df_to_datetime(sheet):
    """Takes in a sheet and returns a dataframe of that sheet with a datetime
    column

    Args:
        sheet (gspread.worksheet): Google sheet with one Date Column as string

    Returns:
        dataframe: Dataframe of the sheet in the input, with Datetime column
    """
    df = pd.DataFrame(sheet.get_all_records())
    df["Date"] = pd.to_datetime(df[df.columns[0]])

    return df


def get_day_list(start_date, end_date):
    """Gets a list of datetime objects between two dates

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


def get_postgre_uri(database):
    load_dotenv()
    username = os.getenv("POSTGRES_USERNAME")
    password = os.getenv("POSTGRES_PASSWORD")
    uri = f"postgresql://{username}:{password}@localhost:5432/{database}"

    return uri


def get_mondays(date_start, date_end):
    date_start = datetime.datetime.strptime(date_start, "%Y-%m-%d")
    date_end = datetime.datetime.strptime(date_end, "%Y-%m-%d")

    dates = []
    while date_start <= date_end:
        if date_start.weekday() == 0:  # 0 == Monday
            dates.append(date_start.strftime("%Y-%m-%d"))
        date_start += datetime.timedelta(days=1)

    return dates
