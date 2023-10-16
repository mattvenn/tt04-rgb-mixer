`default_nettype none
`timescale 1ns/1ps

/*
this testbench just instantiates the module and makes some convenient wires
that can be driven / tested by the cocotb test.py
*/

// testbench is controlled by test.py
module tb ();

    // this part dumps the trace to a vcd file that can be viewed with GTKWave
    initial begin
        $dumpfile ("tb.vcd");
        $dumpvars (0, tb);
        #1;
    end

    // wire up the inputs and outputs
    reg  clk;
    reg  rst_n;
    reg  ena;
    reg  enc0_a, enc0_b, enc1_a, enc1_b, enc2_a, enc2_b;
    reg  [7:0] uio_in;

    wire [7:0] enc_val;
    reg  [1:0] enc_sel;
    wire [7:0] uo_out;
    wire [7:0] uio_oe;

    wire pwm0_out = uo_out[0];
    wire pwm1_out = uo_out[1];
    wire pwm2_out = uo_out[2];
    wire debounce_a = uo_out[3];
    wire debounce_b = uo_out[4];

    tt_um_rgb_mixer tt_um_rgb_mixer (
    // include power ports for the Gate Level test
    `ifdef GL_TEST
        .VPWR( 1'b1),
        .VGND( 1'b0),
    `endif
        .ui_in      ({enc_sel, enc2_b, enc2_a, enc1_b, enc1_a, enc0_b, enc0_a}),    // Dedicated inputs
        .uo_out     (uo_out),   // Dedicated outputs
        .uio_in     (uio_in),   // IOs: Input path
        .uio_out    (enc_val),  // IOs: Output path
        .uio_oe     (uio_oe),   // IOs: Enable path (active high: 0=input, 1=output)
        .ena        (ena),      // enable - goes high when design is selected
        .clk        (clk),      // clock
        .rst_n      (rst_n)     // not reset
        );

endmodule
