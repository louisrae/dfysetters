import src_path
from tracking.weekly_totals import SSBTotals
from helper.constants import *
from helper.common import *
import gspread
from datetime import date


class TestWeeklyTotals:

    start = None
    end = None
    gc = None

    def setup(cls):
        cls.start = date(2022, 1, 1)
        cls.end = date(2022, 1, 15)
        cls.gc = gspread.oauth(
            credentials_filename=GSPREAD_CREDENTIALS,
            authorized_user_filename=AUTHORIZED_USER,
        )

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
        ss = SSBTotals(self.start, self.end).getTotalsDataframe(self.gc, days)
        assert sum(ss.index) == 406
