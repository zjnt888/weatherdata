# weaterdata 0.1 (爬取天气后报网数据)
## 主要模块及功能
* get_weatherurl(city)            根据city参数获取历史逐月天气页面的链接，返回一个list。
* get_weatherdata(urls)           获取含天气信息的表格，返回一个dataframe。
* to_date(series)                 将中文的XX年XX月XX日转换成日期格式
* format_weatherdata(table)       格式化天气信息表格。拆分最高最低气温，转换中文日期并设置为索引。
* plot_weatherdata(table)         根据最高最低温度画出折线趋势图。
