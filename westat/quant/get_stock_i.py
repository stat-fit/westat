def get_stock_i(code=['sh000001','sz399001','sz399006'], language='cn'):
    """
    根据证券代码批量获取股票简要信息
    Returns:
    指定股票的简要信息
    """
    import requests
    import pandas as pd
    from westat.utils import regexp_like

    if isinstance(code, str):
        code = code.split()

    s = ''
    for c in code:
        if len(c)==6 and regexp_like(c[:3],'600|601|603|605|900'):
            c = 'sh' + c
        elif len(c)==6 and regexp_like(c[:3],'000|002|003|200|300'):
            c = 'sz' + c
        elif len(c)==5:
            c = 'hk' + c
        elif not regexp_like(c[:2],'sh|sz|hk') and regexp_like(c.lower(),'[a-z].+') and not regexp_like(c.lower(),'us'):
            c = 'us' + c.replace('.','')
        else:
            c = c

        s = s + 's_' + c + ','

    code_list = s[:-1]
    response = requests.get('http://qt.gtimg.cn/q=' + code_list)

    if response.status_code == 200:

        text = response.text

        if regexp_like(text, 'none_match'):
            print('未匹配到任何数据！')
        else:
            data = text.split(';')
            df = []
            for d in data:
                if len(d) > 1:
                    data = d.split('"')[1].split('~')
                    df.append(data)

            result = pd.DataFrame(df)

            result.drop([8, 10], axis=1, inplace=True)
            result.columns = ['exchange', 'name', 'code', 'now', 'change', 'change_pct', 'volume', 'amount',
                              'market_cap']
            result['change'] = pd.to_numeric(result['change'])
            result['change_pct'] = pd.to_numeric(result['change_pct'])
            result['volume'] = pd.to_numeric(result['volume'])
            result['amount'] = pd.to_numeric(result['amount'])
            result['market_cap'] = pd.to_numeric(result['market_cap'])

            if language == 'cn':
                result.rename(columns={'exchange': '交易所', 'name': '证券简称', 'code': '证券代码', 'now': '现价',
                                       'change': '涨跌额', 'change_pct': '涨跌幅', 'volume': '成交量',
                                       'amount': '成交额',
                                       'market_cap': '总市值'}, inplace=True)

            return result
