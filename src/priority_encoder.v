module priority_encoder (
    input [15:0] In,
    output reg [7:0] C
);
    integer i;
    always @(*) begin
        C = 8'b1111_0000; // Default case
        for (i = 15; i >= 0; i = i - 1) begin
            if (In[i]) begin
                C = i;
                break;
            end
        end
    end
endmodule
