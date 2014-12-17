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

if __name__ == "__main__":
    print u_divide_32(u_bin_se_32(32),u_bin_se_32(9))
    print s_multiply_32(s_bin_se_32(-31),s_bin_se_32(-10))
    print s_multiply_32(s_bin_se_32(31),s_bin_se_32(-10))
    print s_multiply_32(s_bin_se_32(31),s_bin_se_32(-10))

