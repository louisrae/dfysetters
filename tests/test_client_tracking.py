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

gc = gspread.oauth()
app_set = gc.open_by_url(
    "https://docs.google.com/spreadsheets/d/1_tY48qkxcJBiFiGfSFo_IZo2Bop2N-HtH8rfBwvzoB8/edit#gid=790164004"
).worksheet("Appointments Set")


class TestSalesData:
    def test_MonthAndDayColumn(self):
        df = SalesData(app_set).createMonthAndDayColumns()
        assert (
            "SS Outcome" in df.columns
            and "SS Date" in df.columns
            and "Month" in df.columns
            and "Day" in df.columns
        )

    def test_OutputHasFullPercentageAndValueCounts(self):
        df = SalesData(app_set).createMonthAndDayColumns()
        vc = SalesData(app_set).getOutcomesFromDateRange(df)
        o = SalesData(app_set).getDataframeOfOutcomesCountsandPercentages(vc)

        assert o["Percentage"].sum() == 1.0
        assert o["SS Outcome"].sum() == 21


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


initial_date = datetime.datetime(2022, 3, 7)
days_in_future = 1
api = Client(CLOSE_API)
start = str(initial_date) + "Z"
end = str(initial_date + datetime.timedelta(days_in_future)) + "Z"

gc = gspread.oauth()
sheet = gc.open_by_url(APPOINTMENTS_SET_URL).worksheet("Full List Of Sets")


metrics = [
    "calls.outbound.all.count",
    "sms.sent.all.count",
    "emails.sent.all.count",
    "emails.opened.all.count",
    "emails.sent.manual_with_reply.count",
    "sms.received.all.count",
    "leads.contacted.all.count",
]


class TestClose:
    def test_getCorrectNumbersFromAPI(self):
        resp = Close(api).get_total_metrics_from_close(start, end, metrics)
        assert resp["Count"].sum() == 1822

    def test_getAllSSBookingsForDay(self):
        df = pd.DataFrame(sheet.get_all_records())
        ss = Close(api).count_ss_booked(df, initial_date.date())
        assert sum(ss) == 22
