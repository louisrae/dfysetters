import src_path
from helper.common import get_day_list
import datetime


def test_canGetDayList():
    start = datetime.date(2022, 2, 20)
    end = datetime.date(2022, 2, 28)
    list = get_day_list(start, end)
    assert "2022-02-21" in list