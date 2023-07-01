import numpy as np
from numpy import inf
import pandas as pd
from .get_tree_bins import get_tree_bins


def get_bins(data: pd.DataFrame,
             col: str,
             missing: list = [np.nan, None, 'nan', 'null', 'NULL'],
             max_bins: int = 5,
             target: str = 'y',
             method: str = 'optb',
             trend: str = 'auto',
             max_depth=None,
             min_samples_leaf=0.05,
             precision: int = 4) -> pd.DataFrame:
    """
    计算数据集中指定列的WOE和IV值
    Args:
        data: DataFrame,目标数据集
        col: str,需要计算WoE和IV的列名
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
        结果数据集保存各分组名称和分组对应的WoE和IV值
    """
    df = data.copy()

    # 检查数据集中是否存在预定义的缺失值
    missing_list = []
    for m in missing:
        if m in data[col]:
            missing_list.append(m)

    # 决策树分箱
    if method == 'tree' and trend == 'auto':
        if len(missing_list) > 0 or len(data[data[col].isnull()]) > 0:
            df[col].replace(missing, [np.nan] * len(missing), inplace=True)
            bins = get_tree_bins(data=data,
                                 col=col,
                                 target=target,
                                 max_depth=max_depth,
                                 max_leaf_nodes=max_bins,
                                 min_samples_leaf=min_samples_leaf,
                                 precision=precision)
            result = bins
        else:
            bins = get_tree_bins(data=df,
                                 col=col,
                                 target=target,
                                 max_depth=None,
                                 max_leaf_nodes=max_bins,
                                 min_samples_leaf=0.05,
                                 precision=2)
            result = bins

    # 按照optbinning分箱
    else:
        if trend == 'asc':
            monotonic_trend = 'ascending'
        elif trend == 'desc':
            monotonic_trend = 'descending'
        else:
            monotonic_trend = trend

        if len(missing_list) > 0 or len(data[data[col].isnull()]) > 0:
            df[col].replace(missing, [np.nan] * len(missing), inplace=True)
            if str(data[col].dtype) in ('int64', 'float64', 'float32'):
                dtype = 'numerical'
            else:
                dtype = 'categorical'

            from optbinning import OptimalBinning
            optb = OptimalBinning(name=col,
                                  dtype=dtype,
                                  solver='cp',  # 算子
                                  max_n_bins=max_bins,  # 最大分箱数
                                  monotonic_trend=monotonic_trend  # 设置单调趋势
                                  )
            optb.fit(data[col], data[target])
            result = [-inf] + list(optb.splits) + [inf]
        else:
            if str(data[col].dtype) in ('int64', 'float64', 'float32'):
                dtype = 'numerical'
            else:
                dtype = 'categorical'

            from optbinning import OptimalBinning
            optb = OptimalBinning(name=col,
                                  dtype=dtype,
                                  solver='cp',  # 算子
                                  max_n_bins=max_bins,  # 最大分箱数
                                  monotonic_trend=monotonic_trend  # 设置单调趋势
                                  )
            optb.fit(data[col], data[target])
            result = [-inf] + list(optb.splits) + [inf]

    return result
