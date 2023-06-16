def to_multi_byte(input_str):
    """
    将输入的字符串中的半角字符转换为全角字符
    Args:
        input_str: 需要转换的字符串

    Returns:
        转换为全角字符后的字符串
    """
    output_str = ''
    for i in input_str:
        code_i = ord(i)
        if code_i == 32:
            code_i = 12288
        elif 33 <= code_i <= 126:
            code_i += 65248

        output_str += chr(code_i)

    return output_str