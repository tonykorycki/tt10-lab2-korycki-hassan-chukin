# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
import random

@cocotb.test()
async def test_priority_encoder(dut):
# Set up clock
clock = Clock(dut.clk, 10, units="us")
cocotb.start_soon(clock.start())

text
# Reset
dut.ena.value = 1
dut.ui_in.value = 0
dut.uio_in.value = 0
dut.rst_n.value = 0
await ClockCycles(dut.clk, 10)
dut.rst_n.value = 1

# Test case a: In[15:0] = 0010 1010 1111 0001
dut.uio_in.value = 0b00101010  # A[7:0]
dut.ui_in.value = 0b11110001   # B[7:0]
await ClockCycles(dut.clk, 1)

expected = 13
assert dut.uo_out.value == expected, f"Expected {expected}, got {dut.uo_out.value}"

# Test case b: In[15:0] = 0000 0000 0000 0001
dut.uio_in.value = 0b00000000  # A[7:0]
dut.ui_in.value = 0b00000001   # B[7:0]
await ClockCycles(dut.clk, 1)

expected = 0
assert dut.uo_out.value == expected, f"Expected {expected}, got {dut.uo_out.value}"

# Test case c: In[15:0] = 0000 0000 0000 0000
dut.uio_in.value = 0b00000000  # A[7:0]
dut.ui_in.value = 0b00000000   # B[7:0]
await ClockCycles(dut.clk, 1)

expected = 0xF0
assert dut.uo_out.value == expected, f"Expected {expected}, got {dut.uo_out.value}"

# Test each bit position individually
for bit_pos in range(16):
    # Create input with only one bit set
    a_val = 0
    b_val = 0
    
    if bit_pos >= 8:
        a_val = 1 << (bit_pos - 8)
    else:
        b_val = 1 << bit_pos
        
    dut.uio_in.value = a_val
    dut.ui_in.value = b_val
    await ClockCycles(dut.clk, 1)
    
    expected = bit_pos
    assert dut.uo_out.value == expected, f"Bit position {bit_pos}: Expected {expected}, got {dut.uo_out.value}"

# Test with different patterns
test_patterns = [
    # (A[7:0], B[7:0], expected output)
    (0b10000000, 0b00000000, 15),  # MSB is 1
    (0b01000000, 0b00000000, 14),  # Second MSB is 1
    (0b00100000, 0b00000000, 13),  # Third MSB is 1
    (0b00010000, 0b00000000, 12),  # Fourth MSB is 1
    (0b00001000, 0b00000000, 11),  # Fifth MSB is 1
    (0b00000100, 0b00000000, 10),  # Sixth MSB is 1
    (0b00000010, 0b00000000, 9),   # Seventh MSB is 1
    (0b00000001, 0b00000000, 8),   # Eighth MSB is 1
    (0b00000000, 0b10000000, 7),   # Ninth MSB is 1
    (0b00000000, 0b01000000, 6),   # Tenth MSB is 1
    (0b00000000, 0b00100000, 5),   # Eleventh MSB is 1
    (0b00000000, 0b00010000, 4),   # Twelfth MSB is 1
    (0b00000000, 0b00001000, 3),   # Thirteenth MSB is 1
    (0b00000000, 0b00000100, 2),   # Fourteenth MSB is 1
    (0b00000000, 0b00000010, 1),   # Fifteenth MSB is 1
    (0b00000000, 0b00000001, 0),   # LSB is 1
    (0b11111111, 0b11111111, 15),  # All bits are 1
    (0b01111111, 0b11111111, 14),  # All bits except MSB are 1
    (0b00000000, 0b11111111, 7),   # Lower 8 bits all 1
    (0b11111111, 0b00000000, 15),  # Upper 8 bits all 1
    (0b10101010, 0b10101010, 15),  # Alternating pattern
    (0b01010101, 0b01010101, 14),  # Alternating pattern shifted
]

for i, (a, b, expected) in enumerate(test_patterns):
    dut.uio_in.value = a
    dut.ui_in.value = b
    await ClockCycles(dut.clk, 1)
    
    assert dut.uo_out.value == expected, f"Pattern test {i}: Expected {expected}, got {dut.uo_out.value}"

# Test with random patterns
for i in range(20):
    # Generate random 16-bit value
    a_val = random.randint(0, 255)
    b_val = random.randint(0, 255)
    combined = (a_val << 8) | b_val
    
    # Calculate expected output
    if combined == 0:
        expected = 0xF0
    else:
        expected = 15
        for j in range(15, -1, -1):
            if (combined >> j) & 1:
                expected = j
                break
    
    dut.uio_in.value = a_val
    dut.ui_in.value = b_val
    await ClockCycles(dut.clk, 1)
    
    assert dut.uo_out.value == expected, f"Random test {i}: Expected {expected}, got {dut.uo_out.value}"

# Test boundary cases
boundary_cases = [
    (0b11111111, 0b11111110, 15),  # All bits except LSB are 1
    (0b00000000, 0b00000000, 0xF0), # All zeros (special case)
    (0b10000000, 0b00000001, 15),   # MSB and LSB only
    (0b00000001, 0b00000001, 8),    # Bit 8 and bit 0 only
]

for i, (a, b, expected) in enumerate(boundary_cases):
    dut.uio_in.value = a
    dut.ui_in.value = b
    await ClockCycles(dut.clk, 1)
    
    assert dut.uo_out.value == expected, f"Boundary test {i}: Expected {expected}, got {dut.uo_out.value}"
