import numpy as np
import pandas as pd
import statsmodels.api as sm


def get_criterion(lr, crit, x, y):
    if crit == 'aic':
        aic = lr.aic
    return aic


def stepwise_lr(X: pd.DataFrame(),
                y: pd.DataFrame(),
                sort_features: list = [],
                crit: str = 'aic',
                verbose: bool = True):
    """
    批量获取变量WoE值
    Args:
        X: 特征变量数据，DataFrame或二维数组
        y: 目标变量数据，Series或一维数组
        sort_features:根据woe排倒序后的特征列表
        crit:str,筛选特征变量的准则，默认为aic
        verbose: 是否输出详细的调试信息，默认为True

    Returns:
        返回特征列表
    """
    # 逐步筛选入模特征
    sort_features_woe = sort_features

    selected_f = [sort_features_woe[0]]
    n = 0
    for f in sort_features_woe[1:]:

        x0 = X[selected_f].copy()
        lr0 = sm.Logit(y, sm.add_constant(x0)).fit(disp=0)

        try_vars = selected_f + [f]
        x = X[try_vars].copy()
        lr = sm.Logit(y, sm.add_constant(x)).fit(disp=0)

        if verbose:
            n = n + 1
            pvals = lr.pvalues.apply(lambda x: round(x, 4))

            print('\nstep {0},current:{1},selected:{3},max_pvalue:{2},pvalue:{1},pvalues:{5}'.format(n,f,selected_f,
                                                                                                    pvals[-1],
                                                                                                    max(pvals),
                                                                                                    pvals.tolist()))
        # 判断新变量是否显著, 如果不显著则跳过
        if lr.pvalues[-1] >= 0.05:
            if verbose:
                print('新变量不显著')
            continue
        # 如果所有变量都显著，则判断目标函数值是否下降，如果下降则加入变量到候选变量
        elif max(lr.pvalues) < 0.05:
            if verbose:
                print('所有变量都显著')
            if get_criterion(lr, crit, x, y) < get_criterion(lr0, crit, x0, train_y):
                selected_f.append(f)
        # 如果新变量显著，且有老变量不显著，则判断比较两者的损失函数值下降水平，保留更优的
        else:
            if verbose:
                print('新变量显著，且有老变量不显著')
            del try_vars[np.argmax(lr.pvalues)]
            x1 = X[try_vars].copy()
            lr1 = sm.Logit(y, sm.add_constant(x1)).fit(disp=0)
            # 如果去掉不显著变量后目标函数下降，则入选新特征
            aic1 = round(get_criterion(lr1, crit, x1, y), 4)
            aic2 = round(get_criterion(lr0, crit, x0, y), 4)
            if aic1 < aic2:
                if verbose:
                    print('去掉不显著变量后目标函数下降，去掉后的aic:{},去掉前的aic:{}'.format(aic1, aic2))
                    print(np.argmax(lr.pvalues))
                    print(selected_f[np.argmax(lr.pvalues) - 1])
                del selected_f[np.argmax(lr.pvalues) - 1]
                selected_f.append(f)

    return selected_f
