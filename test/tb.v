`default_nettype none
`timescale 1ns / 1ps
module tb ();
  // Dump the signals to a VCD file
  initial begin
    $dumpfile("tb.vcd");
    $dumpvars(0, tb);
    
    // Initialize all inputs
    clk = 0;
    rst_n = 0;
    ena = 0;
    ui_in = 8'h00;
    uio_in = 8'h00;
    
    // Release reset and enable the module
    #10 rst_n = 1;
    ena = 1;
    
    // Test case 1: No bits set - should output 0xF0
    #10 ui_in = 8'h00; uio_in = 8'h00;
    
    // Test case 2: Only LSB set - should output 0
    #10 ui_in = 8'h01; uio_in = 8'h00;
    
    // Test case from problem statement (a): In[15:0] = 0010 1010 1111 0001
    #10 ui_in = 8'hF1; uio_in = 8'h2A; // Should output 13 (0x0D)
    
    // Test case from problem statement (b): In[15:0] = 0000 0000 0000 0001
    #10 ui_in = 8'h01; uio_in = 8'h00; // Should output 0 (0x00)
    
    // Additional test cases for coverage
    #10 ui_in = 8'h00; uio_in = 8'h80; // Bit 15 set, should output 15 (0x0F)
    #10 ui_in = 8'h00; uio_in = 8'h40; // Bit 14 set, should output 14 (0x0E)
    #10 ui_in = 8'h00; uio_in = 8'h08; // Bit 11 set, should output 11 (0x0B)
    
    // All bits set - should prioritize MSB (15)
    #10 ui_in = 8'hFF; uio_in = 8'hFF;
    
    // Alternating bits - should still prioritize MSB
    #10 ui_in = 8'hAA; uio_in = 8'hAA;
    
    // Run for a bit more and finish
    #20 $finish;
  end
  
  // Generate clock
  always #5 clk = ~clk;
  
  // Wire up the inputs and outputs:
  reg clk;
  reg rst_n;
  reg ena;
  reg [7:0] ui_in;    // Lower 8 bits (B[7:0])
  reg [7:0] uio_in;   // Upper 8 bits (A[7:0])
  wire [7:0] uo_out;  // Output C[7:0]
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
      .ui_in  (ui_in),    // Lower 8 bits (B[7:0])
      .uo_out (uo_out),   // Output C[7:0]
      .uio_in (uio_in),   // Upper 8 bits (A[7:0])
      .uio_out(uio_out),  // Not used
      .uio_oe (uio_oe),   // Not used
      .ena    (ena),      // enable
      .clk    (clk),      // clock
      .rst_n  (rst_n)     // not reset
  );
endmodule
