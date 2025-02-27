/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */
`default_nettype none
module tt_um_KHC_module (
    input  wire [7:0] ui_in,    // Lower 8 bits (B[7:0])
    output wire [7:0] uo_out,   // Output C[7:0]
    input  wire [7:0] uio_in,   // Upper 8 bits (A[7:0])
    output wire [7:0] uio_out,  // Not used
    output wire [7:0] uio_oe,   // Set as inputs
    input  wire       ena,      // Enable
    input  wire       clk,      // Clock
    input  wire       rst_n     // Reset (active low)
);
    // Combine input to create 16-bit input for priority encoder
    wire [15:0] combined_input = {uio_in, ui_in};
    reg [7:0] encoder_output;
    
    // Priority encoder logic
    integer i;
    always @(*) begin
        // Default case: If no bits are set, output 0xF0
        encoder_output = 8'b1111_0000;
        
        // Check bits from MSB to LSB
        for (i = 15; i >= 0; i = i - 1) begin
            if (combined_input[i]) begin
                encoder_output = i[7:0]; // Convert integer to 8-bit
                // No need for break; in synthesizable code - 
                // priority is implicit in the loop order
            end
        end
    end
    
    // Assign outputs
    assign uo_out = encoder_output;
    assign uio_out = 8'b0;  // Not used
    assign uio_oe = 8'b0;   // Set as inputs
    
    // Handle unused inputs
    wire _unused = &{ena, clk, rst_n, 1'b0};
endmodule
