import numpy as np
import pandas as pd
from tqdm.notebook import tqdm
from westat.get_col_bins import get_col_bins
from westat.logger import logger


def get_data_discrete(data: pd.DataFrame,                      
                      data_bins: pd.DataFrame = pd.DataFrame(),
                      max_depth=None,
                      max_leaf_nodes: int = 4,
                      min_samples_leaf: float = 0.05,
                      missing: list = [np.nan, None],
                      target: str = 'y',
                      precision: int = 2):
    """
    将原始数据集，按照分箱数据集中的要求，进行离散化处理，并返回离散化后的数据集
    如果数据集中的列不在分箱数据集中，则保留原始数据集中的格式
    Args:
        data: DataFrame,需要进行离散化的目标数据集
        data_bins: DataFrame,存放列名，分箱列表的数据集
        max_depth: int,树的深度
        max_leaf_nodes:最大叶子节点数,默认为 4
        min_samples_leaf:float,叶子节点样本数量最小占比,默认为0.05
        missing: list,缺失值列表
        target:str,目标变量名称，默认为'y'
        precision:int,数据精度，小数点位数，默认为2

    Returns:
        返回离散化后的数据集
    """
    logger.info('根据分箱离散化连续变量进行中。。。')

    if data_bins.empty:
        bins = get_col_bins(data=data,
                            target=target,
                            max_depth=max_depth,
                            max_leaf_nodes=max_leaf_nodes,
                            min_samples_leaf=min_samples_leaf,
                            missing=missing,
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
    logger.info('根据分箱离散化连续变量完成！')
    return result
