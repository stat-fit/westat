import numpy as np
from numpy import inf
import pandas as pd

from .get_psi import get_psi


def get_data_psi(data_actual: pd.DataFrame,
                 data_expected: str,
                 qcut=10,
                 missing: list = [np.nan, None, 'nan'],
                 target='y',
                 precision=6) -> pd.DataFrame:
    """
    计算数据集PSI
    Args:
        data_actual: DataFrame,实际数据集
        data_expected: DataFrame,预期数据集
        col:str,需要计算PSI的列名
        bins:list，计算PSI的分箱
        qcut: int,等额分箱的分组数
        missing: list,缺失值列表
        target: str,目标变量名称，默认为'y'
        precision:数据精度，小数点位数，默认为2
        language: str,数据结果标题列显示语言，默认为 'en',可手动修改为'cn'

    Returns:
        结果数据集保存数据集对应的PSI
    """
    col_psi = []
    for col in [i for i in data_actual.columns if i != target]:
        df_psi = get_psi(data_actual,
                         data_expected,
                         col,
                         qcut=qcut,
                         target=target,
                         missing=missing,
                         precision=precision)
        col_psi.append([col, float(df_psi['Total PSI'].loc[0])])

    result = pd.DataFrame(col_psi, columns=["Name", "PSI"])
    result.sort_values(by='PSI', ascending=False, inplace=True)
    return result
