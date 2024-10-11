import asyncio
import aiohttp
import pandas as pd
from lxml import etree
import sqlite3

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
           #    'Cookie': 'lianjia_uuid=9d3277d3-58e4-440e-bade-5069cb5203a4; UM_distinctid=16ba37f7160390-05f17711c11c3e-454c0b2b-100200-16ba37f716618b; _smt_uid=5d176c66.5119839a; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216ba37f7a942a6-0671dfdde0398a-454c0b2b-1049088-16ba37f7a95409%22%2C%22%24device_id%22%3A%2216ba37f7a942a6-0671dfdde0398a-454c0b2b-1049088-16ba37f7a95409%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _ga=GA1.2.1772719071.1561816174; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1561822858; _jzqa=1.2532744094467475000.1561816167.1561822858.1561870561.3; CNZZDATA1253477573=987273979-1561811144-%7C1561865554; CNZZDATA1254525948=879163647-1561815364-%7C1561869382; CNZZDATA1255633284=1986996647-1561812900-%7C1561866923; CNZZDATA1255604082=891570058-1561813905-%7C1561866148; _qzja=1.1577983579.1561816168942.1561822857520.1561870561449.1561870561449.1561870847908.0.0.0.7.3; select_city=110000; lianjia_ssid=4e1fa281-1ebf-e1c1-ac56-32b3ec83f7ca; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiMzQ2MDU5ZTQ0OWY4N2RiOTE4NjQ5YmQ0ZGRlMDAyZmFhODZmNjI1ZDQyNWU0OGQ3MjE3Yzk5NzFiYTY4ODM4ZThiZDNhZjliNGU4ODM4M2M3ODZhNDNiNjM1NzMzNjQ4ODY3MWVhMWFmNzFjMDVmMDY4NWMyMTM3MjIxYjBmYzhkYWE1MzIyNzFlOGMyOWFiYmQwZjBjYjcyNmIwOWEwYTNlMTY2MDI1NjkyOTBkNjQ1ZDkwNGM5ZDhkYTIyODU0ZmQzZjhjODhlNGQ1NGRkZTA0ZTBlZDFiNmIxOTE2YmU1NTIxNzhhMGQ3Yzk0ZjQ4NDBlZWI0YjlhYzFiYmJlZjJlNDQ5MDdlNzcxMzAwMmM1ODBlZDJkNmIwZmY0NDAwYmQxNjNjZDlhNmJkNDk3NGMzOTQxNTdkYjZlMjJkYjAxYjIzNjdmYzhiNzMxZDA1MGJlNjBmNzQxMTZjNDIzNFwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCIzMGJlNDJiN1wifSIsInIiOiJodHRwczovL2JqLmxpYW5qaWEuY29tL3p1ZmFuZy9yY28zMS8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ=='
           }

async def async_gethtml(url):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=64, verify_ssl=False)) as session:
        async with session.get(url, headers=headers) as response:
            print('获取到网页%s' % url)
            return await response.text()

async def async_gethtmls(urls):
    # 创建任务序列
    tasks = [async_gethtml(url) for url in urls]
    # 执行任务序列
    results = await asyncio.gather(*tasks)
    return results


def makeurls(city, year):
    urls = [
        f"http://lishi.tianqi.com/{city}/{year}{str(i).zfill(2)}.html" for i in range(1, 13)]
    return urls

def prasehtml(results):
    days = []
    weeks = []
    max_temp = []
    min_temp = []
    weh = []
    wind = []
    for month in range(12):
    # 取1个月html
        html = etree.HTML(results[month])
        dates = html.xpath("//ul[@class='thrui']/li/div[@class='th200']/text()")
        temps = html.xpath("//ul[@class='thrui']/li/div[@class='th140']/text()")
        temps = [temps[i:i+4] for i in range(0,len(temps),4)]
        for date in dates:
            days.append(date[:10])
            weeks.append(date[11:-1])
        for temp in temps:
            max_temp.append(temp[0][:-1])
            min_temp.append(temp[1][:-1])
            weh.append(temp[2])
            wind.append(temp[3])
    datas = pd.DataFrame({'日期': days, '星期': weeks, '最高温度': max_temp,
                        '最低温度': min_temp, '天气': weh, '风向': wind})
    print(datas)
    return(datas)

if __name__ == '__main__':
    city='nantong'
    year=2023
    urls = makeurls(city, year)
    results = asyncio.run(async_gethtmls(urls))
    datas=prasehtml(results)
    conn = sqlite3.connect('example.db')
    datas.to_sql('weathdata', conn, if_exists='append', index=False)
