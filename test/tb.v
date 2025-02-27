`default_nettype none
`timescale 1ns / 1ps

/* This testbench just instantiates the module and makes some convenient wires
   that can be driven / tested by the cocotb test.py.
*/
module tb ();

  // Dump the signals to a VCD file. You can view it with gtkwave or surfer.
  initial begin
    $dumpfile("tb.vcd");
    $dumpvars(0, tb);
    #1;
  end

  // Wire up the inputs and outputs:
  reg clk;
  reg rst_n;
  reg ena;
  reg [7:0] ui_in;
  reg [7:0] uio_in;
  wire [7:0] uo_out;
  wire [7:0] uio_out;
  wire [7:0] uio_oe;
`ifdef GL_TEST
  wire VPWR = 1'b1;
  wire VGND = 1'b0;
`endif

  // Instantiate the module with the correct name
  tt_um_KHC_module user_project (
`ifdef GL_TEST
      .VPWR(VPWR),
      .VGND(VGND),
`endif
      .ui_in  (ui_in),    // B[7:0]
      .uo_out (uo_out),   // C[7:0]
      .uio_in (uio_in),   // A[7:0]
      .uio_out(uio_out),  // Not used
      .uio_oe (uio_oe),   // Output enable
      .ena    (ena),      // Enable
      .clk    (clk),      // Clock
      .rst_n  (rst_n)     // Reset
  );

endmodule
