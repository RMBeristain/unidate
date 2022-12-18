"""
Text representation for Unified Dates, styles (long, short) and their variants.
"""

from enum import Enum, unique


@unique
class Variant(Enum):
    "Unified calendar regional variants"
    UNI = "Unified"  # Base Unified State names
    SWT = "SWT"  # South-Western Territories names
    AUS = "Austral"  # Austral hemisphere names


@unique
class Style(Enum):
    """Unified calendar representation styles"""

    LONG = "Long"  # "LongDayName WeekdayNumber, LongMonthName YearNumber" e.g. "Thirday 3, Quarter two-B 7620"
    SHORT = "Short"  # "ShortDayName WeekdayNumber, ShortMonthName YearNumber" e.g "D3 3, Q2B 7620"
    ISO = "ISO"  # ISO 8601U "Year-QuarterMonth-day" e.g. 7620-22-03 (Output is the same for all three variants)
