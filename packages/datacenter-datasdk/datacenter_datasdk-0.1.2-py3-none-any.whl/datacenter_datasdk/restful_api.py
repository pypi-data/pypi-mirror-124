import requests
import json
import pandas as pd
import datetime
from .settings import td_columns, url, token, td_type_map
from .verify import verify_args


def format_date_param(t):
    if isinstance(t, datetime.date) or isinstance(t, str):
        return f"{str(t)} 00:00:00"
    else:
        return t


def get_int_code(code, region):
    if region == 'cn':
        if 'XSHG' in code:
            code_int = int(code.strip('.XSHG')) + 1000000
        else:
            code_int = int(code.strip('.XSHE')) + 2000000
    elif region == 'us':
        code_int = int(code)
    else:
        code_int = int(code)
    return code_int


def get_str_code(code_int, region):
    if region == 'cn':
        if 2000000 > code_int > 1000000:
            code = '{:06d}.XSHG'.format(code_int-1000000)
        else:
            code = '{:06d}.XSHE'.format(code_int-2000000)
    elif region == 'us':
        code = str(code_int)
    else:
        code = str(code_int)
    return code


@verify_args(check={'code': (str, list),
                    'region': str,
                    'frequency': str,
                    'start_date': (datetime.datetime, datetime.date, str),
                    'end_date': (datetime.datetime, datetime.date, str)
                    }
             )
def get_price(code: str or list,
              region: str,
              frequency: str,
              start_date: datetime.datetime or datetime.date or str = datetime.datetime(2005, 1, 1),
              end_date: datetime.datetime or datetime.date or str = datetime.datetime.today(
              ).replace(hour=0, minute=0, second=0, microsecond=0)
              ):
    """
    get kline data, include daily, minute and tick

    code: str or list, single code or multi code as list
    region: str, 'cn' or 'us'
    frequency: str, represent frequency of kline, 'd1', 'm1', 'm5', 'm15', 'm30', 'm60' and 'tick'(only in cn)
    start_date, datetime.datetime or datetime.date or str, start time of data, default '2005-01-01'
    end_date, datetime.datetime or datetime.date or str, end time of data, default 0 o'clock of today 
    """
    if isinstance(code, list):
        codes = tuple([get_int_code(c, region) for c in code])
        code_sql = f'code in {codes}'
    else:
        code_int = get_int_code(code, region)
        code_sql = f'code={code_int}'
    start_date = format_date_param(start_date)
    end_date = format_date_param(end_date)
    sql = f"select * from {region}_{frequency}.{region}_st_{frequency} where ({code_sql}) and (time between '{str(start_date)}' and '{str(end_date)}');"
    r = requests.post(url,
                      headers={'Authorization': f'Basic {token}'},
                      data=sql
                      )
    res = json.loads(r.text)
    column_meta = res['column_meta']
    columns = [i[0] for i in column_meta]
    types = [td_type_map.get(i[1]) for i in column_meta]
    data = res['data']
    rows = res['rows']
    if rows==5000000:
        print('单次查询条数不能大于500W条, 此次返回仅500W条')
    df = pd.DataFrame(data=data, columns=columns)
    if frequency != 'tick':
        df = df[df.open!=0]
    df['time'] = df['time'].apply(
        lambda x: datetime.datetime.fromtimestamp(x/1000))
    if frequency != 'tick':
        df['update_date'] = df['update_date'].apply(
            lambda x: datetime.datetime.fromtimestamp(x/1000))

    for t, c in zip(types, columns):
        df[c] = df[c].astype(t)
    df['code'] = df['code'].apply(lambda x: get_str_code(x, region))
    df = df[td_columns.get(f'{region}_{frequency}')]
    return df
