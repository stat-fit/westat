import numpy as np
def rate(a: float, b: float, method: int = 1,missing=99999999) -> float:
    """
    计算两个数值的比率 a/b
    Args:
        a: 本期数值
        b: 上期数值
        method:比率计算方法，
            1：分子或分母缺失时，赋值为null；分母为0时，结果为null；
            2：分子或分母缺失时，赋值为null；分母为0时，根据分子>0、=0、<0，分别赋值为 missing、0、-missing
    Returns:
        增长率计算结果
    """
    if method == 1:
        if b == 0:
            result = np.nan
        else:
            result = a / b
    elif method == 2:
        if b == 0:
            if a > 0:
                result = missing
            elif a == 0:
                result = 0
            elif a < 0:
                result = -missing
        else:
            result = a / b

    return result