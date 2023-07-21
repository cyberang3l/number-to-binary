#!/usr/bin/env python3
"""
Converts binary, decimal and hexadecimal numbers to all other bases
and shows the bit indices. Based on the size of the input number, 16,
32, 64 or 128 bits will be displayed in the output.

I find this script useful when working with registers or anything that
requires inspecting values at the bit level.

Sample usage:

$ ./to-bin 100   # Will convert the decimal number 100 to hex/binary

$ ./to-bin 0x100 # If the number starts with 0x it will be parsed as hex. This
                 # will convert the hexadecimal 0x100 to decimal/binary

$ ./to-bin 0b100 # If the number starts with 0b it will be parsed as binary. This
                 # will convert the binary 100 to decimal/hexadecimal


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
"""

import sys


class HexBinDecPrinter:
    def __init__(self, raw_value: str, print_split: int = 4, bits_to_show: int = 0):
        self._raw_val: str = raw_value
        self._split: int = print_split
        self._number: int = 0
        self._bits_to_show: int = bits_to_show  # 0 (auto-guess), 8, 16, 32, 64 or 128
        self._hex_str: str = ""
        self._bin_str: str = ""
        self._convert_raw_val_to_num()

    def _convert_raw_val_to_num(self):
        base: int = 10
        explicit: bool = False
        if self._raw_val.startswith("0b"):
            explicit = True
            base = 2
        elif self._raw_val.startswith("0x"):
            explicit = True
            base = 16

        if self._raw_val.startswith("-"):
            print(
                f"Only working with positive integers. {self._raw_val} provided")
            exit(1)

        try:
            self._number = int(self._raw_val, base)
        except ValueError:
            if explicit:
                expected_number_type = "binary" if base == 2 else "hexadecimal"
                print(
                    f"cannot parse '{self._raw_val}' with base {base}. Have you provided a valid {expected_number_type} number?")
                exit(1)
            try:
                # If the user hasn't explicitly provided a valid decimal number, or a
                # number with the prefix 0b (for binary) or 0x (for hex) try to parse
                # the number as hexadecimal. If this attempt fails too, print an
                # invalid number error.
                base = 16
                self._number = int(self._raw_val, base)
            except ValueError:
                print(
                    f"cannot parse '{self._raw_val}' neither as a base 10 integer, base 16 or base 2. Have you provided a valid number?")
                exit(1)

        if not self._bits_to_show:
            self._bits_to_show = 8
            if self._number & 0xFF != self._number:
                self._bits_to_show = 16
            if self._number & 0xFFFF != self._number:
                self._bits_to_show = 32
            if self._number & 0xFFFFFFFF != self._number:
                self._bits_to_show = 64
            if self._number & 0xFFFFFFFFFFFFFFFF != self._number:
                self._bits_to_show = 128

        hex_chars_to_show = int(self._bits_to_show / 4)

        self._hex_str = f"{self._number:0{hex_chars_to_show}x}"
        self._bin_str = bin(self._number)[2:].zfill(self._bits_to_show)
        if len(self._bin_str) > self._bits_to_show:
            raise BaseException(
                f"Only supporting up to {self._bits_to_show} bit conversions")

    def get_spaced_hex_string(self, string: str) -> str:
        hex_spaced: str = ""
        for i in range(0, self._bits_to_show):
            if i % 4 == 3:
                hex_spaced += string[int(i / 4)]
            else:
                hex_spaced += " "

            if i % self._split == self._split - 1:
                hex_spaced += " "
        return hex_spaced

    def get_spaced_bin_string(self, string: str) -> str:
        bin_spaced: str = ""
        for i in range(0, self._bits_to_show):
            bin_spaced += string[i]

            if i % self._split == self._split - 1:
                bin_spaced += " "
        return bin_spaced

    def _get_bin_indices(self, string: str) -> str:
        def vert_lines_for_row(num: int) -> str:
            vert_lines: str = ""
            for i in range(0, num):
                vert_lines += "|"
                if i % self._split == self._split - 1 and i != 0:
                    vert_lines += " "
            return vert_lines

        bin_indices: str = ""
        for i in range(0, self._bits_to_show):
            bin_indices += vert_lines_for_row(i)
            bin_indices += f"{self._bits_to_show - 1 - i}\n"
        return bin_indices

    def print_all(self):
        print("base10:", self._number)
        print("base16:", self._hex_str)
        print(" base2:", self._bin_str)

        print(8 * "-" + self._bits_to_show * "-")

        print(self._get_bin_indices(self._bin_str))
        print(self.get_spaced_bin_string(self._bin_str))
        print(self.get_spaced_hex_string(self._hex_str))


if __name__ == "__main__":
    # Parse hex from input
    raw_val = sys.argv[1]
    split = 4
    printer = HexBinDecPrinter(raw_val, split)
    printer.print_all()
