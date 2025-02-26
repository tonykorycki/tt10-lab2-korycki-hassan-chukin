module bitwise_majority (
    input [7:0] A,
    input [7:0] B,
    output [7:0] C
);
    assign C = A | B;  // Bitwise OR operation
endmodule
