from __future__ import absolute_import
from datetime import timedelta, datetime, date
from calendar import monthrange

import unittest


def tofirstdayinisoweek(year, week):
    """Code taken from http://stackoverflow.com/questions/5882405

    %W takes the first Monday to be in week 1 but ISO defines week
    1 to contain 4 January. So the result from
    datetime.strptime('2011221', '%Y%W%w') is off by one iff the first
    Monday and 4 January are in different weeks. The latter is the
    case if 4 January is a Friday, Saturday or Sunday. So the
    following should work"""

    ret = datetime.strptime('%04d-%02d-1' % (year, week), '%Y-%W-%w')
    if date(year, 1, 4).isoweekday() > 4:
        ret -= timedelta(days=7)
    return ret


def get_current_week():
    return datetime.now().isocalendar()[:2]


def get_next_week(year, week):
    current = tofirstdayinisoweek(year, week)
    d = current + timedelta(days=7)
    return d.isocalendar()[:2]


def get_prev_week(year, week):
    current = tofirstdayinisoweek(year, week)
    d = current - timedelta(days=7)
    return d.isocalendar()[:2]


def get_month_from_week(year, week):
    d = tofirstdayinisoweek(year, week)
    return d.timetuple()[:2]


def get_week_from_day(year, month, day):
    d = date(year, month, day)
    return d.isocalendar()[:2]


def get_current_month():
    return datetime.now().timetuple()[:2]


def get_next_month(year, month):
    _, days = monthrange(year, month)
    d = date(year, month, 1) + timedelta(days=days)
    return d.timetuple()[:2]


def get_prev_month(year, month):
    d = date(year, month, 1) - timedelta(days=1)
    return d.timetuple()[:2]


def get_current_day():
    return datetime.now().timetuple()[:3]


def get_next_day(year, month, day):
    d = date(year, month, day) + timedelta(days=1)
    return d.timetuple()[:3]


def get_prev_day(year, month, day):
    d = date(year, month, day) - timedelta(days=1)
    return d.timetuple()[:3]


class DayTestCase(unittest.TestCase):
    def test_that_next_day_increases_day(self):
        self.assertEquals((2011, 2, 2), get_next_day(2011, 2, 1))

    def test_that_next_day_wraps_month(self):
        self.assertEquals((2011, 2, 1), get_next_day(2011, 1, 31))

    def test_that_next_day_wraps_year(self):
        self.assertEquals((2011, 1, 1), get_next_day(2010, 12, 31))

    def test_that_prev_day_decreases_day(self):
        self.assertEquals((2011, 2, 1), get_prev_day(2011, 2, 2))

    def test_that_prev_day_wraps_month(self):
        self.assertEquals((2011, 1, 31), get_prev_day(2011, 2, 1))

    def test_that_prev_day_wraps_year(self):
        self.assertEquals((2010, 12, 31), get_prev_day(2011, 1, 1))


class MonthTestCase(unittest.TestCase):
    def test_that_next_month_increases_month(self):
        self.assertEquals((2011, 2), get_next_month(2011, 1))

    def test_that_next_month_wraps_year(self):
        self.assertEquals((2012, 1), get_next_month(2011, 12))

    def test_that_prev_month_decreases_month(self):
        self.assertEquals((2011, 2), get_prev_month(2011, 3))

    def test_that_prev_month_wraps_year(self):
        self.assertEquals((2011, 12), get_prev_month(2012, 1))

    def test_that_month_from_week_exists(self):
        self.assertEquals((2011, 2), get_month_from_week(2011, 9))


class WeekTestCase(unittest.TestCase):
    def test_that_tofirstdayinisoweek_finds_monday_31_dec_2012(self):
        d = tofirstdayinisoweek(2013, 1).date()
        self.assertEquals(date(2012, 12, 31), d)

    def test_that_tofirstdayinisoweek_finds_monday_2_jan_2012(self):
        d = tofirstdayinisoweek(2012, 1).date()
        self.assertEquals(date(2012, 1, 2), d)

    def test_that_prev_week_decreases_week(self):
        self.assertEquals((2011, 8), get_prev_week(2011, 9))

    def test_that_next_week_increases_week(self):
        self.assertEquals((2011, 10), get_next_week(2011, 9))

    def test_that_prev_week_decreases_week(self):
        self.assertEquals((2011, 8), get_prev_week(2011, 9))

    def test_that_next_week_wraps_year(self):
        self.assertEquals((2012, 1), get_next_week(2011, 52))

    def test_that_prev_week_wraps_year(self):
        self.assertEquals((2011, 52), get_prev_week(2012, 1))

    def test_that_week_from_day_exists(self):
        self.assertEquals((2011, 6), get_week_from_day(2011, 2, 9))

if __name__ == "__main__":
    unittest.main()
