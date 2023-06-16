import pandas as pd


def get_over_continue(column, over=0, eq=False):
    """
    获取序列连续大于指定值的次数 ，或序列连续相等且大于指定值的次数
    Args:
        column: pd.Series，已经排序的数据序列
        over: int，需要大于的指定值，默认为0
        eq: 是否要求取值相等

    Returns:
        int, 序列连续大于指定值的次数 ，或序列连续相等且大于指定值的次数
    """
    if isinstance(column, list) or isinstance(column, tuple):
        column = pd.Series(column)

    x = 0
    y = []

    # 循环检查序列中的每个元素，是否大于指定值，并与上一个元素相等
    for i in range(len(column)):
        # print(i,' ',column[i],' ',y)
        if i == 0:
            if column[i] > over:
                x = x + 1
                y.append(x)
            else:
                x = 0
                y.append(x)
        else:
            if column[i] > over:
                if eq:
                    if column[i] == column[i - 1]:   # 如果当前元素与上一个元素相等，则统计数+1
                        x = x + 1
                        y.append(x)
                    else:
                        x = 1  # 如果当前元素与上一个元素不相等，则初始化为1
                        y.append(x)
                else:
                    x = x + 1
                    y.append(x)
            else:
                x = 0
                y.append(x)
    return max(y)
