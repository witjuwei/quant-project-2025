# -*- coding: utf-8 -*-
"""
选币策略框架 | 邢不行 | 2024分享会
author: 邢不行
微信: xbx6660
"""


def signal_multi_params(df, param_list) -> dict:
    ret = dict()
    for param in param_list:
        n = int(param)
        ret[str(param)] = (df['taker_buy_quote_asset_volume'] * 2 - df['quote_volume']).rolling(n, min_periods=2).std()
    return ret
