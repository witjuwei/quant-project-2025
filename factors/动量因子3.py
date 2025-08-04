#!/usr/bin/python3
# -*- coding: utf-8 -*-


def signal(*args):
    df = args[0]
    n = args[1]
    factor_name = args[2]

    source_cls = df.columns.tolist()

    df['ma'] = df['close'].rolling(n, min_periods=1).mean()
    df['std'] = df['close'].rolling(n, min_periods=1).std()
    df['zscore'] = (df['close'] - df['ma']) / df['std']
    df['zscore'] = df['zscore'].abs().rolling(n, min_periods=1).mean().shift()
    df['down'] = df['ma'] - df['zscore'] * df['std']

    df['diff'] = df['close'] - df['down']
    df['min'] = df['diff'].rolling(n, min_periods=1).min()
    df['max'] = df['diff'].rolling(n, min_periods=1).max()

    df[factor_name] = (df['diff'] - df['min']) / (df['max'] - df['min'])

    df.drop(columns=list(set(df.columns.values).difference(set(source_cls + [factor_name]))), inplace=True)

    return df


def signal_multi_params(df, param_list) -> dict:
    ret = dict()
    for param in param_list:
        n = int(param)
        ma = df['close'].rolling(n, min_periods=1).mean()
        std = df['close'].rolling(n, min_periods=1).std()
        zscore = (df['close'] - ma) / std
        zscore = zscore.abs().rolling(n, min_periods=1).mean().shift()
        down = ma - zscore * std

        diff = df['close'] - down
        min = diff.rolling(n, min_periods=1).min()
        max = diff.rolling(n, min_periods=1).max()

        factor = (diff - min) / (max - min)
        ret[str(param)] = factor
    return ret