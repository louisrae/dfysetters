from sqlalchemy import create_engine
import pandas as pd
import psycopg2 as pg2


def generate_variables():
    engine = create_engine(
        "postgresql://postgres:qweasdzxcQ101@localhost:5432/general"
    )
    name = input("What is the name of the person you are searching for? ")
    myQuery = f"SELECT * FROM team WHERE full_name = '{name}'"
    df = pd.read_sql_query(myQuery, engine)

    return df
