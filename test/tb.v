`default_nettype none
`timescale 1ns / 1ps

module tb ();
  // Dump the signals to a VCD file
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

  // Instantiate the module
  tt_um_KHC_module user_project (
`ifdef GL_TEST
      .VPWR(VPWR),
      .VGND(VGND),
`endif
      .ui_in  (ui_in),    // A input
      .uo_out (uo_out),   // C output
      .uio_in (uio_in),   // B input
      .uio_out(uio_out),  // Not used
      .uio_oe (uio_oe),   // Not used
      .ena    (ena),      // enable
      .clk    (clk),      // clock
      .rst_n  (rst_n)     // not reset
  );
endmodule
