import numpy as np
import pandas as pd
from tqdm.notebook import tqdm
from .get_woe_iv import get_woe_iv


def get_data_iv(data: pd.DataFrame,
                target='y',
                method='optb',
                bins=[],
                qcut=0,
                missing: list = [np.nan, None, 'nan','null','NULL'],
                max_bins: int = None,
                trend: str = 'auto',
                precision=4):
    """
    批量获取变量IV值
    Args:
        data: DataFrame,目标数据集
        target: str,目标变量名称，默认为'y'
        method: str,分箱方法，
            默认为'tree'表示使用决策树分箱
            当取值为 'discrete'时，表示数据集已经离散化，直接计算WoE和IV
            当取值为 'optb'时，表示使用OptimalBinning进行分箱，此时启用trend参数设置分箱单调性
        bins: list,手动指定的分箱列表
        qcut: int,等额分箱的分组数
        missing: list,缺失值列表
        max_bins:int,最大分箱数，默认分为5箱，仅决策树分箱时可用
        trend:str,设置分箱单调趋势，一般使用的有：ascending，descending，auto_asc_desc，peak，valley
            ascending：单调递增；
            descending：单调递减
            auto_asc_desc：自动增减：
            peak：先增后减
            valley：先减后增
        precision: 数据精度，小数点位数，默认为2

    Returns:
        返回包含特征名称，IV值两列的数据集
    """
    col_iv = []
    for col in tqdm([i for i in data.columns if i != target]):
        if data[col].dtypes in ('int64', 'float64', 'float32'):
            new_method = method
        else:
            new_method = 'discrete'
        col_woe_iv = get_woe_iv(data=data,
                                col=col,
                                target=target,
                                method=new_method,
                                bins=bins,
                                qcut=qcut,
                                missing=missing,
                                max_bins=max_bins,
                                trend=trend,
                                precision=precision)
        col_woe_iv['IV'] = pd.to_numeric(col_woe_iv['IV'])
        col_iv.append([col, col_woe_iv['IV'].iloc[-1]])
    result = pd.DataFrame(col_iv, columns=["Name", "IV"])
    result.sort_values(by='IV', ascending=False, inplace=True)
    result['IV'] = result['IV'].apply(lambda x: format(x, '.' + str(precision) + 'f'))
    return result
