def to_single_byte(input_str):
    """
    将输入的字符串中的全角字符转换为半角字符
    Args:
        input_str: 需要转换的字符串

    Returns:
        转换为半角字符后的字符串
    """
    output_str = ''
    for i in input_str:
        code_i = ord(i)
        if code_i == 12288:
            code_i = 32
        elif 65281 <= code_i <= 65374:
            code_i -= 65248

        output_str += chr(code_i)

    return output_str
