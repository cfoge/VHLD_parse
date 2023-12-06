import re

def convert_vhdl_reg_to_comment(input_str, vhdl_obj):
    lines = input_str.split('\n')

    for line in lines:
        if "regs" in line and ";" in line and "<=" in line:
            packed = []
            from_to = line.split("<=")
            if "&" in from_to[1]:
                packed_reg = from_to[1].split("&")
                for reg in packed_reg:
                    if '"' not in reg and 'x"' not in reg:

                        packed.append(reg.replace(";",""))
            match = re.search(r'x"([^"]*)"', from_to[0])
            if match:
                regnum = match.group(1).strip()

                # -- 0x0000   RW    Switcher video_format(4:0)
                str_out = ''
                start_bit = 0
                for pack in reversed(packed): # go from end to begining
                    for signal in vhdl_obj.signal:
                        if signal[0] == pack.strip():
                            str_out =  f"{pack.strip()}({int(signal[2])+start_bit}:{start_bit}) " + str_out  # extract the width
                            start_bit = start_bit + signal[2]
                print(f"-- 0x{regnum}   R    {str_out}")



