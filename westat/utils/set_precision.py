def set_precision(precision=2):
    """
    设置pandas数据显示精度
    Args:
        precision: int,需要显示的小数位数，默认不显示科学计数法，显示2位小数

    Returns:
        没有返回值
    """
    import pandas as pd
    fmt_str = '{:.' + str(precision) + 'f}'
    pd.set_option('display.float_format', fmt_str.format)
