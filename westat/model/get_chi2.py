def get_chi2(data, precision: int = 4):
    """
        计算指定数据的信息熵
        Args:
            data: 需要计算卡方的数据列表，支持 pd.crosstab 格式的数据表
            precision: 数据精度，小数点位数，默认为2

        Returns:
            返回计算后的卡方
        """
    import pandas as pd
    from scipy.stats import chi2_contingency

    if isinstance(data, pd.DataFrame):
        chi2 = chi2_contingency(data, correction=False).statistic
    else:
        chi2 = 0

    # 数据精度处理
    result = round(chi2, precision)

    return result
