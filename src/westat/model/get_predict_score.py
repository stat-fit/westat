# 预测模型分数

import numpy as np
import pandas as pd

from .get_data_discrete import get_data_discrete


def get_predict_score(data: pd.DataFrame,
                      scorecard: pd.DataFrame,
                      init_score: int = 600,
                      pdo: int = 20,
                      odds: float = 0,
                      target: str = 'y',
                      precision: int = 2):
    """
    根据评分卡表，对目标数据集进行预测得分和概率
    Args:
        data: pd.Dataframe,目标数据集
        scorecard: pd.Dataframe,评分卡表
        init_score:int,初始模型分,默认为600
        pdo:int,坏件率每上升一倍，增加的分数，默认为20
        odds:float,坏样本 / 好样本比例
        target:str,目标变量名称，默认为'y'
        precision:int,数据精度，小数点位数，默认为2

    Returns:
        返回预测结果表，包含模型特征原始值，模型特征得分，汇总评分卡得分，预测概率
    """

    # 复制数据
    df = data.copy()

    # 数据离散化
    col_result = scorecard['Name'].unique().tolist() + [target]
    col_bins = scorecard[['Name', 'Bins']][scorecard['Type'] == 'continuous'].drop_duplicates('Name')
    data_discrete = get_data_discrete(df[col_result], col_bin=col_bins, target=target, precision=precision)

    result = pd.DataFrame()
    col_score_list = []
    for col in scorecard['Name'].unique():
        col_score = col + '_Score'
        col_score_list.append(col_score)
        bins = scorecard['Bin'][scorecard['Name'] == col].tolist()
        score = scorecard['Score'][scorecard['Name'] == col].tolist()
        # 原样显示特征原始值
        result[col] = df[col]

        # 计算每个特征的得分
        result[col_score] = data_discrete[col].replace(bins, score)

        # 设置显示格式
        result[col_score] = result[col_score].apply(lambda x: round(x, precision))

    # 计算模型得分和预测概率
    if odds == 0:
        odds = data[target].sum() / (data[target].count() - data[target].sum())

    b = pdo / np.log(2)
    a = init_score + b * np.log(odds)
    result[target] = df[target]
    result['Score'] = a - b * scorecard['Intercept'][0] + result[col_score_list].sum(axis=1)
    result['Proba'] = 1 - 1 / (1 + np.e ** ((result['Score'] - a) / -b))

    # 设置显示格式
    result['Score'] = result['Score'].apply(lambda x: round(x, 0))
    result['Proba'] = result['Proba'].apply(lambda x: round(x, precision))

    return result
