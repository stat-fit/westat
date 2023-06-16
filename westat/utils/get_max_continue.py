import pandas as pd


def get_max_continue(column, find=0):
    """
    根据已经排序好的序列s，计算find出现的最大连续次数
    Args:
        column:pd.Series，已经排序的数据序列
        find:int，需要查找的值，默认为0
    Returns:
        int,find最大连续出现的次数
    """
    if isinstance(column,list) or isinstance(column,tuple):
        column=pd.Series(column)
    x = 0
    y = []

    for i in column:
        if i != find:
            x = 0
            y.append(x)
        else:
            x = x + 1
            y.append(x)
    return max(y)