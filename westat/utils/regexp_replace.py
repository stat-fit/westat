def regexp_replace(source, pattern, replace_string):
    """
    根据输入的字符串，根据正则公式，查找指定内容，并进行替换
    Args:
        source:要替换的原始字符串
        pattern:要匹配的正则模式
        replace_string:将匹配的pattern替换成的字符串

    Returns:
        返回正则替换后的字符串
    """
    import re
    p = re.compile(pattern)
    output_str = p.sub(replace_string, source)
    return output_str
