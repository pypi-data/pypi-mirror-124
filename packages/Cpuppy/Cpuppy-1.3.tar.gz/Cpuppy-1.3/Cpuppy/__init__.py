
'''
Code by Katemi (20/10/2021)
Feel free to copy and distribute this code always you give me credit
'''

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

def lg_4bit_register(input_a, input_b, input_c, input_d, lg_store):
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

def elg_16adder(input_aa, input_ab, input_ac, input_ad, input_ae, input_af, input_ag, input_ah, input_ai, input_aj, input_ak, input_al, input_am, input_an, input_ao, input_ap, input_ba, input_bb, input_bc, input_bd, input_be, input_bf, input_bg, input_bh, input_bi, input_bj, input_bk, input_bl, input_bm, input_bn, input_bo, input_bp, input_ca):
    ao_1, ao_1a = elg_adder(input_ap, input_bp, input_ca)
    ao_2, ao_2a = elg_adder(input_ao, input_bo, ao_1a)
    ao_3, ao_3a = elg_adder(input_an, input_bn, ao_2a)
    ao_4, ao_4a = elg_adder(input_am, input_bm, ao_3a)
    ao_5, ao_5a = elg_adder(input_al, input_bl, ao_4a)
    ao_6, ao_6a = elg_adder(input_ak, input_bk, ao_5a)
    ao_7, ao_7a = elg_adder(input_aj, input_bj, ao_6a)
    ao_8, ao_8a = elg_adder(input_ai, input_bi, ao_7a)
    ao_9, ao_9a = elg_adder(input_ah, input_bh, ao_8a)
    ao_10, ao_10a = elg_adder(input_ag, input_bg, ao_9a)
    ao_11, ao_11a = elg_adder(input_af, input_bf, ao_10a)
    ao_12, ao_12a = elg_adder(input_ae, input_be, ao_11a)
    ao_13, ao_13a = elg_adder(input_ad, input_bd, ao_12a)
    ao_14, ao_14a = elg_adder(input_ac, input_bc, ao_13a)
    ao_15, ao_15a = elg_adder(input_ab, input_bb, ao_14a)
    ao_16, ao_16a = elg_adder(input_aa, input_ba, ao_15a)
    output_a = ao_16
    output_b = ao_15
    output_c = ao_14
    output_d = ao_13
    output_e = ao_12
    output_f = ao_11
    output_g = ao_10
    output_h = ao_9
    output_i = ao_8
    output_j = ao_7
    output_k = ao_6
    output_l = ao_5
    output_m = ao_4
    output_n = ao_3
    output_o = ao_2
    output_p = ao_1
    output_q = ao_16a
    return output_a, output_b, output_c, output_d, output_e, output_f, output_g, output_h, output_i, output_j, output_k, output_l, output_m, output_n, output_o, output_p, output_q

def elg_alu4(input_aa, input_ab, input_ac, input_ad, input_ba, input_bb, input_bc, input_bd, input_cc):
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

def elg_alu16(input_aa, input_ab, input_ac, input_ad, input_ae, input_af, input_ag, input_ah, input_ai, input_aj, input_ak, input_al, input_am, input_an, input_ao, input_ap, input_ba, input_bb, input_bc, input_bd, input_be, input_bf, input_bg, input_bh, input_bi, input_bj, input_bk, input_bl, input_bm, input_bn, input_bo, input_bp, input_ca):
    input_ba = lg_xor(input_ba, input_ca)
    input_bb = lg_xor(input_bb, input_ca)
    input_bc = lg_xor(input_bc, input_ca)
    input_bd = lg_xor(input_bd, input_ca)
    input_be = lg_xor(input_be, input_ca)
    input_bf = lg_xor(input_bf, input_ca)
    input_bg = lg_xor(input_bg, input_ca)
    input_bh = lg_xor(input_bh, input_ca)
    input_bi = lg_xor(input_bi, input_ca)
    input_bj = lg_xor(input_bj, input_ca)
    input_bk = lg_xor(input_bk, input_ca)
    input_bl = lg_xor(input_bl, input_ca)
    input_bm = lg_xor(input_bm, input_ca)
    input_bn = lg_xor(input_bn, input_ca)
    input_bo = lg_xor(input_bo, input_ca)
    input_bp = lg_xor(input_bp, input_ca)
    output_a, output_b, output_c, output_d, output_e, output_f, output_g, output_h, output_i, output_j, output_k, output_l, output_m, output_n, output_o, output_p, output_q = elg_16adder(
        input_aa, input_ab, input_ac, input_ad, input_ae, input_af, input_ag, input_ah, input_ai, input_aj, input_ak, input_al, input_am, input_an, input_ao, input_ap, input_ca
    )
    output_r = output_a
    output_s = lg_and(lg_and(lg_and(lg_and(lg_and(lg_and(lg_and(lg_and(lg_and(lg_and(lg_and(lg_and(lg_and(lg_and(lg_and(lg_not(output_a), lg_not(output_b)), lg_not(output_c)), lg_not(output_d)), lg_not(output_e)), lg_not(output_f)), lg_not(output_g)), lg_not(output_h)), lg_not(output_i)), lg_not(output_j)), lg_not(output_k)), lg_not(output_l)), lg_not(output_m)), lg_not(output_n)), lg_not(output_o)), lg_not(output_p))
    return output_a, output_b, output_c, output_d, output_e, output_f, output_g, output_h, output_i, output_j, output_k, output_l, output_m, output_n, output_o, output_p, output_q, output_r, output_s

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

def elg_16bit_register(elg_data_1, elg_data_2, elg_data_3, elg_data_4, elg_data_5, elg_data_6, elg_data_7, elg_data_8, elg_data_9, elg_data_10, elg_data_11, elg_data_12, elg_data_13, elg_data_14, elg_data_15, elg_data_16, elg_store, elg_clock):
    output_a = elg_1bit_register(elg_data_1, elg_store, elg_clock)
    output_b = elg_1bit_register(elg_data_2, elg_store, elg_clock)
    output_c = elg_1bit_register(elg_data_3, elg_store, elg_clock)
    output_d = elg_1bit_register(elg_data_4, elg_store, elg_clock)
    output_e = elg_1bit_register(elg_data_5, elg_store, elg_clock)
    output_f = elg_1bit_register(elg_data_6, elg_store, elg_clock)
    output_g = elg_1bit_register(elg_data_7, elg_store, elg_clock)
    output_h = elg_1bit_register(elg_data_8, elg_store, elg_clock)
    output_i = elg_1bit_register(elg_data_9, elg_store, elg_clock)
    output_j = elg_1bit_register(elg_data_10, elg_store, elg_clock)
    output_k = elg_1bit_register(elg_data_11, elg_store, elg_clock)
    output_l = elg_1bit_register(elg_data_12, elg_store, elg_clock)
    output_m = elg_1bit_register(elg_data_13, elg_store, elg_clock)
    output_n = elg_1bit_register(elg_data_14, elg_store, elg_clock)
    output_o = elg_1bit_register(elg_data_15, elg_store, elg_clock)
    output_p = elg_1bit_register(elg_data_16, elg_store, elg_clock)
    return output_a, output_b, output_c, output_d, output_e, output_f, output_g, output_h, output_i, output_j, output_k, output_l, output_m, output_n, output_o, output_p
