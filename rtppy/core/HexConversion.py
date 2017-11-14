def add_two_hex_strings(hex_string_1, hex_string_2):
    """
    Adds to hex strings together and returns the sum as hex string

    :param hex_string_1:
    :param hex_string_2:
    :return: sum of hex_string_1 + hex_string_2 as a hex string
    """

    int_1 = int(hex_string_1, 16)
    int_2 = int(hex_string_2, 16)
    int_sum = int_1 + int_2
    int_to_hex = hex(int_sum)
    hex_string = int_to_hex.lstrip('0x')
    return hex_string.upper()

