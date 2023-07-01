import numpy as np
from numpy import inf
import pandas as pd
from sklearn.tree import DecisionTreeClassifier


def get_tree_bins(data: pd.DataFrame,
                  col: str,
                  target: str = 'y',
                  max_depth=None,
                  max_leaf_nodes: int = 4,
                  min_samples_leaf: float = 0.05,
                  missing: list = [np.nan, None, 'nan','null','NULL'],
                  precision: int = 2) -> list:
    """
    根据决策树对数据集进行特征分箱，默认最大分为5箱
    Args:
        data: DataFrame,将要根据决策树进行分箱的数据集
        col: str,将要分箱的列名
        target: str,目标变量名称，默认为'y'
        max_depth: int,树的深度
        max_leaf_nodes: int,最大叶子节点数,默认为 4
        min_samples_leaf: float,叶子节点样本数量最小占比,默认为0.05
        missing: list,缺失值列表
        precision:int,数据精度，小数点位数，默认为2

    Returns:
        根据决策树结果得到的分箱列表，例如：[-inf,30,40,50,inf]
    """
    df = data.copy()
    df[col].replace(missing, np.nan, inplace=True)

    data_notnull = df[[col, target]][df[col].notnull()]  # 删除空值
    result = []
    if len(np.unique(data_notnull[col])) > 1:
        x = data_notnull[col].values.reshape(-1, 1)
        y = data_notnull[target].values

        clf = DecisionTreeClassifier(criterion='entropy',  # “信息熵”最小化准则划分
                                     max_depth=max_depth,  # 树的深度
                                     max_leaf_nodes=max_leaf_nodes,  # 最大叶子节点数
                                     min_samples_leaf=min_samples_leaf)  # 叶子节点样本数量最小占比
        clf.fit(x, y)

        threshold = np.unique(clf.tree_.threshold)
        x_num = np.unique(x)

        for i in threshold:
            if i != -2:
                point = np.round(max(x_num[x_num < i]), precision)  # 取切分点左边的数
                result.extend([point])
        result = [float(str(i)) for i in list(np.unique(result))]
        result = [-inf] + result + [inf]
    return result
