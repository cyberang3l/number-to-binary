# number-to-binary

Converts binary, decimal and hexadecimal numbers to all other bases
and shows the bit indices. Based on the size of the input number, 16,
32, 64 or 128 bits will be displayed in the output.

I find this script useful when working with registers or anything that
requires inspecting values at the bit level.

Sample usage:

`$ ./to-bin 100`   # Converts the decimal number `100` to hex/binary

`$ ./to-bin 0x100` # If the number starts with `0x` it will be parsed as hex. This will convert the hexadecimal `100` to decimal/binary

`$ ./to-bin 0b100` # If the number starts with `0b` it will be parsed as binary. This will convert the binary `100` to decimal/hexadecimal


Sample output:

    $ to-bin.py 3850
    base10: 3850
    base16: 0f0a
     base2: 0000111100001010
     ------------------------
     15
     |14
     ||13
     |||12
     |||| 11
     |||| |10
     |||| ||9
     |||| |||8
     |||| |||| 7
     |||| |||| |6
     |||| |||| ||5
     |||| |||| |||4
     |||| |||| |||| 3
     |||| |||| |||| |2
     |||| |||| |||| ||1
     |||| |||| |||| |||0

     0000 1111 0000 1010
        0    f    0    a
