"""This module houses common methods used across the codebase"""
import os
from datetime import timedelta
import pandas as pd
import datetime
from dotenv import load_dotenv
from constants import *
from sqlalchemy import create_engine
import psycopg2 as pg2


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


def get_mondays(date_start, date_end):
    date_start = datetime.datetime.strptime(date_start, "%Y-%m-%d")
    date_end = datetime.datetime.strptime(date_end, "%Y-%m-%d")

    dates = []
    while date_start <= date_end:
        if date_start.weekday() == 0:  # 0 == Monday
            dates.append(date_start.strftime("%Y-%m-%d"))
        date_start += datetime.timedelta(days=1)

    return dates


class Databases:
    def __init__(self, table_name, database):

        load_dotenv("/Users/louisrae/Documents/code/published/dfysetters/.env")
        username = os.getenv("POSTGRES_USERNAME")
        password = os.getenv("POSTGRES_PASSWORD")
        uri = f"postgresql://{username}:{password}@localhost:5432/{database}"

        self.engine = create_engine(uri)
        self.table_name = table_name

    def read_dataframe_of_roles(self):
        """Uses postgres to pull through all members in the team database

        Returns:
            dataframe: Returns two columns, name and role for all members in team
        """

        myQuery = f"SELECT full_name,company_role FROM {self.table_name}"
        df = pd.read_sql_query(myQuery, self.engine)
        return df

    def get_row_of_database_based_on_name(self, email_to_search):
        """Gets all of the details from the team database for one employee

        Returns:
            dataframe: One row dataframe with the variables of a given employee
        """
        myQuery = f"SELECT * FROM {self.table_name} WHERE company_email = '{email_to_search}'"
        row_of_df = pd.read_sql_query(myQuery, self.engine)

        return row_of_df

    def get_insert_into_query(
        self, full_name, role, email, pay, start_date, pod, personal_email
    ):
        """Takes input from the user and puts it into a SQL query

        Returns:
            str: SQL query string
        """

        query = f"""
        INSERT INTO team(full_name,company_role,company_email,pay_per_client,
        start_date,active,pod,personal_email) VALUES('{full_name}', '{role}','{email}','{pay}',
        '{start_date}',
        '1','{pod}','{personal_email}') """

        return query

    def add_member_to_database(self, query):
        """Uses psycopg2 to push a given query to a selected database

        Args:
            query (str): sql string with desired query, usually an INSERT INTO
        """
        load_dotenv()

        conn = pg2.connect(
            database="general",
            user=os.getenv("POSTGRES_USERNAME"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )

        conn.cursor().execute(query)
        conn.commit()
        print("Person Added")
