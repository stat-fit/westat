import numpy as np
from numpy import inf
import pandas as pd

from westat.logger import logger


def get_col_psi(data_actual: pd.DataFrame,
                data_expected: str,
                col: str = 'Score',
                bins: list = [],
                qcut=10,
                missing: list = [np.nan, None, 'nan'],
                target='y',
                precision=2,
                language='en') -> pd.DataFrame:
    """
    计算数据集PSI
    Args:
        data_actual: DataFrame,实际数据集
        data_expected: DataFrame,预期数据集
        col:str,需要计算PSI的列名
        bins:list，计算PSI的分箱
        qcut: int,等额分箱的分组数
        missing: list,缺失值列表
        target: str,目标变量名称，默认为'y'
        precision:数据精度，小数点位数，默认为2
        language: str,数据结果标题列显示语言，默认为 'en',可手动修改为'cn'

    Returns:
        结果数据集保存数据集对应的PSI
    """
    logger.info('计算特征的PSI...')
    if len(bins) > 0:
        data_actual['Bins Range'] = pd.cut(data_actual[col], bins, duplicates='drop')
        data_expected['Bins Range'] = pd.cut(data_actual[col], bins, duplicates='drop')
    else:
        data_actual['Bins'] = data_actual[col].replace(missing, np.nan)
        data_expected['Bins'] = data_expected[col].replace(missing, np.nan)

        # 获取切分点
        bins_actual = pd.qcut(data_actual['Bins'], q=qcut, duplicates='drop', retbins=True)[1]
        bins_actual[0] = -inf
        bins_actual[-1] = inf

        # 根据切分点进行分组
        data_actual['Bins Range'] = pd.cut(data_actual['Bins'], bins=bins_actual)
        data_expected['Bins Range'] = pd.cut(data_expected['Bins'], bins=bins_actual)

    # 计算分组后的统计量
    df_actual = data_actual.groupby(by='Bins Range')['Bins Range'].count()
    df_expected = data_expected.groupby(by='Bins Range')['Bins Range'].count()
    df_expected.index = df_actual.index
    result = pd.concat([df_actual, df_expected], axis=1)
    result.columns = ['#Actual', '#Expected']

    # 计算统计量
    result['#Total'] = result['#Actual'] + result['#Expected']
    result['%Actual'] = result['#Actual'] / result['#Actual'].sum()
    result['%Expected'] = result['#Expected'] / result['#Expected'].sum()
    result['%Total'] = result['#Total'] / result['#Total'].sum()
    result['PSI'] = (result['%Actual'] - result['%Expected']) * np.log(result['%Actual'] / result['%Expected'])
    result['Total PSI'] = result['PSI'].fillna(0).sum()
    result['Bins Range'] = result.index
    result.reset_index(drop=True, inplace=True)
    result['No.'] = result.index

    # 设置显示格式
    result['No.'] = result['No.'] + 1
    result['Name'] = col
    result['#Total'] = result['#Total'].apply(lambda x: round(x, precision))
    result['#Actual'] = result['#Actual'].apply(lambda x: round(x, precision))
    result['#Expected'] = result['#Expected'].apply(lambda x: round(x, precision))
    result['%Total'] = result['%Total'].apply(lambda x: format(x, '.' + str(precision) + '%'))
    result['%Actual'] = result['%Actual'].apply(lambda x: format(x, '.' + str(precision) + '%'))
    result['%Expected'] = result['%Expected'].apply(lambda x: format(x, '.' + str(precision) + '%'))
    result['PSI'] = result['PSI'].apply(lambda x: round(x, precision))
    result['Total PSI'] = result['Total PSI'].apply(lambda x: round(x, precision))

    # 标题栏语言设置
    if language == 'cn':
        result = result[
            ['No.', 'Name', 'Bins Range', '#Total', '#Actual', '#Expected', '%Total', '%Actual', '%Expected', 'PSI',
             'Total PSI']]
        result.rename(
            columns={'No.': '序号', 'Name': '名称', 'Bins Range': '分组', '#Total': '#合计', '#Actual': '#实际',
                     '#Expected': '#期望',
                     '%Total': '%合计', '%Actual': '%实际', '%Expected': '%期望', 'Total PSI': 'PSI 合计'},
            inplace=True)

    else:
        result = result[
            ['No.', 'Name', 'Bins Range', '#Total', '#Actual', '#Expected', '%Total', '%Actual', '%Expected', 'PSI',
             'Total PSI']]

    return result


def view_col_psi(data_actual: pd.DataFrame,
                 data_expected: str,
                 col: str = 'Score',
                 bins: list = [],
                 qcut=10,
                 missing: list = [np.nan, None, 'nan'],
                 target='y',
                 color: str = '#007bff',
                 precision=2,
                 language='en') -> pd.DataFrame:
    """
    计算数据集PSI
    Args:
        data_actual: DataFrame,实际数据集
        data_expected: DataFrame,预期数据集
        col:str,需要计算PSI的列名
        bins:list，计算PSI的分箱
        qcut: int,等额分箱的分组数
        missing: list,缺失值列表
        target: str,目标变量名称，默认为'y'
        color:str,显示颜色
        precision:数据精度，小数点位数，默认为2
        language: str,数据结果标题列显示语言，默认为 'en',可手动修改为'cn'

    Returns:
        结果数据集保存数据集对应的PSI
    """
    result = get_col_psi(data_actual=data_actual,
                         data_expected=data_expected,
                         col=col,
                         bins=bins,
                         qcut=qcut,
                         missing=missing,
                         target=target,
                         precision=precision,
                         language=language)
    result['PSI.'] = result['PSI'].replace('', np.nan)
    result['PSI.'] = result['PSI.'].apply(lambda x: float(x))
    result = result.style.bar(subset=['PSI.'], color=color)
    return result
