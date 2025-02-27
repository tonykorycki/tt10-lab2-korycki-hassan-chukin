# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
import random

@cocotb.test()
async def test_priority_encoder(dut):
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
    
    dut._log.info("Test priority encoder operation")
    
    # Test cases from the problem statement
    test_cases = [
        # In[15:0] = {A[7:0], B[7:0]}          Expected C[7:0]
        (0b0010101011110001, 13),           # Example a: 0000 1101 (13)
        (0b0000000000000001, 0),            # Example b: 0000 0000 (0)
        (0b0000000000000000, 0b11110000),   # Special case: 1111 0000
        # Additional test cases - one bit set at each position
        (0b1000000000000000, 15),           # MSB set: 0000 1111 (15)
        (0b0100000000000000, 14),           # Bit 14 set: 0000 1110 (14)
        (0b0000000100000000, 8),            # Middle bit set: 0000 1000 (8)
        (0b0000000010000000, 7),            # Bit 7 set: 0000 0111 (7)
        (0b0000000000000010, 1),            # Bit 1 set: 0000 0001 (1)
        # Multiple bits set
        (0b1010101010101010, 15),           # Alternating bits with MSB set
        (0b0101010101010101, 14),           # Alternating bits with bit 14 set
        (0b0000111100001111, 11),           # Pattern with bit 11 as first set bit
        (0b1111111111111111, 15),           # All bits set
    ]
    
    for input_val, expected in test_cases:
        # Split the 16-bit input into two 8-bit parts for ui_in and uio_in
        dut.ui_in.value = input_val & 0xFF         # Lower 8 bits (B[7:0])
        dut.uio_in.value = (input_val >> 8) & 0xFF # Upper 8 bits (A[7:0])
        
        # Wait for one clock cycle
        await ClockCycles(dut.clk, 1)
        
        # Check the result
        result = int(dut.uo_out.value)
        input_bin = format(input_val, '016b')
        expected_bin = format(expected, '08b') if expected != 0b11110000 else "11110000"
        result_bin = format(result, '08b')
        
        dut._log.info(f"Test: In = {input_bin} (0x{input_val:04x}), Expected = {expected_bin} (0x{expected:02x}), Got = {result_bin} (0x{result:02x})")
        assert result == expected, f"Expected 0x{expected:02x}, got 0x{result:02x}"
    
    # Additional random test cases with one random bit set
    dut._log.info("Running random single-bit test cases")
    for _ in range(16):
        bit_pos = random.randint(0, 15)
        input_val = 1 << bit_pos
        expected = bit_pos
        
        # Split the 16-bit input
        dut.ui_in.value = input_val & 0xFF
        dut.uio_in.value = (input_val >> 8) & 0xFF
        
        await ClockCycles(dut.clk, 1)
        
        result = int(dut.uo_out.value)
        input_bin = format(input_val, '016b')
        result_bin = format(result, '08b')
        
        dut._log.info(f"Random bit test: In = {input_bin} (bit {bit_pos}), Expected = {expected}, Got = {result}")
        assert result == expected, f"Expected {expected}, got {result}"
    
    # Random test cases with multiple bits set
    dut._log.info("Running random multiple-bit test cases")
    for _ in range(20):
        # Create random input with multiple bits
        input_val = random.randint(1, 0xFFFF)  # Avoid all zeros
        
        # Determine expected output (highest bit position that is set)
        expected = 0
        for i in range(15, -1, -1):
            if input_val & (1 << i):
                expected = i
                break
        
        # Split the 16-bit input
        dut.ui_in.value = input_val & 0xFF
        dut.uio_in.value = (input_val >> 8) & 0xFF
        
        await ClockCycles(dut.clk, 1)
        
        result = int(dut.uo_out.value)
        input_bin = format(input_val, '016b')
        
        dut._log.info(f"Random multi-bit test: In = {input_bin}, Expected = {expected}, Got = {result}")
        assert result == expected, f"Expected {expected}, got {result}"
    
    # Test the special case explicitly one more time
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    
    await ClockCycles(dut.clk, 1)
    
    result = int(dut.uo_out.value)
    expected = 0xF0  # 11110000
    
    dut._log.info(f"Special case test: In = 0000000000000000, Expected = 11110000, Got = {format(result, '08b')}")
    assert result == expected, f"Expected 0xF0, got 0x{result:02x}"
    
    dut._log.info("All priority encoder tests passed successfully!")
