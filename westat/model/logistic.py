def logistic(data, target='y', return_model=False):
    """
    根据数据集中的x,y 构建逻辑回归模型
    Args:
        data:pd.DataFrame,目标数据集
        target:str,目标变量名称，默认为'y'
        return_model:是否返回模型

    Returns:
        return_model=True返回逻辑回归模型
        否则返回逻辑回归模型汇总信息
    """
    import statsmodels.api as sm

    y = data['y']
    x = data[[col for col in data.columns if col != 'y']]
    x = sm.add_constant(x)

    lr = sm.Logit(y, x).fit(disp=0)

    if return_model:
        return lr
    else:
        return lr.summary()
