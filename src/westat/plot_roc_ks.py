import numpy as np
import pandas as pd
from .model.get_predict_score import get_predict_score


def plot_roc_ks(data: pd.DataFrame,
                score_card: pd.DataFrame,
                init_score: int = 600,
                pdo: int = 20,
                odds: float = 0,
                target: str = 'y',
                return_data: bool = False,
                precision: int = 2):
    """
    根据评分卡内容，对目标数据集的评分结果计算auc 和ks,并绘图
    Args:
        data:pd.DataFrame,目标数据集
        score_card:pd.DataFrame，评分卡规则表
        init_score:int,初始模型分,默认为600
        pdo:int,坏件率每上升一倍，增加的分数，默认为20
        odds:float,坏样本 / 好样本比例
        target:tr,目标变量名称，默认为'y'
        return_data:是否返回结果数据
        precision:int,数据精度，小数点位数，默认为2

    Returns:
        绘图auc和ks，或根据要求返回结果数据
    """
    from sklearn.metrics import roc_curve, auc
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文字体
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    data_score_proba = get_predict_score(data,
                                         score_card,
                                         init_score=init_score,
                                         pdo=pdo,
                                         odds=odds,
                                         target=target,
                                         precision=precision)

    fpr, tpr, thresholds = roc_curve(data['y'], data_score_proba['Proba'], drop_intermediate=False)
    roc_auc = auc(fpr, tpr)
    plt.figure(figsize=(20, 10))

    # ROC曲线
    plt.subplot(121)
    plt.title('ROC-AUC')
    plt.plot(fpr, tpr, 'b', label='AUC = ' + str(round(roc_auc, precision)))
    plt.legend(loc='upper left', fontsize=16)
    plt.plot([0, 1], [0, 1], 'r--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    plt.xlabel('False positive rate', fontsize=20)
    plt.ylabel('True positive rate', fontsize=20)

    # KS曲线
    plt.subplot(122)
    pre = sorted(data_score_proba['Proba'], reverse=True)
    num = [i * int(len(pre) / 10) for i in range(10)]
    num = num + [(len(pre) - 1)]
    ks_thresholds = [max(thresholds[thresholds <= pre[i]]) for i in num]
    data_ks = pd.DataFrame([fpr, tpr, thresholds, tpr - fpr]).T
    data_ks.columns = ['fpr', 'tpr', 'thresholds', 'ks']
    data_ks = pd.merge(data_ks, pd.DataFrame(ks_thresholds, columns=['thresholds']), on='thresholds', how='inner')
    data_ks.reset_index(drop=True, inplace=True)
    data_ks['No.'] = data_ks.index + 1
    data_ks = data_ks[['No.', 'fpr', 'tpr', 'thresholds', 'ks']]

    ks = round(max(data_ks['ks']), precision)
    plt.title('KS')
    plt.plot(data_ks.index, data_ks['tpr'])
    plt.plot(data_ks.index, data_ks['fpr'])
    plt.plot(data_ks.index, data_ks['tpr'] - data_ks['fpr'], label='K-S = ' + str(round(ks, precision)))

    # 设置数字标签
    a = data_ks['No.'][data_ks['ks'] == data_ks['ks'].max()].iloc[0] - 1
    plt.plot([a, a], [0, ks], 'o--', color='red')

    plt.text(a, ks + 0.02, ks, ha='center', va='bottom', fontsize=12)
    plt.legend(loc='upper left', fontsize=16)
    plt.xlim([0, 10])
    plt.ylim([0.0, 1.0])
    plt.xlabel('% of Population', fontsize=20)
    plt.ylabel('% of total good / %Bad', fontsize=20)
    plt.show()
    if return_data:
        return data_ks
