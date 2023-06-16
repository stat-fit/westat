import numpy as np
from numpy import inf
import pandas as pd


def get_data_check(data: pd.DataFrame,
                      data_dict: pd.DataFrame = pd.DataFrame(),
                      missing: list = [np.nan, None, 'nan'],
                      precision: int = 2,
                      language: str = 'en') -> pd.DataFrame:
    """
    获取目标数据集的描述统计信息
    Args:
        data:DataFrame,需要进行描述统计分析的数据集
        data_dict:DataFrame,数据字典，包含列名（特征英文名Name）和描述(特征中文名 Label)两列的数据集
        missing:list,缺失值列表
        precision:数据精度，小数点位数，默认为2
        language:str,数据结果标题列显示语言，默认为 'en',可手动修改为'cn'

    Returns:
        描述统计结果数据集
    """
    # 获取数据描述
    df = data.copy()

    result = []
    col_total = len(df)
    for col in df.columns:
        # 数据类型
        col_dtype = str(df[col].dtype)

        # 缺失值替换
        df[col].replace(missing, [np.nan] * len(missing), inplace=True)

        # 数据角色
        if col.lower() == 'y' or col.lower() == 'target':
            col_role = 'target'
        elif col.lower().find('_id') > 0:
            col_role = 'ID'
        else:
            col_role = 'feature'

        # 统计量计算
        col_n = len(df[df[col].notnull()])
        col_missing = len(df[df[col].isna()])
        col_unique = df[col].nunique()


        result.append(
            [col, '', col_dtype, col_role, col_total, col_n, col_n / col_total, col_missing, col_missing / col_total,
             col_unique, col_unique / col_total])
    result = pd.DataFrame(result,
                          columns=['Name', 'Describe', 'Type', 'Role', '#Count', '#N', '%N', '#Missing', '%Missing',
                                   '#Unique', '%Unique'])

    # 设置显示格式
    result['#Count'] = result['#Count'].apply(lambda x: round(x, precision))
    result['#N'] = result['#N'].apply(lambda x: round(x, precision))
    result['#Missing'] = result['#Missing'].apply(lambda x: round(x, precision))
    result['#Unique'] = result['#Unique'].apply(lambda x: round(x, precision))

    result['%N'] = result['%N'].apply(lambda x: format(x, '.' + str(precision) + '%'))
    result['%Missing'] = result['%Missing'].apply(lambda x: format(x, '.' + str(precision) + '%'))
    result['%Unique'] = result['%Unique'].apply(lambda x: format(x, '.' + str(precision) + '%'))

    result.index.name = 'No.'
    result.reset_index(drop=True, inplace=True)
    if language == 'cn':
        col_list = ['Name', 'Describe', 'Type', 'Role', '#Count', '#N', '%N', '#Missing', '%Missing', '#Unique',
                    '%Unique']
        result = result[col_list]
        result.rename(columns={'Name': '名称', 'Describe': '描述', 'Type': '类型', 'Role': '角色', '#Count': '#数量',
                               '#Missing': '#缺失值','%Missing': '%缺失值', '#Unique': '#唯一值', '%Unique': '%唯一值'},
                      inplace=True)
    else:
        col_list = ['Name', 'Describe', 'Type', 'Role', '#Count', '#N', '%N', '#Missing', '%Missing', '#Unique',
                    '%Unique']
        result = result[col_list]

    if not data_dict.empty:
        result = result.merge(data_dict, on='Name', how='left')
        result['Describe'][result.iloc[:, -1].notnull()] = result.iloc[:, -1]
        result = result.iloc[:, :-1]

    return result
