import src_path
import pandas as pd
from helper.constants import *
import requests
from helper.common import change_date_column_in_df_to_datetime


class SalesData:
    def __init__(self, sheet):
        self.sheet = sheet

    def createMonthAndDayColumns(self):
        sheet = self.sheet.get_all_records()
        df = pd.DataFrame([i for i in sheet if i["Email"]])
        df["DateTime"] = pd.to_datetime(df["SS Date"])
        df["Month"] = df["DateTime"].apply(lambda x: x.month)
        df["Day"] = df["DateTime"].apply(lambda x: x.day)

        return df

    def getOutcomesFromDateRange(self, dataframe):

        frame = dataframe[
            (dataframe["Day"] >= DAY_NUMBER_WEEK_AGO)
            & (dataframe["Month"] == MONTH_NUMBER_WEEK_AGO)
        ]

        outcomes = frame["SS Outcome"].value_counts()

        return outcomes

    def getDataframeOfOutcomesCountsandPercentages(self, value_counts):
        total_calls = sum([v for k, v in dict(value_counts).items()])
        percent = {}
        for k, v in value_counts.items():
            percent[k] = round(v / total_calls, 2)

        df = (
            pd.DataFrame(percent.items())
            .set_index(0)
            .rename({1: "Percentage"}, axis=1)
        )

        concat_df = pd.concat([df, value_counts], axis=1)

        return concat_df


class ScheduleOnce:
    def __init__(self, url, headers):
        """This module is used with the Schedule Once API to get TC Booked and
        TC Scheduled Data from our clients

        You can see all uses for the API here:
        https://developers.oncehub.com/reference/introduction

        Args:
            url (str): URL for Schedule Once API, usually:
            https://api.oncehub.com/v2/bookings?

            headers (dictionary): Parameters for the API. Usually:
            {"Accept": "application/json",
            "API-Key": "API KEY"}
        """

        self.url = url
        self.headers = headers

    def getBookingData(self, params):
        """Gets all data from the Schedule Once API based on given parameters

        Args:
            params (dictionary): Dictionary of parameters, taken from the
            Schedule Once API reference. Usually used with starting_time and
            creation_time

        Returns:
            list: List of booking objects (dictionaries)
        """

        url = self.url
        bookings = list()

        while True:
            response = requests.request(
                "GET", url=url, headers=self.headers, params=params
            ).json()["data"]

            for i in response:
                bookings.append(i)

            if len(response) >= 100:
                url = (
                    "https://api.oncehub.com/v2/bookings?after="
                    + bookings[-1]["id"]
                    + "&limit=100&expand=booking_page"
                )

            elif len(response) < 100:
                break

        return bookings

    def getValueCountsFromDict(self, data):
        """Takes in a given data set and gives the value counts of the sources
        of the data

        Args:
            data (list): List of bookings (dictionaries) with booking data

        Returns:
            dataframe: 2 column dataframe with the booking page name and source
            as columns. Source is Value Counts
        """

        booking_data = list()
        for booking in data:
            page_source_name = dict()
            page_source_name["Name"] = booking["form_submission"]["name"]
            page_source_name["Page Name"] = booking["booking_page"]["label"]
            try:  # If booked on certain link, there is not a custom field,
                # though we know what the source is
                page_source_name["Source"] = booking["form_submission"][
                    "custom_fields"
                ][0]["value"]
            except:
                page_source_name["Source"] = "Inbound Triage"
            booking_data.append(page_source_name)

        vc = (
            pd.DataFrame(booking_data)
            .groupby("Page Name")["Source"]
            .value_counts()
        )

        return vc


class SSBTotals:
    def __init__(self) -> None:
        """Main class that houses functions to pull data

        Args:
            start_date (datetime.date): The start date used to pull SS Total
            end_date (datetime.date): The end date used to pull SS Total
        """

    @staticmethod
    def getSSForEachDayInDayList(sheet, day_list):
        """Gives the amount of SS booked in a given time period

        Args:
            sheet (gspread.worksheet): Worksheet from a gspread workbook
            day_list (list): List of datetime.date objects to check

        Returns:
            int: Returns int of the amount of SS booked in that time period
        """
        df = change_date_column_in_df_to_datetime(sheet)
        totals = dict()
        list_of_values = list()
        for day in day_list:
            list_of_values.append(df[df["Date"] == day]["Total SSB"].values[0])

        total = sum([i for i in list_of_values if i])
        totals[sheet.title] = total

        return totals

    def getTotalsDataframe(self, gc, day_list):
        """Pulls together all the client SS totals and puts them in dataframe

        Returns:
            df: Dataframe with total SSB based on Timeframe
        """
        totals = dict()

        daily_kpis = gc.open_by_url(DAILY_KPIS_URL)

        for sheet in daily_kpis:
            try:
                totals.update(self.getSSForEachDayInDayList(sheet, day_list))

            except Exception as e:
                print(f"{sheet.title}: {e}")

        totals_df = pd.DataFrame(totals.items()).sort_values(by=1)

        return totals_df


class Close:
    def __init__(self, api) -> None:
        self.api = api

    def get_total_metrics_from_close(self, start, end, metrics):
        data = {
            "datetime_range": {
                "start": start,
                "end": end,
            },
            "type": "overview",
            "metrics": metrics,
        }

        metric_dict = self.api.post("report/activity", data=data)
        totals_for_each_metric = metric_dict["aggregations"]["totals"]
        totals_df = (
            pd.DataFrame(totals_for_each_metric.items())
            .rename({0: "Metric", 1: "Count"}, axis=1)
            .set_index("Metric")
        )

        return totals_df

    def count_ss_booked(self, df, search_date):
        desired_rows = ["Name", "Email", "Taken Date", "Source", "Client Name"]
        df["Taken Date"] = pd.to_datetime(df["Taken Date"])
        df["Taken Date"] = df["Taken Date"].apply(lambda x: x.date())
        new_df = df[desired_rows][df["Taken Date"] == search_date]
        ss_count = (
            pd.DataFrame(new_df).groupby("Client Name")["Source"].value_counts()
        )

        return ss_count
