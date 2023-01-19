# 版本号
global version
version = '0.1.3'

def get_version():
    return version


import sys
import os
from datetime import datetime

import numpy as np
from numpy import inf
import pandas as pd
import matplotlib.pyplot as plt
from tqdm.notebook import tqdm

plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文字体
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 导入westat功能模块
# 日志模块
from westat.logger import logger

# 数据准备 sample
from pandas import read_csv, read_excel


# 数据探索 explorer
from westat.get_data_partition import get_data_partition
from westat.get_data_distribution import get_data_distribution
from westat.get_data_describe import get_data_describe


# 数据处理 modify
from westat.get_data_discrete import get_data_discrete
from westat.get_data_iv import get_data_iv
from westat.get_data_woe import get_data_woe
from westat.get_data_woe_transform import get_data_woe_transform
from westat.get_tree_bins import get_tree_bins
from westat.get_woe_iv import get_woe_iv, view_woe_iv

from westat.check_data_target import check_data_target
# from westat.dataframe_to_table import dataframe_to_table
from westat.get_col_type import get_col_type
from westat.get_col_bins import get_col_bins
from westat.get_col_psi import get_col_psi,view_col_psi
from westat.get_modify_bins import get_modify_bins
from westat.feature_selection import get_feature_by_ivcorr

from westat.get_model_iv import get_model_iv


# 模型开发 model
from westat.get_scorecard import get_scorecard
from westat.get_predict_score import get_predict_score


# 模型评估 access
from westat.get_score_distribution import get_score_distribution, view_score_distribution
from westat.get_auc import get_auc
from westat.get_ks import get_ks


# 绘图
from westat.plot_woe import plot_woe
from westat.plot_iv import plot_iv
from westat.plot_corr import plot_corr
from westat.plot_lift import plot_lift
from westat.plot_roc_ks import plot_roc_ks

# 决策树文件转换
from westat.tree_to_img import tree_to_img
from westat.tree_to_pdf import tree_to_pdf

# 日期处理函数
from westat.date_diff import date_diff

# 设置函数别名
get_data_desc = get_data_describe
get_data_dist = get_data_distribution
get_data_part = get_data_partition
get_score_dist = get_score_distribution
view_score_dist = view_score_distribution




class Table(pd.DataFrame):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'table for westat'
