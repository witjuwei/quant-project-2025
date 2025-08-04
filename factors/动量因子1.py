"""
邢不行™️ 策略分享会
仓位管理框架

版权所有 ©️ 邢不行
微信: xbx6660

本代码仅供个人学习使用，未经授权不得复制、修改或用于商业用途。

Author: 邢不行
"""


def signal(*args):
    df = args[0]
    n = args[1]
    factor_name = args[2]

    source_cls = df.columns.tolist()

    df['max_high'] = df['high'].rolling(n, min_periods=1).max()
    df['min_low'] = df['low'].rolling(n, min_periods=1).min()

    df[factor_name] = (df['close'] - df['min_low']) / (df['max_high'] - df['min_low'])

    df.drop(columns=list(set(df.columns.values).difference(set(source_cls + [factor_name]))), inplace=True)

    return df


def signal_multi_params(df, param_list) -> dict:
    ret = dict()
    for param in param_list:
        n = int(param)
        max_high = df['high'].rolling(n, min_periods=1).max()
        min_low = df['low'].rolling(n, min_periods=1).min()
        factor = (df['close'] - min_low) / (max_high - min_low)
        ret[str(param)] = factor
    return ret
