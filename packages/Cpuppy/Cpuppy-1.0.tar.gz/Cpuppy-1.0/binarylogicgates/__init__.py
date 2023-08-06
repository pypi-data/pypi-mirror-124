def lg_not(input_a):
    output = 0
    if input_a == 1:
        output = 0
    elif input_a == 0:
        output = 1
    return output

def lg_and(input_a, input_b):
    if input_a and input_b == 1:
        output = 1
    else:
        output = 0
    return output

def lg_nand(input_a, input_b):
    output = 0
    if input_a and input_b == 1:
        output = 0
    elif not (input_a and input_b) == 1:
        output = 1
    return output

def lg_or(input_a, input_b):
    if input_a or input_b == 1:
        output = 1
    else:
        output = 0
    return output

def lg_nor(input_a, input_b):
    if not (input_a or input_b) == 1:
        output = 1
    else:
        output = 0
    return output

def lg_xor(input_a, input_b):
    input_c = lg_or(input_a, input_b)
    input_d = lg_nand(input_a, input_b)
    output = lg_and(input_c, input_d)
    return output

def lg_xnor(input_a, input_b):
    output = lg_not(lg_xor(input_a, input_b))
    return output

def lg_sr_latch(lg_set, lg_reset):
    input_d = 0
    input_c = lg_nor(lg_set, input_d)
    input_d = lg_nor(input_c, lg_reset)
    output = input_d
    return output

def lg_data_latch(lg_set, lg_reset):
    input_d = 0
    input_c = lg_nor(lg_and(lg_set, lg_reset), input_d)
    input_d = lg_nor(input_c, lg_and(lg_reset, lg_not(lg_set)))
    output = input_d
    return output

def lg_register(input_a, input_b, input_c, input_d, lg_store):
    output_a = lg_data_latch(input_a, lg_store)
    output_b = lg_data_latch(input_b, lg_store)
    output_c = lg_data_latch(input_c, lg_store)
    output_d = lg_data_latch(input_d, lg_store)
    return output_a, output_b, output_c, output_d

def lg_data_flip_flop(lg_data, lg_clock):
    output = lg_data_latch(lg_data_latch(lg_data, lg_not(lg_clock)), lg_clock)
    return output


# Extra Logic Gates -------------------------------------------------------------------------------
def elg_adder(input_a, input_b, input_c):
    input_d = lg_xor(input_a, input_b)
    input_e = lg_and(input_d, input_c)
    input_f = lg_and(input_a, input_b)
    output_a = lg_xor(input_d, input_c)
    output_b = lg_or(input_e, input_f)
    return output_a, output_b

def elg_4adder(input_aa, input_ab, input_ac, input_ad, input_ba, input_bb, input_bc, input_bd, input_cc):
    ao_1, ao_1a = elg_adder(input_ad, input_bd, input_cc)
    ao_2, ao_2a = elg_adder(input_ac, input_bc, ao_1a)
    ao_3, ao_3a = elg_adder(input_ab, input_bb, ao_2a)
    ao_4, ao_4a = elg_adder(input_aa, input_ba, ao_3a)
    output_a = ao_4
    output_b = ao_3
    output_c = ao_2
    output_d = ao_1
    output_e = ao_4a
    return output_a, output_b, output_c, output_d, output_e

def elg_alu(input_aa, input_ab, input_ac, input_ad, input_ba, input_bb, input_bc, input_bd, input_cc):
    input_ba = lg_xor(input_ba, input_cc)
    input_bb = lg_xor(input_bb, input_cc)
    input_bc = lg_xor(input_bc, input_cc)
    input_bd = lg_xor(input_bd, input_cc)
    output_a, output_b, output_c, output_d, output_e = elg_4adder(
        input_aa, input_ab, input_ac, input_ad, input_ba, input_bb, input_bc, input_bd, input_cc
    )
    output_f = output_a
    output_g = lg_and(lg_and(lg_and(lg_not(output_a), lg_not(output_b)), lg_not(output_c)), lg_not(output_d))
    return output_a, output_b, output_c, output_d, output_e, output_f, output_g

def elg_1bit_register(elg_data, elg_store, elg_clock):
    output = 0
    output = lg_data_flip_flop(lg_or(lg_and(output, lg_not(elg_store)), lg_and(elg_store, elg_data)), elg_clock)
    return output

def elg_4bit_register(elg_data_1, elg_data_2, elg_data_3, elg_data_4, elg_store, elg_clock):
    output_a = elg_1bit_register(elg_data_1, elg_store, elg_clock)
    output_b = elg_1bit_register(elg_data_2, elg_store, elg_clock)
    output_c = elg_1bit_register(elg_data_3, elg_store, elg_clock)
    output_d = elg_1bit_register(elg_data_4, elg_store, elg_clock)
    return output_a, output_b, output_c, output_d
