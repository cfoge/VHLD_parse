import re

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def convert_vhdl_reg_to_comment(input_str, vhdl_obj):
    cpp_header = []
    lower = input_str.lower()
    lines = lower.split(';')
    for line in lines:
        if "regs" in line and "<=" in line:
            packed = []
            from_to = line.split("<=")
            if "&" in from_to[1]:
                packed_reg = from_to[1].split("&")
                for reg in packed_reg:
                    if '"' in reg or "'" in reg:
                        if "x" in reg:
                            zeros = find_between(reg, '"','"')
                            packed.append(int(len(zeros))*4)
                        else:
                            zeros = find_between(reg, '"','"')
                            packed.append(int(len(zeros)))
                    else:
                        if "(" in reg and ")" in reg:
                            reg = find_between(reg, "(", ")")
                        packed.append(reg.replace(";",""))
            else:
                if "(" in from_to[1] and ")" in from_to[1]:
                            from_to[1] = find_between(from_to[1], "(", ")")
                packed.append(from_to[1].strip())
            match = re.search(r'x"([^"]*)"', from_to[0])
            if match:
                regnum = match.group(1).strip()

                # -- 0x0000   RW    Switcher video_format(4:0)
                str_out = ''
                start_bit = 0
                for pack in reversed(packed): # go from end to begining
                    if isinstance(pack, int):
                         start_bit = start_bit + pack
                    else:
                        found_sig = False
                        for signal in vhdl_obj.signal:
                            if signal[0] == pack.strip():
                                found_sig = True
                                str_out =  f"{pack.strip()}({int(signal[2])-1+start_bit}:{start_bit})  " + str_out  # extract the width
                                cpp_shift = start_bit
                                start_bit = start_bit + signal[2] 
                                # cpp_header.append([f"#define {pack}     0x{regnum}", f"#define {pack}_shift     {start_bit}"])
                                print(f"#define {pack.strip()}     0x{regnum}")
                                print(f"#define {pack.strip()}_shift     {cpp_shift}")
                                
                        if found_sig == False: # if the assignment wasnt a signal check if it was a port
                            for signal in vhdl_obj.port:
                                if signal[0] == pack.strip():
                                    found_sig = True
                                    try:
                                        str_out =  f"{pack.strip()}({int(signal[3])-1+start_bit}:{start_bit})  " + str_out  # extract the width
                                        cpp_shift = start_bit
                                        start_bit = start_bit + signal[3] 
                                        # cpp_header.append([f"#define {pack}     0x{regnum}", f"#define {pack}_shift     {start_bit}"])
                                        print(f"#define {pack.strip()}     0x{regnum}")
                                        print(f"#define {pack.strip()}_shift     {cpp_shift}")
                                    except:
                                        print("decode_error")
                                    

                print(f"-- 0x{regnum}   R    {str_out}")
                



