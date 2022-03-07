import src_path
from tracking.weekly_totals import SSBTotals
from helper.common import get_day_list
import gspread
from datetime import date


class TestWeeklyTotals:

    start = None
    end = None
    gc = None

    def setup(cls):
        cls.start = date(2022, 1, 1)
        cls.end = date(2022, 1, 15)
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
        ss = SSBTotals().getTotalsDataframe(self.gc, days)
        assert sum(ss.index) == 406
