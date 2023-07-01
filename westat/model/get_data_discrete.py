import numpy as np
import pandas as pd
from tqdm.notebook import tqdm
from .get_data_bins import get_data_bins


def get_data_discrete(data: pd.DataFrame,
                      data_bins: pd.DataFrame = pd.DataFrame(),
                      method='optb',
                      trend='auto',
                      max_depth=None,
                      max_bins: int = 5,
                      min_samples_leaf: float = 0.05,
                      missing: list = [np.nan, None, 'nan','null','NULL'],
                      target: str = 'y',
                      precision: int = 2):
    """
    将原始数据集，按照分箱数据集中的要求，进行离散化处理，并返回离散化后的数据集
    如果数据集中的列不在分箱数据集中，则保留原始数据集中的格式
    Args:
        data: DataFrame,需要进行离散化的目标数据集
        data_bins: DataFrame,存放列名，分箱列表的数据集
        method: str,分箱方法，
            默认为'tree'表示使用决策树分箱
            当取值为 'optb'时，表示使用OptimalBinning进行分箱，此时启用trend参数设置分箱单调性
        trend:str,设置分箱单调趋势，一般使用的有：ascending，descending，auto_asc_desc，peak，valley
            ascending：单调递增；
            descending：单调递减
            auto_asc_desc：自动增减：
            peak：先增后减
            valley：先减后增
        max_bins:int,最大分箱数，默认分为5箱
        max_depth: int,树的深度
        max_leaf_nodes:最大叶子节点数,默认为 4
        min_samples_leaf:float,叶子节点样本数量最小占比,默认为0.05
        missing: list,缺失值列表
        target:str,目标变量名称，默认为'y'
        precision:int,数据精度，小数点位数，默认为2

    Returns:
        返回离散化后的数据集
    """

    if data_bins.empty:
        bins = get_data_bins(data=data,
                             missing=missing,
                             max_bins=max_bins,
                             target=target,
                             method=method,
                             trend=trend,
                             max_depth=max_depth,
                             min_samples_leaf=min_samples_leaf,
                             precision=precision)
    else:
        bins = data_bins

    # 不在分箱清单中的列，保持原样
    cols = [i for i in data.columns if i not in [i[0] for i in bins]]
    result = data[cols].copy()

    # 其他列按照分箱清单进行离散化
    for i in tqdm(range(len(bins))):
        col = bins.iloc[i, 0]
        cut_points = bins.iloc[i, 1]
        if col in data.columns:
            result[col] = pd.cut(data[col], cut_points).astype('str')

    # 缺失值替换
    result.replace(missing, ['missing'] * len(missing), inplace=True)
    return result
