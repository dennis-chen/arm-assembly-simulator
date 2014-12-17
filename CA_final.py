def add_32(a,b,carry_in='0b0'):
    """takes two 32-digit binary strings and returns their sum in the same format, along with overflow and carryout."""
    assert len(a) == 34, len(b) == 34
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
    assert len(a) == 66, len(b) == 66
    res = None
    msb_carry_out = bin(0)
    print type(int(a,2)+int(b,2)+int(carry_in,2))
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
    assert len(a) == 34, len(b) == 34
    b_inv = invert(b)
    return add_32(a,b_inv,carry_in='0b1')

def subtract_64(a,b):
    """returns a - b, carry out, and overflow. expects two 32-digit binary strings."""
    assert len(a) == 66, len(b) == 66
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
        res,msb_carry_out,over_flow = add_64(inv,bin_se_pos_64(1))
        return res
    else:
        return bin_se_pos_64(0)

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

def s_multiply_ls_32(a,b):
    """multiplies two signed 32 bit strings and returns the least significant 32 bits of the result"""
    assert isinstance(a,str) and isinstance(b,str)
    assert len(a) == 34 and len(b) == 34
    a_int = s_bin_to_int_32(a)
    b_int = s_bin_to_int_32(b)
    res_int = a_int*b_int
    return s_bin_se_64(res_int)[-32:]

def u_multiply_32(a,b):
    """multiplies two unsigned 32 bit strings and returns a 64 bit string"""
    assert isinstance(a,str) and isinstance(b,str)
    assert len(a) == 34 and len(b) == 34
    a_int = int(a,2)
    b_int = int(b,2)
    res_int = a_int*b_int
    return u_bin_se_64(res_int)

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
    return '0b'+a[2+shift_val:]+'0'*shift_val

def r_shift_32_log(a,shift_val):
    """returns 32 bit string shifted right by int shift_val"""
    assert isinstance(a,str) and isinstance(shift_val,int)
    assert len(a) == 34
    return '0b'+'0'*shift_val+a[3:-shift_val]

def r_shift_32_ari(a,shift_val):
    """returns 32 bit string shifted right by int shift_val"""
    assert isinstance(a,str) and isinstance(shift_val,int)
    assert len(a) == 34
    if a[2] == '0':
        return '0b'+'0'*shift_val+a[3:-shift_val]
    else:
        return '0b'+'1'*shift_val+a[3:-shift_val]

def clz_32(a):
    """counts leading zeros of a 32 bit binary str, returns unsigned 32 bit str"""
    #THIS MIGHT BE WRONG! DONT KNOW IF WE SHOULD BE LOOKING AT SIGNED BIT
    raw_str = a[2:]
    counter = 0
    index = 0
    str_len = len(raw_str)
    while index != str_len and raw_str[index] != '1':
        counter += 1
        index += 1
    return s_bin_se_32(counter)

def abs_32(a):
    """returns positive twos complement representation of binary str"""
    if a[2] == '1':
        return s_multiply_32(a,s_bin_32(-1))
    else:
        return a

def s_divide_iq31(dd,dr):
    """divides two iq31 binary strings and returns an iq31 binary str"""
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
    r[4] = s_bin_se_32(min(int(clz_32(r[0]),2),8)) #r4 = min(clz(r0),8))
    r[2] = l_shift_32(r[0],int(r[4],2))
    r[12],c,o = subtract_32(s_bin_se_32(8),r[4])
    r[0] = u_divide_32(r[2],r[1])
    r[3] = clz_32(r[0])
    if s_bin_to_int_32(r[12]) >= s_bin_to_int_32(r[3]):
        return s_bin_se_32(-2147483648)
        #in the original, the stack is popped to the pc counter to branch
    r[2],c,o = subtract_32(r[2],s_multiply_ls_32(r[0],r[1]))
    #in the line above, remainder = dd-quotient*dr
    r[4] = clz_32(r[2])
    if s_bin_to_int_32(r[4]) >= s_bin_to_int_32(r[12]):
        r = div_finished_32(r) #pass register values
    else:
        r = div_more_32(r) #pass register values
    print r[0]
    return s_bin_to_int_32(r[0])

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
        r[0] = s_multiply_32(r[0],s_bin_se_32(-1))
    return r


if __name__ == "__main__":
    zero = '0b'+'0'*32
    dd = '0b001'+'0'*29
    dr = '0b010'+'0'*29
    #res = s_divide_iq31(dd,dr)
    res = s_divide_iq31(dd,zero)
    print res
    res = s_divide_iq31(zero,dr)
    print res

