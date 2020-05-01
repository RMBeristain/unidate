"""
    Unit tests to verify correct functionality of unidate.py
    ========================================================

    Requires pytest and python3.6+

    To run from command line (bash shown. Windows left as an exersise for the reader):
    ```
        $ pytest -x -vv
    ```
"""
import random
import unidate as ud
from copy import deepcopy
from datetime import datetime
from pytest import fixture, raises
from typing import NamedTuple
from unidate import InvalidUnifiedDateValue

YEAR_OFFSET = 5600  # Unified Calendar sets "Year zero" at the invention of writing, this many years "AD"


@fixture
def fixed_date():
    "Set up instance with know fixed date 2019-12-30"
    return ud.UnifiedDate("2019-12-30")


@fixture
def today():
    "Today's system date"
    return datetime.strftime(datetime.now(), "%Y-%m-%d")


@fixture
def gregorian_years():
    "five Gregorian years, including a known leap year"
    return set(tuple(random.sample(range(1901, 2200), k=5)) + (2020,))  # yes, there's a chance we end up with one less


@fixture
def instance():
    return ud.UnifiedDate()


def is_leap(year):
    "Aux function to calculate if Gregorian year is a leap year"
    return year if (year % 4 == 0 and (year % 100 or (year % 100 == year % 400 == 0))) else None


class TestInstance_OK:
    "Everything does what it says on the tin"

    def test_Class_is_callable(self):
        "Class is callable directly"
        assert ud.UnifiedDate()

    def test_instance_is_populated(self):
        "An instance has all the date fields we expect, and those fields have values."
        u = ud.UnifiedDate()
        date_fields = (u.unified_date, u.swt_date, u.austral_date)

        assert isinstance(u, ud.UnifiedDate)
        assert isinstance(u.__str__(), str)

        # all date properties must have a value
        for ppty in date_fields:
            assert ppty

        # all date properties must be present
        assert all(ppty._fields == ("weekday", "day", "month", "year") for ppty in date_fields)

        # all date properties must be named tuples
        assert all(
            (ppty._fields and isinstance(getattr(ppty, field), NamedTuple) for field in ppty._fields)
            for ppty in date_fields
        )  # all properties of UnifiedDate are named tuples

    def test_known_date_has_correct_values(self, fixed_date):
        "An instance started with a known date has correct values in all properties."
        u = fixed_date

        assert u.gregorian_date == "2019-12-30"
        assert u.unified_date == ((1, 6, 360), ("Sixthday", 18), ("Quarter four-E", (4, 5)), 7619)
        assert u.swt_date.month.name == "Winter chill"
        assert u.austral_date.month.name == "Summer break"
        assert u.unified_date.weekday == u.swt_date.weekday == u.austral_date.weekday
        assert u.unified_date.month.numeric == u.swt_date.month.numeric == u.austral_date.month.numeric
        assert u.unified_date.year == u.swt_date.year == u.austral_date.year

    def test_str_and_repr_have_correct_values(self, fixed_date):
        u = fixed_date
        _str = u.__str__()

        assert u.__repr__() == _str
        assert "2019-12-30" in _str
        assert "7619-45-18" in _str
        assert "Winter chill" in _str
        assert "Summer break" in _str

    def test_same_Nth_day_always_repeats(self, gregorian_years):
        "The same day number in any year (e.g. the 154th day) always falls on the same Unified date."
        u = ud.UnifiedDate()
        days_of_year = range(1, 366)
        _number_of_years = len(gregorian_years)

        for day in days_of_year:
            unidate_years = []
            _yer_set = set()
            _mon_set = set()
            _wdy_set = set()
            _day_set = set()

            for year in gregorian_years:
                # get unified dates for the same Nth day of the year in different years
                _date = datetime.strptime("{} {}".format(year, day), "%Y %j")  # Nth day to Gregorian date
                unidate_years.append(u.unify(_date.strftime("%Y-%m-%d")))  # Unify date and append it

            for this_date in unidate_years:
                # Collect unified date properties for every unidate/year.
                _yer_set.add(getattr(this_date, "year"))
                _mon_set.add(getattr(this_date, "month"))
                _wdy_set.add(getattr(this_date, "weekday"))
                _day_set.add(getattr(this_date, "day"))

            assert len(_yer_set) == _number_of_years  # all years are different
            assert len(_mon_set) == 1  # but we always get the same month tuple for same Nth day of the year any year
            assert len(_wdy_set) == 1  # and always same weekday tuple and day number
            assert len(_day_set) == 1  # and always same day tuple

    def test_leap_years(self):
        "Leap years are handled correctly."
        u = ud.UnifiedDate()

        LEAP = ()
        while len(LEAP) <= 10:
            # get 10 random leap years in the '0001 AD' - '4399 BC'  supported range
            gregorian_year = is_leap(random.randint(1, 4399))
            if gregorian_year:
                LEAP += (gregorian_year,)
        else:
            for gregorian_year in LEAP:
                unified_year = gregorian_year + YEAR_OFFSET

                u.unify("{:04d}-02-29".format(gregorian_year))  # Gregorian leap day
                # these values are always the same regardless of gregorian_year. Default format is _Unified Long_
                assert u.unified_date.weekday == (1, 5, 59)
                assert u.unified_date.day == ("Fifthday", 5)
                assert u.unified_date.month.name == "Quarter one-D"
                assert u.unified_date.month.numeric.quarter == 1
                assert u.unified_date.month.numeric.month == 4
                assert u.unified_date.year == unified_year  # only the gregorian_year changes

                # Other formats
                _unified_short = u.format_date("Unified", "Short")
                assert _unified_short == "D5 5, Q1D {:04d}".format(unified_year)
                assert u.format_date("Unified", "Long") == "Fifthday 05, Quarter one-D {}".format(unified_year)
                assert u.format_date("Unified", "ISO") == "{:04d}-14-05".format(unified_year)
                assert u.format_date("SWT", "Long") == "Fifthday 05, Spring low {}".format(unified_year)
                assert u.format_date("SWT", "Short") == _unified_short
                assert u.format_date("Austral", "Long") == "Fifthday 05, Autumn start {}".format(unified_year)
                assert u.format_date("Austral", "Short") == _unified_short

                # The last day of a Unified year is always the festive date "Year End", and always corresponds to the
                # 30th of December, because in the Unified calendar Leap day is inserted in at the end, not in February.
                u.unify("{:04d}-12-30".format(gregorian_year))
                assert u.unified_date.weekday == (0, 4, 365)
                assert u.unified_date.day == ("YE", 0)
                assert u.unified_date.month.name == "Year end"
                assert u.unified_date.month.numeric.quarter == 5  # Yes, quarter 5. Not everything makes sense in life!
                assert u.unified_date.month.numeric.month == 0  # At least festive dates aren't "months" ;)
                assert u.unified_date.year == unified_year

                # Unified leap year is always the last day of the year, and it always corresponds to 31st of Dec
                u.unify("{:04d}-12-31".format(gregorian_year))
                assert u.unified_date.weekday == (0, 5, 366)
                assert u.unified_date.day == ("LD", 0)
                assert u.unified_date.month.name == "Leap day"
                assert u.unified_date.month.numeric.quarter == 6  # Listen, we spoke about this...
                assert u.unified_date.month.numeric.month == 0
                assert u.unified_date.year == unified_year

    def test_reverse_year_works(self, fixed_date, instance, today):
        "function `reverse_year` returns correct Gregorian year from Unified year"
        # for known date
        assert fixed_date.gregorian_date == "2019-12-30"
        _uy = deepcopy(fixed_date.unified_date.year)
        _gy = fixed_date.reverse_year(_uy)
        assert _gy == 2019
        # for system date
        _this_year, *_ = today.split("-")
        _uy = deepcopy(instance.unified_date.year)
        _gy = instance.reverse_year(_uy)
        assert _gy == int(_this_year)

    def test_reverse_unidate_matches(self, gregorian_years):
        "function `reverse_unidate` returns correct Gregorian date"
        for year in gregorian_years:
            _to_uni = ud.UnifiedDate(f"{year}-01-01")
            _range = range(1, 367) if is_leap(year) else range(1, 366)

            for day in _range:
                _ = _to_uni.unify(datetime.strptime(f"{year}-{day:03}", "%Y-%j").strftime("%Y-%m-%d"))
                _original = deepcopy(_to_uni)
                _iso_uni = _to_uni.format_date(style="ISO")
                _greg_from_uni = _to_uni.reverse_unidate(_iso_uni)
                assert _greg_from_uni.strftime("%Y-%m-%d") == _original.gregorian_date


class TestInstance_Errors:
    "Houston..."

    def test_instance_raises_exception_with_invalid_date(self):
        with raises(ValueError):
            assert ud.UnifiedDate("not a date")

    def test_get_uniweek_raises_exception_with_invalid_days(self, instance):
        for bad_day in (0, 367, 543):
            with raises(InvalidUnifiedDateValue):
                assert instance.get_uniweek(days=bad_day)

    def test_format_date_fails_with_unknown_variant(self, instance):
        with raises(ValueError) as err:
            assert instance.format_date(variant="Mistake")
        assert str(err.value) == "Unknown variant: Mistake"

    def test_format_date_fails_without_date(self, instance):
        "`format_date` should complain if there's no valid date in the corresponding field for the variant specified."
        # Clear any existing dates
        instance.unified_date = None
        instance.swt_date = None
        instance.austral_date = None
        # Test
        for variant in ("Unified", "SWT", "Austral"):
            with raises(InvalidUnifiedDateValue) as err:
                assert instance.format_date(variant)
            assert str(err.value) == "None"


class TestInstance_Defaults:
    "Default behaviours when certain values aren't provided"

    def test_instance_has_correct_default_values(self, instance, today):
        "An instance started with no parameters has correct default of 'Today' in all properties."
        assert instance.gregorian_date == today
        assert instance.unified_date.weekday == instance.swt_date.weekday == instance.austral_date.weekday
        assert (
            instance.unified_date.month.numeric
            == instance.swt_date.month.numeric
            == instance.austral_date.month.numeric
        )
        assert instance.unified_date.year == instance.swt_date.year == instance.austral_date.year

    def test_today_method(self, today):
        "An instance started from `today` has correct values in all properties."
        u = ud.UnifiedDate.today()

        assert u.gregorian_date == today
        assert u.unified_date.weekday == u.swt_date.weekday == u.austral_date.weekday
        assert u.unified_date.month.numeric == u.swt_date.month.numeric == u.austral_date.month.numeric
        assert u.unified_date.year == u.swt_date.year == u.austral_date.year
