# IPPcode24_parser - user info
This repository contains a Python script that parses and validates a program written in IPPcode24, transforming it into an XML representation.

## Script usage:
Run the script with an input file
```bash
  python3 parse.py < input_file
```
use `--stats=file` flag to enable statistics output or `--help` flag for usage information

## Exit Codes:
0: Success<br>
10: Invalid arguments or unsupported options.<br>
21: Missing or malformed `.IPPcode24` header.<br>
22: Unsupported instructions after a valid header.<br>
23: Invalid argument format, duplicate headers, or empty input.<br>
12: Duplicate statistics output file usage.<br>

## Example input
```bash 
  .IPPcode24
  MOVE GF@var1 int@10
  WRITE GF@var1
```

## Example output
```bash
  <program language="IPPcode24">
    <instruction order="1" opcode="MOVE">
      <arg1 type="var">GF@var1</arg1>
      <arg2 type="int">10</arg2>
    </instruction>
    <instruction order="2" opcode="WRITE">
      <arg1 type="var">GF@var1</arg1>
    </instruction>
  </program>
```
