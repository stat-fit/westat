import numpy as np
import pandas as pd
from tqdm.notebook import tqdm
from .get_woe_iv import get_woe_iv
from .get_data_iv import get_data_iv


def get_model_iv(data_discrete: pd.DataFrame,
                 data_bins: pd.DataFrame = pd.DataFrame(),
                 data_iv: pd.DataFrame = pd.DataFrame(),
                 data_types: pd.DataFrame = pd.DataFrame(),
                 data_dict: pd.DataFrame = pd.DataFrame(),
                 max_bins: int = 5,
                 target: str = 'y',
                 style: bool = False,
                 precision: int = 4,
                 language: str = 'en'):
    """
    根据给定的数据集，获取全部特征在给定分箱内的woe、iv
    Args:
        data_discrete:pd.DataFrame,已经离散化的数据集
        data_bins:pd.DataFrame,数据集所有特征的切分点
        data_iv:pd.DataFrame,数据集所有特征的iv
        data_types:pd.DataFrame,数据集所有特征的数据类型
        data_dict:pd.DataFrame,数据集所有特征的数据字典,默认为空
        max_bins:int,最大分箱数，默认分为5箱，仅决策树分箱时可用
        target:str,目标变量名称，默认为'y'
        style:bool,是否显示样式字段，默认为否
        precision:int:数据精度，小数点位数，默认为2
        language:str,数据结果标题列显示语言，默认为 'en',可手动修改为'cn'

    Returns:
        根据已经离散化的数据集，返回特征在给定数据集的woe、iv
    """
    result = pd.DataFrame()

    if data_iv.empty:
        data_iv = get_data_iv(data_discrete, method='discrete', precision=precision)

    for col in tqdm(data_discrete.columns):
        if col != target and data_iv['IV'][data_iv['Name'] == col].values[0] != 0:
            df_woe = get_woe_iv(data=data_discrete,
                                col=col,
                                method='discrete',
                                target=target,
                                max_bins=max_bins,
                                show_missing=True,
                                precision=precision)
            df_woe = df_woe.iloc[:-1, :]
            df_woe['New WoE'] = pd.to_numeric(df_woe['WoE'])
            df_woe['New IV'] = pd.to_numeric(df_woe['IV'])
            df_woe['Total IV'] = df_woe['New IV'].sum()
            result = pd.concat([result, df_woe])

    # 如果数据字典不为空，则填充字段说明，否则字段说明为空
    if not data_dict.empty:
        data_dict.columns = ['Name', 'Label']
        result_1 = result.merge(data_dict, on='Name', how='left')
    else:
        result_1 = result
        result_1['Label'] = ''

    # 合并数据类型
    if not data_types.empty:
        result_2 = result_1.merge(data_types, on='Name', how='left')
    else:
        result_2 = result_1
        result['Type'] = ' '

    # 合并数据分箱
    if not data_bins.empty:
        result = result_2.merge(data_bins, on='Name', how='left')
    else:
        result = result_2
        result['Bins'] = ' '

    result.sort_values(by=['Total IV', 'Name', 'No.'], ascending=[False, True, True], inplace=True)
    result.reset_index(drop=True, inplace=True)

    result['WoE.'] = result['New WoE']
    result['Style'] = result['Name'].apply(lambda x: list(result['Name'].unique()).index(x) % 2)
    result['Label'].fillna('', inplace=True)

    # 特征的顺序
    result['Bins No.'] = result['No.']
    result['No.'] = result['Name'].apply(lambda x: list(result['Name'].unique()).index(x) + 1)

    col_list = ['No.', 'Name', 'Label', 'Type', 'Bins No.', 'Bin', 'Bins', '#Total', '#Bad', '#Good', '%Total',
                '%Bad', '%Good', '%BadRate', 'New WoE', 'New IV', 'Total IV', 'WoE.', 'Style']

    # 语言设置
    if language == 'cn':

        if data_dict.empty:
            col_list.remove('Type')
        if data_dict.empty:
            col_list.remove('Label')
        if data_bins.empty:
            col_list.remove('Bins')
        if not style:
            col_list.remove('WoE.')
            col_list.remove('Style')

        result = result[col_list]

        result.rename(
            columns={'No.': '序号', 'Name': '名称', 'Label': '描述', 'Type': '类型', 'Bins No.': '分箱序号',
                     'Bin': '分箱', 'Bins': '切分点', '#Total': '#合计', '#Bad': '#坏', '#Good': '好',
                     '%Total': '%合计', '%Bad': '%坏', '%Good': '%好', 'New WoE': 'WoE', 'New IV': 'IV',
                     '%BadRate': '%坏件率', 'Total IV': 'IV合计', 'Style': '样式'}, inplace=True)
    else:
        if data_types.empty:
            col_list.remove('Type')
        if data_dict.empty:
            col_list.remove('Label')
        if data_bins.empty:
            col_list.remove('Bins')
        if not style:
            col_list.remove('WoE.')
            col_list.remove('Style')

        result = result[col_list]
        result.rename(
            columns={'New WoE': 'WoE', 'New IV': 'IV'}, inplace=True)
    return result


def view_model_iv(data_discrete: pd.DataFrame,
                  data_bins: pd.DataFrame = pd.DataFrame(),
                  data_iv: pd.DataFrame = pd.DataFrame(),
                  data_types: pd.DataFrame = pd.DataFrame(),
                  data_dict: pd.DataFrame = pd.DataFrame(),
                  max_bins: int = 5,
                  target: str = 'y',
                  style: bool = False,
                  precision: int = 4,
                  language: str = 'en',
                  color: str = '#007bff'):
    """
    根据给定的数据集，获取全部特征在给定分箱内的woe、iv
    Args:
        data_discrete:pd.DataFrame,已经离散化的数据集
        data_bins:pd.DataFrame,数据集所有特征的切分点
        data_iv:pd.DataFrame,数据集所有特征的iv
        data_types:pd.DataFrame,数据集所有特征的数据类型
        data_dict:pd.DataFrame,数据集所有特征的数据字典,默认为空
        max_bins:int,最大分箱数，默认分为5箱，仅决策树分箱时可用
        target:str,目标变量名称，默认为'y'
        style:bool,是否显示样式字段，默认为否
        precision:int:数据精度，小数点位数，默认为2
        language:str,数据结果标题列显示语言，默认为 'en',可手动修改为'cn'
        color:str,显示颜色，默认为'#007bff' 蓝色

    Returns:
        根据已经离散化的数据集，返回特征在给定数据集的woe、iv
    """
    result = get_model_iv(data_discrete=data_discrete,
                          data_bins=data_bins,
                          data_iv=data_iv,
                          data_types=data_types,
                          data_dict=data_dict,
                          max_bins=max_bins,
                          target=target,
                          style=style,
                          precision=precision,
                          language=language)
    result['WoE.'] = result['WoE'].replace('', np.nan)
    result['WoE.'] = result['WoE.'].apply(lambda x: float(x))
    result = result.style.bar(subset=['WoE.'], color=color)
    return result
