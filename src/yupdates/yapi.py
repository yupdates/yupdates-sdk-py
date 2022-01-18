"""
This module is a convenience wrapper around a default instance of `YupdatesClient` for quick
scripts and easy calls from a Python interpreter.

This will always maintain parity with the `YupdatesClient` methods, so you can build programs
on top of this module or store one `YupdatesClient` instance in a variable and use the instance
methods on that.

See the `YupdatesClient` class and method documentation for a particular call's usage.

Example:
    from yupdates import yapi

    yapi.ping()
"""

from .client import yupdates_client


def ping():
    return yupdates_client().ping()


def ping_bool():
    return yupdates_client().ping_bool()
