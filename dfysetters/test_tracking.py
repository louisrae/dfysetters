import gspread

from datetime import date

from roles import *
from common import *
from constants import *
from main import *

gc = gspread.oauth()
daily_kpis = gc.open_by_url(DAILY_KPIS_URL)


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
