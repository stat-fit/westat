import pandas as pd
def check_data_target(data:pd.DataFrame) -> bool:
    """
    检查数据集中是否有列名为"y" 或 "target"的目标变量
    Args:
        data: 需要检查的数据集

    Returns:
        bool:返回一个布尔变量
        返回 True,表示数据集中有名为"y" 或 "target"的目标变量
        返回 False,表示数据集中有没有名为"y" 或 "target"的目标变量
    """
    col_list = [x.lower() for x in data.columns]
    if 'y' not in col_list and 'target' not in col_list:
        return False
    else:
        return True
