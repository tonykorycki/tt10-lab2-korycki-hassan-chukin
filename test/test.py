# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
import random

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
    
    # Basic test cases for bitwise OR
    basic_test_cases = [
        (0b11001010, 0b01100011, 0b11101011),  # First test case from original
        (0b10101010, 0b01010101, 0b11111111),  # Second test case from original
        (0, 0, 0),                             # All zeros
        (255, 0, 255),                         # A all ones, B all zeros
        (0, 255, 255),                         # A all zeros, B all ones
        (255, 255, 255),                       # All ones
        (0b10000000, 0b00000001, 0b10000001),  # MSB in A, LSB in B
        (0b00000001, 0b10000000, 0b10000001),  # LSB in A, MSB in B
        (0b00001111, 0b11110000, 0b11111111),  # Lower half and upper half
        (0b01010101, 0b10101010, 0b11111111),  # Alternating bits
        (0b11111110, 0b00000001, 0b11111111),  # All but one bit and the missing bit
        (0b00010000, 0b00100000, 0b00110000),  # Isolated single bits
        (0b11111111, 0b11111111, 0b11111111),  # Double-check all ones
    ]
    
    # Run basic test cases
    for a, b, expected in basic_test_cases:
        dut.ui_in.value = a
        dut.uio_in.value = b
        
        # Wait for one clock cycle
        await ClockCycles(dut.clk, 1)
        
        # Check the result
        result = int(dut.uo_out.value)
        dut._log.info(f"Basic test: {a:08b} | {b:08b} = {result:08b}, Expected: {expected:08b}")
        assert result == expected, f"Expected {expected:08b}, got {result:08b}"
    
    # Random test cases - generate 25 random test pairs
    dut._log.info("Running random test cases")
    for _ in range(25):
        a = random.randint(0, 255)
        b = random.randint(0, 255)
        expected = a | b
        
        dut.ui_in.value = a
        dut.uio_in.value = b
        
        await ClockCycles(dut.clk, 1)
        
        result = int(dut.uo_out.value)
        dut._log.info(f"Random test: {a:08b} | {b:08b} = {result:08b}, Expected: {expected:08b}")
        assert result == expected, f"Expected {expected:08b}, got {result:08b}"
    
    # Edge cases - testing with walking 1s and walking 0s
    dut._log.info("Testing with walking patterns")
    
    # Walking 1s in A, all 0s in B
    for bit_pos in range(8):
        a = 1 << bit_pos  # Single bit set at position bit_pos
        b = 0
        expected = a | b
        
        dut.ui_in.value = a
        dut.uio_in.value = b
        
        await ClockCycles(dut.clk, 1)
        
        result = int(dut.uo_out.value)
        dut._log.info(f"Walking 1 in A: {a:08b} | {b:08b} = {result:08b}, Expected: {expected:08b}")
        assert result == expected, f"Expected {expected:08b}, got {result:08b}"
    
    # All 0s in A, walking 1s in B
    for bit_pos in range(8):
        a = 0
        b = 1 << bit_pos  # Single bit set at position bit_pos
        expected = a | b
        
        dut.ui_in.value = a
        dut.uio_in.value = b
        
        await ClockCycles(dut.clk, 1)
        
        result = int(dut.uo_out.value)
        dut._log.info(f"Walking 1 in B: {a:08b} | {b:08b} = {result:08b}, Expected: {expected:08b}")
        assert result == expected, f"Expected {expected:08b}, got {result:08b}"
    
    # Walking 0s in A (all 1s except one position), all 1s in B
    for bit_pos in range(8):
        a = 0xFF ^ (1 << bit_pos)  # All bits set except at position bit_pos
        b = 0xFF
        expected = a | b
        
        dut.ui_in.value = a
        dut.uio_in.value = b
        
        await ClockCycles(dut.clk, 1)
        
        result = int(dut.uo_out.value)
        dut._log.info(f"Walking 0 in A: {a:08b} | {b:08b} = {result:08b}, Expected: {expected:08b}")
        assert result == expected, f"Expected {expected:08b}, got {result:08b}"
    
    dut._log.info("All tests passed successfully!")
