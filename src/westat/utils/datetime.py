from datetime import datetime


def date_diff(start_date: str,
              end_date: str,
              unit: str = 'd'):
    """
    根据输入的开始日期和结束日期，计算日期差、月份差、年份差，并保留2位小数
    Args:
        start_date: str,开始日期
        end_date: str,结束日期
        unit: str,计算类型，d-日期差，m-月份差，y-年份差，默认为日期差

    Returns:
        int/float,计算日期差、月份差、年份差,计算日期差时返回int，否则返回float
    """
    if len(start_date) < 10 or len(end_date) < 10:
        date1 = datetime.strptime(start_date[0:7], '%Y-%m')
        date2 = datetime.strptime(end_date[0:7], '%Y-%m')
    else:
        date1 = datetime.strptime(start_date, '%Y-%m-%d')
        date2 = datetime.strptime(end_date, '%Y-%m-%d')

    if unit == 'd':
        return int((date2 - date1).days)
    elif unit == 'm':
        from dateutil.relativedelta import relativedelta
        delta = relativedelta(date2, date1)
        return round(delta.years * 12 + delta.months + delta.days / 30, 2)
    elif unit == 'y':
        from dateutil.relativedelta import relativedelta
        delta = relativedelta(date2, date1)
        return round(delta.years + delta.months / 12 + delta.days / 365, 2)
    else:
        print('输入错误， unit：{} 不支持'.format(unit))
