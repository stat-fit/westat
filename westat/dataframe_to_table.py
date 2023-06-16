from prettytable import PrettyTable
from westat.logger import logger


def dataframe_to_table(data):
    """
    将pandas DataFrame 转换为 PrettyTable
    Args:
        data:将要转换的DataFrame

    Returns:

    """
    if data.empty:
        logger.warning('输入的数据集为空')
        return
    else:
        table = PrettyTable(list(data.columns))
        for row in range(len(data)):
            table.add_row(list(data.iloc[row,:]))
        print(table)
        return
