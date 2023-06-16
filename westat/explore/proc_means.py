import numpy as np
from numpy import inf
import pandas as pd


def proc_means(data: pd.DataFrame,
                   var: list,
                   precision: int = 2,
                   language: str = 'en') -> pd.DataFrame:
    """
    获取目标数据集的描述统计信息
    Args:
        data:DataFrame,需要进行统计分析的数据集
        var:list,需要统计的变量
        precision:数据精度，小数点位数，默认为2
        language:str,数据结果标题列显示语言，默认为 'en',可手动修改为'cn'

    Returns:
        描述统计结果数据集
    """

    result = []
    for v in var:
        # 数据类型
        col_dtype = str(data[v].dtype)

        # 如果列是数值型，并且不是全为空，则计算统计量
        if col_dtype in ('int64', 'float64', 'float32') and len(data[data[v].notnull()]):
            v_n = data[v].count()
            v_mean = data[v].mean()
            v_std = data[v].std()
            v_min = data[v].min()
            v_max = data[v].max()
            result.append([v, v_n, v_mean, v_std, v_min, v_max])

    result = pd.DataFrame(result, columns=['Variable', 'N', 'Mean', 'Std Dev', 'Minimum', 'Maximum'])

    # 设置显示格式
    result['N'] = result['N'].apply(lambda x: round(x, precision))
    result['Mean'] = result['Mean'].apply(lambda x: round(x, precision))
    result['Std Dev'] = result['Std Dev'].apply(lambda x: round(x, precision))
    result['Minimum'] = result['Minimum'].apply(lambda x: round(x, precision))
    result['Maximum'] = result['Maximum'].apply(lambda x: round(x, precision))

    return result
