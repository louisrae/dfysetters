"""This module houses common methods used across the codebase"""
from datetime import timedelta
import pandas as pd


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
