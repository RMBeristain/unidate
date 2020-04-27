#!/usr/bin/python3
#pylint: disable=too-few-public-methods,invalid-name,unused-import
"""
Demonstrate subtle problem caused by using
a compile-time defined "default" constant,
instead of using a flag value to request
a runtime calculated default.
"""
import sys
import time
from datetime import datetime

__all__ = 'WithBug', 'WithoutBug', 'harness'

class StrMethod:
    "I'm lazy so I'm defining this only once"
    def __str__(self):
        return str(self._when) # pylint: disable=no-member
    def show(self):
        "Print out the internal datetime object"
        print("Date: %s" % self)

class WithBug(StrMethod):
    "This class will have a 'whenever it was compiled' problem"
    def __init__(self, val=datetime.now()):
        self._when = val

class WithoutBug(StrMethod):
    "This class will set the right default every time"
    def __init__(self, val=None):
        if val is None:
            self._when = datetime.now()
        else:
            self._when = val

def show_timestamp(title):
    "Show the current timestamp"
    print("\n%s: %s" % (title, datetime.now()))

def do_pause(prompt, pause):
    "Print out the current timestamp, optionally prompt for a short delay"
    print(prompt % int(pause))
    time.sleep(pause)

def harness():
    "Run the test"
    show_timestamp("Initial timestamp")
    do_pause("Sleeping %s seconds and creating first set of objects", 5.0)
    unsafe1 = WithBug()
    safe1 = WithoutBug()
    show_timestamp("First round timesatmp")
    print("Got:\n - Unsafe: {u}\n - Safe: {s}\n".format(u=unsafe1, s=safe1))

    do_pause("Sleeping another %s seconds, then creating second set", 7.0)
    unsafe2 = WithBug()
    safe2 = WithoutBug()
    show_timestamp("Second round timestamp")
    print("Got:\n - Unsafe: {u}\n - Safe: {s}\n".format(u=unsafe2, s=safe2))

    print("""\n
Report:
    - Unsafe #1: {u1}
    - Unsafe #2: {u2}
    - Safe #1: {s1}
    - safe #2: {s2}
""".format(u1=unsafe1, u2=unsafe2, s1=safe1, s2=safe2))
    sys.exit(0)

# The End
