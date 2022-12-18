"""
Unified Day and Month names
"""
from dataclasses import dataclass


@dataclass
class Days:
    """
    Day names and their corresponding weekdays, including standard festivities.

    Unified days of the week always fall on the same weekday number and date.
    """

    FESTIVE_DAYS = (1, 92, 183, 274, 365, 366)
    FESTIVE_NAMES_SHORT = ("Q1", "Q2", "Q3", "Q4", "YE", "LD")
    WEEKDAYS = {
        "Firstday": (1, 7, 13),
        "Seconday": (2, 8, 14),
        "Thirday": (3, 9, 15),
        "Fourthday": (4, 10, 16),
        "Fifthday": (5, 11, 17),
        "Sixthday": (6, 12, 18),
    }
