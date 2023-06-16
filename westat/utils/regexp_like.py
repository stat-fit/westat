def regexp_like(source, pattern):
    """
    根据输入的字符串，根据正则公式，检查是否匹配指定内容
    Args:
        source:要替换的原始字符串
        pattern:要匹配的正则模式
    Returns:

    """
    import re
    p = re.compile(pattern)
    re_result = p.findall(source)
    result = len(re_result) > 0
    return result
