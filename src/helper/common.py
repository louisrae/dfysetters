"""This module houses common methods used across the codebase"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[1]) + "/helper")

from datetime import timedelta
from sqlalchemy import create_engine
import pandas as pd
from constants import DATABASE_URI


def read_dataframe_of_roles():
    """Uses postgres to pull through all members in the team database

    Returns:
        dataframe: Returns two columns, name and role for all members in team
    """
    engine = create_engine(DATABASE_URI)

    myQuery = "SELECT full_name,company_role FROM team"
    df = pd.read_sql_query(myQuery, engine)
    return df


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


def generate_variables():
    """Gets all of the details from the team database for one employee

    Returns:
        dataframe: One row dataframe with the variables of a given employee
    """
    engine = create_engine(
        "postgresql://postgres:qweasdzxcQ101@localhost:5432/general"
    )
    name = input("What is the name of the person you are searching for? ")
    myQuery = f"SELECT * FROM team WHERE full_name = '{name}'"
    df = pd.read_sql_query(myQuery, engine)

    return df
