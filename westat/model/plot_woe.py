import numpy as np
import pandas as pd
from .get_woe_iv import get_woe_iv


def plot_woe(data: pd.DataFrame,
             col: str,
             bins: list = [],
             qcut: int = 0,
             missing: list = [np.nan, None, 'nan', 'null', 'NULL'],
             max_bins: int = 5,
             target: str = 'y',
             method: str = 'optb',
             trend: str = 'auto',
             precision: int = 2,
             language: str = 'en',
             color: list = ['#1F77B4', '#FF800B', '#808080', '#C0504D', '#333333'],
             theme: int = None,
             marker: str = 'o',
             linewidth=2,
             linestyle='-',
             style='default',
             figsize: tuple = (8, 5),
             return_data: bool = False):
    """
    绘制条形图，展示data数据集中目标变量col的WoE值，可用于检查WoE分布是否满足单调性要求
    Args:
        data: DataFrame,目标数据集
        col: str,需要计算WoE和IV的列名
        bins: list,手动指定的分箱列表
        qcut: int,等额分箱的分组数
        missing: list,缺失值列表
        max_bins:int,最大分箱数，默认分为5箱，仅决策树分箱时可用
        target: str,目标变量名称，默认为'y'
        method: str,分箱方法，
            默认为'tree'表示使用决策树分箱
            当取值为 'discrete'时，表示数据集已经离散化，直接计算WoE和IV
            当取值为 'optb'时，表示使用OptimalBinning进行分箱，此时启用trend参数设置分箱单调性
        trend:str,设置分箱单调趋势，一般使用的有：ascending，descending，auto_asc_desc，peak，valley
            ascending：单调递增；
            descending：单调递减
            auto_asc_desc：自动增减：
            peak：先增后减
            valley：先减后增
        precision:数据精度，小数点位数，默认为2
        language: str,数据结果标题列显示语言，默认为 'en',可手动修改为'cn'
        color:list,条形图颜色名称,默认为['#1F77B4', '#FF800B', '#808080', '#C0504D', '#333333'],
        theme:int,绘图的颜色主题，取值为1，2，3，4，默认为空
        marker:折线图标记样式，默认为o，即圆点
        linewidth:折线图的线宽，默认为1
        linestyle:折线图中线的类型，默认为 '-'
        style:绘图的样式风格
        figsize:图片大小，默认为(8,5)
        return_data:bool,是否返回IV计算结果数据

    Returns:
        matplotlib条形图结果
    """
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文字体
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    if theme == 1:
        # good bad woe badrate text
        color = ['#326D62', '#CDCDCD', '#F79646', '#C0504D', '#333333']
    elif theme == 2:
        color = ['#326D62', '#C0504D', '#FFC700', '#808080', '#333333']
    elif theme == 3:
        color = ['#4BACC6', '#CDCDCD', '#F79646', '#C0504D', '#333333']
    elif theme == 4:
        color = ['#1F77B4', '#FF800B', '#808080', '#C0504D', '#333333']

    woe_result = get_woe_iv(data=data,
                            col=col,
                            bins=bins,
                            qcut=qcut,
                            missing=missing,
                            max_bins=max_bins,
                            target=target,
                            method=method,
                            trend=trend,
                            precision=precision,
                            language=language)
    result = woe_result.iloc[:-1, :]
    x = [str(x) for x in result['Bin']]
    woe = pd.to_numeric(result['WoE'])
    badrate = pd.to_numeric(result['%BadRate'].apply(lambda x: (x[:-1]))) / 100
    total_badrate = pd.to_numeric((woe_result['%BadRate'].iloc[-1])[:-1]) / 100
    good = result['#Good']
    bad = result['#Bad']
    total_woe = woe.sum()

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
    ax2.plot(x, badrate, marker=marker,
             color=color[3],
             linewidth=linewidth,
             linestyle=linestyle,
             label='BadRate = ' + format(total_badrate, '.' + str(precision) + '%'))
    ax2.set_ylabel('WoE')
    fig.legend(loc=1)
    plt.style.use(style)

    # 设置好坏客户数字标签
    for a, b, c in zip(x, good, bad):
        ax1.text(a, b / 2, b, ha='center', va='center', fontsize=12, color=color[4])
        ax1.text(a, b + c / 2, c, ha='center', va='center', fontsize=12, color=color[4])

    # 设置woe数字标签
    for a, b in zip(x, woe):
        if b < 0:
            p = b - woe.max() / 50
        else:
            p = b + woe.max() / 50

        ax2.text(a, p, b, ha='center', va='bottom', fontsize=12, color=color[2])

    # 设置badrate数字标签
    for a, b in zip(x, badrate):
        if b < 0:
            p = b - badrate.max() / 50
        else:
            p = b + badrate.max() / 50

        ax2.text(a, p, format(b, '.' + str(precision) + '%'), ha='center', va='bottom', fontsize=12, color=color[3])

    # 设置绘图显示语言
    if language == 'cn':
        fig.suptitle('WoE 分布', fontsize=14, fontweight='bold')
    else:
        fig.suptitle('WoE Distributions', fontsize=14, fontweight='bold')

    plt.show()

    # 返回数据结果
    if return_data:
        return woe_result
