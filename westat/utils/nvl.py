import pandas as pd


def nvl(value, new_value):
    """
    如果变量为空则返回新取值，否则返回旧的值
    Args:
        value: 需要判断是否为空的变量
        new_value: 当变量为空时的取值

    Returns:
        如果变量为空则返回新的取值，否则返回旧的值
    """
    if value is None or pd.isna(value):
        return new_value
    else:
        return value
