import pandas as pd
from pandas import Timestamp

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

strptime = datetime.strptime


def date_diff(start_date: str,end_date: str,method: str = 'd'):
    """
    根据输入的开始日期和结束日期，计算日期差、月份差、年份差，并保留2位小数
    Args:
        start_date: str,开始日期，字符串格式的日期，yyyy-mm-dd格式
        end_date: str,结束日期，字符串格式的日期，yyyy-mm-dd格式
        method: str,计算方法，d-日期差，m-月份差，y-年份差，默认为日期差

    Returns:
        int/float,计算日期差、月份差、年份差,计算日期差时返回int，否则返回float
    """
    # 计算日期差
    if method == 'd':
        date1 = strptime(start_date, '%Y-%m-%d')
        date2 = strptime(end_date, '%Y-%m-%d')
        return int((date2 - date1).days)

    # 计算月份差
    elif method == 'm':
        if len(start_date) < 10 or len(end_date) < 10:
            date1 = strptime(start_date[0:7], '%Y-%m')
            date2 = strptime(end_date[0:7], '%Y-%m')
        else:
            date1 = strptime(start_date, '%Y-%m-%d')
            date2 = strptime(end_date, '%Y-%m-%d')

        from dateutil.relativedelta import relativedelta
        delta = relativedelta(date2, date1)
        return round(delta.years * 12 + delta.months + delta.days / 30, 2)

    # 计算年份差
    elif method == 'y':
        if len(start_date) < 10 or len(end_date) < 10:
            date1 = strptime(start_date[0:7], '%Y-%m')
            date2 = strptime(end_date[0:7], '%Y-%m')
        else:
            date1 = strptime(start_date, '%Y-%m-%d')
            date2 = strptime(end_date, '%Y-%m-%d')

        from dateutil.relativedelta import relativedelta
        delta = relativedelta(date2, date1)
        return round(delta.years + delta.months / 12 + delta.days / 365, 2)
    else:
        raise ValueError('输入错误， 不支持的method：{} '.format(method))


def add_months(date, months):
    """
    根据给定的日期和月份差，计算目标日期结果
    Args:
        date:yyyy-mm-dd格式字符串 或 datetime 格式日期
        months:int,需要计算的月份差
    Returns:
        返回日期格式的结果
    """
    if type(date) == str:
        date_fmt = strptime(date, '%Y-%m-%d')
    else:
        date_fmt = date

    from dateutil.relativedelta import relativedelta
    result = date_fmt + relativedelta(months=months)
    return result


def year_start(date):
    """
    返回给定日期对应年份的第一天，例如 xxxx-01-01
    Args:
        date:yyyy-mm-dd格式字符串 或 datetime 格式日期

    Returns:

    """
    if type(date) == str:
        date_fmt = strptime(date, '%Y-%m-%d')
    else:
        date_fmt = date
    result = date_fmt.replace(month=1, day=1)
    return result


def year_end(date):
    """
    返回给定日期对应年份的最后一天，例如 xxxx-12-01
    Args:
        date:给定的字符串 或 datetime 格式日期

    Returns:

    """
    if type(date) == str:
        date_fmt = strptime(date, '%Y-%m-%d')
    else:
        date_fmt = date
    result = date_fmt.replace(month=12, day=31)
    return result


def month_start(date):
    """
    返回给定日期对应月份的第一天的日期
    Args:
        date: 给定的字符串 或 datetime 格式日期

    Returns:
        当月最后一天
    """
    if isinstance(date, str):
        date_fmt = strptime(date, '%Y-%m-%d')
    else:
        date_fmt = date
    result = date_fmt.replace(day=1)
    return result


def month_end(date):
    """
    返回给定日期对应月份的最后一天的日期
    Args:
        date: 给定的字符串 或 datetime 格式日期

    Returns:
        当月最后一天
    """
    if type(date) == str:
        date_fmt = strptime(date, '%Y-%m-%d')
    else:
        date_fmt = date
    from dateutil.relativedelta import relativedelta
    result = date_fmt + relativedelta(months=1, day=1) + timedelta(days=-1)
    return result


def month_diff(start_date: str,end_date: str,  method: str = ''):
    """
    根据结束日期和开始日期，计算两个日期相差的月份数
    Args:
        end_date:str,datetime,pd.Series，结束日期
        start_date:str,datetime,pd.Series，开始日期
        method:计算方法,'mm'：表示将月份差计算时不计算日期，使用对应月份的1日进行计算月份差
    Returns:
        float,返回两个日期相差的月份数，保留2位小数
    """
    if method == 'mm':
        if isinstance(start_date, str):
            start = strptime(start_date, '%Y-%m-%d').replace(day=1)
        else:
            start = start_date.replace(day=1)

        if isinstance(end_date, str):
            end = strptime(end_date, '%Y-%m-%d').replace(day=1)
        else:
            end = end_date.replace(day=1)

        if not isinstance(start_date,pd.Series) or not isinstance(end_date,pd.Series):
            delta = relativedelta(end, start)
            result = delta.years * 12 + delta.months
        else:
            r = []
            for x, y in zip(start, end):
                delta = relativedelta(y, x)
                r.append(delta.years * 12 + delta.months)
                result = pd.Series(r)
        return result

    else:
        if isinstance(start_date, str):
            start = strptime(start_date, '%Y-%m-%d')
        elif type(start_date) == pd.Series:
            start = pd.to_datetime(start_date)
        else:
            start = start_date

        if isinstance(end_date, str):
            end = strptime(end_date, '%Y-%m-%d')
        elif type(end_date) == pd.Series:
            end = pd.to_datetime(end_date)
        else:
            end = end_date

        if not isinstance(start_date,pd.Series) or not isinstance(end_date,pd.Series):
            delta = relativedelta(end, start)
            result = round(delta.years * 12 + delta.months + delta.days / 30, 2)
        else:
            r = []
            for x, y in zip(start, end):
                delta = relativedelta(y, x)
                r.append(round(delta.years * 12 + delta.months + delta.days / 30, 2))
                result = pd.Series(r)
        return result
