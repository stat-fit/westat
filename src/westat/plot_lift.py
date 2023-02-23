import numpy as np
import pandas as pd
from assess.get_score_distribution import get_score_distribution


def plot_lift(data: pd.DataFrame,
              col='Score',
              qcut: int = 10,
              color: list = ['#1f77b4', '#d62728'],
              marker: str = 'o',
              linewidth=2,
              linestyle='-',
              style='default',
              figsize=(15, 8),
              target: str = 'y',
              return_data: bool = False,
              precision: int = 2,
              language: str = 'en'):
    """
    绘制条形图，展示data数据集中目标变量col的WoE值，可用于检查WoE分布是否满足单调性要求
    Args:
        data: DataFrame,目标数据集
        col: str,需要计算WoE和IV的列名
        qcut: int,等额分箱的分组数
        color:list,条形图颜色名称,默认为['#1f77b4', '#d62728']
        marker:折线图标记样式，默认为o，即圆点
        target: str,目标变量名称，默认为'y'
        linewidth:折线图的线宽，默认为1
        linestyle:折线图中线的类型，默认为 '-'
        style:绘图的样式风格
        figsize:图片大小，默认为(15,8)
        target:str,目标变量名称
        return_data:bool,是否返回提升度数据
        precision: int,数据精度，小数点位数，默认为2
        language: str,数据结果标题列显示语言，默认为 'en',可手动修改为'cn'

    Returns:
        matplotlib条形图结果
    """
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文字体
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    result = get_score_distribution(data=data,
                                    col=col,
                                    qcut=qcut,
                                    target=target,
                                    precision=precision)

    x = [str(x) for x in result['Score Range']]
    lift = result['Lift']
    total = result['#Total']

    fig = plt.figure(figsize=figsize)
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.bar(x, total, align='center', color=color[0],
            label='Total =  {}'.format(round(result['#Total'].sum(), precision)))
    ax1.set_title(col)
    ax1.set_xlabel(col)
    ax1.set_ylabel('Count')

    ax2 = ax1.twinx()
    ax2.plot(x, lift, marker=marker,
             color=color[1],
             linewidth=linewidth,
             linestyle=linestyle,
             label='Lift ')
    ax2.set_ylabel('Lift')
    fig.legend(loc=1)
    plt.style.use(style)

    # 设置数字标签
    for a, b in zip(x, total):
        if b < 0:
            p = b - total.max() / 50
        else:
            p = b + total.max() / 50
        ax1.text(a, p, b, ha='center', va='center', fontsize=12, color=color[0])

    # 设置数字标签
    for a, b in zip(x, lift):
        if b < 0:
            p = b - lift.max() / 50
        else:
            p = b + lift.max() / 50

        ax2.text(a, p, b, ha='center', va='bottom', fontsize=12, color=color[1])

    # 设置绘图显示语言
    if language == 'cn':
        fig.suptitle('Lift 分布', fontsize=14, fontweight='bold')
    else:
        fig.suptitle('Lift Distributions', fontsize=14, fontweight='bold')

    plt.show()

    # 返回数据结果
    if return_data:
        return result
