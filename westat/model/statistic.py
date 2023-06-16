import pandas as pd


def median(series, skipna=True):
    """
    计算一组数据的中位数
    Args:
        series: 需要计算的数据
        skipna: 是否跳过空值

    Returns:
        返回数据的中位数
    """
    if not isinstance(series, pd.Series):
        series = pd.Series(series)

    result = series.median(skipna=skipna)
    return result


def mode(series, skipna=True):
    """
    计算一组数据的众数
    Args:
        series: 需要计算的数据
        skipna: 是否跳过空值

    Returns:
        返回数据的众数
    """
    if not isinstance(series, pd.Series):
        series = pd.Series(series)

    result = series.mode(dropna=skipna)
    return result


def mean(series, skipna=True):
    """
    计算一组数据的简单平均数
    Args:
        series: 需要计算的数据
        skipna:是否跳过空值

    Returns:
        返回数据的简单平均数
    """
    if not isinstance(series, pd.Series):
        series = pd.Series(series)

    result = series.mean(skipna=skipna)
    return result


def geomean(series, skipna=True):
    """
    计算一组数据的几何平均数
    Args:
        series: 需要计算的数据
        skipna:是否跳过空值

    Returns:
        返回数据的简单平均数
    """
    if not isinstance(series, pd.Series):
        series = pd.Series(series)

    import numpy as np
    if skipna:
        series.dropna(inplace=True)
        g = 1
        for s in series:
            g = g * s
        result = np.power(g,1/len(series))
    else:
        g = 1
        for s in series:
            g = g * s
        result = np.power(g,1/len(series))

    return result


def sqrt(series, skipna=True):
    """
    计算一组数据的开方
    Args:
        series: 需要计算的数据
        skipna:是否跳过空值

    Returns:
        返回数据的开方
    """
    if not isinstance(series, pd.Series):
        series = pd.Series(series)

    import numpy as np

    if skipna:
        series.dropna(inplace=True)
        result = np.sqrt(series)
    else:
        result = np.sqrt(series)

    return result


def mean_deviation(series,avg=None,count=[],skipna=True):
    """
    计算一组数据的平均差（平均绝对离差）
    Args:
        series: 需要计算的数据
        avg:均值
        count:数量
        skipna:是否跳过空值

    Returns:
        返回数据的平均差（平均绝对离差）
    """
    import numpy as np
    if not isinstance(series, pd.Series):
        series = pd.Series(series)

    if pd.isna(avg):
        avg = series.mean(skipna=skipna)

    if len(count) > 0:
        count = np.sum(count)
    else:
        count = len(series)

    if skipna:
        series.dropna(inplace=True)

        m = 0
        for s in series:
            m = m + abs(s - avg) *

        print(m,count,avg)
        result = m / count
    else:
        m = 0
        for s in series:
            m = m + abs(s - avg)
        result = m / count

    return result