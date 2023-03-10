import numpy as np
import pandas as pd
import statsmodels.api as sm

from .get_col_type import get_col_type
from .get_data_discrete import get_data_discrete
from .get_woe_transform import get_woe_transform
from .get_model_iv import get_model_iv
from .get_data_iv import get_data_iv


def get_scorecard(data: pd.DataFrame,
                  col_bins: pd.DataFrame = pd.DataFrame(),
                  col_dict: pd.DataFrame = pd.DataFrame(),
                  init_score: int = 600,
                  pdo: int = 50,
                  target: str = 'y',
                  return_lr: bool = False,
                  precision: int = 2,
                  language: str = 'en'):
    """
    按照提供的分箱、数据字典，以逻辑回归方法开发评分卡
    Args:
        data:pd.DataFrame,需要开发评分卡的目标数据集
        col_bins:pd.DataFrame,列的分箱
        col_dict:pd.DataFrame,列的数据字典
        init_score:初始模型分,默认为600
        pdo: int,坏件率每上升一倍，增加的分数，默认为50,当pdo为负数时，分数越高，风险越高
        target: str,目标变量名称，默认为'y'
        return_lr:bool,是否返回逻辑回归模型的详细内容
        precision: :int,数据精度，小数点位数，默认为2
        language:str,返回结果的标题语言，默认为英文

    Returns:
        评分卡结果表，包含模型全部特征，分箱，截距，参数，得分
    """

    # 数据类型
    col_types = get_col_type(data)

    # 数据离散化
    data_discrete = get_data_discrete(data=data, col_bin=col_bins, target=target)

    # WoE 转换
    data_woe = get_woe_transform(data_discrete, target=target)

    # 根据手动调整后的分箱，批量计算IV
    data_iv = get_data_iv(data_discrete, target=target, method='discrete')

    # 逻辑回归模型
    y = data_woe[target]
    x = data_woe[[col for col in data.columns if col != target]]
    x = sm.add_constant(x)

    lr = sm.Logit(y, x).fit(disp=0)

    # 评分卡特征准备
    result = get_model_iv(data_discrete=data_discrete,
                          col_iv=data_iv,
                          col_bins=col_bins,
                          col_dict=col_dict,
                          col_types=col_types,
                          target=target,
                          precision=precision)

    # 评分卡模型的截距项
    result['Intercept'] = lr.params[0]
    result['Label'].fillna('', inplace=True)

    # 评分卡模型的参数
    df_coef = pd.DataFrame(data=lr.params, columns=['Coef'])
    df_coef['Name'] = df_coef.index
    result = result.merge(df_coef, how='left', on='Name')

    # 计算评分卡模型的特征得分
    odds = data[target].sum() / (data[target].count() - data[target].sum())

    if pdo > 0:
        b = pdo / np.log(2)
    else:
        b = -pdo / np.log(2)

    a = init_score + b * np.log(odds)

    result['Score'] = -b * result['WoE'] * result['Coef']

    # 设置显示格式
    result.reset_index(drop=True, inplace=True)  # 重置索引
    result['Intercept'] = result['Intercept'].apply(lambda x: round(x, precision))
    result['Coef'] = result['Coef'].apply(lambda x: round(x, precision))
    result['Score'] = result['Score'].apply(lambda x: round(x, 0))
    result['Base Score'] = init_score

    # 语言设置
    if language == 'cn':
        result = result[['No.', 'Name', 'Label', 'Type', 'Bins No.', 'Bin', 'Bins', '#Total', '#Bad',
                         '#Good', '%Total', '%Bad', '%Good', '%BadRate', 'WoE', 'IV', 'Total IV',
                         'WoE.', 'Style', 'Intercept', 'Coef', 'Base Score', 'Score']]
        result.rename(
            columns={'No.': '序号', 'Name': '名称', 'Label': '描述', 'Type': '类型', 'Bins No.': '分箱序号',
                     'Bin': '分箱', 'Bins': '切分点', '#Total': '#合计', '#Bad': '#坏', '#Good': '好',
                     '%Total': '%合计', '%Bad': '%坏', '%Good': '%好', '%BadRate': '%坏件率', 'Total IV': 'IV合计',
                     'Intercept': '截距', 'Coef': '系数', 'Base Score': '基础分', 'Score': '分数', 'Style': '样式'},
            inplace=True)
    else:
        result = result[['No.', 'Name', 'Label', 'Type', 'Bins No.', 'Bin', 'Bins', '#Total', '#Bad',
                         '#Good', '%Total', '%Bad', '%Good', '%BadRate', 'WoE', 'IV', 'Total IV',
                         'WoE.', 'Style', 'Intercept', 'Coef', 'Base Score', 'Score']]

    if return_lr:
        return result, lr, a, b
    else:
        return result
