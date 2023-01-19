import numpy as np
import pandas as pd
from tqdm.notebook import tqdm
from westat.logger import logger
from westat.get_woe_iv import get_woe_iv


def get_data_iv(data: pd.DataFrame,
                target='y',
                criterion='tree',
                bins=[],
                qcut=0,
                missing: list = [np.nan, None],
                precision=2):
    """
    批量获取变量IV值
    Args:
        data: DataFrame,目标数据集
        target: str,目标变量名称，默认为'y'
        criterion: str,分箱方法，默认为决策树分箱
        bins: list,手动指定的分箱列表
        qcut: int,等额分箱的分组数
        missing: list,缺失值列表
        precision: 数据精度，小数点位数，默认为2

    Returns:
        返回包含特征名称，IV值两列的数据集
    """
    logger.info('IV值计算中。。。')
    col_iv = []
    for col in tqdm([i for i in data.columns if i != target]):
        col_woe_iv = get_woe_iv(data=data,
                                col=col,
                                target=target,
                                criterion=criterion,
                                bins=bins,
                                qcut=qcut,
                                missing=missing,
                                precision=precision)
        col_iv.append([col, float(col_woe_iv['Total IV'].loc[0])])
    result = pd.DataFrame(col_iv, columns=["Name", "IV"])
    result.sort_values(by='IV', ascending=False, inplace=True)
    logger.info('IV值计算完成！')
    return result
