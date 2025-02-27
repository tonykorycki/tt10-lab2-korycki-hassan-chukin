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
        casez (combined_input)
            16'b1???????????????: uo_out = 8'd15;
            16'b01??????????????: uo_out = 8'd14;
            16'b001?????????????: uo_out = 8'd13;
            16'b0001????????????: uo_out = 8'd12;
            16'b00001???????????: uo_out = 8'd11;
            16'b000001??????????: uo_out = 8'd10;
            16'b0000001?????????: uo_out = 8'd9;
            16'b00000001????????: uo_out = 8'd8;
            16'b000000001???????: uo_out = 8'd7;
            16'b0000000001??????: uo_out = 8'd6;
            16'b00000000001?????: uo_out = 8'd5;
            16'b000000000001????: uo_out = 8'd4;
            16'b0000000000001???: uo_out = 8'd3;
            16'b00000000000001??: uo_out = 8'd2;
            16'b000000000000001?: uo_out = 8'd1;
            16'b0000000000000001: uo_out = 8'd0;
            16'b0000000000000000: uo_out = 8'b11110000;
            default: uo_out = 8'b11110000; // This should never happen
        endcase
    end
    
    // Assign remaining outputs
    assign uio_out = 8'b0;  // Not used
    assign uio_oe = 8'b0;   // Set as inputs
    
    // Handle unused inputs
    wire unused = &{ena, clk, rst_n, 1'b0};
endmodule
