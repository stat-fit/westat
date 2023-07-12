def gini_impurity(l=None, c=None, precision: int = 2):
    """
    根据传入的数据列表，计算基尼不纯度
    Args:
        l: 需要计算不纯度的数据列表，支持pandas.Series和python列表、元组格式
        c: 已统计的数值结果列表
        precision:数据精度，小数点位数，默认为2
    Returns:
        基尼不纯度 gini impurity
    """
    import pandas as pd

    if not isinstance(l, pd.Series):
        s = pd.Series(l, dtype='object')
    else:
        s = l

    if not isinstance(c, pd.Series):
        c = pd.Series(c, dtype='object')

    if len(l) > 0:
        df = pd.DataFrame(s.value_counts())
        df.columns = ['count']
        df['ratio'] = df['count'] / len(l)
    else:
        df = pd.DataFrame({'count': c}, index=range(len(c)))
        df['ratio'] = df['count'] / sum(c)

    gini = 1 - sum([p ** 2 for p in df['ratio']])

    # 数据精度处理
    result = round(gini, precision)

    return result
