#!/usr/bin/env python

"""Tests for `pitrading` package."""


from pitrading.holidays import Holidays
import unittest

from pitrading import pitrading


class TestPitrading(unittest.TestCase):
    """Tests for `pitrading` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""
        Holidays.tradingday("20200501")
        Holidays.tradingday("20190501")
        Holidays.tradingday("20180501")
        Holidays.tradingday("20170501")
        Holidays.tradingday("20160501")
