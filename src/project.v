`default_nettype none

module tt_um_KHC_module (
    input  wire [7:0] ui_in,    // First 8 bits (B[7:0])
    output wire [7:0] uo_out,   // Output C[7:0]
    input  wire [7:0] uio_in,   // Second 8 bits (A[7:0])
    output wire [7:0] uio_out,  // Not used
    output wire [7:0] uio_oe,   // Set to output mode
    input  wire       ena,      // Enable
    input  wire       clk,      // Clock
    input  wire       rst_n     // Reset (active low)
);

  // Combine inputs to form In[15:0] = {A[7:0], B[7:0]}
  wire [15:0] combined_input = {uio_in, ui_in};
  
  // Priority encoder logic
  reg [7:0] encoder_output;
  
  always @(*) begin
    if (combined_input == 16'h0000) begin
      // Special case: all inputs are 0
      encoder_output = 8'hF0; // 1111 0000
    end else begin
      // Find the first bit that is 1 (starting from MSB)
      encoder_output = 8'h00;
      
      if (combined_input[15]) encoder_output = 8'd15;
      else if (combined_input[14]) encoder_output = 8'd14;
      else if (combined_input[13]) encoder_output = 8'd13;
      else if (combined_input[12]) encoder_output = 8'd12;
      else if (combined_input[11]) encoder_output = 8'd11;
      else if (combined_input[10]) encoder_output = 8'd10;
      else if (combined_input[9]) encoder_output = 8'd9;
      else if (combined_input[8]) encoder_output = 8'd8;
      else if (combined_input[7]) encoder_output = 8'd7;
      else if (combined_input[6]) encoder_output = 8'd6;
      else if (combined_input[5]) encoder_output = 8'd5;
      else if (combined_input[4]) encoder_output = 8'd4;
      else if (combined_input[3]) encoder_output = 8'd3;
      else if (combined_input[2]) encoder_output = 8'd2;
      else if (combined_input[1]) encoder_output = 8'd1;
      else if (combined_input[0]) encoder_output = 8'd0;
    end
  end
  
  //
