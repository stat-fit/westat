import pandas as pd
import os


# 设置自带数据集
def credit_card() -> pd.DataFrame():
    """
    获取自带数据集 uci_credit_card
    Returns:
        返回dataframe格式化的 uci_credit_card 数据集
    """
    from westat.utils import current_path
    file_path = os.path.join(current_path, 'data/UCI_Credit_Card.csv')
    data = pd.read_csv(file_path)
    return data
