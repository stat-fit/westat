from numpy import inf
import pandas as pd


def get_score_distribution(data: pd.DataFrame,
                           col: str = 'Score',
                           qcut: int = 10,
                           target: str = 'y',
                           precision: int = 2,
                           language: str = 'en'):
    """
    根据评分，查看好坏客户分布和提升度 lift
    Args:
        data: pd.DataFrame,目标数据集,需要包含评分、目标变量
        col: str,评分特征的名称，默认为'Score'
        qcut: int,等额分箱的分组数
        target: str,目标变量名称，默认为'y'
        precision: 数据精度，小数点位数，默认为2
        language: str,数据结果标题列显示语言，默认为 'en',可手动修改为'cn'
    Returns:
        评分的分布表，包含各分数区间的好坏客户数量，占比，提升度
    """
    df = data.copy()
    df[col] = df[col].astype(int)

    # 获取分箱切分点，并修改下限为-inf,上限为inf
    bins = pd.qcut(x=df[col], q=qcut, duplicates='drop', retbins=True)[1]
    bins[0] = -inf
    bins[-1] = inf

    # 对得分进行分组
    df['Score Range'] = pd.cut(df[col], bins=bins)

    # 设置统计量
    result = df.groupby('Score Range')[target].agg([('#Bad', lambda target: (target == 1).sum()),
                                                    ('#Good', lambda target: (target == 0).sum()),
                                                    ('#Total', 'count')]).reset_index()

    result['%Bad'] = result['#Bad'] / result['#Bad'].sum()
    result['%Good'] = result['#Good'] / result['#Good'].sum()
    result['%Total'] = result['#Total'] / result['#Total'].sum()
    result['%BadRate'] = result['#Bad'] / result['#Total']
    result['%BadRate Random'] = result['#Bad'].sum() / result['#Total'].sum()
    result['%CumBad'] = result['#Bad'].cumsum() / result['#Total'].cumsum()
    result['%CumTotal'] = result['#Total'].cumsum() / result['#Total'].sum()
    result['Lift'] = result['%CumBad'] / result['%CumTotal']

    # 设置显示格式
    result.reset_index(drop=True, inplace=True)
    result['No.'] = result.index + 1
    result['%Total'] = result['%Total'].apply(lambda x: format(x, '.' + str(precision) + '%'))
    result['%Bad'] = result['%Bad'].apply(lambda x: format(x, '.' + str(precision) + '%'))
    result['%Good'] = result['%Good'].apply(lambda x: format(x, '.' + str(precision) + '%'))
    result['%BadRate'] = result['%BadRate'].apply(lambda x: format(x, '.' + str(precision) + '%'))
    result['%BadRate Random'] = result['%BadRate Random'].apply(lambda x: format(x, '.' + str(precision) + '%'))
    result['%CumBad'] = result['%CumBad'].apply(lambda x: format(x, '.' + str(precision) + '%'))
    result['%CumTotal'] = result['%CumTotal'].apply(lambda x: format(x, '.' + str(precision) + '%'))
    result['Lift'] = result['Lift'].apply(lambda x: round(x, precision))

    if language == 'cn':
        result = result[
            ['No.', 'Score Range', '#Total', '#Bad', '#Good', '%Total', '%Bad', '%Good', '%BadRate', '%BadRate Random',
             '%CumBad', '%CumTotal', 'Lift']]
        result.rename(
            columns={'No.': '序号', 'Score Range': '分数区间', '#Total': '#合计', '#Bad': '#坏', '#Good': '#好',
                     '%Total': '%合计', '%Bad': '%坏',
                     '%Good': '%好', '%BadRate': '%坏件率', '%BadRate Random': '%随机坏件率', '%CumBad': '%累计坏',
                     '%CumTotal': '%累计合计', 'Lift': '提升度'}, inplace=True)
    else:
        result = result[
            ['No.', 'Score Range', '#Total', '#Bad', '#Good', '%Total', '%Bad', '%Good', '%BadRate', '%BadRate Random',
             '%CumBad', '%CumTotal', 'Lift']]
    return result


def view_score_distribution(data: pd.DataFrame,
                            col: str = 'Score',
                            qcut: int = 10,
                            target: str = 'y',
                            color: str = '#007bff',
                            precision: int = 2,
                            language: str = 'en'):
    """
        根据评分，查看好坏客户分布和提升度 lift
        Args:
            data: pd.DataFrame,目标数据集,需要包含评分、目标变量
            col: str,评分特征的名称，默认为'Score'
            qcut: int,等额分箱的分组数
            target: str,目标变量名称，默认为'y'
            color:str,显示颜色
            precision: 数据精度，小数点位数，默认为2
            language: str,数据结果标题列显示语言，默认为 'en',可手动修改为'cn'
        Returns:
            评分的分布表，包含各分数区间的好坏客户数量，占比，提升度
        """
    result = get_score_distribution(data=data, col=col, qcut=qcut, target=target, precision=precision,
                                    language=language)
    result['Lift.'] = result['Lift']
    result = result.style.bar(subset=['Lift.'], color=color)
    return result
