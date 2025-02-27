/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */
`default_nettype none
module tt_um_KHC_module (
    input  wire [7:0] ui_in,    // Lower 8 bits (B[7:0])
    output reg  [7:0] uo_out,   // Output C[7:0] - changed to reg for direct assignment
    input  wire [7:0] uio_in,   // Upper 8 bits (A[7:0])
    output wire [7:0] uio_out,  // Not used
    output wire [7:0] uio_oe,   // Set as inputs
    input  wire       ena,      // Enable
    input  wire       clk,      // Clock
    input  wire       rst_n     // Reset (active low)
);
    // Combine input to create 16-bit input for priority encoder
    wire [15:0] combined_input = {uio_in, ui_in};
    
    // Priority encoder logic
    always @(*) begin
        // Default case: If no bits are set, output 0xF0
        uo_out = 8'b1111_0000;
        
        // Check bits from MSB to LSB
        if (combined_input[15]) uo_out = 8'd15;
        else if (combined_input[14]) uo_out = 8'd14;
        else if (combined_input[13]) uo_out = 8'd13;
        else if (combined_input[12]) uo_out = 8'd12;
        else if (combined_input[11]) uo_out = 8'd11;
        else if (combined_input[10]) uo_out = 8'd10;
        else if (combined_input[9]) uo_out = 8'd9;
        else if (combined_input[8]) uo_out = 8'd8;
        else if (combined_input[7]) uo_out = 8'd7;
        else if (combined_input[6]) uo_out = 8'd6;
        else if (combined_input[5]) uo_out = 8'd5;
        else if (combined_input[4]) uo_out = 8'd4;
        else if (combined_input[3]) uo_out = 8'd3;
        else if (combined_input[2]) uo_out = 8'd2;
        else if (combined_input[1]) uo_out = 8'd1;
        else if (combined_input[0]) uo_out = 8'd0;
        // Default case already set at the beginning
    end
    
    // Assign remaining outputs
    assign uio_out = 8'b0;  // Not used
    assign uio_oe = 8'b0;   // Set as inputs
    
    // Handle unused inputs - fixed the syntax error in rst_n reference
    wire unused = &{ena, clk, rst_n, 1'b0};
endmodule
