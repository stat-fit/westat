import numpy as np
from numpy import inf
import pandas as pd

from westat.get_tree_bins import get_tree_bins


def get_woe_iv(data: pd.DataFrame,
               col: str,
               method: str = 'tree',
               bins: list = [],
               qcut: int = 0,
               missing: list = [np.nan, None, 'nan'],
               target: str = 'y',
               show_missing: bool = False,
               precision: int = 2,
               language: str = 'en') -> pd.DataFrame:
    """
    计算数据集中指定列的WOE和IV值
    Args:
        data: DataFrame,目标数据集
        col: str,需要计算WoE和IV的列名
        method: str,分箱方法，默认为'tree'表示使用决策树分箱,当取值为 'discrete'时，表示数据集已经离散化，直接计算WoE和IV
        bins: list,手动指定的分箱列表
        qcut: int,等额分箱的分组数
        missing: list,缺失值列表
        target: str,目标变量名称，默认为'y'
        show_missing:bool,是否显示缺失值分组，默认为False
        precision:数据精度，小数点位数，默认为2
        language: str,数据结果标题列显示语言，默认为 'en',可手动修改为'cn'

    Returns:
        结果数据集保存各分组名称和分组对应的WoE和IV值
    """
    df = data.copy()

    # 检查数据集中是否存在预定义的缺失值
    missing_list = []
    for m in missing:
        if m in data[col]:
            missing_list.append(m)

    # 自定义分箱
    if len(bins) > 0:
        if len(missing_list) > 0 or len(data[data[col].isnull()]) > 0:
            df[col].replace(missing, [np.nan] * len(missing), inplace=True)
            df[col] = pd.cut(df[col], bins)
            df[col] = df[col].cat.add_categories('missing')
            df[col].fillna('missing', inplace=True)
        else:
            df[col] = pd.cut(df[col], bins)

    # 等频分箱
    elif qcut > 0:
        bins = []

        if len(missing_list) > 0 or len(data[data[col].isnull()]) > 0:
            df[col].replace(missing, [np.nan] * len(missing), inplace=True)
            df[col] = pd.qcut(x=df[col], q=qcut, duplicates='drop')
            df[col] = df[col].cat.add_categories('missing')
            df[col].fillna('missing', inplace=True)
        else:
            df[col] = pd.qcut(x=df[col], q=qcut, duplicates='drop')

    # 决策树分箱
    elif method == 'tree':
        if len(missing_list) > 0 or len(data[data[col].isnull()]) > 0:
            df[col].replace(missing, [np.nan] * len(missing), inplace=True)
            bins = get_tree_bins(data=data, col=col, target=target, max_depth=None, max_leaf_nodes=4,
                                 min_samples_leaf=0.05,
                                 precision=precision)
            df[col] = pd.cut(df[col], bins)
            df[col] = df[col].cat.add_categories('missing')
            df[col].fillna('missing', inplace=True)
        else:
            bins = get_tree_bins(data=df, col=col, target=target, max_depth=None, max_leaf_nodes=4,
                                 min_samples_leaf=0.05,
                                 precision=2)
            df[col] = pd.cut(df[col], bins)

    # 离散分箱
    elif method == 'discrete':
        if len(missing_list) > 0 or len(data[data[col].isnull()]) > 0:
            df[col].replace(missing, [np.nan] * len(missing), inplace=True)
            df[col].fillna('missing', inplace=True)

    result = df.groupby(col)[target].agg([('#Bad', lambda target: (target == 1).sum()),
                                          ('#Good', lambda target: (target == 0).sum()),
                                          ('#Total', 'count')]).reset_index()

    if show_missing:
        if 'missing' not in list(result[col]):
            df_default = pd.DataFrame({col: 'missing', '#Bad': 0, '#Good': 0, '#Total': 0}, index=range(1))
            result = pd.concat([result, df_default])

    result['Name'] = col
    result['%Bad'] = result['#Bad'] / result['#Bad'].sum()
    result['%Good'] = result['#Good'] / result['#Good'].sum()
    result['%Total'] = result['#Total'] / result['#Total'].sum()
    result['%BadRate'] = result['#Bad'] / result['#Total']
    result['WoE'] = np.log(result['%Bad'] / result['%Good'])
    result['IV'] = (result['%Bad'] - result['%Good']) * result['WoE']
    result.replace([-inf, inf], [0, 0], inplace=True)
    result['Total IV'] = result['IV'].sum()
    result = result.rename(columns={col: 'Bin'})

    bins = result['Bin'].unique()

    for i in range(len(bins)):
        for j in range(len(bins)):
            if ',' in ''.join(map(str, bins)):
                m = float(str(bins[i]).split(',')[0].replace('(', '').replace('-inf', '-99999999998').replace('missing',
                                                                                                              '-99999999999').replace(
                    '+', ''))
                n = float(str(bins[j]).split(',')[0].replace('(', '').replace('-inf', '-99999999998').replace('missing',
                                                                                                              '-99999999999').replace(
                    '+', ''))
                if m < n:
                    bins[i], bins[j] = bins[j], bins[i]
            else:
                if str(bins[i]).replace('missing', '-99999999999') < str(bins[j]).replace('missing', '-99999999999'):
                    bins[i], bins[j] = bins[j], bins[i]

    df = pd.DataFrame({'Bin': bins, 'No.': range(len(bins))})
    result = result.merge(df, how='left', on='Bin')
    result.replace([np.nan, ''], [0, 0], inplace=True)

    # 设置显示格式
    result['No.'] = result['No.'] + 1
    result['%Total'] = result['%Total'].apply(lambda x: format(x, '.' + str(precision) + '%'))
    result['%Bad'] = result['%Bad'].apply(lambda x: format(x, '.' + str(precision) + '%'))
    result['%Good'] = result['%Good'].apply(lambda x: format(x, '.' + str(precision) + '%'))
    result['%BadRate'] = result['%BadRate'].apply(lambda x: format(x, '.' + str(precision) + '%'))
    result['WoE'] = result['WoE'].apply(lambda x: round(x, precision))
    result['IV'] = result['IV'].apply(lambda x: round(x, precision))
    result['Total IV'] = result['Total IV'].apply(lambda x: round(x, precision))

    result.sort_values(by='No.', inplace=True)
    result.reset_index(drop=True, inplace=True)

    if language == 'cn':
        result = result[
            ['Name', 'No.', 'Bin', '#Total', '#Bad', '#Good', '%Total', '%Bad', '%Good', '%BadRate', 'WoE', 'IV',
             'Total IV']]
        result.rename(
            columns={'Name': '名称', 'No.': '分组序号', 'Bin': '分组逻辑', '#Total': '#合计', '#Bad': '#坏',
                     '#Good': '#好',
                     '%Total': '%合计', '%Bad': '%坏', '%Good': '%好', '%BadRate': '%坏件率', 'Total IV': 'IV合计'},
            inplace=True)

    else:
        result = result[
            ['Name', 'No.', 'Bin', '#Total', '#Bad', '#Good', '%Total', '%Bad', '%Good', '%BadRate', 'WoE', 'IV',
             'Total IV']]

    return result


def view_woe_iv(data,
                col: str,
                method: str = 'tree',
                bins: list = [],
                qcut: int = 0,
                missing: list = [np.nan, None, 'nan'],
                target: str = 'y',
                color: str = '#007bff',
                precision: int = 2,
                language: str = 'en'):
    """
    计算数据集中指定列的WOE和IV值，并以图形化的形式，对WoE进行展示
    Args:
        data: DataFrame,目标数据集
        col: str,需要计算WoE和IV的列名
        target: str,目标变量名称，默认为'y'
        method: 分箱方法，默认为决策树分箱
        bins: list,手动指定的分箱列表
        qcut: int,等额分箱的分组数
        missing: list,缺失值列表
        color:str,显示颜色
        precision:数据精度，小数点位数，默认为2
        language: str,数据结果标题列显示语言，默认为 'en',可手动修改为'cn'

    Returns:
        结果数据集保存各分组名称和分组对应的WoE和IV值
    """
    result = get_woe_iv(data=data,
                        col=col,
                        method=method,
                        bins=bins,
                        qcut=qcut,
                        missing=missing,
                        target=target,
                        precision=precision,
                        language=language)
    result['WoE.'] = result['WoE'].replace('', np.nan)
    result['WoE.'] = result['WoE.'].apply(lambda x: float(x))
    result = result.style.bar(subset=['WoE.'], color=color)
    return result
