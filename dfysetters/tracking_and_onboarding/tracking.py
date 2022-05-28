"""This module houses all of the functions needed to pull data from a CSV 
(or Google Sheet) with  Facebook message data, and pull the necessary metrics 
from it """


import pandas as pd
import numpy as np
from statistics import mean
import pandas as pd
from helper.constants import *
from helper.common import change_date_column_in_df_to_datetime


class UnansweredMessages:
    def __init__(self, workbook):
        """This class has fucntions that allow you to pass in a sheet and a
        desired name, and check how many unanswered messages that name has

        Args:
            workbook (gspread.Workbook): This workbook should have sheets of
            dowloaded messages from Facebook with Timestamp, Conversation and
            message body columns
        """
        self.workbook = workbook

    def get_sheet_values_to_dataframe(self, sheet):
        """Uses the sheet attribute to get the data needed and return a
        dataframe and grouped dataframe of that data

        Args:
            sheet (gspread.worksheet): Google sheet with message data

        Returns:
            dataframe: Dataframe of all messages in the given sheet, with
            removed empty values
        """
        message_data = sheet.get_all_records()
        cleaned_message_list = [
            i for i in message_data if (len(i["Conversation"]) > 2)
        ]
        message_dataframe = pd.DataFrame(cleaned_message_list)
        return message_dataframe

    def count_unanswered(self, regular_dataframe, sheet):
        """Gives a number of unanswered messages in a certain sheet based on
        the specialist name

        Args:
            regular_dataframe (dataframe): regular dataframe from the list of
            dictionaries generated from a worksheet object

            sheet (gspread.worksheet): Google sheet with message data

        Returns:
            int: Returns a number that represents how many unanswered
            messages there are
        """

        list_of_last_senders = list()
        message_groups = regular_dataframe.groupby(["Conversation"])[
            "Timestamp (ms)"
        ].max()
        specialist = sheet.title[9:].capitalize()
        for row in message_groups:
            last_message_sender = regular_dataframe.loc[
                regular_dataframe["Timestamp (ms)"] == row
            ]["Sender"].values[0]
            list_of_last_senders.append(last_message_sender)

        first_names = [l.split()[0] for l in list_of_last_senders if l]
        last_sender_count = len(first_names) - first_names.count(specialist)

        return last_sender_count

    def get_all_unanswered(self):
        """_summary_

        Args:
            workbook (gspread.Workbook): This workbook should have sheets of
            dowloaded messages from Facebook with Timestamp, Conversation and
            message body columns

        Returns:
            dict: Returns dictionary of how many unanswered messages are in
            each sheet of the workbook, keyed by sheet title
        """
        average_per_sheet = dict()
        for sheet in self.workbook:
            df = UnansweredMessages(
                self.workbook
            ).get_sheet_values_to_dataframe(sheet)
            count = UnansweredMessages(self.workbook).count_unanswered(
                df, sheet
            )
            average_per_sheet[sheet.title] = count

        return average_per_sheet


class AveragePerConversation:
    def __init__(self, sheet):
        """This class passes in a sheet and gives the average amount of time
        elapsed between each message

        Args:
            sheet (gspread.models.Worksheet): This sheet should have a column
            with a list of messages sent, along with who sent them, the time
            it was sent and which overall conversation those messages belong to
        """

        self.sheet = sheet

    def getProspectNamesInDictionary(self):
        """This gets a dictionary of all of the conversation labels in the sheet
        with all of the message time stamps for that conversation

        Returns:
            dict: key: Conversation label value: List of timestamps
        """

        df = pd.DataFrame(self.sheet.get_all_records())
        timestamp_df = df.groupby(["Conversation", "Timestamp (ms)"])[
            "Timestamp (ms)"
        ].unique()
        names = [i for i in df["Conversation"].values if i]
        dictionary_of_reply_times = dict()
        for name in names:
            dictionary_of_reply_times[name] = (
                timestamp_df[name].astype(int).tolist()
            )

        return dictionary_of_reply_times

    def getAverageReplyTimePerConversation(self, reply_time_dict, name):
        """Gives the average time between timestamps in a dictionary of lists,
        keyed by the conversation name

        Args:
            reply_time_dict (dict): Key: Conversation, Value: List of timestamps
             for each message in that conversation

            name (str): Which key to check the average for, usually used in a
            for loop in other function

        Returns:
            np.nan / float: Returns float of average ms between reply times. If
            certain key does not have average, returns nan to use in future math
        """
        reply_times = list()
        for index, time in enumerate(reply_time_dict[name]):
            if index + 1 == len(reply_time_dict[name]):
                pass
            else:
                first_message_time = reply_time_dict[name][index]
                next_message_time = reply_time_dict[name][index + 1]
                reply_times.append(next_message_time - first_message_time)

        if len(reply_times) < 1:
            return np.nan  # Used for calculating averages in later step
        else:
            return mean(reply_times)

    def getAverageMinutesToReplyForAllConversations(self, reply_time_dict):
        """Gets the overall average reply time in a dictionary of lists

        Args:
            reply_time_dict (dict): [Key: Conversation, Value: List of
            timestamps for each message in that conversation

        Returns:
            float: Minutes on average that it took us to reply
        """
        list_of_averages = list()
        for name in reply_time_dict:
            avg_time = self.getAverageReplyTimePerConversation(
                reply_time_dict, name
            )
            list_of_averages.append(str(avg_time))

        cleaned_averages = [float(i) for i in list_of_averages if i != "nan"]

        return round(mean(cleaned_averages) / 60000, 2)


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

    def getTotalsDataframe(self, kpis_sheet, day_list):
        """Pulls together all the client SS totals and puts them in dataframe

        Returns:
            df: Dataframe with total SSB based on Timeframe
        """
        totals = dict()

        for sheet in kpis_sheet:
            try:
                totals.update(self.getSSForEachDayInDayList(sheet, day_list))

            except Exception as e:
                pass

        totals_df = pd.DataFrame(totals.items()).sort_values(by=1)

        return totals_df
