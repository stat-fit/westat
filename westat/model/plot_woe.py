import numpy as np
import pandas as pd
from .get_woe_iv import get_woe_iv


def plot_woe(data: pd.DataFrame,
             col: str,
             target: str = 'y',
             method: str = 'tree',
             bins: list = [],
             qcut: int = 0,
             missing: list = [np.nan, None, 'nan'],
             color: list = ['#1f77b4', '#ff800b', '#d62728', '#333333'],
             marker: str = 'o',
             linewidth=2,
             linestyle='-',
             style='default',
             figsize: tuple = (8, 5),
             return_data: bool = False,
             precision: int = 4,
             language: str = 'en'):
    """
    绘制条形图，展示data数据集中目标变量col的WoE值，可用于检查WoE分布是否满足单调性要求
    Args:
        data: DataFrame,目标数据集
        col: str,需要计算WoE和IV的列名
        target: str,目标变量名称，默认为'y'
        method: 分箱方法，默认为决策树分箱
        bins: list,手动指定的分箱列表
        qcut: int,等额分箱的分组数
        missing: list,缺失值列表
        color:list,条形图颜色名称,默认为['#1f77b4', '#ff800b', '#d62728', '#333333'],
        marker:折线图标记样式，默认为o，即圆点
        linewidth:折线图的线宽，默认为1
        linestyle:折线图中线的类型，默认为 '-'
        style:绘图的样式风格
        figsize:图片大小，默认为(8,5)
        return_data:bool,是否返回IV计算结果数据
        precision: int,数据精度，小数点位数，默认为2
        language: str,数据结果标题列显示语言，默认为 'en',可手动修改为'cn'

    Returns:
        matplotlib条形图结果
    """
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文字体
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    result = get_woe_iv(data=data,
                        col=col,
                        target=target,
                        method=method,
                        bins=bins,
                        qcut=qcut,
                        missing=missing,
                        precision=precision)
    x = [str(x) for x in result['Bin']]
    result['WoE'] = pd.to_numeric(result['WoE'])
    woe = result['WoE']
    good = result['#Good']
    bad = result['#Bad']
    total_woe = result['WoE'].sum()

    fig = plt.figure(figsize=figsize)
    ax1 = fig.add_subplot(1, 1, 1)

    ax1.bar(x, good, bottom=0, align='center', color=color[0],
            label='Good =  {}'.format(round(result['#Good'].sum(), precision)))

    ax1.bar(x, bad, bottom=good, align='center', color=color[1],
            label='Bad =  {}'.format(round(result['#Bad'].sum(), precision)))

    ax1.set_title(col)
    ax1.set_xlabel(col)
    ax1.set_ylabel('Count')

    ax2 = ax1.twinx()
    ax2.plot(x, woe, marker=marker,
             color=color[2],
             linewidth=linewidth,
             linestyle=linestyle,
             label='WoE = {}'.format(round(total_woe, precision)))
    ax2.set_ylabel('WoE')
    fig.legend(loc=1)
    plt.style.use(style)

    # 设置好坏客户数字标签
    for a, b, c in zip(x, good, bad):
        ax1.text(a, b / 2, b, ha='center', va='center', fontsize=12, color=color[3])
        ax1.text(a, b + c / 2, c, ha='center', va='center', fontsize=12, color=color[3])

    # 设置woe数字标签
    for a, b in zip(x, woe):
        if b < 0:
            p = b - woe.max() / 50
        else:
            p = b + woe.max() / 50

        ax2.text(a, p, b, ha='center', va='bottom', fontsize=12, color=color[2])

    # 设置绘图显示语言
    if language == 'cn':
        fig.suptitle('WoE 分布', fontsize=14, fontweight='bold')
    else:
        fig.suptitle('WoE Distributions', fontsize=14, fontweight='bold')

    plt.show()

    # 返回数据结果
    if return_data:
        return result
