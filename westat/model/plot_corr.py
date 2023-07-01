import pandas as pd


def plot_corr(data: pd.DataFrame,
              data_dict: pd.DataFrame = pd.DataFrame(),
              rotation: list = [0, 0],
              figsize: tuple = (10, 6)):
    """
    绘制目标数据集中指定特征的相关性表
    Args:
        data: 目标数据集
        data_dict: 特征的数据字典，包含Name,Label两列
        rotation:list,x和y坐标轴文字方向,默认为[0,0] 即x轴文字和y轴文字均为水平
        figsize:tuple,图片大小
    Returns:
        返回相关性图表
    """
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文字体
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    import seaborn as sns
    if data_dict.empty:
        corr = data.corr()  # 计算各变量的相关性系数
    else:
        result = data.copy()
        for col in result.columns:
            if col in data_dict['Name'].to_list():
                label = data_dict[data_dict['Name'] == col].iat[0, -1]
                result.rename(columns={col: label}, inplace=True)

        corr = result.corr()  # 计算各变量的相关性系数

    fig = plt.figure(figsize=figsize)
    ax = sns.heatmap(corr, annot=True, cbar=True)
    ax.set_xticklabels(corr.columns, rotation=rotation[0])
    ax.set_yticklabels(corr.columns, rotation=rotation[1])
    plt.show()
