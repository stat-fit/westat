import pandas as pd
import os
from .utils import current_path


# 设置自带数据集
def credit_card() -> pd.DataFrame():
    """
    获取自带数据集 uci_credit_card
    Returns:
        返回dataframe格式化的 uci_credit_card 数据集
    """

    file_path = os.path.join(current_path, 'data/UCI_Credit_Card.csv')
    data = pd.read_csv(file_path)
    return data


class GiveMeSomeCredit():

    def __init__(self):
        """
        获取自带数据集 GiveMeSomeCredit
        Returns:
            返回dataframe格式化的 GiveMeSomeCredit 数据集
        """
        train_path = os.path.join(current_path, 'data', 'GiveMeSomeCredit', 'cs-training.csv')
        self.train = pd.read_csv(train_path)

        test_path = os.path.join(current_path, 'data', 'GiveMeSomeCredit', 'cs-test.csv')
        self.test = pd.read_csv(test_path)
