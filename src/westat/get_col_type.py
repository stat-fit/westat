import pandas as pd
from westat.logger import logger


def get_col_type(data: pd.DataFrame) -> pd.DataFrame:
    """
    划分离散和连续变量 （连续变量：int64,float64，float32；离散变量：其他）
    Args:
        data:需要划分离散和连续变量的数据集

    Returns:
        返回 DataFrame ,存放列名和列的类型（连续、离散）
    """
    col_all = data.columns
    col_all_type = data.dtypes
    col_type = []
    for i in range(len(col_all)):
        if col_all[i] != 'y':
            if str(col_all_type[i]) in ('int64', 'float64', 'float32'):
                col_type.append([col_all[i], 'continuous'])
            else:
                col_type.append([col_all[i], 'discrete'])
    df = pd.DataFrame(col_type, columns=['Name', 'Type'])
    return df
