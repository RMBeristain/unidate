"""
Unified Date Information
"""

from typing import NamedTuple


class UniWeek(NamedTuple):
    """Abreviated representation of a Unified Week"""

    regular: int  # flag to indicate if date is regular or festive: 0=festive, 1=regular
    number: int  # day of the week [1-6]
    yearday: int  # day of the year [1-366]
