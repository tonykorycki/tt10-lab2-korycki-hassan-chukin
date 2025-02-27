`timescale 1ns / 1ps
module tb ();
    reg [7:0] A, B;
    wire [7:0] C;
    
    tt_um_KHC_module user_projet (
        .A(A),
        .B(B),
        .C(C)
    );

    initial begin
        $dumpfile("tb_bitwise_majority.vcd");
        $dumpvars(0, tb_bitwise_majority);

        A = 8'b11001010; B = 8'b01100011; #10;
        A = 8'b10101010; B = 8'b01010101; #10;

        $finish;
    end
endmodule
