import numpy as np
import pandas as pd


def get_ks(data: pd.DataFrame,
           col: str = 'Proba',
           target: str = 'y',
           qcut: int = 10,
           method: str = '',
           return_data: bool = False,
           precision: int = 2):
    """
    根据评分卡内容，对目标数据集的评分结果计算 KS
    Args:
        data:pd.DataFrame,目标数据集
        col:str，正例的概率估计字段名
        target:tr,目标变量名称，默认为'y'
        qcut:int,分组数，默认切分为10组
        method:str,计算ks的方法，默认为空，可选sklearn
        return_data:是否返回结果数据
        precision:int,数据精度，小数点位数，默认为2

    Returns:
        计算ks的值，或根据要求返回结果数据
    """

    if method == 'sklearn':
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

        # 数据显示格式处理
        result['fpr'] = result['fpr'].apply(lambda x: round(x, precision))
        result['tpr'] = result['tpr'].apply(lambda x: round(x, precision))
        result['ks'] = result['ks'].apply(lambda x: round(abs(x), precision))
        result = result.head(qcut)
        ks = round(result['ks'].max(), precision)
    else:
        df = data.copy()
        df[col] = pd.qcut(x=df[col], q=qcut, duplicates='drop')
        total = df.groupby([col])[target].count()
        bad = df.groupby([col])[target].sum()
        result = pd.DataFrame({'#Total': total, '#Bad': bad})
        result['#Good'] = result['#Total'] - result['#Bad']
        result['Proba'] = result.index
        result.index = range(len(result))
        result = result.sort_values(by='Proba', ascending=True)
        result['%Bad'] = result['#Bad'] / result['#Bad'].sum()
        result['%Good'] = result['#Good'] / result['#Good'].sum()
        result['%Total'] = result['#Total'] / result['#Total'].sum()
        result['%BadRate'] = result['#Bad'] / result['#Total']

        result['%CumBad'] = result['#Bad'].cumsum() / result['#Bad'].sum()
        result['%CumGood'] = result['#Good'].cumsum() / result['#Good'].sum()
        result['KS'] = result['%CumGood'] - result['%CumBad']
        result.reset_index(drop=True, inplace=True)
        result['No.'] = result.index + 1
        result = result[
            ['No.', 'Proba', '#Total', '#Bad', '#Good', '%Total', '%Bad', '%Good', '%BadRate', '%CumBad', '%CumGood',
             'KS']]

        result['KS'] = result['KS'].apply(lambda x: round(abs(x), precision))
        result['%Total'] = result['%Total'].apply(lambda x: format(x, '.' + str(precision) + '%'))
        result['%Bad'] = result['%Bad'].apply(lambda x: format(x, '.' + str(precision) + '%'))
        result['%Good'] = result['%Good'].apply(lambda x: format(x, '.' + str(precision) + '%'))
        result['%BadRate'] = result['%BadRate'].apply(lambda x: format(x, '.' + str(precision) + '%'))
        result['%CumBad'] = result['%CumBad'].apply(lambda x: format(x, '.' + str(precision) + '%'))
        result['%CumGood'] = result['%CumGood'].apply(lambda x: format(x, '.' + str(precision) + '%'))
        ks = round(result['KS'].max(), precision)

    if return_data:
        return ks, result

    else:
        return ks
