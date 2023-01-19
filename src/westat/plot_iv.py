import numpy as np
import pandas as pd
from westat.get_woe_iv import get_woe_iv


def plot_iv(data: pd.DataFrame,
            col: str,
            target: str = 'y',
            criterion: str = 'tree',
            bins: list = [],
            qcut: int = 0,
            missing: list = [np.nan, None],
            color: list = ['#1f77b4', '#d62728'],
            marker: str = 'o',
            linewidth: int = 2,
            linestyle: str = '-',
            style='default',
            figsize: tuple = (8, 5),
            return_data: bool = False,
            precision: int = 2,
            language: str = 'en'):
    """
    绘制条形图，展示data数据集中目标变量col的IV值，可用于检查IV分布是否满足单调性要求
    Args:
        data: DataFrame,目标数据集
        col: str,需要计算WoE和IV的列名
        target: str,目标变量名称，默认为'y'
        criterion: 分箱方法，默认为决策树分箱
        bins: list,手动指定的分箱列表
        qcut: int,等额分箱的分组数
        missing: list,缺失值列表
        color:list,条形图颜色名称,默认为['#1f77b4', '#d62728']
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

    result = get_woe_iv(data=data, col=col, target=target, criterion=criterion, bins=bins, qcut=qcut, missing=missing,
                        precision=precision)
    x = [str(x) for x in result['Bin']]
    iv = result['IV']
    total = result['#Total']
    total_iv = result['Total IV'].iloc[0]

    fig = plt.figure(figsize=figsize)
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.bar(x, total, align='center', color=color[0],
            label='Total =  {}'.format(round(result['#Total'].sum(), precision)))
    ax1.set_title(col)
    ax1.set_xlabel(col)
    ax1.set_ylabel('Count')

    ax2 = ax1.twinx()
    ax2.plot(x, iv, marker=marker,
             color=color[1],
             linewidth=linewidth,
             linestyle=linestyle,
             label='IV = {}'.format(round(total_iv, precision)))
    ax2.set_ylabel('IV')
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
    for a, b in zip(x, iv):
        if b < 0:
            p = b - iv.max() / 50
        else:
            p = b + iv.max() / 50

        ax2.text(a, p, b, ha='center', va='bottom', fontsize=12, color=color[1])

    # 设置绘图显示语言
    if language == 'cn':
        fig.suptitle('IV 分布', fontsize=14, fontweight='bold')
    else:
        fig.suptitle('IV Distributions', fontsize=14, fontweight='bold')

    plt.show()

    # 返回数据结果
    if return_data:
        return result
