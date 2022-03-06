import src_path
import pandas as pd
from helper.constants import DAY_NUMBER_WEEK_AGO, MONTH_NUMBER_WEEK_AGO


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
