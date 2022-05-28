import pytest
import src_path
from tracking_and_onboarding.sheets_and_databases import *


@pytest.fixture()
def daily_kpis():
    table_name = "tracking"
    metric_for_aggregate = "fb_group_tc_booked"
    daily_kpis = CreateDailyKPIsQueries(table_name, metric_for_aggregate)
    return daily_kpis


def test_create_queries(daily_kpis):
    full, percentage = daily_kpis.get_full_create_and_add_query()

    assert (
        "CREATE TABLE tracking (date DATE PRIMARY KEY,fb_group_reach_outs"
        in full
    )
    assert (
        "ALTER TABLE tracking ADD fb_group_reach_out_to_replies_pc float"
        in percentage[0]
    )


def test_total_tc_and_ss(daily_kpis):
    tc, ss = daily_kpis.get_total_tc_and_ss_query()
    assert " ALTER TABLE tracking ADD total_tc_booked" in tc
    assert " ALTER TABLE tracking ADD total_ss_booked" in ss


def test_view_query(daily_kpis):
    view_name = "tracking_raw"
    f = daily_kpis.create_view_query(view_name)
    assert "CREATE VIEW tracking_raw AS SELECT date,fb_group_reach_outs" in f


def test_totals_query(daily_kpis):

    query = daily_kpis.get_totals_query()
    assert (
        "CREATE TABLE totals.fb_group_tc_booked AS SELECT two_percent_theory_raw.date"
        in query
    )


def test_df_from_database_creation():

    dbtosheet = DatabaseToGoogleSheet("the_flipstress")
    df = dbtosheet.create_df_from_database()
    assert df["total_ss_booked"].sum() == 378.0


def test_moving_table():
    old = "public"
    new = "inactive"
    table = "the_flipstress_raw"

    query = move_table_to_new_schema(old, new, table)[0]

    assert (
        "CREATE TABLE inactive.the_flipstress_raw (LIKE public.the_flipstress_raw INCLUDING ALL)"
        in query
    )
