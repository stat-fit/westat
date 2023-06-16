def get_stock_pk(code='sh000001', language='cn'):
    """
    根据证券代码获取股票盘口数据
    Returns:
    指定股票的盘口数据
    """
    import requests
    import pandas as pd
    from westat.utils import regexp_like

    if len(code) == 6 and regexp_like(code[:3], '600|601|603|605|900'):
        code = 'sh' + code
    elif len(code) == 6 and regexp_like(code[:3], '000|002|003|200|300'):
        code = 'sz' + code
    elif len(code) == 5:
        code = 'hk' + code
    elif not regexp_like(code[:2],'sh|sz|hk') and regexp_like(code.lower(),'[a-z].+') and not regexp_like(code.lower(),'us'):
        code = 'us' + code.replace('.','')
    else:
        code = code

    response = requests.get('http://qt.gtimg.cn/q=s_pk' + code)

    if response.status_code == 200:
        text = response.text

        if regexp_like(text, 'none_match'):
            print('未匹配到任何数据！')
        else:

            data = text.split('"')[1].split('~')
            result = pd.DataFrame(data, index=range(len(data))).T
            result.columns = ['buy_big', 'buy_small', 'sale_big', 'sale_small']
            result['time'] = pd.to_numeric(result['time'])

            if language == 'cn':
                result.rename(columns={'buy_big': '买盘大单', 'buy_small': '买盘小单', 'sale_big': '卖盘大单',
                                       'sale_small': '卖盘小单'})

            return result
