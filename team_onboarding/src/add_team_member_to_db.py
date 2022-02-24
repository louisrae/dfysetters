"""This module is used to add a new team member to the team database"""

import psycopg2 as pg2


def get_query():
    """Takes input from the user and puts it into a SQL query

    Returns:
        str: SQL query string
    """

    full_name = input("What is the full name of the person you want to add? ")
    role = input("What role is this person in? ")
    email = input("What is this person's email address? ")
    pay = input("How much is this person getting paid per client? (USD): ")
    start_date = input(
        "What is the start date of the person you want to add? (YYYY-MM-DD) "
    )
    pod = input("What pod is this person in? ")

    query = f"""
    INSERT INTO team(full_name,company_role,company_email,pay_per_client,
    start_date,active,pod) VALUES('{full_name}', '{role}','{email}','{pay}',
    '{start_date}',
    '1','{pod}') """

    return query


def add_member(query):
    """Uses psycopg2 to push a given query to a selected database

    Args:
        query (str): sql string with desired query, usually an INSERT INTO
    """

    conn = pg2.connect(
        database="general", user="postgres", password="qweasdzxcQ101"
    )
    conn.cursor().execute(query)
    conn.commit()
    print("Person Added")
