import numpy as np
import pandas as pd
from tqdm.notebook import tqdm
from westat.logger import logger
from westat.get_data_iv import get_data_iv
from westat.get_col_type import get_col_type


def get_feature_by_ivcorr(data: pd.DataFrame,
                          data_iv: pd.DataFrame = pd.DataFrame(),
                          min_iv: float = 0.02,
                          max_corr: float = 0.6,
                          keep: list = [],
                          drop: list = [],
                          target: str = 'y',
                          return_drop: bool = False,
                          precision:int = 2):
    """
    根据最小IV值 和 最大相关性 筛选特征
    Args:
        data:DataFrame,将要筛选特征的数据集
        data_iv:DataFrame,列的IV汇总，包含Name,IV 两列的数据集
        min_iv:筛选后允许的最小IV值
        max_corr:筛选后允许的最大相关性
        keep:list,需要保留的特征
        drop:list,需要删除的特征
        target:str,目标变量名称，默认为'y'
        return_drop:是否返回已删除的特征
        precision:数据精度，小数点位数，默认为2

    Returns:
        默认返回筛选后的特征名单，
        当return_drop为True时，同时返回筛选后的特征名单、删除的特征名单、相关性和IV数据表
    """
    df = data.copy()

    # 如果没有特征IV入参，则按照默认的决策树方法，批量计算特征IV
    if data_iv.empty:
        data_iv = get_data_iv(data, target=target)

    # 根据每一列的IV值，计算相关矩阵
    col_iv_filter = data_iv[data_iv['Name'].isin(df.columns)]

    # 如果列的数据类型不是连续型特征，则赋值为0后计算相关性，否则直接计算相关性
    col_type = get_col_type(data)
    for col in col_iv_filter['Name']:
        if col_type['Type'][col_type['Name'] == col].iloc[0] != 'continuous':
            df[col] = 0

    data_corr = df[col_iv_filter['Name']].corr()

    col_iv_result = []
    for i in range(len(col_iv_filter)):
        for j in range(len(col_iv_filter)):
            col1 = col_iv_filter.iloc[i, 0]
            iv1 = col_iv_filter.iloc[i, 1]
            col2 = col_iv_filter.iloc[j, 0]
            iv2 = col_iv_filter.iloc[j, 1]
            col_iv_result.append([col1, col2, iv1, iv2, iv1 - iv2])

    result = pd.DataFrame(col_iv_result, columns=['Name1', 'Name2', 'IV1', 'IV2', 'IV1-IV2'])
    result['Corr'] = data_corr.values.reshape(-1, 1)
    result = result[result['Name1'] != result['Name2']]

    col_drop_by_iv = result['Name1'][result['IV1'] <= min_iv].unique()
    col_drop_by_corr = result['Name1'][(result['Corr'] > max_corr) & (result['IV1-IV2'] < 0)].unique()

    col_result = [col for col in result['Name1'].unique() if
                  col not in col_drop_by_iv and col not in col_drop_by_corr and col not in drop]
    col_keep = sorted(list(set(col_result + keep)))

    # 设置显示格式
    result['IV1'] = result['IV1'].apply(lambda x: round(x, precision))
    result['IV2'] = result['IV2'].apply(lambda x: round(x, precision))
    result['IV1-IV2'] = result['IV1-IV2'].apply(lambda x: round(x, precision))
    result['Corr'] = result['Corr'].apply(lambda x: round(x, precision))


    # 是否返回已删除特征和相关矩阵
    if return_drop:
        return col_keep, col_drop_by_iv, col_drop_by_corr, result
    else:
        return col_keep