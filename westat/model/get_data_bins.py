import numpy as np
import pandas as pd
from .get_bins import get_bins
from .get_data_type import get_data_type


def get_data_bins(data: pd.DataFrame,
                  missing: list = [np.nan, None, 'nan','null','NULL'],
                  max_bins: int = 5,
                  target: str = 'y',
                  method: str = 'optb',
                  trend: str = 'auto',
                  precision: int = 4,
                  max_depth=None,
                  min_samples_leaf: float = 0.05,
                  ) -> pd.DataFrame:
    """
    将数据集中所有列，根据决策树进行分箱
    连续变量的分箱，按小于等于，大于切分，空值单独归位一类，例如:['age', [-inf, 22, 35, 50, 60, inf]]
    Args:
        data: DataFrame,目标数据集
        missing: list,缺失值列表
        max_bins:int,最大分箱数，默认分为5箱
        target: str,目标变量名称，默认为'y'
        method: str,分箱方法，
            默认为'tree'表示使用决策树分箱
            当取值为 'optb'时，表示使用OptimalBinning进行分箱，此时启用trend参数设置分箱单调性
        trend:str,设置分箱单调趋势，一般使用的有：ascending，descending，auto_asc_desc，peak，valley
            ascending：单调递增；
            descending：单调递减
            auto_asc_desc：自动增减：
            peak：先增后减
            valley：先减后增
        precision:数据精度，小数点位数，默认为2
        max_depth:int,树的深度
        min_samples_leaf:叶子节点样本数量最小占比,默认为0.05

    Returns:
        返回数据集，包含列名，分箱结果两列，分箱结果使用list保存
    """
    col_types = get_data_type(data)
    col_continuous_bins = []
    for i in range(len(col_types)):
        col = col_types.iloc[i, 0]
        col_type = col_types.iloc[i, 1]
        if col_type == 'continuous' and col in data.columns and col != target:
            bins = get_bins(data=data[[col, target]],
                             col=col,
                             target=target,
                             max_depth=max_depth,
                             max_bins=max_bins,
                             min_samples_leaf=min_samples_leaf,
                             missing=missing,
                             precision=precision)
            if bins:
                col_continuous_bins.append([col, bins])
    result = pd.DataFrame(col_continuous_bins, columns=['Name', 'Bins'])
    return result
