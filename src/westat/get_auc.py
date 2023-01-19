import numpy as np
import pandas as pd
from westat.get_predict_score import get_predict_score


def get_auc(data: pd.DataFrame,
            score_card: pd.DataFrame,
            init_score: int = 600,
            pdo: int = 20,
            target: str = 'y',
            return_data: bool = False,
            precision: int = 2):
    """
    根据评分卡内容，对目标数据集的评分结果计算auc
    Args:
        data:pd.DataFrame,目标数据集
        score_card:pd.DataFrame，评分卡规则表
        init_score:int,初始模型分,默认为600
        pdo:int,坏件率每上升一倍，增加的分数，默认为20
        target:tr,目标变量名称，默认为'y'
        return_data:是否返回结果数据
        precision:int,数据精度，小数点位数，默认为2

    Returns:
        计算roc_auc的值，或根据要求返回结果数据
    """
    from sklearn.metrics import roc_curve, auc

    data_score_proba = get_predict_score(data, score_card, init_score=init_score, pdo=pdo, target=target,
                                         precision=precision)
    fpr, tpr, thresholds = roc_curve(data['y'], data_score_proba['Proba'], drop_intermediate=False)
    result = pd.DataFrame([fpr, tpr, thresholds]).T
    result.columns = ['fpr', 'tpr', 'thresholds']

    auc = round(auc(tpr, tpr), precision)
    if return_data:
        return auc, result
    else:
        return auc
