import numpy as np
import pandas as pd
import statsmodels.api as sm


def stepwise_forward(X, y, initial_list=[], threshold_in=0.01, threshold_out=0.05, verbose=True):
    """
    使用逐步向前法实现逻辑回归特征选择。

    参数：
    X: 特征变量数据，DataFrame或二维数组
    y: 目标变量数据，Series或一维数组
    initial_list: 初始特征列表，默认为空
    threshold_in: 添加特征的p值阈值，默认为0.01
    threshold_out: 移除特征的p值阈值，默认为0.05
    verbose: 是否输出详细的调试信息，默认为True

    返回值：
    selected_features: 选中的特征列表
    """

    included = list(initial_list)
    while True:
        changed = False
        excluded = list(set(X.columns) - set(included))

        # 添加特征
        new_pval = pd.Series(index=excluded, dtype=np.float64)
        for new_column in excluded:
            model = sm.Logit(y, sm.add_constant(X[included + [new_column]])).fit(disp=0)
            new_pval[new_column] = model.pvalues[new_column]
        best_pval = new_pval.min()
        if best_pval < threshold_in:
            best_feature = new_pval.idxmin()
            included.append(best_feature)
            changed = True
            if verbose:
                print(f'Add  {best_feature} with p-value {best_pval}')

        # 移除特征
        model = sm.Logit(y, sm.add_constant(X[included])).fit(disp=0)
        p_values = model.pvalues.iloc[1:]
        worst_pval = p_values.max()
        if worst_pval > threshold_out:
            changed = True
            worst_feature = p_values.idxmax()
            included.remove(worst_feature)
            if verbose:
                print(f'Drop {worst_feature} with p-value {worst_pval}')

        if not changed:
            break

    return included
