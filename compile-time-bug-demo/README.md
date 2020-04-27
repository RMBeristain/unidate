# compile-time vs. runtime

One of more subtle types of bugs you'll find in Python are compile-time bugs, which usually manifest in the right-hand side of default arguments to functions, or in class constants, stuff like that.

Part of what makes them insidious is that they aren't obvious when you read the code, and they don't manifest immediately, or under ordinary conditions, or all the time; they strike when you least expect it and suddently you have dead people on the floor and wondering "how the heck did this happen".

I've included a small example of what's going on, and I'll explain why it's happening too; here are these two classes:

```python
class WithBug(StrMethod):
    "This class will have a 'whenever it was compiled' problem"
    def __init__(self, val=datetime.now()):
        self._when = val

class WithoutBug(StrMethod):
    "This class will set the right default every time"
    def __init__(self, val=None):
        self._when = datetime.now() if val is None else val
```

One with the bug, the other without the bug.

We've all read somewhere or another "_don't use mutable objects as default arguments_" and with good reason, the reference to that one single mutable object is passed to all instances of that class, and applied to every execution of that function (for their respective cases) and ... you're not getting what you expect (an empty list when none is passed, for example).

In the case above, `datetime.now()` is calculated at compile time (during import, for example) and will be reused every time a new object is created, even hours later. If the intent is to have the current timestamp used whenever the argument is omitted, then the second version will do what you're expecting, with no corner cases.

I've included a short script in this directory that you can use to show this behavior; when you run the script (`comptime_main.py`) you'll see the output; the expected behavior is that the `unsafe` variables will have the same value as the `safe` variables, and that is, that they're around the same timestamp as when they're created; instead, what you will see is that the `unsafe` variables will have a weird timestamp that's before they were created, rather it's closed to the "**Initial timestamp**" that appears at the top of the run; plus, they will both match, and the `safe` timestamps won't match, they shouldn't.

And there's more! If you have the environment variable `PYTHONDONTWRITEBYTECODE` set to a non-empty value, or any other method to prevent python bytecode to be written out to disk, they that buggy timestamp will be refreshed every time you run your program because the bytecode is being generated every time; on the other hand, if you're caching your bytecode to disk, then the "_unsafe_" timestamp will be static and will match whenever your library was first imported.

## Example run

Here are the results of an example run:

```shell
$ python3 comptime_main.py 

Initial timestamp: 2020-04-27 11:05:32.141586
Sleeping 5 seconds and creating first set of objects

First round timesatmp: 2020-04-27 11:05:37.146762
Got:
 - Unsafe: 2020-04-27 11:05:32.141560
 - Safe: 2020-04-27 11:05:37.146750

Sleeping another 7 seconds, then creating second set

Second round timestamp: 2020-04-27 11:05:44.150234
Got:
 - Unsafe: 2020-04-27 11:05:32.141560
 - Safe: 2020-04-27 11:05:44.150222



Report:
    - Unsafe #1: 2020-04-27 11:05:32.141560
    - Unsafe #2: 2020-04-27 11:05:32.141560
    - Safe #1: 2020-04-27 11:05:37.146750
    - safe #2: 2020-04-27 11:05:44.150222
```

