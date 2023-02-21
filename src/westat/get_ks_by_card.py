import numpy as np
import pandas as pd
from westat.get_predict_score import get_predict_score


def get_ks_by_card(data: pd.DataFrame,
           scorecard: pd.DataFrame,
           init_score: int = 600,
           pdo: int = 50,
           target: str = 'y',
           return_data: bool = False,
           precision: int = 2):
    """
    根据评分卡内容，对目标数据集的评分结果计算ks
    Args:
        data:pd.DataFrame,目标数据集
        scorecard:pd.DataFrame，评分卡规则表
        init_score:int,初始模型分,默认为600
        pdo:int,坏件率每上升一倍，增加的分数，默认为50
        target:tr,目标变量名称，默认为'y'
        return_data:是否返回结果数据
        precision:int,数据精度，小数点位数，默认为2

    Returns:
        计算ks的值，或根据要求返回结果数据
    """
    from sklearn.metrics import roc_curve

    data_score = get_predict_score(data, scorecard, init_score=init_score, pdo=pdo, target=target, precision=precision)
    fpr, tpr, thresholds = roc_curve(data['y'], data_score['Proba'], drop_intermediate=False)

    pre = sorted(data_score['Proba'], reverse=True)
    num = [i * int(len(pre) / 10) for i in range(10)]
    num = num + [(len(pre) - 1)]
    ks_thresholds = [max(thresholds[thresholds <= pre[i]]) for i in num]
    result = pd.DataFrame([fpr, tpr, thresholds, tpr - fpr]).T
    result.columns = ['fpr', 'tpr', 'thresholds', 'ks']
    result = pd.merge(result, pd.DataFrame(ks_thresholds, columns=['thresholds']), on='thresholds', how='inner')
    result.reset_index(drop=True, inplace=True)
    result['No.'] = result.index + 1
    result = result[['No.', 'fpr', 'tpr', 'thresholds', 'ks']]

    total = data_score.groupby(['Proba'])[target].count()
    bad = data_score.groupby(['Proba'])[target].sum()
    data_ks = pd.DataFrame({'#Total': total, '#Bad': bad})
    data_ks['#Good'] = data_ks['#Total'] - data_ks['#Bad']
    data_ks['Proba'] = data_ks.index
    data_ks.index = range(len(data_ks))
    data_ks = data_ks.sort_values(by='Proba', ascending=True)
    data_ks['%CumBad'] = data_ks['#Bad'].cumsum() / data_ks['#Bad'].sum()
    data_ks['%CumGood'] = data_ks['#Good'].cumsum() / data_ks['#Good'].sum()
    data_ks['KS'] = data_ks['%CumGood'] - data_ks['%CumBad']
    data_ks.reset_index(drop=True, inplace=True)
    data_ks['No.'] = data_ks.index + 1
    data_ks = data_ks[['No.', 'Proba', '#Total', '#Bad', '#Good', '%CumBad', '%CumGood', 'KS']]
    ks = round(result['ks'].max(), precision)

    if return_data:
        return ks, result
    else:
        return ks
