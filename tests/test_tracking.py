import src_path
import gspread
import pytest
from tracking_and_onboarding.tracking import *
from helper.constants import *
from helper.roles import *
import src_path
import gspread
from datetime import date
import gspread
from helper.constants import *
from helper.common import *
from tracking_and_onboarding.tracking import *

gc = gspread.oauth()
daily_kpis = gc.open_by_url(DAILY_KPIS_URL)


class TestUnansweredMessages:
    gc = gspread.oauth()
    message_data_workbook = gc.open_by_url(MESSAGE_DATA_WORKBOOK)

    @pytest.fixture()
    def tracking(self):
        tracking = UnansweredMessages(self.message_data_workbook)
        return tracking

    def test_specialistIsInDataframe(self, tracking):
        df = tracking.get_sheet_values_to_dataframe(
            self.message_data_workbook.sheet1
        )
        assert "Tylee Evans Groll" in list(df["Sender"].values)

    def test_canPerformMathOnTimestamp(self, tracking):
        d = tracking.get_all_unanswered()
        assert 50 == sum(d.values())


class TestAveragePerConversation:
    @pytest.fixture()
    def average(self):
        gc = gspread.oauth()
        message_data_workbook = gc.open_by_url(MESSAGE_DATA_WORKBOOK)
        average = AveragePerConversation(message_data_workbook.sheet1)
        return average

    def test_DictionaryHasTimetampValues(self, average):
        d = average.getProspectNamesInDictionary()
        total_timestamps = sum([sum(ls) for ls in list(d.values())])
        assert total_timestamps == 60763938034603

    def test_DictionaryReturnsCorrectAverage(self, average):
        d = average.getProspectNamesInDictionary()
        avg = average.getAverageMinutesToReplyForAllConversations(d)
        assert avg == 6.62


class TestWeeklyTotals:

    start = None
    end = None
    gc = None

    def setup(cls):
        cls.start = date(2022, 1, 1)
        cls.end = date(2022, 1, 2)
        cls.gc = gspread.oauth()

    def test_canWTDListOfDaysIsListAndContainsDates(self):
        days = get_day_list(self.start, self.end)
        first_date = days[0]
        assert isinstance(days, list) and "2022" in first_date

    def test_canMTDListOfDaysIsListAndContainsDates(self):
        days = get_day_list(self.start, self.end)
        first_date = days[0]
        assert isinstance(days, list) and "2022" in first_date

    def test_allClientsAreInDataframe(self):
        days = get_day_list(self.start, self.end)
        ss = SSBTotals().getTotalsDataframe(daily_kpis, days)
        assert sum(ss.index) == 325
