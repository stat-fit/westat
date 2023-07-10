import numpy as np
from numpy import inf
import pandas as pd

from .get_tree_bins import get_tree_bins


def get_woe_iv(data: pd.DataFrame,
               col: str,
               bins: list = [],
               qcut: int = 0,
               missing: list = [np.nan, None, 'nan', 'null', 'NULL'],
               max_bins: int = 5,
               target: str = 'y',
               method: str = 'optb',
               trend: str = 'auto',
               show_missing: bool = False,
               precision: int = 4,
               language: str = 'en') -> pd.DataFrame:
    """
    计算数据集中指定列的WOE和IV值
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
    if len(bins) > 0 and trend == 'auto':
        if len(missing_list) > 0 or len(data[data[col].isnull()]) > 0:
            df[col].replace(missing, [np.nan] * len(missing), inplace=True)
            df[col] = pd.cut(df[col], bins)
            df[col] = df[col].cat.add_categories('missing')
            df[col].fillna('missing', inplace=True)
        else:
            df[col] = pd.cut(df[col], bins)

    # 等频分箱
    elif qcut > 0 and trend == 'auto':
        bins = []

        if len(missing_list) > 0 or len(data[data[col].isnull()]) > 0:
            df[col].replace(missing, [np.nan] * len(missing), inplace=True)
            df[col] = pd.qcut(x=df[col], q=qcut, duplicates='drop')
            df[col] = df[col].cat.add_categories('missing')
            df[col].fillna('missing', inplace=True)
        else:
            df[col] = pd.qcut(x=df[col], q=qcut, duplicates='drop')

    # 决策树分箱
    elif method == 'tree' and trend == 'auto':
        if len(missing_list) > 0 or len(data[data[col].isnull()]) > 0:
            df[col].replace(missing, [np.nan] * len(missing), inplace=True)
            bins = get_tree_bins(data=data, col=col, target=target, max_depth=None,
                                 max_leaf_nodes=max_bins,
                                 min_samples_leaf=0.05,
                                 precision=precision)
            df[col] = pd.cut(df[col], bins)
            df[col] = df[col].cat.add_categories('missing')
            df[col].fillna('missing', inplace=True)
        else:
            bins = get_tree_bins(data=df, col=col, target=target, max_depth=None, max_leaf_nodes=max_bins,
                                 min_samples_leaf=0.05,
                                 precision=2)
            df[col] = pd.cut(df[col], bins)

    # 离散分箱
    elif method == 'discrete' and trend == 'auto':
        if len(missing_list) > 0 or len(data[data[col].isnull()]) > 0:
            df[col].replace(missing, [np.nan] * len(missing), inplace=True)
            df[col].fillna('missing', inplace=True)

    # 按照optbinning分箱
    else:
        if trend == 'asc':
            monotonic_trend = 'ascending'
        elif trend == 'desc':
            monotonic_trend = 'descending'
        else:
            monotonic_trend = trend

        if len(missing_list) > 0 or len(data[data[col].isnull()]) > 0:
            df[col].replace(missing, [np.nan] * len(missing), inplace=True)
            if str(data[col].dtype) in ('int64', 'float64', 'float32'):
                dtype = 'numerical'
            else:
                dtype = 'categorical'

            from optbinning import OptimalBinning
            optb = OptimalBinning(name=col, dtype=dtype,
                                  solver='cp',  # 算子
                                  max_n_bins=max_bins,  # 最大分箱数
                                  monotonic_trend=monotonic_trend  # 设置单调趋势
                                  )
            optb.fit(data[col], data[target])
            df[col] = pd.cut(df[col], [-inf] + list(optb.splits) + [inf])
            df[col] = df[col].cat.add_categories('missing')
            df[col].fillna('missing', inplace=True)
        else:
            if str(data[col].dtype) in ('int64', 'float64', 'float32'):
                dtype = 'numerical'
            else:
                dtype = 'categorical'

            from optbinning import OptimalBinning
            optb = OptimalBinning(name=col, dtype=dtype,
                                  solver='cp',  # 算子
                                  max_n_bins=max_bins,  # 最大分箱数
                                  monotonic_trend=monotonic_trend  # 设置单调趋势
                                  )
            optb.fit(data[col], data[target])
            df[col] = pd.cut(df[col], [-inf] + list(optb.splits) + [inf])

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
    result.sort_values(by='No.', inplace=True)
    result.reset_index(drop=True, inplace=True)

    # 添加 gini
    from .gini_impurity import gini_impurity
    gini_list = []
    for row in result.index:
        gini_list.append(gini_impurity(c=[result.loc[row, '#Bad'], result.loc[row, '#Good']], precision=4))
    result['Gini'] = gini_list

    # 添加汇总行
    total = result.iloc[:, 1:].apply(lambda x: x.sum())
    row = pd.DataFrame([''] + total.to_list()).T
    row.columns = result.columns
    result = pd.concat([result, row], ignore_index=True)

    # 设置显示格式
    result.replace([np.nan, ''], [0, 0], inplace=True)

    result['No.'] = result['No.'] + 1
    result['%Total'] = result['%Total'].apply(lambda x: format(x, '.' + str(precision) + '%'))
    result['%Bad'] = result['%Bad'].apply(lambda x: format(x, '.' + str(precision) + '%'))
    result['%Good'] = result['%Good'].apply(lambda x: format(x, '.' + str(precision) + '%'))

    result['WoE'] = result['WoE'].apply(lambda x: format(x, '.' + str(precision) + 'f'))
    result['IV'] = result['IV'].apply(lambda x: format(x, '.' + str(precision) + 'f'))


    result = result[
        ['Name', 'No.', 'Bin', '#Total', '#Bad', '#Good', '%Total', '%Bad', '%Good', '%BadRate', 'WoE', 'IV','Gini']]
    result.iat[-1, 0] = 'Total'
    result.iat[-1, 1] = ''
    result.iat[-1, 2] = ''
    result.iat[-1, 9] = result['#Bad'].sum() / result['#Total'].sum()
    result['%BadRate'] = result['%BadRate'].apply(lambda x: format(x, '.' + str(precision) + '%'))

    if language == 'cn':
        result.rename(
            columns={'Name': '名称', 'No.': '分组序号', 'Bin': '分组逻辑', '#Total': '#合计', '#Bad': '#坏',
                     '#Good': '#好', '%Total': '%合计', '%Bad': '%坏', '%Good': '%好', '%BadRate': '%坏件率',
                     'Gini': '基尼不纯度'},
            inplace=True)

    # 设置显示精度
    from westat.utils import set_precision
    set_precision(precision)

    return result


def view_woe_iv(data: pd.DataFrame,
                col: str,
                bins: list = [],
                qcut: int = 0,
                missing: list = [np.nan, None, 'nan', 'null', 'NULL'],
                max_bins: int = 5,
                target: str = 'y',
                method: str = 'optb',
                trend: str = 'auto',
                show_missing: bool = False,
                precision: int = 4,
                language: str = 'en',
                color: str = '#007bff'):
    """
    计算数据集中指定列的WOE和IV值，并以图形化的形式，对WoE进行展示
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
        show_missing:bool,是否显示缺失值分组，默认为False
        precision:数据精度，小数点位数，默认为2
        language: str,数据结果标题列显示语言，默认为 'en',可手动修改为'cn'
        color:str,显示颜色，默认为'#007bff' 蓝色

    Returns:
        结果数据集保存各分组名称和分组对应的WoE和IV值
    """
    result = get_woe_iv(data=data,
                        col=col,
                        bins=bins,
                        qcut=qcut,
                        missing=missing,
                        max_bins=max_bins,
                        target=target,
                        method=method,
                        trend=trend,
                        show_missing=show_missing,
                        precision=precision,
                        language=language)
    result['WoE.'] = result['WoE'].replace('', np.nan)
    result['WoE.'] = result['WoE.'].apply(lambda x: float(x))
    result = result.style.bar(subset=['WoE.'], color=color)
    return result
