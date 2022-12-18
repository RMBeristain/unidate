"""
Unified Date Information
"""

from typing import NamedTuple


class UniDay(NamedTuple):
    """Abreviated representation of a Unified day"""

    name: str  # Unified weekday name
    number: int  # Unified weekday number


class UniWeek(NamedTuple):
    """Abreviated representation of a Unified Week"""

    regular: int  # flag to indicate if date is regular or festive: 0=festive, 1=regular
    number: int  # day of the week [1-6]
    yearday: int  # day of the year [1-366]


class UniMonth(NamedTuple):
    """Abreviated representation of a Unified Month"""

    name: str  # Unified month name
    numeric: NamedTuple  # Unified month descriptor: (quarter #, month #)


class UQ(NamedTuple):
    """Abreviated representation of a Unified quarter"""

    quarter: int  # Unified quarter number
    month: int  # Unified month number


class UnifiedDateType(NamedTuple):
    """Abreviated representation of a Unified date"""

    weekday: NamedTuple  # Unified week descriptor: (regular flag, day of the week, day of the year)
    day: NamedTuple  # Unified day descriptor: (weekday name, weekday number)
    month: NamedTuple  # Unified month descriptor: (month name, numeric descriptor(quarter #, month #), year)
    year: int  # Unified year
