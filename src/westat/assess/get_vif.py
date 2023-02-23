import pandas as pd


def get_vif(data,
            col,
            target='y',
            return_data=False,
            precision=2):
    """
    根据指定的特征清单，计算数据集中每个特征的方差膨胀因子 VIF
    Args:
        data:pd.DataFrame,目标数据集
        col:str，需要计算VIF的特征列表
        target:str,目标变量名称，默认为'y'
        return_data:是否返回结果数据
        precision:int,数据精度，小数点位数，默认为2

    Returns:
        计算 VIF 的值，或根据要求返回结果数据
    """
    from statsmodels.stats.outliers_influence import variance_inflation_factor

    X = data[[i for i in col if i != target]]

    # 计算VIF
    vif = pd.DataFrame()
    vif["variables"] = X.columns
    vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    vif_max = round(vif['VIF'].max(), precision)
    vif["VIF"] = vif["VIF"].apply(lambda x: round(x, precision))
    if return_data:
        return vif_max, vif
    else:
        return vif_max
