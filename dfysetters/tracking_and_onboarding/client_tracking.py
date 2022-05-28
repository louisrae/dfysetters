import src_path
import pandas as pd
from helper.constants import *
from helper.common import change_date_column_in_df_to_datetime


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
            print("Run")

        total = sum([i for i in list_of_values if i])
        totals[sheet.title] = total

        return totals

    def getTotalsDataframe(self, kpis_sheet, day_list):
        """Pulls together all the client SS totals and puts them in dataframe

        Returns:
            df: Dataframe with total SSB based on Timeframe
        """
        totals = dict()

        for sheet in kpis_sheet:
            try:
                totals.update(self.getSSForEachDayInDayList(sheet, day_list))
                print("Run")

            except Exception as e:
                print(e)

        totals_df = pd.DataFrame(totals.items()).sort_values(by=1)

        return totals_df
