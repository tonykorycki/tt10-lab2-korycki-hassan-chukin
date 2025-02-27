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
        (0b10000000, 0b00000000, 15), # Bit 15 is 1
        (0b01000000, 0b00000000, 14), # Bit 14 is 1
        (0b00100000, 0b00000000, 13), # Bit 13 is 1
        (0b00010000, 0b00000000, 12), # Bit 12 is 1
        (0b00001000, 0b00000000, 11), # Bit 11 is 1
        (0b00000100, 0b00000000, 10), # Bit 10 is 1
        (0b00000010, 0b00000000, 9), # Bit 9 is 1
        (0b00000001, 0b00000000, 8), # Bit 8 is 1
        (0b00000000, 0b10000000, 7), # Bit 7 is 1
        (0b00000000, 0b01000000, 6), # Bit 6 is 1
        (0b00000000, 0b00100000, 5), # Bit 5 is 1
        (0b00000000, 0b00010000, 4), # Bit 4 is 1
        (0b00000000, 0b00001000, 3), # Bit 3 is 1
        (0b00000000, 0b00000100, 2), # Bit 2 is 1
        (0b00000000, 0b00000010, 1), # Bit 1 is 1
        (0b00000000, 0b00000001, 0), # Bit 0 is 1
        (0b00000000, 0b00000000, 0xF0), # No bits are 1 (special case)

    ]
    
    for i, (a, b, expected) in enumerate(test_cases):
        dut._log.info(f"Additional test case {i+1}: A={a:08b}, B={b:08b}")
        dut.uio_in.value = a
        dut.ui_in.value = b
        await ClockCycles(dut.clk, 1)
        
        assert dut.uo_out.value == expected, f"Expected {expected}, got {dut.uo_out.value}"
        dut._log.info(f"Additional test case {i+1} passed: uo_out = {dut.uo_out.value}")

    dut._log.info("All tests passed!")
