`default_nettype none
module tt_um_KHC_module (
    input  wire [7:0] ui_in,    // Lower 8 bits (B[7:0])
    output reg  [7:0] uo_out,   // Output C[7:0]
    input  wire [7:0] uio_in,   // Upper 8 bits (A[7:0])
    output wire [7:0] uio_out,  // Not used
    output wire [7:0] uio_oe,   // Set as inputs
    input  wire       ena,      // Enable
    input  wire       clk,      // Clock
    input  wire       rst_n     // Reset (active low)
);
    wire [15:0] combined_input = {uio_in, ui_in};
    
    integer i;
    always @(*) begin
        uo_out = 8'b11110000; // Default case
        for (i = 15; i >= 0; i = i - 1) begin
            if (combined_input[i]) begin
                uo_out = i[7:0];
                break;
            end
        end
    end
    
    assign uio_out = 8'b0;
    assign uio_oe = 8'b0;
    
    wire unused = &{ena, clk, rst_n, 1'b0};
endmodule
