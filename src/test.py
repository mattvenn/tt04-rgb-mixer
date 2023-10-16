import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles
from encoder import Encoder

clocks_per_phase = 10

async def run_encoder_test(dut, encoder, max_count):
    count = 0
    for i in range(clocks_per_phase * 2 * max_count):
        await encoder.update(1)
        if (i+clocks_per_phase) % (2*clocks_per_phase) == 0:
            assert count == int(dut.enc_val.value)
            count += 1

    # let noisy transition finish, otherwise can get an extra count
    for i in range(10):
        await encoder.update(0)

    
@cocotb.test()
async def test_rgb_mixer(dut):
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # reset
    dut._log.info("reset")
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    dut.enc0_a.value = 0
    dut.enc0_b.value = 0
    dut.enc1_a.value = 0
    dut.enc1_b.value = 0
    dut.enc2_a.value = 0
    dut.enc2_b.value = 0
    await ClockCycles(dut.clk, 10)

    encoder0 = Encoder(dut.clk, dut.enc0_a, dut.enc0_b, clocks_per_phase = clocks_per_phase, noise_cycles = clocks_per_phase / 4)
    encoder1 = Encoder(dut.clk, dut.enc1_a, dut.enc1_b, clocks_per_phase = clocks_per_phase, noise_cycles = clocks_per_phase / 4)
    encoder2 = Encoder(dut.clk, dut.enc2_a, dut.enc2_b, clocks_per_phase = clocks_per_phase, noise_cycles = clocks_per_phase / 4)

    # pwm should all be low at start
    assert dut.pwm0_out.value == 0
    assert dut.pwm1_out.value == 0
    assert dut.pwm1_out.value == 0

    # do 3 ramps for each encoder 
    max_count = 255

    # set the encoder to appear on the debug output so we can check the value is correct
    dut.enc_sel.value = 0
    await run_encoder_test(dut, encoder0, max_count)
    dut.enc_sel.value = 1
    await run_encoder_test(dut, encoder1, max_count)
    dut.enc_sel.value = 2
    await run_encoder_test(dut, encoder2, max_count)

    # sync to pwm
    await RisingEdge(dut.pwm0_out)
    await RisingEdge(dut.clk)

    # pwm should all be on for max_count 
    for i in range(max_count): 
        assert dut.pwm0_out.value == 1
        assert dut.pwm1_out.value == 1
        assert dut.pwm2_out.value == 1
        await ClockCycles(dut.clk, 1)
