# datacenter_datasdk

### INSTALL

step.1 
```
pip install datacenter-datasdk
```

step.2 set environment variable: TD_TOKEN, TD_URL, PG_STATIC (ask for admin)


### USAGE

```
from datacenter_datasdk import auth, get_price, get_trade_days, get_security_info

auth(token, password)

data = get_price('600033.XSHG', 'cn', 'm1', start_date='2010-01-01', end_date='2021-01-01')

trade_days = get_trade_days('cn', start_date='2021-01-01', count=10)

info = get_security_info('cn', '600033.XSHG')
```

### API
---
#### *get_price()*
get kline data, include daily, minute and tick

**params**

code: str or list, single code or multi code as list

region: str, 'cn' or 'us'

frequency: str, represent frequency of kline, 'd1', 'm1', 'm5', 'm15', 'm30', 'm60' and 'tick'(only in cn)

start_date, datetime.datetime or datetime.date or str, start time of data, default '2005-01-01'

end_date, datetime.datetime or datetime.date or str, end time of data, default 0 o'clock of today

**return**

dataframe

---

#### *get_trade_days()*
get trade days

**params**

region: str, 'cn' or 'us'

start_date, datetime.datetime or datetime.date or str, start time of data, default None

end_date, datetime.datetime or datetime.date or str, end time of data, default None

count, int, default None

**return**

list of date

---

#### *get_security_info()*
get security info

**params**

region: str, 'cn' or 'us'

code: str, default None (get all code info)

**return**

dataframe

---

