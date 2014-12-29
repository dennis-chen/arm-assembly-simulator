import random

def add_32(a,b,carry_in='0b0'):
    """takes two 32-digit binary strings and returns their sum in the same format, along with overflow and carryout."""
    assert len(a) == 34 and len(b) == 34
    res = None
    msb_carry_out = bin(0)
    temp_sum = bin(int(a,2)+int(b,2)+int(carry_in,2))
    if len(temp_sum) < 34:
        res = s_bin_se_32(int(a,2)+int(b,2)+int(carry_in,2))
    else:
        res = '0b'+temp_sum[-32:]
    if len(temp_sum) > len(a):
        msb_carry_out = bin(1)
    over_flow = detect_overflow(a[3:],b[3:],carry_in,msb_carry_out)
    return res,msb_carry_out,over_flow

def add_64(a,b,carry_in='0b0'):
    """takes two 64-digit binary strings and returns their sum in the same format, along with overflow and carryout."""
    assert len(a) == 66 and len(b) == 66
    res = None
    msb_carry_out = bin(0)
    temp_sum = bin(int(a,2)+int(b,2)+int(carry_in,2))
    if len(temp_sum) < 66:
        res = s_bin_se_64(int(a,2)+int(b,2)+int(carry_in,2))
    else:
        res = '0b'+temp_sum[-64:]
    if len(temp_sum) > len(a):
        msb_carry_out = bin(1)
    over_flow = detect_overflow(a[3:],b[3:],carry_in,msb_carry_out)
    return res,msb_carry_out,over_flow

def detect_overflow(a,b,carry_in,msb_carry_out):
    """returns 1 digit binary string representing XOR of the carryin+carryout of the MSB. is passed the carryout of the MSB."""
    msb_carry_in = bin(0)
    temp_sum = bin(int(a,2)+int(b,2)+int(carry_in,2))
    if len(temp_sum) > len(a):
        msb_carry_in = bin(1)
    return bin(int(msb_carry_in,2)^int(msb_carry_out,2))

def invert(bin_str):
    """inverts binary string of any length. expects it in the format of '0b...'. This particularly nifty list comprehension found on http://stackoverflow.com/questions/3920494/python-flipping-binary-1s-and-0s-in-a-string"""
    assert isinstance(bin_str,str)
    raw_num = bin_str[2:]
    return '0b'+''.join('1' if x == '0' else '0' for x in raw_num)

def subtract_32(a,b):
    """returns a - b, carry out, and overflow. expects two 32-digit binary strings."""
    assert len(a) == 34 and len(b) == 34
    b_inv = invert(b)
    return add_32(a,b_inv,carry_in='0b1')

def subtract_64(a,b):
    """returns a - b, carry out, and overflow. expects two 32-digit binary strings."""
    assert len(a) == 66 and len(b) == 66
    b_inv = invert(b)
    return add_64(a,b_inv,carry_in='0b1')

def str_se_64(bin_str):
    """sign extends binary strings to 64 bit binary strings"""
    assert isinstance(bin_str,str)
    raw_bin = bin(bin_str)[2:]
    orig_len = len(raw_bin)
    if raw_bin[0] == 0:
        return '0b'+'0'*(64-orig_len)+raw_bin
    else:
        return '0b'+'1'*(64-orig_len)+raw_bin

def u_bin_se_32(num):
    """converts an int to a binary number and sign extends it with zeros to be 32 bits. Does not accept negative numbers."""
    assert isinstance(num,int)
    assert num >= 0
    raw_bin = bin(num)[2:]
    orig_len = len(raw_bin)
    return '0b'+'0'*(32-orig_len)+raw_bin

def u_bin_se_64(num):
    """converts an int to a binary number and sign extends it with zeros to be 64 bits. Does not accept negative numbers."""
    assert isinstance(num,int) or isinstance(num,long)
    assert num >= 0
    raw_bin = bin(num)[2:]
    orig_len = len(raw_bin)
    return '0b'+'0'*(64-orig_len)+raw_bin

def s_bin_se_32(num):
    """converts an int to a 32 bit binary number. Automatically converts negative ints to twos complement representation."""
    assert isinstance(num,int)
    if num > 0:
        return u_bin_se_32(num)
    elif num < 0:
        raw_bin = bin(num)[3:]
        orig_len = len(raw_bin)
        pos_rep = '0b'+'0'*(32-orig_len)+raw_bin
        inv = invert(pos_rep)
        res,msb_carry_out,over_flow = add_32(inv,'0b00000000000000000000000000000001')
        return res
    else:
        return '0b00000000000000000000000000000000'

def s_bin_se_64(num):
    """converts an int to a 64 bit binary number. Automatically converts negative ints to twos complement representation."""
    assert isinstance(num,int)
    if num > 0:
        return u_bin_se_64(num)
    elif num < 0:
        raw_bin = bin(num)[3:]
        orig_len = len(raw_bin)
        pos_rep = '0b'+'0'*(64-orig_len)+raw_bin
        inv = invert(pos_rep)
        res,msb_carry_out,over_flow = add_64(inv,'0b'+'0'*63+'1')
        return res
    else:
        return '0b'+'0'*64

def s_bin_to_int_32(bin_str):
    """converts 32 bit binary strings in twos complement representation into an integer"""
    assert isinstance(bin_str,str)
    assert len(bin_str) == 34
    raw_bin_str = bin_str[2:]
    if raw_bin_str[0] == '0':
        return int(bin_str,2)
    else:
        inv = invert(bin_str)
        pos_rep = add_32(inv,s_bin_se_32(1))[0]
        return -1*int(pos_rep,2)

def s_multiply_32(a,b):
    """multiplies two signed 32 bit strings and returns a 64 bit string"""
    assert isinstance(a,str) and isinstance(b,str)
    assert len(a) == 34 and len(b) == 34
    a_int = s_bin_to_int_32(a)
    b_int = s_bin_to_int_32(b)
    res_int = a_int*b_int
    return s_bin_se_64(res_int)

def s_multiply_32_2(a,b):
    """multiplies two signed 32 bit strings and returns two 32 bit bit strings"""
    assert isinstance(a,str) and isinstance(b,str)
    assert len(a) == 34 and len(b) == 34
    a_int = s_bin_to_int_32(a)
    b_int = s_bin_to_int_32(b)
    res_int = a_int*b_int
    res_64 = s_bin_se_64(res_int)
    return res_64[:34],'0b'+res_64[34:]

def s_multiply_ls_32(a,b):
    """multiplies two signed 32 bit strings and returns the least significant 32 bits of the result"""
    assert isinstance(a,str) and isinstance(b,str)
    assert len(a) == 34 and len(b) == 34
    a_int = s_bin_to_int_32(a)
    b_int = s_bin_to_int_32(b)
    res_int = a_int*b_int
    return '0b'+s_bin_se_64(res_int)[-32:]

def u_multiply_32(a,b):
    """multiplies two unsigned 32 bit strings and returns a 64 bit string"""
    assert isinstance(a,str) and isinstance(b,str)
    assert len(a) == 34 and len(b) == 34
    a_int = int(a,2)
    b_int = int(b,2)
    res_int = a_int*b_int
    return u_bin_se_64(res_int)

def u_multiply_32_2(a,b):
    """multiplies two unsigned 32 bit strings and two 32 bit bit strings"""
    assert isinstance(a,str) and isinstance(b,str)
    assert len(a) == 34 and len(b) == 34
    a_int = int(a,2)
    b_int = int(b,2)
    res_int = a_int*b_int
    res_64 = u_bin_se_64(res_int)
    return res_64[:34],'0b'+res_64[34:]

def s_divide_32(a,b):
    """returns a/b, signed integer division."""
    assert isinstance(a,str) and isinstance(b,str)
    assert len(a) == 34 and len(b) == 34
    a_int = s_bin_to_int_32(a)
    b_int = s_bin_to_int_32(b)
    res_int = a_int/b_int
    return s_bin_se_32(res_int)

def u_divide_32(a,b):
    """returns a/b, unsigned integer division."""
    assert isinstance(a,str) and isinstance(b,str)
    assert len(a) == 34 and len(b) == 34
    a_int = int(a,2)
    b_int = int(b,2)
    res_int = a_int/b_int
    return u_bin_se_32(res_int)

def l_shift_32(a,shift_val):
    """returns 32 bit string shifted left by int shift_val"""
    assert isinstance(a,str) and isinstance(shift_val,int)
    assert len(a) == 34
    assert shift_val <= 32
    assert len('0b'+a[2+shift_val:]+'0'*shift_val) == 34
    return '0b'+a[2+shift_val:]+'0'*shift_val

def r_shift_32_log(a,shift_val):
    """returns 32 bit string shifted right by int shift_val"""
    assert isinstance(a,str) and isinstance(shift_val,int)
    assert len(a) == 34
    assert shift_val <= 32
    return '0b'+'0'*shift_val+a[2:-shift_val]
    assert len('0b'+'0'*shift_val+a[2:-shift_val]) == 34

def r_shift_32_ari(a,shift_val):
    """returns 32 bit string shifted right by int shift_val"""
    assert isinstance(a,str) and isinstance(shift_val,int)
    assert len(a) == 34
    assert shift_val <= 32
    if a[2] == '0':
        assert len('0b'+'0'*shift_val+a[2:-shift_val]) == 34
        return '0b'+'0'*shift_val+a[2:-shift_val]
    else:
        assert len('0b'+'1'*shift_val+a[2:-shift_val]) == 34
        return '0b'+'1'*shift_val+a[2:-shift_val]

def clz_32(a):
    """counts leading zeros of a 32 bit binary str, returns unsigned 32 bit str. Ignores the signed MSB"""
    raw_str = a[2:]
    counter = 0
    index = 1
    str_len = len(raw_str)
    while index != str_len and raw_str[index] != '1':
        counter += 1
        index += 1
    return s_bin_se_32(counter)

def abs_32(a):
    """returns positive twos complement representation of binary str"""
    assert len(a) == 34
    if a[2] == '1':
        return s_multiply_ls_32(a,s_bin_32(-1))
    else:
        return a

def s_divide_iq30(dd,dr):
    """divides two iq30 binary strings and returns an iq30 binary str"""
    assert len(dd) == 34 and len(dr) == 34
    r = [None]*32 #register list
    r[0] = dd
    r[1] = dr
    if int(dr,2) == 0:
        #if divisor == 0 return largest possible positive number
        return s_bin_se_32(2147483647)
    #in original program, value of link register and r[4] are pushed to the stack here
    r[31] = s_bin_se_32(1) #link register is set to 1
    if (dd[2] != dr[2]): #dd[2] is the MSB of the bit string so this statement checks for sign equality
        r[31] = s_bin_se_32(0)
    r[0] = abs_32(r[0])
    r[1] = abs_32(r[1])
    r[4] = s_bin_se_32(min(int(clz_32(r[0]),2),30)) #r4 = min(clz(r0),30))
    r[2] = l_shift_32(r[0],int(r[4],2))
    r[12],c,o = subtract_32(s_bin_se_32(30),r[4])
    r[0] = u_divide_32(r[2],r[1])
    r[3] = clz_32(r[0])
    if s_bin_to_int_32(r[12]) >= s_bin_to_int_32(r[3]):
        r[0],c,o = subtract_32(s_bin_se_32(-2147483648),r[31])
        return r[0]
        #in the original, the stack is popped to the pc counter to branch
    r[2],c,o = subtract_32(r[2],s_multiply_ls_32(r[0],r[1]))
    #in the line above, remainder = dd-quotient*dr
    r[4] = clz_32(r[2])
    if s_bin_to_int_32(r[4]) >= s_bin_to_int_32(r[12]):
        r = div_finished_32(r) #pass register values
    else:
        r = div_more_32(r) #pass register values
    return r[0]

def div_more_32(r):
    r[12],c,o = subtract_32(r[12],r[4])
    assert s_bin_to_int_32(r[4]) >= 0
    r[2] = l_shift_32(r[2],s_bin_to_int_32(r[4]))
    r[0] = l_shift_32(r[0],s_bin_to_int_32(r[4]))
    r[3] = u_divide_32(r[2],r[1])
    r[2],c,o = subtract_32(r[2],s_multiply_ls_32(r[1],r[3]))
    r[0],c,o = add_32(r[0],r[3])
    r[4] = clz_32(r[2])
    if s_bin_to_int_32(r[4]) <= s_bin_to_int_32(r[12]):
        r = div_more_32(r)
    else:
        r = div_finished_32(r)
    return r

def div_finished_32(r):
    r[2] = l_shift_32(r[2],s_bin_to_int_32(r[12]))
    r[0] = l_shift_32(r[0],s_bin_to_int_32(r[12]))
    r[3] = u_divide_32(r[2],r[1])
    r[0],c,o = add_32(r[0],r[3])
    if s_bin_to_int_32(r[31]) == 0:
        r[0] = s_multiply_ls_32(r[0],s_bin_se_32(-1))
    return r

def iq30_to_float(a):
    """converts a iq30 number to a float"""
    assert isinstance(a,str)
    assert len(a) == 34
    sign_bit = a[2]
    raw_num = a[4:]
    float_res = 0
    if sign_bit == '0':
        for i, bit in enumerate(raw_num):
            float_res += 2**-(i+1)*int(bit,2)
    else:
        for i, bit in enumerate(raw_num):
            float_res -= 2**-(i+1)*int(bit,2)
    return float_res

def float_to_iq30(a):
    """converts a float to an iq30 number"""
    abs_a = abs(a)
    assert abs_a <= 1
    if a >= 0:
        iq30 = '0b'+'0'+31*'0'
    else:
        iq30 = '0b'+'1'+31*'0'
    iq30_l = list(iq30)
    remainder = abs_a
    for i in range(30):
        if 2**-(i+1) <= remainder:
            iq30_l[i+4] = '1'
            exp = -(i+1)
            remainder -= 2**-(i+1)
    return ''.join(iq30_l)

def test_div_accuracy():
    """evaluates accuracy of ARM fixed point IQ30 division vs python's floating point division, which we'll take as perfectly accurate."""
    num_tests = 1000
    test_vals = []
    total_accuracy = 0
    for i in xrange(num_tests):
        a = random.uniform(0,1)
        b = random.uniform(0,1)
        if a < b:
            test_vals.append((a,b))
        else:
            test_vals.append((b,a))
    for test_val in test_vals:
        temp_res = s_divide_iq30(float_to_iq30(test_val[0]),float_to_iq30(test_val[1]))
        arm_res = iq30_to_float(temp_res)
        python_res = test_val[0]/test_val[1]
        pcnt_accuracy = abs((python_res - arm_res)/(python_res))
        total_accuracy += pcnt_accuracy
    total_accuracy = total_accuracy/num_tests
    print "fixed point division within " + str(100*total_accuracy) + "% of pythons' floating point division on average over "+str(num_tests)+" test runs!"

def test_float_to_iq30():
    res = s_divide_iq30(float_to_iq30(.25),float_to_iq30(.25))
    print iq30_to_float(res)
    res = s_divide_iq30(float_to_iq30(.25),float_to_iq30(0))
    print iq30_to_float(res)
    res = s_divide_iq30(float_to_iq30(0),float_to_iq30(.25))
    print iq30_to_float(res)
    res = s_divide_iq30(float_to_iq30(.2325),float_to_iq30(.91))
    print iq30_to_float(res)

def iq29_to_float(a):
    """converts a iq29 number to a float"""
    assert isinstance(a,str)
    assert len(a) == 34
    sign_bit = a[2]
    raw_num = a[5:]
    float_res = 0
    if sign_bit == '0':
        for i, bit in enumerate(raw_num):
            float_res += 2**-(i+1)*int(bit,2)
    else:
        for i, bit in enumerate(raw_num):
            float_res -= 2**-(i+1)*int(bit,2)
    return float_res

def float_to_iq29(a):
    """converts a float to an iq29 number"""
    abs_a = abs(a)
    assert abs_a <= 1
    if a >= 0:
        iq29 = '0b'+'0'+31*'0'
    else:
        iq29 = '0b'+'1'+31*'0'
    iq29_l = list(iq29)
    remainder = abs_a
    for i in range(29):
        if 2**-(i+1) <= remainder:
            iq29_l[i+5] = '1'
            exp = -(i+1)
            remainder -= 2**-(i+1)
    return ''.join(iq29_l)

def and_32(a,b):
    """returns 32 bit and of two bit strings"""
    assert isinstance(a,str) and isinstance(b,str)
    assert len(a) == 34 and len(b) == 34
    res = ''
    for a_char,b_char in zip(a[2:],b[2:]):
        if a_char == b_char and a_char == '1':
            res += '1'
        else:
            res += '0'
    assert len('0b'+res) == 34
    return '0b'+res

def rotate_r_ext(a,shift_in_val):
    """returns 32 bit string shifted right by one place. The value shifted in on the left is specified as an integer, 0 or 1."""
    assert isinstance(a,str) and isinstance(shift_in_val,int)
    assert len(a) == 34
    assert len('0b'+str(shift_in_val)+a[2:-1]) == 34
    return '0b'+str(shift_in_val)+a[2:-1]

def IQ29atan(a,b):
    """returns arctan(a/b) as an IQ29 binary str"""
    assert isinstance(a,str) and isinstance(b,str)
    assert len(a) == 34 and len(b) == 34
    r = [None]*32 #register list
    r[0] = a
    r[1] = b
    print r[0]
    print s_bin_se_32(-2147483648)
    r[12] = and_32(r[0],s_bin_se_32(-2147483648))
    print r[12]
    r[0] = abs_32(r[0])
    print r[0]
    r[2] = l_shift_32(r[1],1)
    if s_bin_to_int_32(r[1]) < 0:
        r[1] = abs_32(r[1])
        r[12] = rotate_r_ext(r[12],1)
    else:
        r[12] = r_shift_32_log(r[12],1)
    if s_bin_to_int_32(r[0]) == s_bin_to_int_32(r[1]):
        r = operands_are_equal_30(r)
    if s_bin_to_int_32(r[0]) > s_bin_to_int_32(r[1]):
        r[2] = r[0]
        r[0] = r[1] #swap r[0] and r[1]
        r[1] = r[2]
        #push r[4] and r[5] to the stack
    r[5] = clz_32(r[1])
    r[1] = l_shift_32(r[1],s_bin_to_int_32(r[5]))
    r[2] = r_shift_32_log(r[1],22)
    #r[3] = div_table_st
    r[3] = float_to_iq29(random.uniform(0,1))
    r[2] = float_to_iq29(random.uniform(0,1))
    #r[2] = div_table_st
    u_multiply_32_2(r[2],r[2])
    r[3],r[4] = u_multiply_32_2(r[2],r[2])
    r[3],r[4] = u_multiply_32_2(r[3],r[1])
    r[3] = subtract_32(r[2],r[3])[0]
    r[2] = l_shift_32(r[3],1)
    r[3],r[4] = u_multiply_32_2(r[2],r[2])
    r[3],r[4] = u_multiply_32_2(r[3],r[1])
    r[2] = subtract_32(r[2],r[3])[0]
    r[0],r[1] = u_multiply_32_2(r[0],r[2])
    r[5] = add_32(r[5],s_bin_se_32(2))[0]
    r[4] = subtract_32(s_bin_se_32(32),r[5])[0]
    r[1] = r_shift_32_log(r[1],s_bin_to_int_32(r[4]))
    r[0] = l_shift_32(r[0],s_bin_to_int_32(r[5]))
    r[0] = r[1] #BUT MIKES UNSURE WHAT THIS RLY IS
    r[2] = r_shift_32_log(r[0],24)
    r[2] = add_32(r[2],l_shift_32(r[2],1))[0]
    #r[3] = atan2putable
    r[3] = float_to_iq29(random.uniform(0,1))
    #r[3] = atan2putable
    r[3] = add_32(r[3],l_shift_32(r[2],2))[0]
    r[4] = r[3]#BUT MIKES UNSURE WHAT THIS RLY IS
    r[1],r[2] = u_multiply_32_2(r[0],r[4])
    r[4] = r[5]#BUT MIKES UNSURE WHAT THIS RLY IS
    r[4] = subtract_32(r[4],r[1])[0]
    r[1],r[2] = u_multiply_32_2(r[0],r[4])
    r[0] = add_32(r[1],r[5])[0]
    print r[0]
    r[0] = r_shift_32_log(r[0],2)
    r = equal_operands_reentry_point_30(r)
    return r[0]

def equal_operands_reentry_point_30(r):
    if s_bin_to_int_32(r[12]) < 0:
        r[0] = subtract_32('0b0010'+'0'*28,r[0])[0]
    r[12] = l_shift_32(r[12],1)
    if s_bin_to_int_32(r[12]) < 0:
        r[0] = subtract_32('0b0100'+'0'*28,r[0])[0]
    r[12] = l_shift_32(r[12],1)
    if s_bin_to_int_32(r[12]) < 0:
        r[0] = abs_32(r[0])
    r[1] = '0b01100100100001111110110101010001'
    r[0],r[1] = s_multiply_32_2(r[1],r[0])
    #not sure if final bit or the 19th bit sets the flag
    if r[0][-1] == '1':
        r[0] = r_shift_32_ari(r[0],19)
        r[0] = add_32(r[0],s_bin_se_32(1))
    else:
        r[0] = r_shift_32_ari(r[0],19)
    #ADC.W Does something???
    #pop r4,r5 off the stack
    return r

def operands_are_equal_30(r):
    if s_bin_to_int_32(r[0]) == 0:
        return r
    else:
        r[0] = s_bin_se_32(-2147483648)
        #push r4 and r5 to the stack
        equal_operands_reentry_point_30(r)
        return r

if __name__ == "__main__":
    #test_div_accuracy()
    #print float_to_iq30(.4)
    #print float_to_iq30(.7)
    #print subtract_32('0b00011001100110011001100110011001','0b00000000000000000000000000000000')
