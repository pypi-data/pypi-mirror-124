# -*- coding: utf-8 -*-

# The MIT License (MIT) - Copyright (c) 2016-2021 Dave Vandenbout.

import pytest

from skidl import ERC, Net, Part, erc_logger, generate_netlist, super

from .setup_teardown import setup_function, teardown_function


def test_subclass_1():
    class Resistor(Part):
        def __init__(self, value, ref=None, footprint="Resistors_SMD:R_0805"):
            super().__init__("Device", "R", value=value, ref=ref, footprint=footprint)

    gnd = Net("GND")  # Ground reference.
    vin = Net("VI")  # Input voltage to the divider.
    vout = Net("VO")  # Output voltage from the divider.

    r1 = Resistor("1k")
    r2 = Resistor("500")

    r1[1] += vin  # Connect the input to the first resistor.
    r2[2] += gnd  # Connect the second resistor to ground.
    vout += r1[2], r2[1]  # Output comes from the connection of the two resistors.

    ERC()
    generate_netlist()


def test_subclass_2():
    class CustomPart(Part):
        pass

    r1 = Part("Device", "R")
    r2 = CustomPart("Device", "R")
    r1 & r2  # Make a connection so resistors don't get culled.

    ERC()
    assert erc_logger.warning.count == 2
