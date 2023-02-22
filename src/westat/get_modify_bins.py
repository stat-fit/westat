import numpy as np
import pandas as pd
from westat.logger import logger


def set_modify_bins(col_bins: pd.DataFrame,
                    modify_list: list):
    """
    根据手动调整后的分箱，修改自动化生成的分箱结果
    Args:
        col_bins: 自动化生成的分箱结果
        modify_list: 手动调整后的分箱

    Returns:
        返回合并后的分箱结果
        如果手动有调整分箱，则按照调整后的分箱执行，否则按照自动化分箱结果执行
    """
    col_bins_adjust = pd.DataFrame(modify_list, columns=['Name', 'NewBins'])

    result = col_bins.merge(col_bins_adjust, on='Name', how='left')
    result = result.rename(columns={'Bins': 'OldBins', 'NewBins': 'Bins'})
    result['Bins'][result['Bins'].isnull()] = result['OldBins']
    return result[['Name', 'Bins']]
