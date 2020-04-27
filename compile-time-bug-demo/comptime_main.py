#!/usr/bin/python3
#pylint: disable=too-few-public-methods,invalid-name,unused-import
"""
Demonstrate subtle problem caused by using
a compile-time defined "default" constant,
instead of using a flag value to request
a runtime calculated default.
"""
from comptime_lib import harness

if __name__ == "__main__":
    harness()
# Fin.
