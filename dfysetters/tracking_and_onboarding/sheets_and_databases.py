import src_path
from helper.constants import *
import os
import glob
import gspread
import pandas as pd
import psycopg2 as pg2
from sqlalchemy import create_engine
from gspread_formatting import *


class CreateDailyKPIsQueries:
    def __init__(self, table_name, metric_for_aggregate):
        self.table_name = table_name
        self.metric_for_aggregate = metric_for_aggregate

    def get_percentage_query(self, column_name, small_metric, large_metric):

        query = f"""ALTER TABLE {self.table_name} ADD {column_name} float; 
        UPDATE {self.table_name} SET {column_name} = CASE 
                WHEN {small_metric} IS NULL
                    OR {small_metric} = 0
                    OR {large_metric} IS NULL
                    OR {large_metric} = 0
                    THEN 0
                ELSE CAST(({large_metric} * 100.0) / {small_metric} AS DECIMAL(10, 2))
                END"""

        return query

    def column_constraints(self):
        list_of_column_constraints = [
            (item + f" INTEGER CHECK({item} BETWEEN 0 and 1000),")
            for item in ORDERED_COLUMNS
            if "pc" not in item
        ]

        return list_of_column_constraints

    def add_percentage_columns(self):
        list_of_queries = list()
        for i in PERCENTAGE_COLUMNS.values():
            for a in i:
                column_name = a["column_name"]
                small_metric = a["small_metric"]
                large_metric = a["large_metric"]
                query = self.get_percentage_query(
                    column_name, small_metric, large_metric
                )
                list_of_queries.append(query)

        return list_of_queries

    def get_full_create_and_add_query(self):
        cons = self.column_constraints()
        query = (
            f"CREATE TABLE {self.table_name} ("
            + "date DATE PRIMARY KEY,"
            + " ".join(cons)
        )
        full_query = query[:-1] + ")"  # Removes the last comma
        percentage_queries = self.add_percentage_columns()

        return full_query, percentage_queries

    def get_total_tc_and_ss_query(self):
        total_tc_query = f""" ALTER TABLE {self.table_name} ADD total_tc_booked 
        INTEGER; UPDATE {self.table_name} SET total_tc_booked = 
        fb_group_tc_booked + ghl_tc_booked + email_tc_booked + fb_page_tc_booked
        + outbound_dials_tc_booked"""

        total_ss_query = f""" ALTER TABLE {self.table_name} ADD total_ss_booked 
        INTEGER;UPDATE {self.table_name} SET total_ss_booked = 
        fb_group_ss_booked + ghl_ss_booked + email_ss_booked + fb_page_ss_booked
         + outbound_dials_ss_booked + inbound_triage_ss_booked"""

        return total_tc_query, total_ss_query

    def create_view_query(self, view_name):

        columns = ""
        for i in ORDERED_COLUMNS:
            columns += i
            columns += ","

        select = f"SELECT date,{columns[:-1]},total_tc_booked,total_ss_booked"
        from_order_by = f" FROM {self.table_name} ORDER BY date"

        return f"CREATE VIEW {view_name} AS " + select + from_order_by

    def get_client_list(self):
        engine = create_engine(TRACKING_URI)
        query = "SELECT tablename FROM pg_catalog.pg_tables where schemaname = 'public'"
        df = pd.read_sql_query(query, engine)
        client_list = list(df["tablename"].values)
        return client_list

    def get_totals_query(self):

        client_list = self.get_client_list()
        create_table = f"CREATE TABLE totals.{self.metric_for_aggregate} AS "
        select = f"SELECT {client_list[0]}.date,"

        for i in client_list:
            select += f"{i}.{self.metric_for_aggregate} AS {i}_{self.metric_for_aggregate},"

        inner_join = f" FROM {client_list[0]} "
        for i in client_list:
            if i == client_list[0]:
                pass
            else:
                inner_join += (
                    f"INNER JOIN {i} ON {client_list[0]}.date = {i}.date "
                )
        order_by = "ORDER BY date"

        return create_table + select[:-1] + inner_join + order_by


class GoogleSheetToDatabase:
    def __init__(self, worksheet_name, psql_password) -> None:
        self.worksheet_name = worksheet_name
        self.conn = pg2.connect(
            database="tracking", user="postgres", password=psql_password
        )
        self.gc = gspread.oauth()

    def create_database(self):
        table_name = f"{self.worksheet_name}_raw"
        view_name = f"{self.worksheet_name}_view"

        table = CreateDailyKPIsQueries(table_name, "total_tc_booked")
        tc, ss = table.get_total_tc_and_ss_query()
        full, percentage = table.get_full_create_and_add_query()
        create_view = table.create_view_query(view_name)
        try:
            drop = f"DROP TABLE {table_name} CASCADE"
            self.conn.cursor().execute(drop)
            self.conn.commit()
        except:
            self.conn.commit()
        self.conn.cursor().execute(full)
        self.conn.commit()

        import_query = f"COPY {table_name} FROM '{PATH_TO_DATABASE_FILE}/{self.worksheet_name}.csv' DELIMITER ',' CSV HEADER;"
        self.conn.cursor().execute(import_query)
        for i in percentage:
            self.conn.cursor().execute(i)

        self.conn.cursor().execute(tc)
        self.conn.cursor().execute(ss)
        self.conn.cursor().execute(create_view)

        self.conn.commit()

        files = glob.glob(f"{PATH_TO_DATABASE_FILE}*")
        for f in files:
            os.remove(f)

    def get_client_sheet_to_csv(self):

        sheet = self.gc.open_by_url(EXPORTS_URL).worksheet(self.worksheet_name)
        csv_name = sheet.title + ".csv"

        df = pd.DataFrame(sheet.get_all_records())
        df.set_index(sheet.title).to_csv(PATH_TO_DATABASE_FILE + csv_name)


class DatabaseToGoogleSheet:
    def __init__(self, client, db_name) -> None:
        self.client = client
        self.engine = create_engine(
            f"postgresql://postgres:{POSTGRES_PASSWORD}@localhost:5432/{db_name}"
        )

    def create_df_from_database(self):
        myQuery = f"SELECT * FROM {self.client}_view"
        df = pd.read_sql_query(myQuery, self.engine)
        df["date"] = df["date"].astype(str)
        df.fillna(0, inplace=True)

        return df

    def update_sheet_with_df(self):

        df = self.create_df_from_database()
        gc = gspread.oauth()
        list_of_columns = [
            i.replace("_", " ").title() for i in df.columns.values.tolist()
        ]

        sheet_name = " ".join(self.client.split("_")).title()
        sheet = gc.open_by_url(NEW_DAILY_KPIS_URL)
        # Here + sheet1 above
        try:
            sheet.del_worksheet(sheet.worksheet(sheet_name))
        except gspread.exceptions.WorksheetNotFound:
            print(f"Creating new sheet for {sheet_name}")

        new_sheet = sheet.add_worksheet(sheet_name, rows=1000, cols=50)
        new_sheet.update(
            [list_of_columns] + df.values.tolist(),
            value_input_option="USER_ENTERED",  # This was added
        )

    def update_all_sheets(self):
        myQuery = f"SELECT tablename FROM pg_catalog.pg_tables where schemaname = 'public'"
        df = pd.read_sql_query(myQuery, self.engine)

        dbs = list(df["tablename"])
        client_list = [i[:-4] for i in dbs if "raw" in i]

        for client in client_list:
            DatabaseToGoogleSheet(client, "tracking").update_sheet_with_df()


class FormatSheet:
    def __init__(self, sheet) -> None:
        self.sheet = sheet
        self.updater = batch_updater(self.sheet.spreadsheet)

    def sheet_wide(self):

        self.updater.format_cell_range(
            self.sheet,
            HEADER_COLUMNS,
            CellFormat(textFormat=TextFormat(bold=True)),
        )
        self.updater.format_cell_range(
            self.sheet,
            WHOLE_SHEET,
            CellFormat(
                horizontalAlignment="CENTER", verticalAlignment="MIDDLE"
            ),
        )
        self.updater.format_cell_range(
            self.sheet,
            DATE,
            CellFormat(numberFormat=NumberFormat("NUMBER", "ddd mmmdd")),
        )

        set_frozen(self.sheet, rows=1)
        set_frozen(self.sheet, cols=1)

    def color_and_wrap(self):

        for column in PERCENT_COLUMNS:
            self.updater.format_cell_range(
                self.sheet,
                column,
                CellFormat(
                    backgroundColor=Color(52, 52, 52),
                    textFormat=TextFormat(fontSize=8),
                ),
            )
            self.updater.set_column_width(self.sheet, column.split(":")[1], 50)

        for column in NON_PERCENT_COLUMNS:
            self.updater.format_cell_range(
                self.sheet, column, CellFormat(wrapStrategy="WRAP")
            )

    def title_colors(self):

        self.updater.format_cell_range(
            self.sheet,
            FB_TITLES,
            CellFormat(backgroundColor=Color(64, 51, 51)),
        )
        self.updater.format_cell_range(
            self.sheet,
            GHL_TITLES,
            CellFormat(backgroundColor=Color(64, 58, 51)),
        )
        self.updater.format_cell_range(
            self.sheet,
            EMAIL_TITLES,
            CellFormat(backgroundColor=Color(64, 64, 51)),
        )
        self.updater.format_cell_range(
            self.sheet,
            OUTBOUND_DIALS_TITLES,
            CellFormat(backgroundColor=Color(58, 64, 51)),
        )
        self.updater.format_cell_range(
            self.sheet,
            FB_PAGE_TITLES,
            CellFormat(backgroundColor=Color(51, 64, 58)),
        )
        self.updater.format_cell_range(
            self.sheet,
            INBOUND_TRIAGE_TITLES,
            CellFormat(backgroundColor=Color(51, 58, 64)),
        )

    def borders(self):
        df = pd.DataFrame(self.sheet.get_all_records())

        dates_in_sheet = set(df["Date"].values)
        common = list(set(dates_in_sheet).intersection(MONDAYS))

        for i in common:
            default_row = df.index[df["Date"] == i].tolist()[0]
            adjusted_row = f"A{default_row+2}:{default_row+2}"
            self.updater.format_cell_range(
                self.sheet,
                adjusted_row,
                CellFormat(borders=Borders(top=Border(style="SOLID"))),
            )

        for column in ALL_END_COLUMNS:
            self.updater.format_cell_range(
                self.sheet,
                column,
                CellFormat(borders=Borders(right=Border(style="SOLID_MEDIUM"))),
            )

    def format_whole_sheet(self):
        self.sheet_wide()
        self.color_and_wrap()
        self.title_colors()
        self.borders()
        self.updater.execute()


def move_table_to_new_schema(old_schema, new_schema, table_to_move):
    move_query = f"""CREATE TABLE {new_schema}.{table_to_move} (LIKE {old_schema}.{table_to_move} INCLUDING ALL); 

    INSERT INTO {new_schema}.{table_to_move} SELECT * FROM {old_schema}.{table_to_move};"""

    delete_old = f"DROP TABLE {old_schema}.{table_to_move} CASCADE"

    return move_query, delete_old
