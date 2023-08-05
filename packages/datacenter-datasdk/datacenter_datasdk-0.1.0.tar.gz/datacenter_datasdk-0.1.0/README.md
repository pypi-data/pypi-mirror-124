# datacenter_utils

### INSTALL

step.1 
```
pip install datacenter-datasdk
```

step.2 set environment variable: TD_TOKEN, TD_URL(ask for admin)


### USAGE

```
from datacenter-datasdk import get_price

data = get_price('600033.XSHG', 'cn', 'm1', start_date='2010-01-01', end_date='2021-01-01')
```

### API

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