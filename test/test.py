# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_priority_encoder(dut):
    dut._log.info("Starting Priority Encoder Test")

    # Set up clock
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # Test case a: In[15:0] = 0010 1010 1111 0001
    dut._log.info("Test case a: In[15:0] = 0010 1010 1111 0001")
    dut.uio_in.value = 0b00101010  # A[7:0]
    dut.ui_in.value = 0b11110001   # B[7:0]
    await ClockCycles(dut.clk, 1)
    
    expected = 13
    assert dut.uo_out.value == expected, f"Expected {expected}, got {dut.uo_out.value}"
    dut._log.info(f"Test case a passed: uo_out = {dut.uo_out.value}")

    # Test case b: In[15:0] = 0000 0000 0000 0001
    dut._log.info("Test case b: In[15:0] = 0000 0000 0000 0001")
    dut.uio_in.value = 0b00000000  # A[7:0]
    dut.ui_in.value = 0b00000001   # B[7:0]
    await ClockCycles(dut.clk, 1)
    
    expected = 0
    assert dut.uo_out.value == expected, f"Expected {expected}, got {dut.uo_out.value}"
    dut._log.info(f"Test case b passed: uo_out = {dut.uo_out.value}")

    # Test case c: In[15:0] = 0000 0000 0000 0000
    dut._log.info("Test case c: In[15:0] = 0000 0000 0000 0000")
    dut.uio_in.value = 0b00000000  # A[7:0]
    dut.ui_in.value = 0b00000000   # B[7:0]
    await ClockCycles(dut.clk, 1)
    
    expected = 0xF0
    assert dut.uo_out.value == expected, f"Expected {expected}, got {dut.uo_out.value}"
    dut._log.info(f"Test case c passed: uo_out = {dut.uo_out.value}")

    # Additional test cases
    test_cases = [
        (0b0010101011110001, 13),
        (0b0000000000000001, 0),
        (0b0000000000000000, 0xF0),
        (0b1000000000000000, 15),
        (0b0100000000000000, 14),
        (0b0000000100000000, 8),
        (0b0000000010000000, 7),
        (0b0000000000000010, 1),
        (0b1010101010101010, 15),
        (0b0101010101010101, 14),
        (0b0000111100001111, 11),
        (0b1111111111111111, 15),
    ]
    
    for i, (a, b, expected) in enumerate(test_cases):
        dut._log.info(f"Additional test case {i+1}: A={a:08b}, B={b:08b}")
        dut.uio_in.value = a
        dut.ui_in.value = b
        await ClockCycles(dut.clk, 1)
        
        assert dut.uo_out.value == expected, f"Expected {expected}, got {dut.uo_out.value}"
        dut._log.info(f"Additional test case {i+1} passed: uo_out = {dut.uo_out.value}")

    dut._log.info("All tests passed!")
