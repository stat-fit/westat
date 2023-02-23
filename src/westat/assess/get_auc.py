import numpy as np
import pandas as pd


def get_auc(data: pd.DataFrame,
            col: str = 'Proba',
            target: str = 'y',
            return_data: bool = False,
            precision: int = 2):
    """
    根据评分卡内容，对目标数据集的评分结果计算auc
    Args:
        data:pd.DataFrame,目标数据集
        col:str，正例的概率估计字段名
        target:tr,目标变量名称，默认为'y'
        return_data:是否返回结果数据
        precision:int,数据精度，小数点位数，默认为2

    Returns:
        计算roc_auc的值，或根据要求返回结果数据
    """
    from sklearn.metrics import roc_curve, auc

    fpr, tpr, thresholds = roc_curve(data[target], data[col], drop_intermediate=False)
    result = pd.DataFrame([fpr, tpr, thresholds]).T
    result.columns = ['fpr', 'tpr', 'thresholds']

    auc = round(auc(fpr, tpr), precision)
    if return_data:
        return auc, result
    else:
        return auc
