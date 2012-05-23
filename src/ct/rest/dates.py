from __future__ import absolute_import
from datetime import datetime, date

import unittest

def get_year_and_week_number(date):
    return date.isocalendar()[:2]


def get_current_week():
    return get_year_and_week_number(datetime.now())


class WeekTestCase(unittest.TestCase):
    def test_get_year_and_week_number(self):
        self.assertEquals((2013, 1),
                          get_year_and_week_number(date(2012, 12, 31)))


if __name__ == "__main__":
    unittest.main()
