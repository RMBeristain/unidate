"""
Unified Day and Month names
"""
from collections import ChainMap
from dataclasses import dataclass, field

from .definitions import UniMonth, UQ


@dataclass(frozen=True)
class FestiveDate:
    """
    Festive Date short names and their corresponding day of the year.

    These dates are considered single-day months but don't have a month number, only a name.
    """

    DAY = (1, 92, 183, 274, 365, 366)
    SHORT_NAME = ("Q1", "Q2", "Q3", "Q4", "YE", "LD")


@dataclass(frozen=True)
class RegularDate:
    """
    Regular date day and month names, and their corresponding day of the year.
    """

    WEEKDAY: dict[str, tuple[int, ...]] = field(
        default_factory=lambda: {
            "Firstday": (1, 7, 13),
            "Seconday": (2, 8, 14),
            "Thirday": (3, 9, 15),
            "Fourthday": (4, 10, 16),
            "Fifthday": (5, 11, 17),
            "Sixthday": (6, 12, 18),
        }
    )

    UNIFIED_MONTH_NAME_SHORT: dict[str | int, UniMonth] = field(
        # Short-format unified month names. Territorian and Austral variants use these same short names.
        default_factory=lambda: {
            "Q1": UniMonth("Q10", UQ(1, 0)),
            1: UniMonth("Q1A", UQ(1, 1)),
            2: UniMonth("Q1B", UQ(1, 2)),
            3: UniMonth("Q1C", UQ(1, 3)),
            4: UniMonth("Q1D", UQ(1, 4)),
            5: UniMonth("Q1E", UQ(1, 5)),
            "Q2": UniMonth("Q20", UQ(2, 0)),
            6: UniMonth("Q2A", UQ(2, 1)),
            7: UniMonth("Q2B", UQ(2, 2)),
            8: UniMonth("Q2C", UQ(2, 3)),
            9: UniMonth("Q2D", UQ(2, 4)),
            10: UniMonth("Q2E", UQ(2, 5)),
            "Q3": UniMonth("Q30", UQ(3, 0)),
            11: UniMonth("Q3A", UQ(3, 1)),
            12: UniMonth("Q3B", UQ(3, 2)),
            13: UniMonth("Q3C", UQ(3, 3)),
            14: UniMonth("Q3D", UQ(3, 4)),
            15: UniMonth("Q three E", UQ(3, 5)),
            "Q4": UniMonth("Quarter four", UQ(4, 0)),
            16: UniMonth("Q4A", UQ(4, 1)),
            17: UniMonth("Q4B", UQ(4, 2)),
            18: UniMonth("Q4C", UQ(4, 3)),
            19: UniMonth("Q4D", UQ(4, 4)),
            20: UniMonth("Q4E", UQ(4, 5)),
            "YE": UniMonth("YE", UQ(5, 0)),
            "LD": UniMonth("LD", UQ(6, 0)),
        }
    )

    UNIFIED_MONTH_NAME_LONG: dict[str | int, UniMonth] = field(
        default_factory=lambda: {
            "Q1": UniMonth("Quarter one", UQ(1, 0)),
            1: UniMonth("Quarter one-A", UQ(1, 1)),
            2: UniMonth("Quarter one-B", UQ(1, 2)),
            3: UniMonth("Quarter one-C", UQ(1, 3)),
            4: UniMonth("Quarter one-D", UQ(1, 4)),
            5: UniMonth("Quarter one-E", UQ(1, 5)),
            "Q2": UniMonth("Quarter two", UQ(2, 0)),
            6: UniMonth("Quarter two-A", UQ(2, 1)),
            7: UniMonth("Quarter two-B", UQ(2, 2)),
            8: UniMonth("Quarter two-C", UQ(2, 3)),
            9: UniMonth("Quarter two-D", UQ(2, 4)),
            10: UniMonth("Quarter two-E", UQ(2, 5)),
            "Q3": UniMonth("Quarter three", UQ(3, 0)),
            11: UniMonth("Quarter three-A", UQ(3, 1)),
            12: UniMonth("Quarter three-B", UQ(3, 2)),
            13: UniMonth("Quarter three-C", UQ(3, 3)),
            14: UniMonth("Quarter three-D", UQ(3, 4)),
            15: UniMonth("Quarter three-E", UQ(3, 5)),
            "Q4": UniMonth("Quarter four", UQ(4, 0)),
            16: UniMonth("Quarter four-A", UQ(4, 1)),
            17: UniMonth("Quarter four-B", UQ(4, 2)),
            18: UniMonth("Quarter four-C", UQ(4, 3)),
            19: UniMonth("Quarter four-D", UQ(4, 4)),
            20: UniMonth("Quarter four-E", UQ(4, 5)),
            "YE": UniMonth("Year end", UQ(5, 0)),
            "LD": UniMonth("Leap day", UQ(6, 0)),
        }
    )

    TERRITORIAN_MONTH_NAME_BASE: dict[str | int, UniMonth] = field(
        default_factory=lambda: {
            1: UniMonth("Winter freeze", UQ(1, 1)),
            2: UniMonth("Winter wane", UQ(1, 2)),
            3: UniMonth("Winter end", UQ(1, 3)),
            4: UniMonth("Spring low", UQ(1, 4)),
            5: UniMonth("Spring break", UQ(1, 5)),
            6: UniMonth("Spring height", UQ(2, 1)),
            7: UniMonth("Spring wane", UQ(2, 2)),
            8: UniMonth("Spring end", UQ(2, 3)),
            9: UniMonth("Summer low", UQ(2, 4)),
            10: UniMonth("Summer break", UQ(2, 5)),
            11: UniMonth("Summer height", UQ(3, 1)),
            12: UniMonth("Summer wane", UQ(3, 2)),
            13: UniMonth("Summer end", UQ(3, 3)),
            14: UniMonth("Autumn low", UQ(3, 4)),
            15: UniMonth("Autumn fall", UQ(3, 5)),
            16: UniMonth("Autumn lull|height", UQ(4, 1)),
            17: UniMonth("Autumn wane", UQ(4, 2)),
            18: UniMonth("Autumn end", UQ(4, 3)),
            19: UniMonth("Winter low", UQ(4, 4)),
            20: UniMonth("Winter chill", UQ(4, 5)),
        }
    )

    AUSTRAL_MONTH_NAME_BASE: dict[str | int, UniMonth] = field(
        default_factory=lambda: {
            1: UniMonth("Summer height", UQ(1, 1)),
            2: UniMonth("Summer wane", UQ(1, 2)),
            3: UniMonth("Summer close", UQ(1, 3)),
            4: UniMonth("Autumn start", UQ(1, 4)),
            5: UniMonth("Autumn fall", UQ(1, 5)),
            6: UniMonth("Autumn lull", UQ(2, 1)),
            7: UniMonth("Autumn wane", UQ(2, 2)),
            8: UniMonth("Autumn close", UQ(2, 3)),
            9: UniMonth("Winter start", UQ(2, 4)),
            10: UniMonth("Winter chill", UQ(2, 5)),
            11: UniMonth("Winter lull", UQ(3, 1)),
            12: UniMonth("Winter wane", UQ(3, 2)),
            13: UniMonth("Winter close", UQ(3, 3)),
            14: UniMonth("Spring start", UQ(3, 4)),
            15: UniMonth("Spring break", UQ(3, 5)),
            16: UniMonth("Spring run", UQ(4, 1)),
            17: UniMonth("Spring wane", UQ(4, 2)),
            18: UniMonth("Spring close", UQ(4, 3)),
            19: UniMonth("Summer start", UQ(4, 4)),
            20: UniMonth("Summer break", UQ(4, 5)),
        }
    )

    @property
    def TERRITORIAN_MONTH_NAME_LONG(self) -> dict[str, tuple[int, ...]]:
        return ChainMap(self.TERRITORIAN_MONTH_NAME_BASE, self.UNIFIED_MONTH_NAME_LONG)

    @property
    def AUSTRAL_MONTH_NAME_LONG(self) -> dict[str, tuple[int, ...]]:
        return ChainMap(self.AUSTRAL_MONTH_NAME_BASE, self.UNIFIED_MONTH_NAME_LONG)
