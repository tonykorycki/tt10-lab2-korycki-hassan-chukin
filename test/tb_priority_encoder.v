`timescale 1ns / 1ps
module tb_priority_encoder;
    reg [15:0] In;
    wire [7:0] C;
    
    priority_encoder uut (  // Instantiating the module
        .In(In),
        .C(C)
    );

    initial begin
        $dumpfile("tb_priority_encoder.vcd"); // Generates waveform file
        $dumpvars(0, tb_priority_encoder);

        In = 16'b0010_1010_1111_0001; #10;
        In = 16'b0000_0000_0000_0001; #10;
        In = 16'b0000_0000_0000_0000; #10;

        $finish;
    end
endmodule
