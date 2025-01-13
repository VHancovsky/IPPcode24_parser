# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IPP project 1
# Author: Viktor Hančovský, xhanco00
# Date: 12. 3. 2024
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import sys
import re
from collections import Counter

# Initialize global variables
header = False
stats_b = False
order = 0
cmnt_cnt = 0
inst_cnt = 0
label_cnt = 0
jump_cnt = 0
fwjump_cnt = 0
badjump_cnt = 0
file_name = []
lbls_list = []
jmp_lbl_list = []
inst_list = []

# Function to find the most frequent instruction in input file
def most_frequent(List):
    counts = Counter(List)
    max_count = max(counts.values())
    most_freq = []
    for key, value in counts.items():
        if value == max_count:
            most_freq.append(key)
    most_freq.sort()
    most_freq_str = ','.join(most_freq)
    return most_freq_str

# Function to check if the argument is a variable
def is_var(arg, arg_c):
    var_rgx = r"^(LF|GF|TF)@[a-zA-Z_\-$&%*!?][a-zA-Z_\-$&%*!?0-9]*$"
    if re.match(var_rgx, arg):
        arg_arr = arg.split("@", 1)
        arg_val = arg_arr[1].replace("&", "&amp;")
        print(f"\t\t<arg{arg_c} type=\"var\">{arg_arr[0]}@{arg_val}</arg{arg_c}>")
    else:
        sys.exit(23)

# Function to check if the argument is a symbol
def is_sym(arg, arg_c):
    var_rgx = r"^(LF|GF|TF)@[a-zA-Z_\-$&%*!?][a-zA-Z_\-$&%*!?0-9]*$"
    nil_rgx = r"^nil@nil$"
    int_rgx = r"^int@(-|\+)?(0x[0-9A-Fa-f]{1,16}|\d+|0o[0-7]{1,7})$"
    bool_rgx = r"^bool@(true|false)$"
    string_rgx = r"^string@((?:\\[0-9][0-9][0-9])|(?:\\\\)|(?:[^\\\\\s#]))*$"
    
    if re.match(var_rgx, arg):
        print(f"\t\t<arg{arg_c} type=\"var\">{arg}</arg{arg_c}>")
    elif re.match(nil_rgx, arg) or re.match(int_rgx, arg) or re.match(bool_rgx, arg):
        arg_arr = arg.split("@", 1)
        print(f"\t\t<arg{arg_c} type=\"{arg_arr[0]}\">{arg_arr[1]}</arg{arg_c}>")
    elif re.match(string_rgx, arg):
        arg_val = arg.split("@", 1)[1]
        arg_val = arg_val.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        print(f"\t\t<arg{arg_c} type=\"string\">{arg_val}</arg{arg_c}>")
    else:
        sys.exit(23)

# Function to check if the argument is a label
def is_label(arg, arg_c):
    if re.match(r"^[a-zA-Z_\-$&%*!?][\w\-$&%*!?]*$", arg):
        arg = arg.replace("&", "&amp;")
        print(f"\t\t<arg{arg_c} type=\"label\">{arg}</arg{arg_c}>")
    else:
        sys.exit(23)

# Function to check if the argument is a type
def is_type(arg, arg_c):
    if arg in ["bool", "int", "string"]:
        print(f"\t\t<arg{arg_c} type=\"type\">{arg}</arg{arg_c}>")
    else:
        sys.exit(23)

# Function to parse instructions and generate XML output
def parse_instruction(line):
    global order
    global inst_cnt
    global label_cnt
    global jump_cnt
    global fwjump_cnt

    # Separates instruction from it's arguments in each line, takes the first as an opcode
    sep_inst = line.split()
    opcode = sep_inst[0].upper()
    inst_list.append(sep_inst[0])
    
    if opcode in ["CREATEFRAME", "PUSHFRAME", "POPFRAME", "RETURN", "BREAK"]:       # ---
        if len(sep_inst) == 1:
            order += 1
            inst_cnt += 1
            if opcode == "RETURN":
                jump_cnt += 1
            print(f"\t<instruction order=\"{order}\" opcode=\"{opcode}\"/>")
        else:
            sys.exit(23)
    elif opcode in ["DEFVAR", "POPS"]:                                              # <var>
        if len(sep_inst) == 2:
            order += 1
            inst_cnt += 1
            print(f"\t<instruction order=\"{order}\" opcode=\"{opcode}\">")
            is_var(sep_inst[1], 1)
            print("\t</instruction>")
        else:
            sys.exit(23)
    elif opcode in ["PUSHS", "WRITE", "DPRINT", "EXIT"]:                            # <sym>
        if len(sep_inst) == 2:
            order += 1
            inst_cnt += 1
            print(f"\t<instruction order=\"{order}\" opcode=\"{opcode}\">")
            is_sym(sep_inst[1], 1)
            print("\t</instruction>")
        else:
            sys.exit(23)
    elif opcode in ["CALL", "LABEL", "JUMP"]:                                       # <label>
        if len(sep_inst) == 2:
            order += 1
            inst_cnt += 1
            if opcode == "LABEL":
                label_cnt += 1
                lbls_list.append(sep_inst[1])
            if opcode == "JUMP":
                jump_cnt += 1
                jmp_lbl_list.append(sep_inst[1])
                if sep_inst[1] not in lbls_list:
                    fwjump_cnt += 1
            print(f"\t<instruction order=\"{order}\" opcode=\"{opcode}\">")
            is_label(sep_inst[1], 1)
            print("\t</instruction>")
        else:
            sys.exit(23)
    elif opcode in ["MOVE", "INT2CHAR", "STRLEN", "NOT", "TYPE"]:                   # <var> <sym>
        if len(sep_inst) == 3:
            order += 1
            inst_cnt += 1
            print(f"\t<instruction order=\"{order}\" opcode=\"{opcode}\">")
            is_var(sep_inst[1], 1)
            is_sym(sep_inst[2], 2)
            print("\t</instruction>")
        else:
            sys.exit(23)
    elif opcode in ["READ"]:                                                        # <var> <type>
        if len(sep_inst) == 3:
            order += 1
            inst_cnt += 1
            print(f"\t<instruction order=\"{order}\" opcode=\"{opcode}\">")
            is_var(sep_inst[1], 1)
            is_type(sep_inst[2], 2)
            print("\t</instruction>")
        else:
            sys.exit(23)
    elif opcode in ["ADD", "SUB", "MUL", "IDIV", "LT", "GT", "EQ", "AND",
                     "OR", "STRI2INT", "CONCAT", "GETCHAR", "SETCHAR"]:             # <var> <sym> <sym>
        if len(sep_inst) == 4:
            order += 1
            inst_cnt += 1
            print(f"\t<instruction order=\"{order}\" opcode=\"{opcode}\">")
            is_var(sep_inst[1], 1)
            is_sym(sep_inst[2], 2)
            is_sym(sep_inst[3], 3)
            print("\t</instruction>")
        else:
            sys.exit(23)
    elif opcode in ["JUMPIFEQ", "JUMPIFNEQ"]:                                       # <label> <sym> <sym>
        if len(sep_inst) == 4:
            order += 1
            inst_cnt += 1
            jump_cnt += 1
            jmp_lbl_list.append(sep_inst[1])
            if sep_inst[1] not in lbls_list:
                fwjump_cnt += 1
            print(f"\t<instruction order=\"{order}\" opcode=\"{opcode}\">")
            is_label(sep_inst[1], 1)
            is_sym(sep_inst[2], 2)
            is_sym(sep_inst[3], 3)
            print("\t</instruction>")
        else:
            sys.exit(23)
    else:
        if header == True:
            sys.exit(22)

# Check if any command-line arguments are provided
if len(sys.argv) == 2 and sys.argv[1] == "--help":
    print("\033[2mParameter --help was called. To run the program, type: \033[0m\033[1m\"python parse.py < input_file\"\033[0m.")
    sys.exit(0)

# Read input from stdin line by line
for line in sys.stdin:
    line = line.strip()
    if '#' in line:
        cmnt_cnt += 1
    # Check for comments and empty lines
    if line.startswith('#') or not line:
        continue
    line = line.split('#', 1)[0].strip()
    # Prints XML header if correct header in the input file is found and the header
    if (line =='.IPPcode24') and not header:
        header = True
        print("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
        print("<program language=\"IPPcode24\">")
        continue
    # Check for file without header
    elif not (line =='.IPPcode24') and not header:
        sys.exit(21)
    # Check for double header
    elif (line =='.IPPcode24') and header:
        sys.exit(23)
    parse_instruction(line)

# Extension STATP
for i in range(1,len(sys.argv)):
    # Check for "--stats=" argument
    if stats_b:
        # Check for each statistics argument
        if sys.argv[i] == "--loc":
            file.write(str(inst_cnt) + "\n")
        elif sys.argv[i] == "--comments":
            file.write(str(cmnt_cnt) + "\n")
        elif sys.argv[i] == "--labels":
            file.write(str(label_cnt) + "\n")
        elif sys.argv[i] == "--jumps":
            file.write(str(jump_cnt) + "\n")
        elif sys.argv[i] == "--fwjumps":
            file.write(str(fwjump_cnt) + "\n")
        elif sys.argv[i] == "--backjumps":
            file.write(str(jump_cnt - fwjump_cnt) + "\n")
        elif sys.argv[i] == "--badjumps":
            for j in jmp_lbl_list:
                if j not in lbls_list:
                    badjump_cnt += 1
            file.write(str(badjump_cnt) + "\n")
        elif sys.argv[i] == "--frequent":
            freq_inst = most_frequent(inst_list)
            file.write(str(freq_inst) + "\n")
        elif sys.argv[i].startswith("--print="):
            print_arg, print_val = sys.argv[i].split("=")
            file.write(str(print_val) + "\n")
        elif sys.argv[i] == "--eol":
            file.write("\n")
        # Check if the following file is different from the ones already used
        elif sys.argv[i].startswith("--stats="):
            stats_arg, stats_file = sys.argv[i].split("=")
            if stats_file not in file_name:
                file = open(stats_file, "w")
            else:
                sys.exit(12)
        else:
            sys.exit(10)
    # Check for first "--stats=" argument
    else:
        if sys.argv[i].startswith("--stats="):
            stats_b = True
            stats_arg, stats_file = sys.argv[i].split("=")
            file = open(stats_file, "w")
            file_name.append(stats_file)
        else:
            sys.exit(10)

# Check for empty input file
if not header:
    sys.exit(21)

print("</program>")
sys.exit(0)
