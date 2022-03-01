import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[1]) + "/helper")

from constants import *
from sqlalchemy import create_engine
import pandas as pd
import psycopg2 as pg2


class Databases:
    def __init__(self, table_name):
        self.engine = create_engine(DATABASE_URI)
        self.table_name = table_name

    def read_dataframe_of_roles(self):
        """Uses postgres to pull through all members in the team database

        Returns:
            dataframe: Returns two columns, name and role for all members in team
        """

        myQuery = f"SELECT full_name,company_role FROM {self.table_name}"
        df = pd.read_sql_query(myQuery, self.engine)
        return df

    def generate_variables(self):
        """Gets all of the details from the team database for one employee

        Returns:
            dataframe: One row dataframe with the variables of a given employee
        """
        name = input("What is the name of the person you are searching for? ")
        myQuery = f"SELECT * FROM {self.table_name} WHERE full_name = '{name}'"
        df = pd.read_sql_query(myQuery, self.engine)

        return df

    def get_query(self):
        """Takes input from the user and puts it into a SQL query

        Returns:
            str: SQL query string
        """

        full_name = input(
            "What is the full name of the person you want to add? "
        )
        role = input("What role is this person in? ")
        email = input("What is this person's email address? ")
        pay = input("How much is this person getting paid per client? (USD): ")
        start_date = input(
            "What is the start date of the person you want to add? (YYYY-MM-DD) "
        )
        pod = input("What pod is this person in? ")
        personal_email = input("What is this person's personal email address? ")

        query = f"""
        INSERT INTO team(full_name,company_role,company_email,pay_per_client,
        start_date,active,pod,personal_email) VALUES('{full_name}', '{role}','{email}','{pay}',
        '{start_date}',
        '1','{pod}','{personal_email}') """

        return query

    def add_member(self, query):
        """Uses psycopg2 to push a given query to a selected database

        Args:
            query (str): sql string with desired query, usually an INSERT INTO
        """

        conn = pg2.connect(
            database=POSTGRES_DATABASE,
            user=POSTGRES_USERNAME,
            password=POSTGRES_PASSWORD,
        )
        conn.cursor().execute(query)
        conn.commit()
        print("Person Added")
