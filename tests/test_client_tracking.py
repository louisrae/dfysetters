import src_path
import pytest
import gspread
from datetime import date
import datetime
import pandas as pd
import gspread

from closeio_api import Client
from helper.constants import *
from helper.common import *
from tracking_and_onboarding.client_tracking import *
from helper.credentials.apis import CLOSE_API


class TestSalesData:

    gc = gspread.oauth()
    app_set = gc.open_by_url(APP_SET_SHEET_URL).worksheet("Appointments Set")

    def test_MonthAndDayColumn(self):
        df = SalesData(self.app_set).createMonthAndDayColumns()
        assert (
            "SS Outcome" in df.columns
            and "SS Date" in df.columns
            and "Month" in df.columns
            and "Day" in df.columns
        )

    def test_OutputHasFullPercentageAndValueCounts(self):
        df = SalesData(self.app_set).createMonthAndDayColumns()
        vc = SalesData(self.app_set).getOutcomesFromDateRange(df)
        o = SalesData(self.app_set).getDataframeOfOutcomesCountsandPercentages(
            vc
        )

        assert o["Percentage"].sum() == 0.99
        assert o["SS Outcome"].sum() == 493


class TestScheduleOnce:

    from_date = None
    to_date = None

    def setup(cls):
        cls.from_date = str(datetime.date(2022, 2, 21))
        cls.to_date = str(datetime.date(2022, 2, 22))

    @pytest.fixture()
    def scheduleonce(self):
        scheduleonce = ScheduleOnce(SCHEDULE_ONCE_URL, SCHEDULE_ONCE_HEADERS)
        return scheduleonce

    def test_allTCScheduledInValueCounts(self, scheduleonce):
        scheduled_params = {
            "starting_time.gt": self.from_date,
            "starting_time.lt": self.to_date,
        }

        scheduled = scheduleonce.getBookingData(scheduled_params)
        tcs = ScheduleOnce(
            SCHEDULE_ONCE_URL, SCHEDULE_ONCE_HEADERS
        ).getValueCountsFromDict(scheduled)

        assert tcs.values.sum() == 71

    def test_allTCBookedInValueCounts(self, scheduleonce):
        booked_params = {
            "creation_time.gt": self.from_date,
            "creation_time.lt": self.to_date,
        }

        booked = scheduleonce.getBookingData(booked_params)
        tcb = ScheduleOnce(
            SCHEDULE_ONCE_URL, SCHEDULE_ONCE_HEADERS
        ).getValueCountsFromDict(booked)

        assert tcb.values.sum() == 60


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


class TestClose:

    gc = gspread.oauth()
    sets_sheet = gc.open_by_url(APPOINTMENTS_SET_URL).worksheet(
        "Full List Of Sets"
    )
    initial_date = datetime.datetime(2022, 3, 7)
    api = Client(CLOSE_API)
    start = str(initial_date) + "Z"
    end = str(initial_date + datetime.timedelta(1)) + "Z"

    def test_getCorrectNumbersFromAPI(self):
        resp = Close(self.api).get_total_metrics_from_close(
            self.start, self.end, CLOSE_METRICS
        )
        assert resp["Count"].sum() == 1831

    def test_getAllSSBookingsForDay(self):
        df = pd.DataFrame(self.sets_sheet.get_all_records())
        ss = Close(self.api).count_ss_booked(df, self.initial_date.date())
        assert sum(ss) == 22
