import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

@cocotb.test()
async def test_priority_encoder(dut):
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut.rst_n.value = 0
    await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    dut.ena.value = 1

    # Test cases
    test_cases = [
        (0b0010101011110001, 13),
        (0b0000000000000001, 0),
        (0b0000000000000000, 0xF0),
        (0b0010101011110001, 13),           # Example a: 0000 1101 (13)
        (0b0000000000000001, 0),            # Example b: 0000 0000 (0)
        (0b0000000000000000, 0xF0),         # Special case: 1111 0000
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
        (0b1111111111111111, 15), 
        # Add more test cases here
    ]

    for input_val, expected in test_cases:
        dut.ui_in.value = input_val & 0xFF
        dut.uio_in.value = (input_val >> 8) & 0xFF
        await RisingEdge(dut.clk)
        await FallingEdge(dut.clk)
        result = dut.uo_out.value
        assert result == expected, f"Expected {expected}, got {result} for input {input_val:016b}"
