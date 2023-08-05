# -*-coding:utf-8 -*-
import numpy as np
import os

td_type_map = {
    1: np.bool_,
    2: np.int8,
    3: np.int16,
    4: np.int32,
    5: np.int64,
    6: np.float_,
    7: np.double,
    8: np.string_,
    9: 'datetime64[ns]',
    10: np.string_
}

token = os.environ.get('TD_TOKEN')
url = os.environ.get('TD_URL')

td_columns = {
    "cn_d1":  ["code", "time", "open", "close", "low", "high", "volume", "money",
               "factor", "high_limit", "low_limit", "avg", "pre_close",
               "paused", "update_date"],
    "cn_m1": ["code", "time", "open", "close", "low", "high", "volume", "money",
              "factor", "high_limit", "low_limit", "avg", "pre_close",
              "paused", "update_date"],
    "cn_m5": ["code", "time", "open", "close", "low", "high", "volume", "money",
              "factor", "high_limit", "low_limit", "avg", "pre_close",
              "paused", "update_date"],
    "cn_m15": ["code", "time", "open", "close", "low", "high", "volume", "money",
               "factor", "high_limit", "low_limit", "avg", "pre_close",
               "paused", "update_date"],
    "cn_m30": ["code", "time", "open", "close", "low", "high", "volume", "money",
               "factor", "high_limit", "low_limit", "avg", "pre_close",
               "paused", "update_date"],
    "cn_m60": ["code", "time", "open", "close", "low", "high", "volume", "money",
               "factor", "high_limit", "low_limit", "avg", "pre_close",
               "paused", "update_date"],
    "cn_tick":  ["code",  "time",  "current",  "high",  "low",  "volume",  "money",
                 "a1_v", "a2_v", "a3_v", "a4_v", "a5_v", "a1_p", "a2_p",
                 "a3_p", "a4_p", "a5_p",  "b1_v",  "b2_v",  "b3_v",  "b4_v",  "b5_v",
                 "b1_p",  "b2_p",  "b3_p",  "b4_p",  "b5_p"],
    "us_d1": ["code", "time", "open", "high", "low", "close", "pre_close", "avg",
              "volume", "money", "unix_timestamp", "update_date"],
    "us_m1": ["code", "time", "open", "high", "low", "close", "pre_close", "avg",
              "volume", "money", "unix_timestamp", "update_date"],
    "us_m5": ["code", "time", "open", "high", "low", "close", "pre_close", "avg",
              "volume", "money", "unix_timestamp", "update_date"],
    "us_m15": ["code", "time", "open", "high", "low", "close", "pre_close", "avg",
              "volume", "money", "unix_timestamp", "update_date"],
    "us_m30": ["code", "time", "open", "high", "low", "close", "pre_close", "avg",
              "volume", "money", "unix_timestamp", "update_date"],
    "us_m60": ["code", "time", "open", "high", "low", "close", "pre_close", "avg",
              "volume", "money", "unix_timestamp", "update_date"]
}
