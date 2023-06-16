import numpy as np
import pandas as pd


def plot_col(data: pd.DataFrame,
             col: str = 'y',
             missing: list = [np.nan, None, 'nan'],
             color: list = ['#1f77b4', '#ff800b', '#d62728', '#333333'],
             marker: str = 'o',
             linewidth: int = 2,
             linestyle: str = '-',
             style='default',
             figsize: tuple = (8, 5),
             return_data: bool = False,
             precision: int = 2,
             language='en'):
    """
    绘图展示指定列在数据集中的分布情况，例如每个取值的数量、占比
    Args:
        data: DataFrame,需要检查数据分布的数据集
        col: str,需要检查的列名
        missing: list,缺失值列表
        color: 条形图颜色名称,默认为['#1f77b4', '#ff800b', '#d62728', '#333333'],
        marker: 折线图标记样式，默认为o，即圆点
        linewidth: 折线图的线宽，默认为1
        linestyle: 折线图中线的类型，默认为 '-'
        style: 绘图的样式风格
        figsize: 图片大小，默认为(8,5)
        return_data: bool,是否返回计算结果数据
        precision: int,数据精度，小数点位数，默认为2
        language: str,数据结果标题列显示语言，默认为 'en',可手动修改为'cn'

    Returns:
        绘图展示指定列在数据集中的分布情况
    """
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文字体
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    data[col].replace(missing, len(missing) * np.nan, inplace=True)
    result = pd.DataFrame(data[col].value_counts())
    result.columns = ['count']
    result = result.sort_values(by=['count'], ascending=[False])
    result['Name'] = col
    result['Value'] = result.index
    result['#Count'] = result['count']
    result['ratio'] = result['count'] / len(data[col])
    result['%Ratio'] = result['ratio'].apply(lambda x: format(x, '.' + str(precision) + '%'))
    result.reset_index(drop=True, inplace=True)
    result['No.'] = result.index + 1

    x = result['Value']
    y = result['count']
    z = result['ratio']

    fig = plt.figure(figsize=figsize)
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.bar(x, y, bottom=0, align='center', color=color, label='Count')

    # 设置计数标签
    for a, b, c in zip(x, y, y):
        ax1.text(a, b / 2, b, ha='center', va='center', fontsize=12, color=color[3])

    ax1.set_title(col)
    ax1.set_xticks(x, result.index)
    ax1.set_xlabel(col)
    ax1.set_ylabel('Count')

    ax2 = ax1.twinx()
    ax2.plot(x, z, marker=marker,
             color=color[2],
             linewidth=linewidth,
             linestyle=linestyle,
             label='Ratio')
    ax2.set_ylabel('Ratio')

    # 设置比例标签
    for a, b in zip(x, z):
        if b < 0:
            p = b - z.max() / 100
        elif b == z.max():
            p = b - z.max() / 100
        else:
            p = b + z.max() / 100

        ax2.text(a + 0.1, p, format(b, '.2%'), ha='center', va='bottom', fontsize=12, color=color[2])

    fig.legend(loc=1)
    plt.show()

    # 标题栏语言设置
    if language == 'cn':
        result = result[['No.', 'Name', 'Value', '#Count', '%Ratio']]

        result.rename(columns={'No.': '序号', 'Name': '名称', 'Value': '值', '#Count': '#数量', '%Ratio': '%占比'},
                      inplace=True)
    else:
        result = result[['No.', 'Name', 'Value', '#Count', '%Ratio']]

    # 返回数据结果
    if return_data:
        return result
