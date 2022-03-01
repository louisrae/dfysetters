import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[1]) + "/helper")

from constants import DATABASE_URI
from sqlalchemy import create_engine
import pandas as pd


def read_dataframe_of_roles(table_name):
    """Uses postgres to pull through all members in the team database

    Returns:
        dataframe: Returns two columns, name and role for all members in team
    """
    engine = create_engine(DATABASE_URI)

    myQuery = f"SELECT full_name,company_role FROM {table_name}"
    df = pd.read_sql_query(myQuery, engine)
    return df


def generate_variables(table_name):
    """Gets all of the details from the team database for one employee

    Returns:
        dataframe: One row dataframe with the variables of a given employee
    """
    engine = create_engine(
        "postgresql://postgres:qweasdzxcQ101@localhost:5432/general"
    )
    name = input("What is the name of the person you are searching for? ")
    myQuery = f"SELECT * FROM {table_name} WHERE full_name = '{name}'"
    df = pd.read_sql_query(myQuery, engine)

    return df


def generate_variables(table_name):
    """Gets all of the details from the team database for one employee

    Returns:
        dataframe: One row dataframe with the variables of a given employee
    """
    engine = create_engine(
        "postgresql://postgres:qweasdzxcQ101@localhost:5432/general"
    )
    name = input("What is the name of the person you are searching for? ")
    myQuery = f"SELECT * FROM {table_name} WHERE full_name = '{name}'"
    df = pd.read_sql_query(myQuery, engine)

    return df
