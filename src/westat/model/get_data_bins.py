import numpy as np
import pandas as pd
from .get_tree_bins import get_tree_bins
from .get_col_type import get_col_type


def get_data_bins(data: pd.DataFrame,
                  target: str = 'y',
                  max_depth=None,
                  max_leaf_nodes: int = 4,
                  min_samples_leaf: float = 0.05,
                  missing: list = [np.nan, None, 'nan'],
                  precision=2) -> pd.DataFrame:
    """
    将数据集中所有列，根据决策树进行分箱
    连续变量的分箱，按小于等于，大于切分，空值单独归位一类，例如:['age', [-inf, 22, 35, 50, 60, inf]]
    Args:
        data:DataFrame,需要分箱的数据集
        target:str,目标变量名称，默认为'y'
        max_depth:int,树的深度
        max_leaf_nodes:最大叶子节点数,默认为 4
        min_samples_leaf:叶子节点样本数量最小占比,默认为0.05
        missing: list,缺失值列表
        precision:int,数据精度，小数点位数，默认为2

    Returns:
        返回数据集，包含列名，分箱结果两列，分箱结果使用list保存
    """
    col_types = get_col_type(data)
    col_continuous_bins = []
    for i in range(len(col_types)):
        col = col_types.iloc[i, 0]
        col_type = col_types.iloc[i, 1]
        if col_type == 'continuous' and col in data.columns and col != target:
            point = get_tree_bins(data=data[[col, target]],
                                  col=col,
                                  target=target,
                                  max_depth=max_depth,
                                  max_leaf_nodes=max_leaf_nodes,
                                  min_samples_leaf=min_samples_leaf,
                                  missing=missing,
                                  precision=precision)
            if point:
                col_continuous_bins.append([col, point])
    result = pd.DataFrame(col_continuous_bins, columns=['Name', 'Bins'])
    return result
