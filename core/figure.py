"""
邢不行｜策略分享会
选币策略框架𝓟𝓻𝓸

版权所有 ©️ 邢不行
微信: xbx1717

本代码仅供个人学习使用，未经授权不得复制、修改或用于商业用途。

Author: 邢不行
"""
import os
import platform
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
import webbrowser
from matplotlib import pyplot as plt
from plotly import subplots
from plotly.offline import plot
from plotly.subplots import make_subplots

from core.utils.path_kit import get_file_path


def show_without_plot_native_show(fig, save_path: Path):
    save_path = save_path.absolute()
    print('⚠️ 因为新版pycharm默认开启sci-view功能，导致部分同学会在.show()的时候假死')
    print(f'因此我们会先保存HTML到: {save_path}, 然后调用默认浏览器打开')
    fig.write_html(save_path)

    """
    跨平台在默认浏览器中打开 URL 或文件
    """
    system_name = platform.system()  # 检测操作系统
    if system_name == "Darwin":  # macOS
        os.system(f'open "" "{save_path}"')
    elif system_name == "Windows":  # Windows
        os.system(f'start "" "{save_path}"')
    elif system_name == "Linux":  # Linux
        os.system(f'xdg-open "" "{save_path}"')
    else:
        # 如果不确定操作系统，尝试使用 webbrowser 模块
        webbrowser.open(save_path)


def draw_equity_curve_plotly(df, data_dict, date_col=None, right_axis=None, pic_size=None, chg=False, title=None,
                             path=get_file_path('data', 'pic.html', as_path_type=True), show=True, desc=None,
                             show_subplots=False):
    """
    绘制策略曲线
    :param df: 包含净值数据的df
    :param data_dict: 要展示的数据字典格式：｛图片上显示的名字:df中的列名｝
    :param date_col: 时间列的名字，如果为None将用索引作为时间列
    :param right_axis: 右轴数据 ｛图片上显示的名字:df中的列名｝
    :param pic_size: 图片的尺寸
    :param chg: datadict中的数据是否为涨跌幅，True表示涨跌幅，False表示净值
    :param title: 标题
    :param path: 图片路径
    :param show: 是否打开图片
    :param desc: 图片描述
    :param show_subplots: 是否展示子图，显示多空仓位比例
    :return:
    """
    if pic_size is None:
        pic_size = [1500, 920]

    draw_df = df.copy()

    # 设置时间序列
    if date_col:
        time_data = draw_df[date_col]
    else:
        time_data = draw_df.index

    # 创建子图
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,  # 共享 x 轴，主，子图共同变化
        vertical_spacing=0.03,  # 减少主图和子图之间的间距
        row_heights=[0.8, 0.1, 0.1],  # 主图高度占 80%，子图高度占 10%
        specs=[[{"secondary_y": True}], [{"secondary_y": False}], [{"secondary_y": False}]]
    )

    # 主图：绘制左轴数据
    for key in data_dict:
        if chg:
            draw_df[data_dict[key]] = (draw_df[data_dict[key]] + 1).fillna(1).cumprod()
        fig.add_trace(go.Scatter(x=time_data, y=draw_df[data_dict[key]], name=key), row=1, col=1)

    # 绘制右轴数据
    if right_axis:
        key = list(right_axis.keys())[0]
        fig.add_trace(go.Scatter(x=time_data, y=draw_df[right_axis[key]], name=key + '(右轴)',
                                 marker=dict(color='rgba(220, 220, 220, 0.8)'),
                                 # marker_color='orange',
                                 opacity=0.1, line=dict(width=0),
                                 fill='tozeroy',
                                 yaxis='y2'))  # 标明设置一个不同于trace1的一个坐标轴
        for key in list(right_axis.keys())[1:]:
            fig.add_trace(go.Scatter(x=time_data, y=draw_df[right_axis[key]], name=key + '(右轴)',
                                     #  marker=dict(color='rgba(220, 220, 220, 0.8)'),
                                     opacity=0.1, line=dict(width=0),
                                     fill='tozeroy',
                                     yaxis='y2'))  # 标明设置一个不同于trace1的一个坐标轴

    if show_subplots:
        # 子图：按照 matplotlib stackplot 风格实现堆叠图
        # 最下面是多头仓位占比
        fig.add_trace(go.Scatter(
            x=time_data,
            y=draw_df['long_cum'],
            mode='lines',
            line=dict(width=0),
            fill='tozeroy',
            fillcolor='rgba(30, 177, 0, 0.6)',
            name='多头仓位占比',
            hovertemplate="多头仓位占比: %{customdata:.4f}<extra></extra>",
            customdata=draw_df['long_pos_ratio']  # 使用原始比例值
        ), row=2, col=1)

        # 中间是空头仓位占比
        fig.add_trace(go.Scatter(
            x=time_data,
            y=draw_df['short_cum'],
            mode='lines',
            line=dict(width=0),
            fill='tonexty',
            fillcolor='rgba(255, 99, 77, 0.6)',
            name='空头仓位占比',
            hovertemplate="空头仓位占比: %{customdata:.4f}<extra></extra>",
            customdata=draw_df['short_pos_ratio']  # 使用原始比例值
        ), row=2, col=1)

        # 最上面是空仓占比
        fig.add_trace(go.Scatter(
            x=time_data,
            y=draw_df['empty_cum'],
            mode='lines',
            line=dict(width=0),
            fill='tonexty',
            fillcolor='rgba(0, 46, 77, 0.6)',
            name='空仓占比',
            hovertemplate="空仓占比: %{customdata:.4f}<extra></extra>",
            customdata=draw_df['empty_ratio']  # 使用原始比例值
        ), row=2, col=1)

        # 子图：右轴绘制 long_short_ratio 曲线
        fig.add_trace(go.Scatter(
            x=time_data,
            y=draw_df['symbol_long_num'],
            name='多头选币数量',
            mode='lines',
            line=dict(color='rgba(30, 177, 0, 0.6)', width=2)
        ), row=3, col=1)

        fig.add_trace(go.Scatter(
            x=time_data,
            y=draw_df['symbol_short_num'],
            name='空头选币数量',
            mode='lines',
            line=dict(color='rgba(255, 99, 77, 0.6)', width=2)
        ), row=3, col=1)

    fig.update_layout(template="none", width=pic_size[0], height=pic_size[1], title_text=title,
                      hovermode="x unified", hoverlabel=dict(bgcolor='rgba(255,255,255,0.5)', ),
                      annotations=[
                          dict(
                              text=desc,
                              xref='paper',
                              yref='paper',
                              x=0.5,
                              y=1.05,
                              showarrow=False,
                              font=dict(size=12, color='black'),
                              align='center',
                              bgcolor='rgba(255,255,255,0.8)',
                          )
                      ]
                      )
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=[
                    dict(label="线性 y轴",
                         method="relayout",
                         args=[{"yaxis.type": "linear"}]),
                    dict(label="Log y轴",
                         method="relayout",
                         args=[{"yaxis.type": "log"}]),
                ])],
    )
    plot(figure_or_data=fig, filename=str(path), auto_open=False)

    fig.update_yaxes(
        showspikes=True, spikemode='across', spikesnap='cursor', spikedash='solid', spikethickness=1,  # 峰线
    )
    fig.update_xaxes(
        showspikes=True, spikemode='across+marker', spikesnap='cursor', spikedash='solid', spikethickness=1,  # 峰线
    )

    # 打开图片的html文件，需要判断系统的类型
    if show:
        show_without_plot_native_show(fig, path)


def plotly_plot(draw_df: pd.DataFrame, save_dir: str | Path, name: str):
    rows = len(draw_df.columns)
    s = (1 / (rows - 1)) * 0.5
    fig = subplots.make_subplots(rows=rows, cols=1, shared_xaxes=True, shared_yaxes=True, vertical_spacing=s)

    for i, col_name in enumerate(draw_df.columns):
        trace = go.Bar(x=draw_df.index, y=draw_df[col_name], name=f"{col_name}")
        fig.add_trace(trace, i + 1, 1)
        # 更新每个子图的x轴属性
        fig.update_xaxes(showticklabels=True, row=i + 1, col=1)  # 旋转x轴标签以避免重叠

    # 更新每个子图的y轴标题
    for i, col_name in enumerate(draw_df.columns):
        fig.update_xaxes(title_text=col_name, row=i + 1, col=1)

    fig.update_layout(height=200 * rows, showlegend=True, title_text=name)
    show_without_plot_native_show(fig, get_file_path(save_dir, f"{name}.html", as_path_type=True))


def mat_heatmap(draw_df: pd.DataFrame, name: str):
    sns.set_theme()  # 设置一下展示的主题和样式
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
    plt.title(name)  # 设置标题
    sns.heatmap(draw_df, annot=True, xticklabels=draw_df.columns, yticklabels=draw_df.index, fmt='.2f')  # 画图
    plt.show()
