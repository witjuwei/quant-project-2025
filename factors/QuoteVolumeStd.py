# -*- coding: utf-8 -*-
"""
选币策略框架 | 邢不行 | 2024分享会
author: 邢不行
微信: xbx6660
"""


def signal(*args):
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df[factor_name] = df['quote_volume'].rolling(n, min_periods=1).std()

    return df


def signal_multi_params(df, param_list) -> dict:
    """
    使用同因子多参数聚合计算，可以有效提升回测、实盘 cal_factor 的速度，
    相对于 `signal` 大概提升3倍左右
    :param df: k线数据的dataframe
    :param param_list: 参数列表
    """
    ret = dict()
    for param in param_list:
        n = int(param)
        ret[str(param)] = df['quote_volume'].rolling(n, min_periods=1).std()
    return ret
