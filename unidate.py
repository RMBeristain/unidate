"""
    Unified Calendar
    ================

    Module to convert Gregorian calendar dates to Unified calendar dates as featured in the science-fiction novel

     A P A R T
     O F T H E
     W O R L D

    by R.M. Beristain


    To run on python interpreter:
    ```
        >>> from unidate import UnifiedDate as UD

        >>> ud = UD()                       # creates instance and initializes to today's date in Unified format.
        >>> ud.unify('YYYY-MM-DD')          # converts Gregorian ISO date to Unified date.
        >>> ud.reverse_unidate('YYY-QM-DD') # converts Unified ISO date to Gregorian date.
        >>> print(ud)                       # displays Gregorian date and various Unified date formats.
        >>> ud.print_calendar()             # prints this year's Unified calendar
    ```
    For more details see `help(unidate.UnifiedDate)`

    Requires Python 3.6+

    License
    -------
    This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Australia License.
    To view a copy of this license, visit http: //creativecommons.org/licenses/by-sa/3.0/au/
    or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
"""
__author__ = "R.M. Beristain"
__version__ = "1.0.0"
from collections import ChainMap, namedtuple
from datetime import datetime, timedelta
from math import trunc
from typing import Optional

UniWeekTuple = namedtuple("UnifiedWeek", "regular number yearday")
UniDayTuple = namedtuple("UnifiedDay", "name number")
UniMonthTuple = namedtuple("UnifiedMonth", "name numeric")
UQT = namedtuple("UnifiedQuarter", "quarter month")
UnifiedDateType = namedtuple("UnifiedDateType", "weekday day month year")


class InvalidUnifiedDateValue(ValueError):
    "Not a valid value for UnifiedDate"


class UnifiedDate:
    """
        Transform Gregorian dates to Unified.

        By default we Unify current system date if instantiated without parameters. To convert an arbitrary date,
        call your instance with an ISO 8601-formatted date string. E.g:
        ```
        udate=UnifiedDate('2015-04-20')
        ```
        You can also pass an ISO 8601-formatted date to an existing instance by calling the `unify` method.

        `UnifiedDate` can be printed to show Unified format along with Sout-Western Territory and Austral formats.

        Unified Calendar Year Zero starts at Gregorian 5600 BC. This program doesn't convert prehistoric dates.

        Parameters
        ----------
        - user_date: ISO 8601-format date string (e.g. '2019-01-01')

        Properties
        ----------
        - gregorian_date : ISO 8601-format date string (e.g. '2019-01-01')
        - unified_date: Unified Date named tuple containing the following fields:
            - UnifiedWeek tuple
            - UnifiedDay tuple
            - UnifiedMonth tuple
            - year: unified year
    """

    festive = [1, 92, 183, 274, 365, 366]
    festive_short = ["Q1", "Q2", "Q3", "Q4", "YE", "LD"]

    # Short-format unified month names. There are no short-format variants for Territorian or Austral.
    _unified_month_name_short = {
        "Q1": UniMonthTuple("Q10", UQT(1, 0)),
        1: UniMonthTuple("Q1A", UQT(1, 1)),
        2: UniMonthTuple("Q1B", UQT(1, 2)),
        3: UniMonthTuple("Q1C", UQT(1, 3)),
        4: UniMonthTuple("Q1D", UQT(1, 4)),
        5: UniMonthTuple("Q1E", UQT(1, 5)),
        "Q2": UniMonthTuple("Q20", UQT(2, 0)),
        6: UniMonthTuple("Q2A", UQT(2, 1)),
        7: UniMonthTuple("Q2B", UQT(2, 2)),
        8: UniMonthTuple("Q2C", UQT(2, 3)),
        9: UniMonthTuple("Q2D", UQT(2, 4)),
        10: UniMonthTuple("Q2E", UQT(2, 5)),
        "Q3": UniMonthTuple("Q30", UQT(3, 0)),
        11: UniMonthTuple("Q3A", UQT(3, 1)),
        12: UniMonthTuple("Q3B", UQT(3, 2)),
        13: UniMonthTuple("Q3C", UQT(3, 3)),
        14: UniMonthTuple("Q3D", UQT(3, 4)),
        15: UniMonthTuple("Q three E", UQT(3, 5)),
        "Q4": UniMonthTuple("Quarter four", UQT(4, 0)),
        16: UniMonthTuple("Q4A", UQT(4, 1)),
        17: UniMonthTuple("Q4B", UQT(4, 2)),
        18: UniMonthTuple("Q4C", UQT(4, 3)),
        19: UniMonthTuple("Q4D", UQT(4, 4)),
        20: UniMonthTuple("Q4E", UQT(4, 5)),
        "YE": UniMonthTuple("YE", UQT(5, 0)),
        "LD": UniMonthTuple("LD", UQT(6, 0)),
    }

    _unified_month_name_long = {
        "Q1": UniMonthTuple("Quarter one", UQT(1, 0)),
        1: UniMonthTuple("Quarter one-A", UQT(1, 1)),
        2: UniMonthTuple("Quarter one-B", UQT(1, 2)),
        3: UniMonthTuple("Quarter one-C", UQT(1, 3)),
        4: UniMonthTuple("Quarter one-D", UQT(1, 4)),
        5: UniMonthTuple("Quarter one-E", UQT(1, 5)),
        "Q2": UniMonthTuple("Quarter two", UQT(2, 0)),
        6: UniMonthTuple("Quarter two-A", UQT(2, 1)),
        7: UniMonthTuple("Quarter two-B", UQT(2, 2)),
        8: UniMonthTuple("Quarter two-C", UQT(2, 3)),
        9: UniMonthTuple("Quarter two-D", UQT(2, 4)),
        10: UniMonthTuple("Quarter two-E", UQT(2, 5)),
        "Q3": UniMonthTuple("Quarter three", UQT(3, 0)),
        11: UniMonthTuple("Quarter three-A", UQT(3, 1)),
        12: UniMonthTuple("Quarter three-B", UQT(3, 2)),
        13: UniMonthTuple("Quarter three-C", UQT(3, 3)),
        14: UniMonthTuple("Quarter three-D", UQT(3, 4)),
        15: UniMonthTuple("Quarter three-E", UQT(3, 5)),
        "Q4": UniMonthTuple("Quarter four", UQT(4, 0)),
        16: UniMonthTuple("Quarter four-A", UQT(4, 1)),
        17: UniMonthTuple("Quarter four-B", UQT(4, 2)),
        18: UniMonthTuple("Quarter four-C", UQT(4, 3)),
        19: UniMonthTuple("Quarter four-D", UQT(4, 4)),
        20: UniMonthTuple("Quarter four-E", UQT(4, 5)),
        "YE": UniMonthTuple("Year end", UQT(5, 0)),
        "LD": UniMonthTuple("Leap day", UQT(6, 0)),
    }

    _territorian = {
        1: UniMonthTuple("Winter freeze", UQT(1, 1)),
        2: UniMonthTuple("Winter wane", UQT(1, 2)),
        3: UniMonthTuple("Winter end", UQT(1, 3)),
        4: UniMonthTuple("Spring low", UQT(1, 4)),
        5: UniMonthTuple("Spring break", UQT(1, 5)),
        6: UniMonthTuple("Spring height", UQT(2, 1)),
        7: UniMonthTuple("Spring wane", UQT(2, 2)),
        8: UniMonthTuple("Spring end", UQT(2, 3)),
        9: UniMonthTuple("Summer low", UQT(2, 4)),
        10: UniMonthTuple("Summer break", UQT(2, 5)),
        11: UniMonthTuple("Summer height", UQT(3, 1)),
        12: UniMonthTuple("Summer wane", UQT(3, 2)),
        13: UniMonthTuple("Summer end", UQT(3, 3)),
        14: UniMonthTuple("Autumn low", UQT(3, 4)),
        15: UniMonthTuple("Autumn fall", UQT(3, 5)),
        16: UniMonthTuple("Autumn lull|height", UQT(4, 1)),
        17: UniMonthTuple("Autumn wane", UQT(4, 2)),
        18: UniMonthTuple("Autumn end", UQT(4, 3)),
        19: UniMonthTuple("Winter low", UQT(4, 4)),
        20: UniMonthTuple("Winter chill", UQT(4, 5)),
    }

    _austral = {
        1: UniMonthTuple("Summer height", UQT(1, 1)),
        2: UniMonthTuple("Summer wane", UQT(1, 2)),
        3: UniMonthTuple("Summer close", UQT(1, 3)),
        4: UniMonthTuple("Autumn start", UQT(1, 4)),
        5: UniMonthTuple("Autumn fall", UQT(1, 5)),
        6: UniMonthTuple("Autumn lull", UQT(2, 1)),
        7: UniMonthTuple("Autumn wane", UQT(2, 2)),
        8: UniMonthTuple("Autumn close", UQT(2, 3)),
        9: UniMonthTuple("Winter start", UQT(2, 4)),
        10: UniMonthTuple("Winter chill", UQT(2, 5)),
        11: UniMonthTuple("Winter lull", UQT(3, 1)),
        12: UniMonthTuple("Winter wane", UQT(3, 2)),
        13: UniMonthTuple("Winter close", UQT(3, 3)),
        14: UniMonthTuple("Spring start", UQT(3, 4)),
        15: UniMonthTuple("Spring break", UQT(3, 5)),
        16: UniMonthTuple("Spring run", UQT(4, 1)),
        17: UniMonthTuple("Spring wane", UQT(4, 2)),
        18: UniMonthTuple("Spring close", UQT(4, 3)),
        19: UniMonthTuple("Summer start", UQT(4, 4)),
        20: UniMonthTuple("Summer break", UQT(4, 5)),
    }

    _territorian_month_name_long = ChainMap(_territorian, _unified_month_name_long)  # type: ignore
    _austral_month_name_long = ChainMap(_austral, _unified_month_name_long)  # type: ignore
    _year_start: Optional[datetime] = None  # datetime object containing first day of date's year
    unified_date: Optional[UnifiedDateType] = None
    swt_date: Optional[UnifiedDateType] = None
    austral_date: Optional[UnifiedDateType] = None

    @classmethod
    def today(cls, style="Long"):
        "Create a UnifiedDate instance from today's date"
        return cls(datetime.now().date().isoformat(), style)

    def __init__(self, user_date: str, style: str = "Long") -> None:
        """
            Initialises default values

            Parameters
            ----------
            - user_date: Gregorian date in ISO 8601 format.
            - style - month representation style. Can be one of 'Long' or 'Short'
        """
        # This will validate it is (more or less) correct.
        user_date = datetime.strptime(user_date, '%Y-%m-%d').date().isoformat()
        self.gregorian_date = user_date
        self.unified_date = self.unify(user_date, style)

    def __str__(self) -> str:
        "returns unified date in a nice format"
        return (
            f"{'Gregorian:':<15}{self.gregorian_date:>10} - "
            f"{datetime.strptime(self.gregorian_date, '%Y-%m-%d').strftime('%A %d of %B, %Y')}\n"
            f"{'Unified ISO:':<15}{self.format_date(variant='Unified', style='ISO'):>10}\n"
            f"{'Unified Short:':<15}{self.format_date('Unified', style='Short')}\n"
            f"{'Unified Long:':<15}{self.format_date('Unified', 'Long')}\n"
            f"{'Territorian:':<15}{self.format_date('SWT', 'Long')}\n"
            f"{'Austral:':<15}{self.format_date('Austral', 'Long')}\n"
            f"\t{self.unified_date}\n"
        )

    def __repr__(self) -> str:
        return self.__str__()

    def format_date(self, variant: str = "Unified", style: str = "Long") -> str:
        """
            Return Unified Date formatted according to a regional variant (e.g. South-Western Territories).

            NOTE: Non-unified variants don't have a short-format name; they use the same as the Unified variant.
            If style="Short" is specified for "SWT" or "Austral" variants, `format_date` will return a short-format
            **string**, but the actual tuple stored will retain the Long name of the month for those variants. Only the
            day name is shortened.
            For example:

            ```
                >>> ud.format_date(variant='SWT', style='Short')
                'D4 4, Q2B 7620'

                >>> ud.swt_date.month.name
                'Spring wane'
            ```

            Parameters
            ==========
            - variant: Variant to use. One of ['Unified', 'SWT', 'Austral']
            - style: Date formatting style to use.
                - 'Long': "LongDayName day, LongMonthName Year" -- Thirday 3, Quarter two-B 7620
                - 'Short': "ShortDayName day, ShortMonthName Year" -- D3 3, Q2B 7620
                - 'ISO': ISO 8601U "Year-QuarterMonth-day" -- 7620-22-03 (Output is the same for all three variants)

            Returns:
            ========
            - Unified date in specified format.
        """
        if variant == "Unified":
            date = self.unified_date
        elif variant == "SWT":
            date = self.swt_date
        elif variant == "Austral":
            date = self.austral_date
        else:
            raise ValueError(f"Unknown variant: {variant}")

        style = style.strip().title()

        if style == "Iso":  # ISO 8601U "Unified ISO format"
            return f"{date.year}-{date.month.numeric.quarter}{date.month.numeric.month}-{date.day.number:02}"
        else:
            if date.weekday.regular:
                date = UnifiedDateType(  # replace existing date tuple with requested format
                    weekday=date.weekday,
                    day=self.get_uniday(
                        weekday=date.weekday,
                        # invalid or unknown formats are also displayed as 'Long'
                        style="Short" if style == "Short" else "Long",
                    ),
                    month=self.get_unimonth(weekday=date.weekday, variant=variant, style=style),
                    year=date.year,
                )

                if style == "Short":
                    _day_number = f"{date.day.number}"
                else:
                    _day_number = f"{date.day.number:02}"

                return f"{date.day.name} {_day_number}, {date.month.name} {date.year}"
            else:
                # festive
                return "{month} {year}".format(month=date.month.name, year=date.year)

    def get_uniweek(self, days: int) -> UniWeekTuple:
        """
            Parameters
            ==========
            - days: number (1..366) from any year.

            Returns:
            ========
            - UnifiedWeek namedtuple contaning:
                - regular - flag to indicate if date is regular or festive: 0=festive, 1=regular
                - number - numeric value for day of the week [1-6]
                - yearday - numeric value for day of the year [1-366]
        """
        if days in self.festive:
            return UniWeekTuple(0, self.festive.index(days), days)
        else:
            if 1 < days <= 91:
                days -= 1
            elif 92 < days <= 182:
                days -= 2
            elif 183 < days <= 273:
                days -= 3
            elif 274 < days <= 364:
                days -= 4
            else:
                raise InvalidUnifiedDateValue(f"Day out of range: {days!r}")

            return UniWeekTuple(1, (((days % 90) % 18) % 6) or 6, days)

    def get_uniday(self, weekday: UniWeekTuple, style: str = "Long") -> UniDayTuple:
        """
            Takes a UniWeekTuple and returns UniDayTuple with (name of the week day, date)

            If `style` is specified, return day name in that format. Applies only to regular week days; festive
            day names don't change.

            Parameters
            ----------
            - weekday: UniWeekTuple
            - style: Date formatting style to use.
                - 'Long': Long Day Name (e.g. Seconday)
                - 'Short': Short Day Name (e.g. D2)
        """
        month_day = ((weekday.yearday % 90) % 18) or 18
        if month_day < 1 or month_day > 18:
            raise UnvalidUnifiedDateValue(f"Invalid week tuple: {weekday!r}")
        if weekday.regular == 0:
            return UniDayTuple(self.festive_short[weekday.number], 0)
        if style == 'Long'
            WEEKDAYS = ["Firstday", "Seconday", "Thirday", "Fourthday", "Fifthday", "Sixthday"]
            wday_num = weekday.number % 6
            return UniDayTuple(WEEKDAYS[wday_num], month_day)
        return UniDayTuple(f"D{month_day}", month_day)

    def get_unimonth(self, weekday: UniWeekTuple, variant: str = "Unified", style: str = "Long") -> UniMonthTuple:
        """
            Take a unified weekday, return unified month.

            Parameters
            ----------
            - weekday - Unified weekday namedtuple
            - variant - Regional month name variant. Can be one of 'Unified', 'Austral', or 'SWT'
            - style - month representation style. Can be one of 'Long' or 'Short'
        """
        if weekday.regular:
            # date is a regular day
            month_number = int(trunc((weekday.yearday - 1) / 18.0)) + 1
            if month_number > 20:
                month_number = 20
        else:
            # date is a festivity. These months don't have number, only name.
            month_number = self.festive_short[weekday.number]  # use week day number as index

        if style.title() == "Short":
            # Return short style only if explicitely requested, else Long.
            return self._unified_month_name_short[month_number]

        variant = variant.strip()
        if variant.title() == "Austral":
            return self._austral_month_name_long[month_number]
        if variant.upper() == "SWT":
            return self._territorian_month_name_long[month_number]
        # invalid or unknown variants are returned as "Unified"
        return self._unified_month_name_long[month_number]

    def unify(self, user_date: str = "Today", style: str = "Long") -> UnifiedDateType:
        """
            Convert user-provided Gregorian date to Unified and Territorian dates.

            Takes a gregorian date string and returns a UnifiedDateType tuple containing:
            unified weekday tuple, unified day name tuple, unified month.

            Also populates SWT and Austral dates, but those aren't returned.

            NOTE: Only dates between 1AD and 9999AD in _Gregorian_ Calendar can be converted (but Julian dates
            aren't supported)

            Parameters
            ==========
            - user_date: ISO 8601-formatted Gregorian date (e.g. '2020-12-31'). Optionally accepts the sting 'Today' for
                current sytem date. If no value (None) is provided, defaults to 'Today'
            - style - month representation style. Can be one of 'Long' or 'Short'

            Returns:
            ========
            - Unified Date as UnifiedDateType {'weekday': UnifiedWeek, 'day': UnifiedDay, 'month': UnifiedMonth, 'year': year}
        """
        if not user_date or user_date.title() == "Today":
            user_date = datetime.now().date().isoformat()
        self.gregorian_date = user_date

        try:
            udate = datetime.strptime(user_date, "%Y-%m-%d")
        except ValueError:
            msg = f"Date {user_date!r} must be in ISO-8601 format (YYYY-MM-DD)"
            print(f"Sorry, {msg}")
            raise ValueError(msg)

        try:
            self._year_start = datetime.strptime(f"{udate.year:04}-01-01", "%Y-%m-%d")
        except ValueError as err:
            msg = f"Unable to process date {udate!r}: {err}"
            print(msg)
            raise ValueError(msg)

        days = udate.timetuple().tm_yday
        year = udate.year + 5600
        uni_weekday = self.get_uniweek(days)
        uni_day = self.get_uniday(uni_weekday, style=style)

        try:
            self.unified_date = UnifiedDateType(
                uni_weekday,
                uni_day,
                self.get_unimonth(weekday=uni_weekday, variant="Unified", style=style),
                year,
            )
            self.swt_date = UnifiedDateType(
                uni_weekday, uni_day, self.get_unimonth(weekday=uni_weekday, variant="SWT"), year
            )
            self.austral_date = UnifiedDateType(
                uni_weekday, uni_day, self.get_unimonth(weekday=uni_weekday, variant="Austral"), year
            )
        except Exception as e:
            print(f"Error {type(e)}:{e}. Values: weekday={uni_weekday}, day={uni_day}")
            raise
        else:
            return self.unified_date

    def print_calendar(self) -> None:  # pragma: no cover
        "Print entire year calendar for current Gregorian date"

        print(f"{'Gregorian':12} {'Unified':12} {'Long':36} {'Territorian':20} Austral")
        _save_date = self.gregorian_date
        year_start = self._year_start
        prev = None

        for d in range(0, 366):
            self.gregorian_date = (year_start + timedelta(days=d)).date().isoformat()
            self.unify(self.gregorian_date)
            iso = self.format_date("Unified", "ISO")
            uni = self.format_date("Unified")
            swt = self.swt_date.month.name
            aus = self.austral_date.month.name

            date = f"{self.gregorian_date:12} {iso:12} {uni:36} {swt:20} {aus}"

            if self.unified_date.weekday.regular == 0:
                print(f"\n{'=' * 104}")
            elif self.unified_date.month.name != prev:
                print(f"{'-' * 104}")

            if d < 365:
                print(date)
            elif self.unified_date.month.numeric.quarter == 6:
                print(date)

            prev = self.unified_date.month.name

        self.unify(_save_date)  # restore last used date.

    def print_festive(self) -> None:  # pragma: no cover
        """
            Print gregorian dates corresponding to unified festive dates
            in the year of current Gregorian date.
        """
        from datetime import timedelta
        from copy import deepcopy

        year_start = deepcopy(self._year_start)
        _save_date = self.gregorian_date

        for d in self.festive:
            self.gregorian_date = (year_start + timedelta(days=d - 1)).date().isoformat()
            self.unify(self.gregorian_date)
            print(f"{'_' * 50}\n{self}")

        self.unify(_save_date)

    def print_month(self) -> None:  # pragma: no cover
        "Print unified dates for the whole month corresponding to current Gregorian date."
        from calendar import monthrange

        print(f"\nMonth for Gregorian date {self.gregorian_date}\n{'^' * 40}\n")

        _save_date = self.gregorian_date
        gd = datetime.strptime(self.gregorian_date, "%Y-%m-%d")
        last_day = monthrange(gd.year, gd.month)[1]

        for d in range(1, last_day + 1):
            self.gregorian_date = datetime.strptime(f"{gd.year}-{gd.month:02}-{d:02}", "%Y-%m-%d").date().isoformat()
            self.unify(self.gregorian_date)
            if self.unified_date.month.numeric.month == 0:
                print(f'{self.gregorian_date}\t{self.format_date("Unified", "Long")}\n{"-" * 40}')
            elif self.unified_date.day.number == 1 and self.unified_date.month.numeric.month > 1:
                print(f'\n{self.gregorian_date}\t{self.format_date("Unified", "Long")}')
            else:
                print(f'{self.gregorian_date}\t{self.format_date("Unified", "Long")}')

        self.unify(_save_date)

    def reverse_year(self, unified_year: int) -> Optional[int]:
        """
            Parameter
            =========
            - unified_year: numeric Unified year

            Returns:
            ========
            - numeric Gregorian year
        """
        if unified_year is None:
            raise InvalidUnifiedDateValue("Invalid year value: None")
        else:
            try:
                unified_year = int(unified_year)
                if unified_year >= 0:
                    return unified_year - 5600
                else:
                    print("Sorry, cannot convert Unified prehistoric dates.")
                    return None
            except ValueError:
                raise InvalidUnifiedDateValue(f"{unified_year!r} - Not a valid year.")

    def reverse_unidate(self, u_date: str) -> datetime:
        """
            Convert Unified date string to Gregorian date.

            Parameters
            ==========
            - unified_date: ISO 8601U-formatted Unified Date string.

            Returns:
            ========
            - datetime object.
        """
        user_date = u_date
        try:
            _year, _quarter_month, _day = user_date.split("-")
            _year = int(_year)
            _quarter = int(_quarter_month[0])
            _month = int(_quarter_month[1])
            _day = int(_day)
        except Exception as err:
            print(f"{err}\nPlease enter Unified Date string in ISO 8601U format (YYYY-QM-DD)")
        else:
            _gyear = self.reverse_year(_year)  # Gregorian year

            if _month == 0:
                if _quarter == 1:
                    _gday = datetime.strptime(f"{_gyear}-001", "%Y-%j")
                elif _quarter == 2:
                    _gday = datetime.strptime(f"{_gyear}-092", "%Y-%j")
                elif _quarter == 3:
                    _gday = datetime.strptime(f"{_gyear}-183", "%Y-%j")
                elif _quarter == 4:
                    _gday = datetime.strptime(f"{_gyear}-274", "%Y-%j")
                elif _quarter == 5:
                    _gday = datetime.strptime(f"{_gyear}-365", "%Y-%j")
                elif _quarter == 6:
                    _gday = datetime.strptime(f"{_gyear}-366", "%Y-%j")
                else:
                    raise InvalidUnifiedDate(
                        f"{user_date!r} isn't a valid Unified Date. Please use a date in ISO 8601U format (YYYY-QM-DD)"
                    )
            else:
                _julian = (90 * (_quarter - 1)) + (18 * (_month - 1)) + _day
                _gday = datetime.strptime(f"{_gyear}-{_julian:003}", "%Y-%j") + timedelta(days=_quarter)

            self.unify(_gday.strftime("%Y-%m-%d"))
            return _gday


def startup():
    today = UnifiedDate(style="Short")
    print(f"""{__doc__}\n\nG'day! Today is: {today.format_date(style="Short")}\n\n{today}""")


if __name__ == "__main__":
    startup()
else:
    startup()
