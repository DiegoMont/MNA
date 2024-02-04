"""Prints decimal, binary and hexadecimal representation of a number in a file
"""
import sys
import time


def to_binary(decimal_number: int) -> str:
    """Returns the binary representation of the decimal number
    """
    if decimal_number == 0:
        return "0"
    bits = []
    while decimal_number > 0:
        digit = str(decimal_number % 2)
        bits.insert(0, digit)
        decimal_number //= 2
    bin_representation = "".join(bits)
    return bin_representation


def to_hex(decimal_number: int) -> str:
    """Returns the hexadecimal representation of the decimal number
    """
    if decimal_number == 0:
        return "0"
    digit_map = ['0', '1', '2', '3', '4', '5', '6', '7',
                 '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    digits = []
    while decimal_number > 0:
        digit = digit_map[decimal_number % 16]
        digits.insert(0, digit)
        decimal_number //= 16
    hex_representation = "".join(digits)
    return hex_representation


if __name__ == "__main__":
    start = time.time()
    filename = sys.argv[1]
    CONVERSION_RESULTS = ""
    with open(filename, encoding="utf-8") as file:
        for line in file:
            try:
                num = int(line)
                if num < 0:
                    BINARY = to_binary(-num)
                    HEXADECIMAL = to_hex(-num)
                    CONVERSION_RESULTS += f"{num}   -{BINARY}   -{HEXADECIMAL}\n"
                else:
                    BINARY = to_binary(num)
                    HEXADECIMAL = to_hex(num)
                    CONVERSION_RESULTS += f"{num}   {BINARY}   {HEXADECIMAL}\n"
            except ValueError:
                CONVERSION_RESULTS += f"{line}   #VALUE!   #VALUE!\n"
    elapsed_time = time.time() - start
    time_report = f"EXECUTION TIME: {elapsed_time:10.3f}s"
    CONVERSION_RESULTS += time_report
    print(CONVERSION_RESULTS)
    with open("ConvertionResults.txt", "w", encoding="utf-8") as results_file:
        results_file.write(CONVERSION_RESULTS)
