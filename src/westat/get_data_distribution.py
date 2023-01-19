import pandas as pd


def get_data_distribution(data: pd.DataFrame,
                          col='y',
                          by=['#Count', 'Name'],
                          ascending=[True, False],
                          total=True,
                          display=False,
                          precision=2,
                          language='en') -> pd.DataFrame:
    """
    查看数据集data中col列的数据分布情况
    Args:
        data:DataFrame,需要检查数据分布的数据集
        by:list,根据指定列进行排序，默认根据数量（降序）、名称（升序）排序
        ascending:list,指定列对应的排序列表
        total:bool,是否显示合计信息
        col:需要检查数据分布的列，默认为'y'
        display:bool,是否显示详细信息
        precision:数据精度，默认为2位小数
        language:显示语言，en：显示为英文，cn：显示为中文
    Returns:
        返回包含数据量、数据占比的数据集
    """
    df_ratio = pd.DataFrame(data=data[col].value_counts())
    df_ratio['%Ratio'] = df_ratio[col] / len(data)
    df_ratio['Value'] = df_ratio.index
    df_ratio['Name'] = col
    df_ratio = df_ratio.rename(columns={col: '#Count'})
    df_ratio = df_ratio[['Name', 'Value', '#Count', '%Ratio']]

    # 排序
    df_ratio.sort_values(by=by, ascending=ascending, inplace=True)

    # 拼接汇总结果
    df_ratio = pd.concat(
        [df_ratio, pd.DataFrame({'Name': '', 'Value': '', '#Count': df_ratio['#Count'].sum(), '%Ratio': 1}, index=[0])])
    df_ratio.reset_index(drop=True, inplace=True)
    df_ratio['No.'] = df_ratio.index + 1

    # 数据精度设置
    df_ratio['%Ratio'] = df_ratio['%Ratio'].apply(lambda x: format(x, '.' + str(precision) + '%'))

    # 标题栏语言设置
    if language == 'cn':
        df_ratio.rename(columns={'No.': '序号', 'Name': '名称', 'Value': '值', '#Count': '#数量', '%Ratio': '%占比'},
                        inplace=True)
        if display:
            df_ratio = df_ratio[['序号', '名称', '值', '#数量', '%占比']]
            # 是否显示合计
            if total:
                df_ratio.iloc[-1, 1] = '合计'
            else:
                df_ratio = df_ratio[df_ratio['名称'] != '']
        else:
            df_ratio = df_ratio[['值', '#数量', '%占比']]
            # 是否显示合计
            if total:
                df_ratio.iloc[-1, 0] = '合计'
            else:
                df_ratio = df_ratio[df_ratio['名称'] != '']

    else:
        if display:
            df_ratio = df_ratio[['No.', 'Name', 'Value', '#Count', '%Ratio']]
            # 是否显示合计
            if total:
                df_ratio.iloc[-1, 1] = 'Total'
            else:
                df_ratio = df_ratio[df_ratio['Value'] != '']
        else:
            df_ratio = df_ratio[['Value', '#Count', '%Ratio']]
            # 是否显示合计
            if total:
                df_ratio.iloc[-1, 0] = 'Total'
            else:
                df_ratio = df_ratio[df_ratio['Value'] != '']

    return df_ratio
