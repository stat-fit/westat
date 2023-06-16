def get_stock_m(code='sh000001', language='cn'):
    """
    根据证券代码获取股票分钟数据
    Returns:
    指定股票的分钟数据
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

    response = requests.get('https://web.ifzq.gtimg.cn/appstock/app/minute/query?code=' + code)

    if response.status_code == 200:
        text = response.json()
        if response.json()['msg'] == 'code param error':
            print('未匹配到任何数据！')
        else:
            data = text['data'][code]['data']['data']

            data_list = []
            for d in data:
                row = d.split(' ')
                minute = row[0]
                price = row[1]
                vol = row[2]
                amount = row[3]
                data_list.append([minute, price, vol, amount])
            result = pd.DataFrame(data_list, columns=['time', 'price', 'volume', 'amount'])
            result['time'] = pd.to_numeric(result['time'])
            result['price'] = pd.to_numeric(result['price'])
            result['volume'] = pd.to_numeric(result['volume'])
            result['amount'] = pd.to_numeric(result['amount'])

            if language == 'cn':
                result.rename(columns={'time': '时间', 'price': '价格', 'volume': '成交量', 'amount': '成交额'},inplace=True)
            return result
