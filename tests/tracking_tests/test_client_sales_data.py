import src_path
from tracking.client_sales_data import SalesData
import pytest
import gspread

gc = gspread.oauth()
app_set = gc.open_by_url(
    "https://docs.google.com/spreadsheets/d/1_tY48qkxcJBiFiGfSFo_IZo2Bop2N-HtH8rfBwvzoB8/edit#gid=790164004"
).worksheet("Appointments Set")


@pytest.fixture
def salesdata():
    salesdata = SalesData(app_set)
    return salesdata


def test_MonthAndDayColumn(salesdata):
    df = salesdata.createMonthAndDayColumns()
    assert (
        "SS Outcome" in df.columns
        and "SS Date" in df.columns
        and "Month" in df.columns
        and "Day" in df.columns
    )


def test_OutputHasFullPercentageAndValueCounts(salesdata):
    df = salesdata.createMonthAndDayColumns()
    vc = salesdata.getOutcomesFromDateRange(df)
    o = salesdata.getDataframeOfOutcomesCountsandPercentages(vc)

    assert o["Percentage"].sum() == 1.0
    assert o["SS Outcome"].sum() == 15
