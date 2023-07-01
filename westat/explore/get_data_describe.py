import numpy as np
from numpy import inf
import pandas as pd


def get_data_describe(data: pd.DataFrame,
                      data_dict: pd.DataFrame = pd.DataFrame(),
                      missing: list = [np.nan, None, 'nan','null','NULL'],
                      key: list = [],
                      precision: int = 2,
                      language: str = 'en') -> pd.DataFrame:
    """
    获取目标数据集的描述统计信息
    Args:
        data:DataFrame,需要进行描述统计分析的数据集
        data_dict:DataFrame,数据字典，包含列名（特征英文名Name）和描述(特征中文名 Label)两列的数据集
        missing:list,缺失值列表
        key:list,额外增加的统计量关键词,例如：['#Sum','#Min','#Q1','#Median','#Q3','#Max','#Mode','#Var','#Std','#Mean','#Kurt','#Skew','#StdMean','#Range','#Cv','#Sum_of_squares','Top1','Top2','Top3']
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
        elif col.lower().find('_id') > 0 or col.lower() == 'id':
            col_role = 'ID'
        else:
            col_role = 'feature'

        # 统计量计算
        col_n = len(df[df[col].notnull()])
        col_missing = len(df[df[col].isna()])
        col_unique = df[col].nunique()

        # 如果列是数值型，并且不是全为空，则计算统计量
        if col_dtype in ('int64', 'float64', 'float32') and len(df[df[col].notnull()]):
            col_sum = df[col].sum()
            col_min = df[col].min()
            col_max = df[col].max()
            col_mean = df[col].mean()
            col_median = df[col].median()
            col_mode = df[col].mode().iloc[0]
            col_std = df[col].std()
            col_var = df[col].var()
            col_sem = df[col].sem()
            col_skew = df[col].skew()
            col_kurt = df[col].kurt()
            col_q1 = df[col].quantile(0.25)
            col_q3 = df[col].quantile(0.75)
            col_range = col_max - col_min
            col_sum_of_squares = df[col].pow(2).sum()

            if col_mean != 0:
                col_cv = col_std / col_mean
            else:
                col_cv = np.nan
        else:
            col_sum = np.nan
            col_min = np.nan
            col_max = np.nan
            col_mean = np.nan
            col_median = np.nan
            col_mode = np.nan
            col_std = np.nan
            col_var = np.nan
            col_sem = np.nan
            col_skew = np.nan
            col_kurt = np.nan
            col_q1 = np.nan
            col_q3 = np.nan
            col_range = np.nan
            col_sum_of_squares = np.nan
            col_cv = np.nan

        if len(df[df[col].notnull()]) > 0:
            col_top_list = df[col].value_counts().index
            if len(col_top_list) >= 3:
                col_top3 = col_top_list[2]
                col_top2 = col_top_list[1]
                col_top1 = col_top_list[0]
            elif len(col_top_list) >= 2:
                col_top3 = np.nan
                col_top2 = col_top_list[1]
                col_top1 = col_top_list[0]
            elif len(col_top_list) >= 1:
                col_top3 = np.nan
                col_top2 = np.nan
                col_top1 = col_top_list[0]
            else:
                col_top3 = np.nan
                col_top2 = np.nan
                col_top1 = np.nan
        result.append(
            [col,  col_dtype, col_role, col_total, col_n, col_n / col_total, col_missing, col_missing / col_total,
             col_unique, col_unique / col_total, col_sum,
             col_min, col_mean, col_q1, col_median, col_q3, col_max, col_range, col_mode, col_var, col_std, col_cv,
             col_sem, col_skew, col_kurt, col_sum_of_squares, col_top1, col_top2, col_top3])
    result = pd.DataFrame(result,
                          columns=['Name', 'Type', 'Role', '#Count', '#N', '%N', '#Missing', '%Missing',
                                   '#Unique', '%Unique',
                                   '#Sum', '#Min', '#Mean', '#Q1', '#Median', '#Q3', '#Max', '#Range', '#Mode', '#Var',
                                   '#Std', '#Cv', '#StdMean', '#Skew', '#Kurt', '#Sum_of_squares', 'Top1', 'Top2',
                                   'Top3'])

    # 设置显示格式
    result['#Count'] = result['#Count'].apply(lambda x: round(x, precision))
    result['#N'] = result['#N'].apply(lambda x: round(x, precision))
    result['#Missing'] = result['#Missing'].apply(lambda x: round(x, precision))
    result['#Unique'] = result['#Unique'].apply(lambda x: round(x, precision))
    result['#Sum'] = result['#Sum'].apply(lambda x: round(x, precision))
    result['#Min'] = result['#Min'].apply(lambda x: round(x, precision))
    result['#Mean'] = result['#Mean'].apply(lambda x: round(x, precision))
    result['#Q1'] = result['#Q1'].apply(lambda x: round(x, precision))
    result['#Median'] = result['#Median'].apply(lambda x: round(x, precision))
    result['#Q3'] = result['#Q3'].apply(lambda x: round(x, precision))
    result['#Max'] = result['#Max'].apply(lambda x: round(x, precision))
    result['#Range'] = result['#Range'].apply(lambda x: round(x, precision))
    result['#Mode'] = result['#Mode'].apply(lambda x: round(x, precision))
    result['#Var'] = result['#Var'].apply(lambda x: round(x, precision))
    result['#Std'] = result['#Std'].apply(lambda x: round(x, precision))
    result['#Sum_of_squares'] = result['#Sum_of_squares'].apply(lambda x: round(x, precision))
    result['#StdMean'] = result['#StdMean'].apply(lambda x: round(x, precision))
    result['#Skew'] = result['#Skew'].apply(lambda x: round(x, precision))
    result['#Kurt'] = result['#Kurt'].apply(lambda x: round(x, precision))
    result['%N'] = result['%N'].apply(lambda x: format(x, '.' + str(precision) + '%'))
    result['%Missing'] = result['%Missing'].apply(lambda x: format(x, '.' + str(precision) + '%'))
    result['%Unique'] = result['%Unique'].apply(lambda x: format(x, '.' + str(precision) + '%'))
    result['#Cv'] = result['#Cv'].apply(lambda x: format(x, '.' + str(precision) + '%'))

    result.index.name = 'No.'
    result.reset_index(drop=True, inplace=True)

    col_list = ['Type', 'Role', '#Count', '#N', '%N', '#Missing', '%Missing', '#Unique',
                '%Unique', '#Sum', '#Min', '#Mean', '#Q1', '#Median', '#Q3', '#Max', 'Top1', 'Top2', 'Top3']

    # 如果数据字典非空，则匹配字典值作为变量描述
    if not data_dict.empty:
        data_dict.columns=['Name','Describe']
        result = result.merge(data_dict, on='Name', how='left')
        result.fillna('',inplace=True)

    if language == 'cn':
        if len(key) > 0:
            if not data_dict.empty:
                result = result[['Name', 'Describe'] + key]
            else:
                result = result[['Name'] + key]
        else:
            if not data_dict.empty:
                result = result[['Name', 'Describe'] + col_list]
            else:
                result = result[['Name'] + col_list]

        result.rename(columns={'Name': '名称', 'Describe': '描述', 'Type': '类型', 'Role': '角色', '#Count': '#数量',
                               '#Missing': '#缺失值', '%Missing': '%缺失值', '#Unique': '#唯一值', '%Unique': '%唯一值',
                               '#Sum': '#合计','#Min': '#最小值', '#Mean': '#均值', '#Median': '#中位数', '#Max': '#最大值',
                               '#Mode': '#众数','#Var': '#方差', '#Std': '#标准差','#Skew': '#偏度', '#Kurt': '#峰度',
                               '#Q1': '下四分位数', '#Q3': '上四分位数','#StdMean': '#标准误差', '#Range': '#极差',
                               '#Cv': '#变异系数','#Sum_of_squares': '#平方和'}, inplace=True)
    else:
        if len(key) > 0:
            if not data_dict.empty:
                result = result[['Name', 'Describe'] + key]
            else:
                result = result[['Name'] + key]
        else:
            if not data_dict.empty:
                result = result[['Name', 'Describe'] + col_list]
            else:
                result = result[['Name'] + col_list]

    from westat.utils import set_precision
    set_precision(precision)

    return result
