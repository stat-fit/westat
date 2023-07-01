# -*- coding:utf-8 -*-

# 版本号
__title__ = 'westat'
__version__ = '0.2.4'
__author__ = 'westat <westat@foxmail.com>'
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

pd.set_option('max_colwidth', 100)  # 设置value的显示长度为100，默认为50
pd.set_option('display.max_columns', 100)  # 把最大列显示设置成100
pd.set_option('display.max_rows', 100)  # 把最大行显示设置成30




version = __version__

# 导入westat功能模块

# 自带数据集
from .dataset import credit_card, GiveMeSomeCredit

# 数据准备 sample
from .sample import read_csv, read_excel, get_data_partition

# 数据探索 explorer
from .explore import (check_data_target,
                      get_data_describe,
                      get_data_distribution,
                      get_data_check,
                      proc_means,
                      plot_col,
                      )

# 数据处理 modify
from .modify import set_update_bins

# 模型开发 model
from .model import (get_feature_by_ivcorr,
                    get_data_type,
                    get_data_bins,
                    get_data_discrete,
                    get_data_iv,
                    get_data_woe,
                    get_woe_transform,
                    get_model_iv,
                    view_model_iv,
                    get_predict_score,
                    get_scorecard,
                    get_tree_bins,
                    get_bins,
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

                    gini_impurity,
                    debx,
                    debj,
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
                     plot_roc_ks,
                     plot_ks)

# 工具
from .utils import (current_path,
                    user_name,
                    host_name,
                    host_ip,
                    sin,
                    cos,
                    date_diff,
                    add_months,
                    year_start,
                    year_end,
                    month_start,
                    month_end,
                    month_diff,
                    get_max_continue,
                    get_over_continue,
                    nvl,
                    growth_rate,
                    rate,
                    regexp_replace,
                    regexp_like,
                    to_single_byte,
                    to_multi_byte,
                    set_precision)

# 量化
from .quant import get_stock,get_stock_pk,get_stock_m,get_stock_i,get_stock_index

# 设置函数别名
uci_credit_card = credit_card
# 数据描述
data_desc = get_data_describe
data_describe = get_data_describe

data_dist = get_data_distribution
value_counts = get_data_distribution
plot_counts = plot_col

# 数据分区
data_split = get_data_partition

# 分数分布
score_dist = get_score_distribution
view_score_dist = view_score_distribution

# get_data_discrete
data_discrete = get_data_discrete

# 分箱
tree_bins = get_tree_bins
update_bins = set_update_bins

# 模型
woe_transform = get_woe_transform
woe_iv = get_woe_iv
data_iv = get_data_iv
data_woe = get_data_woe
model_iv = get_model_iv
# 特征筛选
iv_corr = get_feature_by_ivcorr

# 检查缺失值和唯一值
check_data = get_data_check

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
    'version',
    'sin',
    'cos',

    # 工具
    'current_path',
    'user_name',
    'host_name',
    'host_ip',

    # 日期处理函数
    'date_diff',
    'add_months',
    'year_start',
    'year_end',
    'month_start',
    'month_end',
    'month_diff',
    'get_max_continue',
    'get_over_continue',
    'nvl',
    'growth_rate',
    'rate',
    'regexp_replace',
    'regexp_like',
    'to_single_byte',
    'to_multi_byte',
    'set_precision',

    # 自带数据集
    'credit_card',
    'uci_credit_card',
    'GiveMeSomeCredit',
    # 数据获取 sample
    'read_csv',
    'read_excel',

    # 数据探索 explorer
    'get_data_partition',
    'get_data_distribution',
    'get_data_describe',
    'get_data_check',
    'check_data',
    'proc_means',
    'plot_col',
    'plot_counts',

    # 数据检查
    'check_data_target',

    # 数据处理 modify
    'get_data_discrete',
    'data_discrete',
    'get_data_iv',
    'data_iv',
    'get_data_woe',
    'data_woe',
    'get_woe_transform',
    'woe_transform',
    'get_tree_bins',
    'tree_bins',
    'get_bins',
    'get_woe_iv',
    'woe_iv',
    'view_woe_iv',
    # 'dataframe_to_table',
    'get_data_type',
    'get_data_bins',
    'set_update_bins',
    'update_bins',

    # 模型开发 model
    'get_model_iv',
    'model_iv',
    'view_model_iv',

    'get_scorecard',
    'get_predict_score',
    'plot_woe',
    'plot_iv',
    'plot_corr',
    'plot_tree',
    # 特征筛选
    'get_feature_by_ivcorr',
    'iv_corr',
    'stepwise_lr',
    'stepwise_forward',
    # 决策树文件转换
    'tree_to_img',
    'tree_to_pdf',
    # 统计指标
    'gini_impurity',

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
    'plot_ks',

    # 其他
    'data_desc',
    'data_dist',
    'value_counts',
    'data_split',
    'score_dist',
    'view_score_dist',
    'debx',
    'debj',

    'get_stock',
    'get_stock_pk',
    'get_stock_m',
    'get_stock_i',
    'get_stock_index',
)



