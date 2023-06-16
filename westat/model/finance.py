import pandas as pd


def debx(amount: float = 1000000, rate: float = 0.043, period: int = 360, precision=2, return_data=False):
    """
    计算等额本息还款方式下贷款还款每月金额，月还款本金、月利息金额
    Args:
        amount:float,贷款金额
        rate:float,贷款年利率
        period:int,贷款期限
        precision:int,数据精度，小数点位数，默认为2
        return_data:bool,是否返回还款计划数据
    Returns:
        默认返回月还款金额，指定返回数据时，可以返回还款计划数据
    """
    period_rate = rate / 12
    repay = (amount * period_rate * (1 + period_rate) ** period) / ((1 + period_rate) ** period - 1)
    repay = round(repay, precision)

    i_amount = 0
    i_interest = 0
    i_remain = amount
    data_list = []
    for i in range(period):
        i_interest = round(i_remain * period_rate, precision)
        i_amount = round(repay - i_interest, precision)
        i_remain = round(i_remain - i_amount, precision)
        data_list.append([i + 1, repay, i_amount, i_interest, i_remain])

    data = pd.DataFrame(data_list, columns=['期数', '每月还款', '本期本金', '本期利息', '本期剩余'])

    if return_data:
        return {'repay': repay, 'data': data}
    else:
        return repay


def debj(amount: float = 1000000, rate: float = 0.043, period: int = 360, precision=2, return_data=False):
    """
    计算等额本金还款方式下贷款每月还款金额，月还款本金、月利息金额
    Args:
        amount:float,贷款金额
        rate:float,贷款年利率
        period:int,贷款期限
        precision:int,数据精度，小数点位数，默认为2
        return_data:bool,是否返回还款计划数据
    Returns:
        默认返回月还款金额，指定返回数据时，可以返回还款计划数据
    """
    period_rate = rate / 12

    i_amount = 0
    i_interest = 0
    i_remain = amount
    data_list = []
    for i in range(period):
        repay = round(amount / period + i_remain * period_rate, precision)
        i_amount = round(amount / period, precision)
        i_interest = round(repay - amount / period, precision)
        i_remain = round(i_remain - amount / period, precision)

        data_list.append([i + 1, i_amount + i_interest, i_amount, i_interest, i_remain])

    data = pd.DataFrame(data_list, columns=['期数', '每月还款', '本期本金', '本期利息', '本期剩余'])

    if return_data:
        return {'repay': repay, 'data': data}
    else:
        return repay
