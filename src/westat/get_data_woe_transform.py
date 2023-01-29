import numpy as np
import pandas as pd
from tqdm.notebook import tqdm
from westat.logger import logger
from westat.get_woe_iv import get_woe_iv


def get_data_woe_transform(data_discrete,
                           target='y',
                           criterion='discrete',
                           missing: list = [np.nan, None, 'nan'],
                           precision=2):
    """
    根据离散化数据集，进行WoE转换
    Args:
        data_discrete: DataFrame,目标数据集
        target: str,目标变量名称，默认为'y'
        criterion: str,分箱方法，默认为'discrete'，表示使用已经离散化的数据计算WoE
        missing: list,缺失值列表
        precision: 数据精度，小数点位数，默认为2

    Returns:
        返回经过WoE转换后的数据集
    """
    logger.info('WOE转换中。。。')
    data_woe = pd.DataFrame()
    for col in tqdm([i for i in data_discrete.columns if i != target]):
        col_woe = get_woe_iv(data_discrete, col=col, target=target, criterion=criterion, missing=missing, precision=precision)
        s = data_discrete[col].replace(list(col_woe['Bin']), list(col_woe['WoE']))
        data_woe = pd.concat([data_woe, s], axis=1)
    data_woe[target] = data_discrete[target]
    logger.info('WOE转换完成！')
    return data_woe
