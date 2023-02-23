import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


def get_data_partition(data: pd.DataFrame,
                       test_size: float = 0.25,
                       random_state=1234,
                       target: str = 'y'):
    """
        划分训练集和测试集
    Args:
        data: DataFrame,将要进行数据分区的目标数据集
        target: str,目标变量名称，默认为'y'
        test_size:float 测试集所占比例，默认为0.25
        random_state: 随机种子，默认为1234

    Returns:
        返回数据分区后的训练集和测试集
    """
    X = data[[col for col in data.columns if col != target]]
    y = data[target]
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    data_train = x_train.reset_index()
    del data_train['index']
    data_train[target] = y_train.reset_index()[target]
    data_test = x_test.reset_index()
    del data_test['index']
    data_test[target] = y_test.reset_index()[target]
    return data_train, data_test
