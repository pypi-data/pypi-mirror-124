# -*- coding: utf-8 -*-

# The MIT License (MIT) - Copyright (c) 2016-2021 Dave Vandenbout.

import pytest

from skidl import Part

from .setup_teardown import setup_function, teardown_function


def test_fields_1():
    """Test field creation."""

    r1 = Part("Device", "R", value=500)

    num_fields = len(r1.fields)

    r1.fields["test1"] = "test1 value"

    assert len(r1.fields) == num_fields + 1
    assert r1.test1 == r1.fields["test1"]

    r1.test1 = "new test1 value"

    assert r1.fields["test1"] == "new test1 value"

    r2 = r1()

    assert r2.test1 == r1.test1

    r2.fields["test1"] = "new r2 test1 value"

    assert r2.test1 == "new r2 test1 value"

    assert r1.test1 == "new test1 value"
