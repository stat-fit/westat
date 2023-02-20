import pandas as pd
from westat import tqdm
from westat.get_woe_iv import get_woe_iv


def get_model_iv(data_discrete: pd.DataFrame,
                 col_iv: pd.DataFrame,
                 col_bins: pd.DataFrame,
                 col_types: pd.DataFrame,
                 col_dict: pd.DataFrame = pd.DataFrame(),
                 target: str = 'y',
                 precision: int = 2,
                 language: str = 'en'):
    """
    根据给定的数据集，获取全部特征在给定分箱内的woe、iv
    Args:
        data_discrete:pd.DataFrame,已经离散化的数据集
        col_iv:pd.DataFrame,数据集所有特征的iv
        col_bins:pd.DataFrame,数据集所有特征的切分点
        col_types:pd.DataFrame,数据集所有特征的数据类型
        col_dict:pd.DataFrame,数据集所有特征的数据字典,默认为空
        target:str,目标变量名称，默认为'y'
        precision:int:数据精度，小数点位数，默认为2
        language:str,数据结果标题列显示语言，默认为 'en',可手动修改为'cn'

    Returns:
        根据已经离散化的数据集，返回特征在给定数据集的woe、iv
    """
    result = pd.DataFrame()
    for col in tqdm(data_discrete.columns):
        if col != target and col_iv['IV'][col_iv['Name'] == col].values[0] != 0:
            df_woe = get_woe_iv(data=data_discrete,
                                col=col,
                                method='discrete',
                                target=target,
                                show_missing=True,
                                precision=precision)
            result = pd.concat([result, df_woe])

    # 如果数据字典不为空，则填充字段说明，否则字段说明为空
    if col_dict.empty:
        result_1 = result
        result_1['Label'] = ''
    else:
        result_1 = result.merge(col_dict, on='Name', how='left')
        result_1['Label'] = result_1.iloc[:, -1]

    # 合并数据类型
    result_2 = result_1.merge(col_types, on='Name', how='left')

    # 合并数据分箱
    result = result_2.merge(col_bins, on='Name', how='left')
    result.sort_values(by=['Total IV', 'Name', 'No.'], ascending=[False, True, True], inplace=True)
    result.reset_index(drop=True, inplace=True)

    result['WoE.'] = result['WoE']
    result['Style'] = result['Name'].apply(lambda x: list(result['Name'].unique()).index(x) % 2)
    result['Label'].fillna('', inplace=True)

    # 特征的顺序
    result['Bins No.'] = result['No.']
    result['No.'] = result['Name'].apply(lambda x: list(result['Name'].unique()).index(x) + 1)

    # 语言设置
    if language == 'cn':
        result = result[['No.', 'Name', 'Label', 'Type', 'Bins No.', 'Bin', 'Bins', '#Total', '#Bad', '#Good', '%Total',
                         '%Bad', '%Good', '%BadRate', 'WoE', 'IV', 'Total IV', 'WoE.', 'Style']]
        result.rename(
            columns={'No.': '序号', 'Name': '名称', 'Label': '描述', 'Type': '类型', 'Bins No.': '分箱序号',
                     'Bin': '分箱', 'Bins': '切分点', '#Total': '#合计', '#Bad': '#坏', '#Good': '好',
                     '%Total': '%合计', '%Bad': '%坏', '%Good': '%好',
                     '%BadRate': '%坏件率', 'Total IV': 'IV合计', 'Style': '样式'}, inplace=True)
    else:
        result = result[['No.', 'Name', 'Label', 'Type', 'Bins No.', 'Bin', 'Bins', '#Total', '#Bad', '#Good', '%Total',
                         '%Bad', '%Good', '%BadRate', 'WoE', 'IV', 'Total IV', 'WoE.', 'Style']]
    return result
