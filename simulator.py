import re
import sys
import os

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

class simulator():
    """simulates an arm program given to it as a text file"""
    def __init__(self,txt):
        self.txt = txt
        self.prog = self.convert_txt(self.txt)
        #prog is a list of strings that will be executed, with the exception that it is an integer if we are meant to jump at that point in execution
        self.run_prog(self.prog)

    def convert_txt(self,txt_file):
        content = []
        with open(txt_file) as f:
            content = f.readlines()
        for i,c in enumerate(content):
            word_list = c.split()
            for j,word in enumerate(word_list):
                if word[-1] == ',':
                    word_list[j] = word[:-1]
                if word[-1] == '}':
                    word_list[j] = word[:-1]
                    if word[0] == '{':
                        word_list[j] = word[1:-1]
                if word[0] == '#':
                    word_list[j] = str(int(word[-1:],16))
            content[i] = word_list
        #print content
        for c in content:
            for i,j in enumerate(c):
                if i!=0:
                    c[i] = "'"+str(c[i])+"'"
        new_content = []
        for c in content:
            if c[0][:2] != 'IT':
                new_content.append(c)
        for i,c in enumerate(new_content):
            if len(c) > 1:
                new_c = c[0]+'('
                for j in xrange(len(c)-1):
                    new_c += c[j+1]
                    if j != len(c) - 2:
                        new_c += ','
                new_c += ')'
                new_content[i] = new_c
        for i,string in enumerate(new_content):
            if type(string) is str:
                new_content[i] = 'self.'+string.replace(".","")
        #print new_content
        return new_content
        #for i,string in enumerate(new_content):
        #    if type(string) is str:
        #        new_content[i] = re.sub("R([^,]+)",
        #print "text conversion finished! output to your_orig_to_python.txt"
        #outfile = self.txt[:-4] + "_to_python.txt"
        #f=open(outfile,'w+')
        #s1=''.join(str(new_content))
        #f.write(s1)
        #f.close()

    def MOVW(self,reg,num):
        """moves number to register"""
        if len(reg) == 1:
            self.regs[int(reg[1])] = u_bin_se_32(int(num))
        elif len(reg) == 2:
            self.regs[int(reg[1:2])] = u_bin_se_32(int(num))

    def ADD(self,string):
        """takes three arguments, writes B+C to A"""
        args = string.split(',')
        b = self.regs[int(args[1][1:])]
        c = self.regs[int(args[2][1:])]
        self.regs[int(args[0][1:])] = add_32(b,c)[0]

    def run_prog(self,prog):
        """takes a list of strings that python executes"""
        self.regs = [None]*32 #register list
        self.PC = 0
        prog_len = len(prog)
        while self.PC < prog_len:
            if isinstance(prog[self.PC],int):
                self.PC = prog[self.PC]
            else:
                print prog[self.PC]
                exec prog[self.PC]
                print self.regs
                self.PC+=1
        print "Simulation finished!"

if __name__ == "__main__":
    for arg in sys.argv:
        assert os.path.isfile(arg)
    s = simulator(sys.argv[1])
