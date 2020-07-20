# 从网站获取所有历史页面的链接
# 构造类似'http://www.tianqihoubao.com/lishi/nantong/month/202006.html'链接列表格式
from requests_html import HTMLSession   # 最新的爬虫工具requests-html
import re                               # 正则表达式
from xpinyin import Pinyin              # 拼音库


def get_url(city):
    # 获取city下历史月份页面中的所有链接
    session = HTMLSession()
    url_city = 'http://www.tianqihoubao.com/lishi/' + city + '.html'
    r = session.get(url_city)
    link_all = r.html.absolute_links
    regex = '[0-9]{6}'
    url_months = [x for x in link_all if re.compile(regex).findall(x)]
    return(url_months)

if __name__ == '__main__':
    # 输入城市名称，如果输入的中文，则转换成拼音
    city=input('请输入城市名称：')
    p=Pinyin()
    for ch in city:
        if '\u4e00' <= ch <= '\u9fff':
            city = p.get_pinyin(city, '')
    # 调用模块
    print('开始获取链接......')
    url_months = get_url(city)
    if url_months == []:
        print('没有成功获取链接（城市名称错或其它原因）')
    else:
        print(url_months)
