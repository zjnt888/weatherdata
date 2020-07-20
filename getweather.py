import pandas as pd
import requests
import matplotlib.pyplot as plt
from requests_html import HTMLSession  # 最新的爬虫工具requests-html
import re  # 正则表达式


# 获取每个月天气的链接
def get_weatherurl(city):
    # 获取city下历史月份页面中的所有链接
    session = HTMLSession()
    url_city = 'http://www.tianqihoubao.com/lishi/' + city + '.html'
    r = session.get(url_city)
    link_all = r.html.absolute_links
    regex = '[0-9]{6}'  # 匹配有6个数字
    url_months = [x for x in link_all if re.compile(regex).findall(x)]
    return url_months


# 获取urls列表中的天气数据并合并输出模块
def get_weatherdata(urls):
    table_months = pd.DataFrame()
    for url in urls:
        response = requests.get(url)
        # 使用pandas内置的read_html函数读取表格，合并到table_months一张大表中
        table_day = pd.read_html(response.text, header=0)[0]
        table_months = pd.concat([table_months, table_day])
    return table_months


# 处理中文日期
def to_date(series):
    res = pd.to_datetime(series, errors='coerce')
    if pd.isna(res).sum() == 0:
        return res
    else:
        parts = series.astype(str).str.split('年|月|日', expand=True)
        # 处理xxxx年xx月xx日格式的日期
        dt = pd.to_datetime(parts[0] + '/' + parts[1] + '/' + parts[2], format='%Y/%m/%d', errors='coerce')
        res = res.fillna(dt)
        if pd.isna(res).sum() == 0:
            return res
        else:
            # 处理xxxx年xx月的日期，在后面加01日
            dt = pd.to_datetime(parts[0] + '/' + parts[1] + '/01', format='%Y/%m/%d', errors='coerce')
            return res.fillna(dt)


# 处理天气表格数据模块
def format_weatherdata(table):
    # 拆分最高最低温度
    table['最高气温'] = table['气温'].map(lambda x: x.split('/')[0])
    table['最低气温'] = table['气温'].map(lambda x: x.split('/')[1])
    table['最高气温'] = table['最高气温'].str.replace('℃', '').replace(' ', '').astype(int)
    table['最低气温'] = table['最低气温'].str.replace('℃', '').replace(' ', '').astype(int)
    table = table.drop(['气温'], axis=1)
    # 处理中文日期
    table['日期'] = to_date(table['日期'])
    # 将日期列作为索引
    table.set_index(['日期'], inplace=True)
    return table


# 画最高最低温度折线图
def plot_weatherdata(table):
    # 防止中文乱码，显示中文
    plt.rcParams['font.sans-serif'] = [u'SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # 取出最高最低温度列
    dates = table.index.values
    highs = table['最高气温']
    lows = table['最低气温']
    # 画图
    fig = plt.figure(dpi=128, figsize=(8, 4))
    plt.plot(dates, highs, c='red', label='最高温度')
    plt.plot(dates, lows, c='blue', label='最低温度')
    # plt.fill_between(dates, highs, lows, facecolor='blue', alpha=0.2)
    # 设置图形格式
    plt.title('气温变化趋势图', fontsize=14)
    plt.xlabel('', fontsize=14)
    fig.autofmt_xdate()  # 绘制斜的日期标签，避免重叠
    plt.ylabel('气温(℃)', fontsize=12)
    plt.tick_params(axis='both', which='major', labelsize=10)
    plt.xticks(dates[::30])  # 修改刻度
    # 显示折线图
    plt.show()


if __name__ == '__main__':
    table1 = format_weatherdata(get_weatherdata(['http://www.tianqihoubao.com/lishi/nantong/month/201601.html',
                                                 'http://www.tianqihoubao.com/lishi/nantong/month/201602.html',
                                                 'http://www.tianqihoubao.com/lishi/nantong/month/201603.html']))
    print(table1)
    plot_weatherdata(table1)
