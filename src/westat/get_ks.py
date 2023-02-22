import numpy as np
import pandas as pd


def get_ks(data: pd.DataFrame,
           col: str = 'Proba',
           target: str = 'y',
           qcut: int = 10,
           return_data: bool = False,
           precision: int = 2):
    """
    根据评分卡内容，对目标数据集的评分结果计算 KS
    Args:
        data:pd.DataFrame,目标数据集
        col:str，正例的概率估计字段名
        target:tr,目标变量名称，默认为'y'
        qcut:int,分组数，默认切分为10组
        return_data:是否返回结果数据
        precision:int,数据精度，小数点位数，默认为2

    Returns:
        计算ks的值，或根据要求返回结果数据
    """
    from sklearn.metrics import roc_curve

    fpr, tpr, thresholds = roc_curve(data[target], data[col], drop_intermediate=False)

    pre = sorted(data[col], reverse=True)
    num = [i * int(len(pre) / qcut) for i in range(qcut)]
    num = num + [(len(pre) - 1)]
    ks_thresholds = [max(thresholds[thresholds <= pre[i]]) for i in num]
    result = pd.DataFrame([fpr, tpr, thresholds, tpr - fpr]).T
    result.columns = ['fpr', 'tpr', 'thresholds', 'ks']
    result = pd.merge(result, pd.DataFrame(ks_thresholds, columns=['thresholds']), on='thresholds', how='inner')
    result.reset_index(drop=True, inplace=True)
    result['No.'] = result.index + 1
    result = result[['No.', 'fpr', 'tpr', 'thresholds', 'ks']]
    result['ks'] = result['ks'].apply(lambda x: round(abs(x), precision))
    ks_qcut = round(result['ks'].max(), precision)

    total = data.groupby([col])[target].count()
    bad = data.groupby([col])[target].sum()
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
    data_ks['KS'] = data_ks['KS'].apply(lambda x: round(abs(x), precision))
    ks_cum = round(data_ks['KS'].max(), precision)

    if return_data:
        if qcut > 0:
            return ks_qcut, result.head(qcut)
        else:
            return ks_cum, result
    else:
        if qcut > 0:
            return ks_qcut
        else:
            return ks_cum
