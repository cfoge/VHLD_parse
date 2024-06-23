# VHDL_parse 🚀
A collection of Python tools to simplify your VHDL workflow without heavyweight IDEs like Vivado or Quartus. Great for automating boring tasks in VHDL!
---
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/donate/?hosted_button_id=LSMYWSM7M7EEA)
Open to donations and contributors with VHDL or Python experience. 😀 

> [!IMPORTANT]
> Designed to run in the command line, VHDL_parse lets you explore, navigate and manipulate VHDL files effortlessly. No additional libraries are required, just the magic of Python3.

## VHDL_parse is for Automating VHDL creation, creating top-level and constraint files from schematics, searching large projects, and visualising module hierarchy and signal flow.

## Tools 🕵️‍♂️
found in the "vhdl_tokeniser/tools" folder 
### Search:
Searches all VHDL files in a directory for VHDL FEATURES matching string. Eg. fconst.py searches for constants, ftype.py searches for types ect...
arg 1 = search string, arg 2 = -d directory

**Example farch.py:** 
```bash
python .\farch.py Behavioral -d test
```

Returns:
```
Searching for architecture with 'Behavioral' in directory: test...
test\my_entity.vhd  : line 14: architecture Behavioral of my_entity is
Info: 2 files checked.
```
**Example ftype.py:** 
```bash
python .\ftype.py MY_TYPE -d test
```

Returns:
```
Searching for type with 'MY_TYPE' in directory: test...
test\my_package.vhd  : line 10: type MY_TYPE is record    
Info: 2 files checked.
```
**Example pfind.py:** 
```bash
python .\pfind.py clk in -d test
```
Searches for 2 words on the same line, useful for doing things like finding all the VHDL modules with specific input names or libraries.

Returns:
```
test\my_entity.vhd  : line 7: clk : in  std_logic;
Info: 2 files checked.
```
---
#### Working Python Comand Line Scripts
- **instanc.py** = creates a template instantiation from a VHDL file in the terminal or as a .txt file
- **component.py** = creates a template component declaration from a VHDL file in the terminal or as a .txt file
- **wrapper.py** = create a wrapper that declares an entity, instantiates the VHDL files passed to it and optionally creates signals with matching port names connected to each instance.

##### Current features:
- Display VHDL module hierarchies from a directory
- Auto-generate entity and module instantiations
- Auto-generate VHDL wrappers for multiple entities
##### Future potential:
- Test bench creation automation
- Signal tracing/search through multiple files
- Diff two vhdl files by port,generics,contants ect.. rather than line by line like a regular diff would

### what_in.py 📜
List VHDL entities, constants, attributes, signals, and processes:

| Arg 1        | Arg 2           |
| ------------- |:-------------:| 
| vhdl file     | param (optional)|

The second (optional) is a parameter to filter the results:
"f" shows all
"a" shows attributes
"v" shows variables
"c" shows constants
"p" shows processes
"s" shows signals

Example: 
```bash
what_in.py input.vhd a
```


### make_xdc.py 🧩
Transform the ports on your top-level VHDL file into a constraints file in either Xilinx or Quartus format with make_xdc.py. Just two inputs needed:

| Arg 1        | Arg 2           | Arg 3 (optional)|
| ------------- |:-------------:| ------------- |
| XDC output file name    | Input Top level.vhd file| q (quartus mode)|

Example: 
```bash
check_xdc.py output input.vhd 
```
(optional 3rd argument "q" generates Quartus output)


#### I hope these scripts make your FPGA and VHDL work a bit smoother! I use them all the time and they have saved me countless hrs already. 🎉

