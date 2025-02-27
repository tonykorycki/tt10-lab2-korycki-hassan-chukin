# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")
    # Set the clock period to 10 us (100 KHz)
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
    
    dut._log.info("Test bitwise OR operation")
    
    # Test cases for bitwise OR
    test_cases = [
        (0b11001010, 0b01100011, 0b11101011),  # First test case from original
        (0b10101010, 0b01010101, 0b11111111),  # Second test case from original
        (0, 0, 0),                             # All zeros
        (255, 0, 255),                         # A all ones, B all zeros
        (0, 255, 255),                         # A all zeros, B all ones
        (255, 255, 255)                        # All ones
    ]
    
    for a, b, expected in test_cases:
        dut.ui_in.value = a
        dut.uio_in.value = b
        
        # Wait for one clock cycle
        await ClockCycles(dut.clk, 1)
        
        # Check the result
        result = int(dut.uo_out.value)
        dut._log.info(f"Test: {a:08b} | {b:08b} = {result:08b}, Expected: {expected:08b}")
        assert result == expected, f"Expected {expected:08b}, got {result:08b}"
