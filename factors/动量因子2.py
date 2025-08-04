# -*- coding: utf-8 -*-
"""
中性策略框架 | 邢不行 | 2024分享会
author: 邢不行
微信: xbx6660
"""


def signal(*args):
    df = args[0]
    n = args[1]
    factor_name = args[2]

    source_cls = df.columns.tolist()

    df['tp'] = (df['close'] + df['high'] + df['low']) / 3
    df['tp2'] = df['tp'].ewm(span=n, adjust=False).mean()
    df['diff'] = df['tp'] - df['tp2']
    df['min'] = df['diff'].rolling(n, min_periods=1).min()
    df['max'] = df['diff'].rolling(n, min_periods=1).max()

    df[factor_name] = (df['diff'] - df['min']) / (df['max'] - df['min'])

    df.drop(columns=list(set(df.columns.values).difference(set(source_cls + [factor_name]))), inplace=True)

    return df


def signal_multi_params(df, param_list) -> dict:
    tp = (df['close'] + df['high'] + df['low']) / 3
    ret = dict()
    for param in param_list:
        n = int(param)
        tp_ma = tp.ewm(span=n, adjust=False).mean()
        diff = tp - tp_ma
        min = diff.rolling(n, min_periods=1).min()
        max = diff.rolling(n, min_periods=1).max()
        factor = (diff - min) / (max - min)
        ret[str(param)] = factor
    return ret
