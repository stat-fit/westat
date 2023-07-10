import pandas as pd


def get_data_distribution(data: pd.DataFrame,
                          col='y',
                          by=['#Count', 'Name'],
                          ascending=[False, False],
                          precision=2,
                          language='en') -> pd.DataFrame:
    """
    查看数据集data中col列的数据分布情况
    Args:
        data:DataFrame,需要检查数据分布的数据集
        by:list,根据指定列进行排序，默认根据数量（降序）、名称（升序）排序
        ascending:list,指定列对应的排序列表
        col:需要检查数据分布的列，默认为'y'
        display:bool,是否显示详细信息
        precision:数据精度，默认为2位小数
        language:显示语言，en：显示为英文，cn：显示为中文
    Returns:
        返回包含数据量、数据占比的数据集
    """
    result = pd.DataFrame(data=data[col].value_counts())
    result.columns = ['count']
    result['%Ratio'] = result['count'] / len(data)
    result['Value'] = result.index
    result['Name'] = col
    result = result.rename(columns={'count': '#Count'})
    result = result[['Name', 'Value', '#Count', '%Ratio']]

    # 排序
    result.sort_values(by=by, ascending=ascending, inplace=True)

    # 添加汇总行
    total = result.iloc[:, 1:].apply(lambda x: x.sum())
    row = pd.DataFrame([''] + total.to_list()).T
    row.columns = result.columns
    result = pd.concat([result, row], ignore_index=True)

    result.reset_index(drop=True, inplace=True)
    result['No.'] = result.index + 1

    # 数据精度设置
    result['#Count'] = result['#Count'].apply(lambda x: format(x, '.' + str(precision) + 'f'))
    result['%Ratio'] = result['%Ratio'].apply(lambda x: format(x, '.' + str(precision) + '%'))

    result = result[['No.', 'Name', 'Value', '#Count', '%Ratio']]
    result.iat[-1,0] = 'Total'
    result.iat[-1,1] = ''
    result.iat[-1,2] = ''

    # 标题栏语言设置
    if language == 'cn':
        result.rename(columns={'No.': '序号', 'Name': '名称', 'Value': '值', '#Count': '#数量', '%Ratio': '%占比'},
                      inplace=True)


    return result
