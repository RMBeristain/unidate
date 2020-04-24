Unified Calendar
================

Module to convert Grgorian calendar dates to Unified calendar dates as featured in the science-fiction novel

 A P A R T
 O F T H E
 W O R L D

by R.M. Beristain

DISCLAIMER
----------
This software is distributed 'as is' and with absolutely no warranties of any kind, whether express or implied,
including but not limited to, any warranty of merchantability or fitness for a particular purpose.

The user (you) must assume the entire risk of using the software.

In no event shall any individual, company or organization involved in any way in the development, sale or distribution
of this software be liable for any damages whatsoever relating to the use, misuse, or inability to use this software
(including, but not limited to, damages for loss of profits, business interruption, loss of information, or any other
loss).


### Info Badges
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/) ![Python application](https://github.com/RMBeristain/unidate/workflows/Python%20application/badge.svg)


The Unified Calendar explained
------------------------------

In the Unified State people have adopted a new calendar that completely does away with the division used by the
Western Gregorian calendar.

### Years and years

The Gregorian calendar starts counting from zero at the birth of the founder of Christianity, over two thousand and
twenty years ago, at the time of this writing. The Unified calendar sets its year zero at the earliest known evidence of
writting, over 5600 years ago. Therefore, Unified dates look like they are 'far in the future' as compared to Gregorian.
The year 2020 is the year 7620 in the Unified calendar.

### Months and quarters

It's almost certain we'll be familiar with the months of the Gregorian calendar: The year is split in 12 months. Each
month has between 28 and 31 days in an almost-but-not-quite alternating pattern. Month names are called after antiquity
deities and Roman Emperors.

Because 12 is divisible by 4, some people like to divide the year into 4 quarters of 3 months each, which is useful for
certain administrative tasks.

So the Gregorian calendar months look like this:

- January, 31 days
- Febriary, 28|29 days
- March, 31
- April, 30
- May, 31
- June, 30
- July, 31
- August, 31
- September, 30
- October, 31
- November, 30
- December, 31

The Unified calendar is perfectly regular: The year is split in 20 months. Each month has exactly 18 days. The odd 5 or
6 days that remain are always festive. Unified month names are rather boringly named with numbers and letters, but
Territorian and Austral variants have more colourful names for the same divisions.

In the Unified calendar quarters are integrated; the first 4 of these festive days mark the start of each quarter. The
fifth festive is always Year End; the sixth one is Leap Day and it is always added at the end of the year when needed.

The Unified Calendar months look like this:

- Quarter one, 1 day (festive, marks the start of the quarter)
- Quarter one-A, 18 days
- Quarter one-B, 18
- Quarter one-C, 18
- Quarter one-D, 18
- Quarter one-E, 18
- Quarter two, 1 day (festive, marks the start of the quarter)
- Quarter two-A, 18
- Quarter two-B, 18
- Quarter two-C, 18
- Quarter two-D, 18
- Quarter two-E, 18
- Quarter three, 1 day (festive, marks the start of the quarter)
- Quarter three-A, 18
- Quarter three-B, 18
- Quarter three-C, 18
- Quarter three-D, 18
- Quarter three-E, 18
- Quarter four, 1 day (festive, marks the start of the quarter)
- Quarter four-A, 18
- Quarter four-B, 18
- Quarter four-C, 18
- Quarter four-D, 18
- Quarter four-E, 18
- Year end, 1 day (festive, marks the end of the year)
- Leap day, 1 day (festive, marks a leap year)

### Weeks and days

In the Gregorian calendar, every week is composed of seven days, whose names usually honour deities of antiquity, but
vary per country and language. Each week is further subdivided in "working" days and "weekend" days that are usually
but not always days of rest.

The Gregorian week looks like this:

- Work days
    - Moon's day
    - Tiwaz's day
    - Woden's day
    - Thor's day
    - Frija's day
- Week end days
    - Saturn's day
    - Sun's day

Of course, you may know them by slightly different names ;)

The unified week has only six days because they are big on regularity and standards in the Unified State. They still
keep a 2-day weekend, meaning they have only 4 working days. However, other regions that have adopted the Unified
calendar didn't necessarily adopt this change too. For instance, in the South-Western Territories they instead kept 5
working days and only 1 week end day.

The Unified State experienced a strong secular movement around the time they reformed their calendar, so they removed
all personal and mythological references in order to make it more universally representative of the cultures that formed
it. So, again, their week day names are quite boring.

The Unified week looks like this:

- Work days
    - Firstday
    - Seconday
    - Thirday
    - Fourthday
- Week end days
    - Fifthday
    - Sixthday

As a nice bonus of their emphasis in regularity, in the Unified calendar every date always falls on the same day number
and week day every year, unlike in the Gregorian calendar where one may have been born on a Sunday, but every year the
date moves around the week. In the Unified State, if we were born on a Fourthday, our birthday will always fall on a
Fourthday.

Running
-------

To run on python interpreter:
```python
    >>> from unidate import UnifiedDate as UD

    >>> ud = UD()                       # creates instance and initializes to today's date in Unified format.
    >>> ud.unify('YYYY-MM-DD')          # converts Gregorian ISO date to Unified date.
    >>> ud.reverse_unidate('YYY-QM-DD') # converts Unified ISO date to Gregorian date.
    >>> print(ud)                       # displays Gregorian date and various Unified date formats.
    >>> ud.print_calendar()             # prints this year's Unified calendar
```
For more details see `help(unidate.UnifiedDate)`

IMPORTANT
=========

**Requires Python 3.6+**

Main Class properties
---------------------

`UnifiedDate` stores converted dates in four variants, each in its own property.

- `.gregorian_date`: A string with the date portion of our "normal" Gregorian calendar in ISO 8601 format.

- `.unified_date`: A _UnifiedDateType_ named tuple with date in Unified format. Unified tuple contains:
    - weekday: A _UniWeekTuple_ describing the Unified week. Week named tuple contains:
        - regular: A numeric flag to indicate if the week is festive (0) or regular (1)
        - number: Numeric value for the day of the week [1-6]
        - yearday: Numeric value for the day of the year [1-366]

    - day: A _UniDayTuple_ describing the Unified day of the week. Day named tuple contains:
        - name: Long or Short-format name of the week day [Firstday..Sixthday]
        - number: Ordinal day of the week [1-6]

    - month: A _UniMonthTuple_ describing the Unified month. Month named tuple contains:
        - name: Long or Short-format name of the month. Names are different depending on variant chosen (Unified,
            Territorian, Austral). The full list of names for each is stored on private properties (
            \_unified_month_name_short, \_unified_month_name_long, \_territorian_month_name_long,
            \_austral_month_name_long). There are no short variants for Territorian or Austral, they use Unified Short.

        - numeric: A _UQT_ Unified Quarter Tuple describing the Quarter to which the month belongs. UQT contains:
            - quarter: Ordinal start of the festive "quarter" [1-6]. There are 2 pseudo-quarters: Year end and Leap day.
            - month: Ordinal month of the year [1-20]

    - year: Ordinal Unified year [0-9999]

- `.swt_date`: A _UnifiedDateType_ named tuple with date in South-Western Territories (Territorianl) variant. Same
  contents as _unified_date_

- `.austral_date`: A _UnifiedDateType_ named tuple with date in Austral format. Same contents as _unified_date_


Main Class methods
------------------

Basic usage is very simple, but the class allows you to convert parts of the Gregorian calendar to Unified calendar if
you so choose.


### unify

One of the two methods we're most likely to use, `unify` takes a Gregorian date in ISO 8601 format (YYYY-MM-DD) and
returns a _UnifiedDateType_ named tuple with the Unified date version. It also populates all date properties including
unified_date, swt_date and austral_date.

Example:

```python
    >>> ud.unify('2020-04-23')
    UnifiedDateType(weekday=UnifiedWeek(regular=1, number=4, yearday=112), day=UnifiedDay(name='Fourthday', number=4),
        month=UnifiedMonth(name='Quarter two-B', numeric=UnifiedQuarter(quarter=2, month=2)), year=7620)

    >>> print(ud)
    Gregorian:     2020-04-23 - Thursday 23 of April, 2020
    Unified ISO:   7620-22-04
    Unified Short: D4 4, Q2B 7620
    Unified Long:  Fourthday 04, Quarter two-B 7620
    Territorian:   Fourthday 04, Spring wane 7620
    Austral:       Fourthday 04, Autumn wane 7620
            UnifiedDateType(weekday=UnifiedWeek(regular=1, number=4, yearday=112), day=UnifiedDay(name='Fourthday',
                number=4), month=UnifiedMonth(name='Quarter two-B', numeric=UnifiedQuarter(quarter=2, month=2)),
                year=7620)

```

### reverse_unidate

The second method we're most likely to use, `reverse_unidate` takes a Unified date in fictional ISO 8601U format
(YYYY-QM-DD) and returns a Gregorian datetime object.

There is no function to convert long-format dates at this point, perhaps in a future version if there's interest.

```python
    >>> ud.reverse_unidate('7620-22-04')
    datetime.datetime(2020, 4, 23, 0, 0)
```

### print_month

Prints the **Gregorian** month of a given date, and its corresponding Unified dates. I.e., if you have previously
"unified" a date like 2020-04-23, `print_month` with print the month of April 2020 along with its associated Unified
dates.

### print_calendar

Prints the **Unified** year calendar for the entire year. I.e. if you have previously "unified" a date like 2020-04-23,
`print_calendar` will print the calendar for the entire year 2020.

### print_festive

Prints the **Unified** festive days corresponding to a year. I.e. if you have previously "unified" a date like
2020-04-23, `print_festive` will print the 5 or 6 festive days corresponding to 2020 (6 in this case).

### format_date

Return Unified Date formatted according to a regional variant (e.g. South-Western Territories) and style (e.g. "Long").

Only the tuple corresponding to the format is updated. For instance, if we want the "Unified ISO" format:

```python
    >>> # assume gregorian date is 2020-04-23
    >>> ud.format_date(style='ISO')
    '7620-22-04'

    >>>  ud.unified_date.month
    UnifiedMonth(name='Quarter two-B', numeric=UnifiedQuarter(quarter=2, month=2))
```

Long and Short versions:
```python
    >>> ud.format_date(style='Long')
    'Fourthday 04, Quarter two-B 7620'

    >>> ud.format_date(style='Short')
    'D4 4, Q2B 7620'

    >>>  ud.unified_date.month
    UnifiedMonth(name='Quarter two-B', numeric=UnifiedQuarter(quarter=2, month=2))  # this didn't change
```

**NOTE:**
    Non-unified variants don't have a short-format name; they use the same as the Unified variant.
    If style="Short" is specified for "SWT" or "Austral" variants, `format_date` will return a short-format
    **string**, but the actual tuple stored will retain the Long name of the month for those variants. Only the
    day name is shortened.

For example:

```python
    >>> ud.format_date(variant='SWT', style='Short')
    'D4 4, Q2B 7620'

    >>> ud.swt_date.month.name
    'Spring wane'
```
