"""
Unified Day and Month names
"""
from dataclasses import dataclass


@dataclass
class FestiveDate:
    """
    Festive Date short names and their corresponding day of the year.
    """

    DAY = (1, 92, 183, 274, 365, 366)
    SHORT_NAME = ("Q1", "Q2", "Q3", "Q4", "YE", "LD")
