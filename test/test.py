import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

@cocotb.test()
async def test_priority_encoder(dut):
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut.rst_n.value = 0
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    await RisingEdge(dut.clk)
    dut.rst_n.value = 1

    # Test cases
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

    for input_val, expected in test_cases:
        dut.ui_in.value = input_val & 0xFF
        dut.uio_in.value = (input_val >> 8) & 0xFF
        await RisingEdge(dut.clk)
        await FallingEdge(dut.clk)
        result = int(dut.uo_out.value)
        assert result == expected, f"Expected {expected}, got {result} for input {input_val:016b}"
