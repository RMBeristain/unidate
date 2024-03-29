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

        >>> ud = UD()                        # creates instance and initializes to today's date in Unified format.
        >>> ud.unify('YYYY-MM-DD')           # converts Gregorian ISO date to Unified date.
        >>> ud.reverse_unidate('YYYY-QM-DD') # converts Unified ISO date to Gregorian date.
        >>> print(ud)                        # displays Gregorian date and various Unified date formats.
        >>> ud.print_calendar()              # prints this year's Unified calendar
    ```
    For more details see `help(unidate.UnifiedDate)`

    Requires Python 3.6+

    License
    -------
    This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Australia License.
    To view a copy of this license, visit http: //creativecommons.org/licenses/by-sa/3.0/au/
    or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
"""
from __future__ import annotations

__author__ = "R.M. Beristain"
__version__ = "1.1.1"

from datetime import datetime, timedelta
from math import trunc

from calendar_data.definitions import UniDay, UniWeek, UniMonth, UQ, UnifiedDateType
from calendar_data.names import FestiveDate, RegularDate
from exceptions import InvalidUnifiedDateValue
from presentation.styling import Style, Variant


class UnifiedDate:
    """
    Transform Gregorian dates to Unified.

    By default we Unify the current system date if instantiated without parameters.
    To convert an arbitrary date, create an instance with an ISO 8601-formatted date string. E.g:

    ```
    udate=UnifiedDate('2015-04-20')
    ```

    You can also pass an ISO 8601-formatted date to an existing instance by calling the `unify` method.

    `UnifiedDate` can be printed to show a date's Unified format along with Sout-Western Territory and Austral
    formats.

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

    _regular_date = RegularDate()

    WEEKDAY = _regular_date.WEEKDAY
    _UNIFIED_MONTH_NAME_SHORT = _regular_date.UNIFIED_MONTH_NAME_SHORT
    _UNIFIED_MONTH_NAME_LONG = _regular_date.UNIFIED_MONTH_NAME_LONG
    _TERRITORIAN_MONTH_NAME_BASE = _regular_date.TERRITORIAN_MONTH_NAME_BASE
    _AUSTRAL_MONTH_NAME_BASE = _regular_date.AUSTRAL_MONTH_NAME_BASE
    _TERRITORIAN_MONTH_NAME_LONG = _regular_date.TERRITORIAN_MONTH_NAME_LONG
    _AUSTRAL_MONTH_NAME_LONG = _regular_date.AUSTRAL_MONTH_NAME_LONG

    del _regular_date

    _year_start: datetime | None = None  # datetime object containing first day of date's year
    unified_date: UnifiedDateType | None = None
    swt_date: UnifiedDateType | None = None
    austral_date: UnifiedDateType | None = None
    gregorian_date: datetime | None = None

    def __init__(self, user_date: str = None, style: str = "Long") -> None:
        """
        Initialises default values

        Parameters
        ----------
        - user_date: Gregorian date in ISO 8601 format.
        - style - month representation style. Can be one of 'Long' or 'Short'
        """
        # This will validate it is (more or less) correct.
        user_date = (
            datetime.strptime(user_date, "%Y-%m-%d").date().isoformat()
            if user_date
            else datetime.now().date().isoformat()
        )
        self.gregorian_date = user_date
        self.unified_date = self.unify(user_date, style)

    def __str__(self) -> str:
        "returns unified date in a nice format"
        return (
            f"{'Gregorian:':<15}{self.gregorian_date:>10} - "
            f"{datetime.strptime(self.gregorian_date, '%Y-%m-%d').strftime('%A %d of %B, %Y')}\n"
            f"{'Unified ISO:':<15}{self.format_date(variant=Variant.UNI, style='ISO'):>10}\n"
            f"{'Unified Short:':<15}{self.format_date(Variant.UNI, style='Short')}\n"
            f"{'Unified Long:':<15}{self.format_date(Variant.UNI, 'Long')}\n"
            f"{'Territorian:':<15}{self.format_date(Variant.SWT, 'Long')}\n"
            f"{'Austral:':<15}{self.format_date(Variant.AUS, 'Long')}\n"
            f"\t{self.unified_date}\n"
        )

    def __repr__(self) -> str:
        return self.__str__()

    def __check_variant(self, variant: Variant | str) -> Variant | str:
        """Check if value given is a valid Unified Calendar `Variant`.

        If the value is a `Variant` instance or a known `Variant` value, return the `Variant`. If not, return the
        original parameter unchanged.

        Parameters
        ----------
        variant : any
            Unified calendar Variant. Should be a valid `Variant` Enum, but can also be one of the Enum's
            values (e.g Variant.UNI or 'Unified' are both accepted)

        Returns
        -------
        Union[Variant, str]
            A `Variant`, or the original parameter.
        """
        if isinstance(variant, Variant):
            return variant
        else:
            for this in Variant:
                if this.value.upper() == variant.upper().strip():
                    return this

        return variant

    def __check_style(self, style: Style | str) -> Style | str:
        """Check if value given is a valid Unified `Style` of date representaion.

        If the value is a known `Style` instance, return the `Style`. If not, return the original parameter unchanged.

        Parameters
        ----------
        style : any
            Representation style for a Unified Calendar variant. Should be a valid `Style` Enum, but can also be one of
            the Enum's values (e.g. Style.LONG or 'Long' are both accepted)

        Returns
        -------
        Union[Style, str]
            A `Style`, or the original parameter.
        """
        if isinstance(style, Style):
            return style
        else:
            for this in Style:
                if this.value.upper() == style.upper().strip():
                    return this

        return style

    def format_date(self, variant: Variant = Variant.UNI, style: Style = Style.LONG) -> str:
        """
        Set and return Unified Date, formatted according to a regional variant (e.g. South-Western Territories).

        NOTE: Non-unified variants don't have a short-format name; they use the same name as the Unified variant.

        If ``style="Short"`` is specified for "SWT" or "Austral" variants, `format_date` will return a short-format
        **string**, but the actual tuple stored will retain the Long name of the month. Only the day name is
        shortened.
        For example:

        ```
            >>> ud.format_date(variant=Variant.SWT, style='Short')
            'D4 4, Q2B 7620'  # returned day name is shortened for SWT and Austral variants.

            >>> ud.swt_date.month.name
            'Spring wane'  # stored month name is always kept in long-format for all variants.
        ```

        Parameters
        ----------
        - variant: Regional month name variant. Variants are defined in `Variant` Enum.
        - style: Calendar representation style. Styles are defined in `Style` Enum.

        Returns
        -------
        - Unified date in specified format.
        """
        variant = self.__check_variant(variant)
        style = self.__check_style(style)

        if variant == Variant.UNI:
            date = self.unified_date
        elif variant == Variant.SWT:
            date = self.swt_date
        elif variant == Variant.AUS:
            date = self.austral_date
        else:
            raise ValueError(f"Unknown variant: {variant}. Expected {Variant}")

        if not date:
            raise InvalidUnifiedDateValue(date)

        if style == Style.ISO:  # ISO 8601U "Unified ISO format"
            return f"{date.year}-{date.month.numeric.quarter}{date.month.numeric.month}-{date.day.number:02}"

        if date.weekday.regular:
            date = UnifiedDateType(  # replace existing date tuple with requested format
                weekday=date.weekday,
                day=self.get_uniday(
                    weekday=date.weekday,
                    # invalid or unknown formats are also displayed as 'Long'
                    style=Style.SHORT if style == Style.SHORT else Style.LONG,
                ),
                month=self.get_unimonth(weekday=date.weekday, variant=variant, style=style),
                year=date.year,
            )

            if style == Style.SHORT:
                _day_number = f"{date.day.number}"
            else:
                _day_number = f"{date.day.number:02}"  # For Style.LONG and .ISO

            return f"{date.day.name} {_day_number}, {date.month.name} {date.year}"

        # festive
        return "{month} {year}".format(month=date.month.name, year=date.year)

    def get_uniweek(self, day: int) -> UniWeek:
        """
        Parameters
        ==========
        - day: day number (1..366) of the year.

        Returns:
        ========
        - UnifiedWeek namedtuple contaning:
            - regular - flag to indicate if date is regular or festive: 0=festive, 1=regular
            - number - numeric value for day of the week [1-6]
            - yearday - numeric value for day of the year [1-366]
        """
        if day in FestiveDate.DAY:
            return UniWeek(0, FestiveDate.DAY.index(day), day)

        if 1 < day <= 91:
            day -= 1
        elif 92 < day <= 182:
            day -= 2
        elif 183 < day <= 273:
            day -= 3
        elif 274 < day <= 364:
            day -= 4
        else:
            raise InvalidUnifiedDateValue(f"Day out of range: {day!r}")

        return UniWeek(1, (((day % 90) % 18) % 6) or 6, day)

    def get_uniday(self, weekday: UniWeek, style: Style = Style.LONG) -> UniDay:
        """
        Takes a UniWeek and returns UniDayTuple with (name of the week day, date)

        If `style` is specified, return day name in that format. Applies only to regular week days; festive
        day names don't change.

        All weeks always start in a Firstday and end in a Sixtday.

        Parameters
        ----------
        - weekday: UniWeek
        - style: Calendar representation style. Styles are defined in `Style` Enum.
        """
        if weekday.regular == 0:
            return UniDay(FestiveDate.SHORT_NAME[weekday.number], 0)

        month_day = ((weekday.yearday % 90) % 18) or 18
        if month_day < 1 or month_day > 18:
            raise InvalidUnifiedDateValue(f"Invalid week tuple: {weekday!r}")

        if self.__check_style(style) == Style.LONG:
            return UniDay("".join(k for k, v in self.WEEKDAY.items() if weekday.number in v), month_day)

        return UniDay(f"D{month_day}", month_day)

    def get_unimonth(self, weekday: UniWeek, variant: Variant = Variant.UNI, style: Style = Style.LONG) -> UniMonth:
        """
        Take a unified weekday, return unified month.

        Parameters
        ----------
        - weekday:
            Unified weekday namedtuple
        - variant:
            Regional month name variant. Variants are defined in `Variant` Enum.
        - style:
            Calendar representation style. Styles are defined in `Style` Enum.
        """
        if weekday.regular:
            # date is a regular day
            month_number = int(trunc((weekday.yearday - 1) / 18.0)) + 1
            if month_number > 20:
                month_number = 20
        else:
            # date is a festivity. These months don't have number, only name.
            month_number = FestiveDate.SHORT_NAME[weekday.number]  # use week day number as index

        if self.__check_style(style) == Style.SHORT:
            # Return short style only if explicitely requested, else Long.
            return self._UNIFIED_MONTH_NAME_SHORT[month_number]

        variant = self.__check_variant(variant)

        if variant == Variant.AUS:
            return self._AUSTRAL_MONTH_NAME_LONG[month_number]
        if variant == Variant.SWT:
            return self._TERRITORIAN_MONTH_NAME_LONG[month_number]
        # invalid or unknown variants are returned as "Unified"
        return self._UNIFIED_MONTH_NAME_LONG[month_number]

    def unify(self, user_date: str = None, style: Style = Style.LONG) -> UnifiedDateType:
        """
        Convert user-provided Gregorian date to Unified and Territorian dates.

        Takes a gregorian date string and returns a UnifiedDateType tuple containing:
        unified weekday tuple, unified day name tuple, unified month.

        Also populates SWT and Austral dates, but those aren't returned.

        NOTE: Only dates between 1AD and 9999AD in _Gregorian_ Calendar can be converted (but Julian dates
        aren't supported)

        Parameters
        ----------
        - user_date:
            ISO 8601-formatted Gregorian date (e.g. '2020-12-31'). Optionally accepts the sting 'Today' for
            current sytem date. If no value (None) is provided, defaults to 'Today'
        - style:
            Calendar representation style. Styles are defined in `Style` Enum.

        Returns
        -------
        - Unified Date as UnifiedDateType {'weekday': UnifiedWeek, 'day': UnifiedDay, 'month': UnifiedMonth, 'year': year}
        """
        if not user_date:
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
                self.get_unimonth(weekday=uni_weekday, variant=Variant.UNI, style=style),
                year,
            )
            self.swt_date = UnifiedDateType(
                uni_weekday, uni_day, self.get_unimonth(weekday=uni_weekday, variant=Variant.SWT), year
            )
            self.austral_date = UnifiedDateType(
                uni_weekday, uni_day, self.get_unimonth(weekday=uni_weekday, variant=Variant.AUS), year
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
        from copy import deepcopy

        year_start = deepcopy(self._year_start)
        _save_date = self.gregorian_date

        for d in self.FESTIVE_DAYS:
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

    def reverse_year(self, unified_year: int) -> int:
        """
        Parameter
        ---------
        - unified_year: numeric Unified year

        Returns
        -------
        - numeric Gregorian year
        """
        if unified_year is None:
            raise InvalidUnifiedDateValue("Invalid year value: None")

        try:
            unified_year = int(unified_year)
            if unified_year >= 0:
                return unified_year - 5600
            raise InvalidUnifiedDateValue("Cannot convert Unified prehistoric dates.")
        except ValueError:
            raise InvalidUnifiedDateValue(f"{unified_year!r} - Not a valid year.")
        return None

    def reverse_unidate(self, u_date: str) -> datetime:
        """
        Convert Unified date string to Gregorian date.

        Parameters
        ==========
        - u_date: ISO 8601U-formatted Unified Date string.

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
        except AttributeError as err:
            print(f"Expected a string: {err}")
            raise
        except IndexError as err:
            print(f"Quarter or Month seem to be out of range: {user_date}")
            raise
        except ValueError as err:
            print(f"Expected an ISO-8601U (YYYY-QM-DD) date: {user_date}: {err}")
            raise

        _gyear = self.reverse_year(_year)  # Gregorian year

        if _month == 0:
            DAYNUMS = [None, 1, 92, 183, 274, 365, 366]
            if _quarter < 1 or _quarter > 6:
                raise InvalidUnifiedDateValue(f"Not an ISO-8601U date: {user_date!r}")
            _gday = datetime.strptime(f"{_gyear}-{DAYNUMS[_quarter]:03}", "%Y-%j")
        else:
            _julian = (90 * (_quarter - 1)) + (18 * (_month - 1)) + _day
            _gday = datetime.strptime(f"{_gyear}-{_julian:003}", "%Y-%j") + timedelta(days=_quarter)

        self.unify(_gday.date().isoformat())
        return _gday

    @classmethod
    def today(cls, style="Long"):
        "Create a UnifiedDate instance from today's date"
        return cls(datetime.now().date().isoformat(), style)


def startup():
    "Display today's date in Unidate standard"
    today = UnifiedDate.today(style="Short")
    print(f"""{__doc__}\n\nG'day! Today is: {today.format_date(style="Short")}\n\n{today}""")


if __name__ == "__main__":
    startup()
else:
    startup()
