"""
邢不行｜策略分享会
选币策略框架𝓟𝓻𝓸

版权所有 ©️ 邢不行
微信: xbx1717

本代码仅供个人学习使用，未经授权不得复制、修改或用于商业用途。

Author: 邢不行
"""

import os
from pathlib import Path

from core.utils.path_kit import get_folder_path

# ====================================================================================================
# ** 数据配置 **
# ====================================================================================================
# 数据存储路径，填写绝对路径
# 使用官方准备的预处理数据，专门用于本框架回测使用，大幅提高速度
# 现货和合约1小时预处理数据（pkl格式）：https://www.quantclass.cn/data/coin/coin-binance-spot-swap-preprocess-pkl-1h
# 格式可以是：pre_data_path = r'D:\data\coin-binance-spot-swap-preprocess-pkl-1h'
pre_data_path = r'D:\DATA2025\coin-binance-spot-swap-preprocess-pkl-1h'


# ** 额外数据 **
# 当且仅当用到额外数据的因子时候，该配置才需要配置，且自动生效
data_source_dict = {
    # 数据源的标签: ('加载数据的函数名', '数据存储的绝对路径')
    # 说明：数据源的标签,需要与因子文件中的 extra_data_dict 中的 key 保持一致，数据存储的路径需要表达清楚
    "coin-cap": ('load_coin_cap', r'D:\DATA2025\coin-cap',)
}

# ====================================================================================================
# ** 回测策略细节配置 **
# 需要配置需要的策略以及遍历的参数范围
# ====================================================================================================
# start_date = '2021-01-01'  # 回测开始时间
# end_date = '2024-12-24 23:00:00'  # 回测结束时间

start_date = '2024-01-01'  # 回测开始时间
end_date = '2024-05-31 23:00:00'  # 回测结束时间

# ====================================================================================================
# ** 策略配置 **
# 需要配置需要的策略以及遍历的参数范围
# ====================================================================================================
backtest_name = '浪淘沙策略'  # 回测的策略组合的名称。可以自己任意取。一般建议，一个回测组，就是实盘中的一个账户。
"""策略配置"""
strategy_list = [
    # =====1.多头(资金占比0.5)
    # === 1.1大学生纯多策略+后置过滤(资金占比0.25)
    {
        # 策略名称。与strategy目录中的策略文件名保持一致。
        "strategy": "Strategy_大学生",
        "offset_list": [17],
        "hold_period": "24H",
        "is_use_spot": True,
        # 资金权重。程序会自动根据这个权重计算你的策略占比，具体可以看1.8的直播讲解
        'cap_weight': 0.25,
        'long_cap_weight': 1,
        'short_cap_weight': 0,
        'long_select_coin_num': 0.1,
        'short_select_coin_num': 0,
        # 选币因子信息列表，用于`2_选币_单offset.py`，`3_计算多offset资金曲线.py`共用计算资金曲线
        "factor_list": [
            ('CirculatingMcap', True, 1, 1),  # 多头因子名（和factors文件中相同），排序方式，参数，权重。
        ],
        "filter_list": [
            ('ZfStd', 12, 'pct:<0.8')
        ],
        "filter_list_post": [
            ('VolumeMeanQ', 840, 'val:>0.5')
        ],
        "use_custom_func": False  # 使用系统内置因子计算、过滤函数
    },
    # =====2.空头(资金占比0.5)
    # ===2.1 先使用QuoteVolumeMean，再使用动量因子，资金占比为空头的0.6(总资金的0.3)
    {
        # 策略名称。与strategy目录中的策略文件名保持一致。
        "strategy": "Strategy_黄果树系列1",
        "offset_list": [16],  # 只选部分offset[1, 3, 6]；
        "hold_period": "24H",  # 小时级别可选1H到24H；也支持1D交易日级别
        "is_use_spot": False,  # 多头支持交易现货；
        # 资金权重。程序会自动根据这个权重计算你的策略占比
        'cap_weight': 0.3,
        'long_cap_weight': 0,  # 可以多空比例不同，多空不平衡对策略收益影响大
        'short_cap_weight': 1,
        # 选币数量
        'long_select_coin_num': 0,  # 可适当减少选币数量，对策略收益影响大
        'short_select_coin_num': 0.5,  # 四种形式：整数， 小数，'long_nums', 区间选币：(0.1, 0.2), (1, 3)
        # 选币因子信息列表，用于2_选币_单offset.py，3_计算多offset资金曲线.py共用计算资金曲线
        "factor_list": [
            ('Cci', False, 648, 1),  # 多空因子名（和factors文件中相同），排序方式，参数，权重。支持多空分离，多空选币因子不一样；
        ],
        "filter_list": [
            ('QuoteVolumeMean', 648, 'pct:<0.2', False),  # 后置过滤filter_list_post，三种形式：pct, rank, val；支持多空分离，多空过滤因子不一样；
        ],
        "filter_list_post": [
            ('ZfMeanQ', 648, 'val:<0.5'),  # 后置过滤filter_list_post，三种形式：pct, rank, val；支持多空分离，多空过滤因子不一样；
        ],
    },
    # ===2.2 先使用动量因子，再使用QuoteVolumeMean，资金占比为空头的0.2(总资金的0.1)
    {
        # 策略名称。与strategy目录中的策略文件名保持一致。
        "strategy": "Strategy_黄果树系列2",
        "offset_list": [15],  # 只选部分offset[1, 3, 6]；
        "hold_period": "24H",  # 小时级别可选1H到24H；也支持1D交易日级别
        "is_use_spot": False,  # 多头支持交易现货；
        # 资金权重。程序会自动根据这个权重计算你的策略占比
        'cap_weight': 0.1,
        'long_cap_weight': 0,  # 可以多空比例不同，多空不平衡对策略收益影响大
        'short_cap_weight': 1,
        # 选币数量
        'long_select_coin_num': 0,  # 可适当减少选币数量，对策略收益影响大
        'short_select_coin_num': 0.5,  # 四种形式：整数， 小数，'long_nums', 区间选币：(0.1, 0.2), (1, 3)
        # 选币因子信息列表，用于2_选币_单offset.py，3_计算多offset资金曲线.py共用计算资金曲线
        "factor_list": [
            ('QuoteVolumeMean', True, 432, 1),  # 多空因子名（和factors文件中相同），排序方式，参数，权重。支持多空分离，多空选币因子不一样；
        ],
        "filter_list": [
            ('MinMax', 432, 'pct:<0.2'),  # 后置过滤filter_list_post，三种形式：pct, rank, val；支持多空分离，多空过滤因子不一样；
        ],
        "filter_list_post": [
            ('VolumeMeanQ', 432, 'val:<0.5'),  # 后置过滤filter_list_post，三种形式：pct, rank, val；支持多空分离，多空过滤因子不一样；
        ],
    },
    # ===2.3 同时使用QuoteVolumeMean和动量因子过滤，全选剩下的币种，资金占比为空头的0.2(总资金的0.1)
    {
        # 策略名称。与strategy目录中的策略文件名保持一致。
        "strategy": "Strategy_黄果树系列3",
        "offset_list": [7],  # 只选部分offset[1, 3, 6]；
        "hold_period": "24H",  # 小时级别可选1H到24H；也支持1D交易日级别
        "is_use_spot": False,  # 多头支持交易现货；
        # 资金权重。程序会自动根据这个权重计算你的策略占比
        'cap_weight': 0.1,
        'long_cap_weight': 0,  # 可以多空比例不同，多空不平衡对策略收益影响大
        'short_cap_weight': 1,
        # 选币数量
        'long_select_coin_num': 0,  # 可适当减少选币数量，对策略收益影响大
        'short_select_coin_num': 999,  # 四种形式：整数， 小数，'long_nums', 区间选币：(0.1, 0.2), (1, 3)
        # 选币因子信息列表，用于2_选币_单offset.py，3_计算多offset资金曲线.py共用计算资金曲线
        "factor_list": [
            ('QuoteVolumeMean', True, 1, 1),  # 多空因子名（和factors文件中相同），排序方式，参数，权重。支持多空分离，多空选币因子不一样；
        ],
        "filter_list": [
            ('BiasQ', 576, 'pct:<0.15'),  # 后置过滤filter_list_post，三种形式：pct, rank, val；支持多空分离，多空过滤因子不一样；
            ('QuoteVolumeMean', 576, 'pct:<0.15', False),
        ],
        "filter_list_post": [
            ('VolumeMeanQ', 576, 'val:<0.5'),  # 后置过滤filter_list_post，三种形式：pct, rank, val；支持多空分离，多空过滤因子不一样；
        ],
    },
]

min_kline_num = 168  # 最少上市多久，不满该K线根数的币剔除，即剔除刚刚上市的新币。168：标识168个小时，即：7*24
black_list = ['BTC-USDT', 'ETH-USDT']  # 拉黑名单，永远不会交易。不喜欢的币、异常的币。例：LUNA-USDT, 这里与实盘不太一样，需要有'-'
white_list = []  # 如果不为空，即只交易这些币，只在这些币当中进行选币。例：LUNA-USDT, 这里与实盘不太一样，需要有'-'

# ====================================================================================================
# ** 回测模拟下单配置 **
# ====================================================================================================
account_type = '普通账户'  # '统一账户'或者'普通账户'
initial_usdt = 1_0000  # 初始资金
leverage = 1  # 杠杆数。我看哪个赌狗要把这里改成大于1的。高杠杆如梦幻泡影。不要想着一夜暴富，脚踏实地赚自己该赚的钱。
margin_rate = 0.05  # 维持保证金率，净值低于这个比例会爆仓

swap_c_rate = 6 / 10000  # 合约手续费(包含滑点)
spot_c_rate = 1 / 1000  # 现货手续费(包含滑点)

swap_min_order_limit = 5  # 合约最小下单量。最小不能低于5
spot_min_order_limit = 10  # 现货最小下单量。最小不能低于10

avg_price_col = 'avg_price_1m'  # 用于模拟计算的平均价，预处理数据使用的是1m，'avg_price_1m'表示1分钟的均价, 'avg_price_5m'表示5分钟的均价。

# ====================================================================================================
# ** 回测全局设置 **
# 这些设置是客观事实，基本不会影响到回测的细节
# ====================================================================================================
job_num = max(os.cpu_count() - 1, 1)  # 回测并行数量

# ==== factor_col_limit 介绍 ====
factor_col_limit = 64  # 内存优化选项，一次性计算多少列因子。64是 16GB内存 电脑的典型值
# - 数字越大，计算速度越快，但同时内存占用也会增加。
# - 该数字是在 "因子数量 * 参数数量" 的基础上进行优化的。
#   - 例如，当你遍历 200 个因子，每个因子有 10 个参数，总共生成 2000 列因子。
#   - 如果 `factor_col_limit` 设置为 64，则计算会拆分为 ceil(2000 / 64) = 32 个批次，每次最多处理 64 列因子。
# - 对于16GB内存的电脑，在跑含现货的策略时，64是一个合适的设置。
# - 如果是在16GB内存下跑纯合约策略，则可以考虑将其提升到 128，毕竟数值越高计算速度越快。
# - 以上数据仅供参考，具体值会根据机器配置、策略复杂性、回测周期等有所不同。建议大家根据实际情况，逐步测试自己机器的性能极限，找到适合的最优值。


# ====================================================================================================
# ** 全局变量及自动化 **
# 没事别动这边的东西 :)
# ====================================================================================================
raw_data_path = Path(pre_data_path)
# 现货数据路径
spot_path = raw_data_path / 'spot_dict.pkl'
# 合约数据路径
swap_path = raw_data_path / 'swap_dict.pkl'

# 回测结果数据路径。用于发帖脚本使用
backtest_path = Path(get_folder_path('data', '回测结果'))
backtest_iter_path = Path(get_folder_path('data', '遍历结果'))

# 稳定币信息，不参与交易的币种
stable_symbol = ['BKRW', 'USDC', 'USDP', 'TUSD', 'BUSD', 'FDUSD', 'DAI', 'EUR', 'GBP', 'USBP', 'SUSD', 'PAXG', 'AEUR',
                 'EURI']

if len(pre_data_path) == 0:
    print('⚠️ 请先准确配置预处理数据的位置（pre_data_path）。建议直接复制绝对路径，并且粘贴给 pre_data_path')
    exit()

if (not spot_path.exists()) or (not swap_path.exists()):
    print(f'⚠️ 预处理数据不存在，请检查配置 `pre_data_path`: {pre_data_path}')
    exit()
