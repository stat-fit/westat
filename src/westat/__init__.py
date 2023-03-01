# -*- coding:utf-8 -*-

# 版本号
__title__ = 'westat'
__version__ = '0.1.14'
__author__ = 'statfit <statfit@hotmail.com>'
__license__ = 'GPL, see LICENSE.txt'
__copyright__ = 'Copyright (c) 2022-2023 statfit'

import sys
import os
from datetime import datetime
import numpy as np
from numpy import inf
import pandas as pd
import matplotlib.pyplot as plt
from tqdm.notebook import tqdm
import warnings

plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文字体
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 导入westat功能模块

# 自带数据集
from .dataset import credit_card

# 数据准备 sample
from .sample import read_csv, read_excel, get_data_partition

# 数据探索 explorer
from .explore import (check_data_target,
                      get_data_describe,
                      get_data_distribution,
                      proc_means,
                      )

# 数据处理 modify
from .modify import set_update_bins

# 模型开发 model
from .model import (get_feature_by_ivcorr,
                    get_col_type,
                    get_data_bins,
                    get_data_discrete,
                    get_data_iv,
                    get_data_woe,
                    get_woe_transform,
                    get_model_iv,
                    get_predict_score,
                    get_scorecard,
                    get_tree_bins,
                    get_woe_iv,
                    view_woe_iv,
                    stepwise_forward,
                    stepwise_lr,
                    tree_to_img,
                    tree_to_pdf,
                    plot_corr,
                    plot_iv,
                    plot_woe,
                    plot_tree,
                    )

# 模型评估 access
from .assess import (get_score_distribution,
                     view_score_distribution,
                     get_auc,
                     get_auc_by_card,
                     get_ks,
                     get_ks_by_card,
                     get_vif,
                     get_psi,
                     view_psi,
                     get_data_psi,
                     plot_lift,
                     plot_roc_ks)


# 工具
from .utils import current_path, user_name, host_name, host_ip, date_diff

# 设置函数别名
get_data_desc = get_data_describe
get_data_dist = get_data_distribution
get_data_part = get_data_partition
get_score_dist = get_score_distribution
view_score_dist = view_score_distribution

__all__ = (
    'os',
    'sys',
    'datetime',
    'np',
    'pd',
    'inf',
    'plt',
    'tqdm',
    'warnings',

    # 工具
    'current_path',
    'user_name',
    'host_name',
    'host_ip',
    # 日期处理函数
    'date_diff',
    # 自带数据集
    'credit_card',

    # 数据获取 sample
    'read_csv',
    'read_excel',

    # 数据探索 explorer
    'get_data_partition',
    'get_data_distribution',
    'get_data_describe',
    'proc_means',
    # 数据检查
    'check_data_target',

    # 数据处理 modify
    'get_data_discrete',
    'get_data_iv',
    'get_data_woe',
    'get_woe_transform',
    'get_tree_bins',
    'get_woe_iv',
    'view_woe_iv',
    # 'dataframe_to_table',
    'get_col_type',
    'get_data_bins',
    'set_update_bins',
    'get_model_iv',

    # 模型开发 model
    'get_scorecard',
    'get_predict_score',
    'plot_woe',
    'plot_iv',
    'plot_corr',
    'plot_tree',
    # 特征筛选
    'get_feature_by_ivcorr',
    'stepwise_lr',
    'stepwise_forward',
    # 决策树文件转换
    'tree_to_img',
    'tree_to_pdf',

    # 模型评估 access
    'get_score_distribution',
    'view_score_distribution',
    'get_auc',
    'get_auc_by_card',
    'get_ks',
    'get_ks_by_card',
    'get_vif',
    'get_psi',
    'view_psi',
    'get_data_psi',
    'plot_lift',
    'plot_roc_ks',

    # 其他
    'get_data_desc',
    'get_data_dist',
    'get_data_part',
    'get_score_dist',
    'view_score_dist',
)


class Table(pd.DataFrame):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'table for westat'
