# -*- coding:utf-8 -*-
# flask/bin/python
# Date:2017-12-28
# Author:Pboy Tom:)
# QQ:360254363/pboy@sina.cn
# E-mail:cylcjy009@gmail.com
# Website:www.pboy8.top pboy8.taobao.com
# Desc: Create a Gaode's heatmap from nginx logs or iis logs...(By default: Nginx access log)
# Project home: https://github.com/tompboy/HeatMap_Gaode
# Version:V 0.01

import pandas as pd
import pygeoip
import types
import os

DIR='/home/getip'
#判断/home/getip目录是否存在，不存在则使用当前目录
if os.path.exists(DIR):
	DIR=DIR
else:
	DIR=os.getcwd()

#指定log所在目录
LOG_DIR='/usr/local/nginx/logs/access.log'
os.environ['DIR']=str(DIR)
os.environ['LOG_DIR']=str(LOG_DIR)

#os.system(r"echo $DIR")
#清空文件
os.system(r">$DIR/iplist.csv")
#筛选IP
os.system(r"cat $LOG_DIR |awk '{print $1}' > $DIR/iplist.csv")
#清空文件
os.system(r">$DIR/app/templates/index.html")
#IP转经纬度
GI = pygeoip.GeoIP(r'$DIR/flask/lib/python2.7/site-packages/GeoLiteCity.dat',pygeoip.MEMORY_CACHE)
f = open('$DIR/app/templates/index.html','w+')
txt1 = '''
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no, width=device-width">
    <title>热力图</title>
    <link rel="stylesheet" href="http://cache.amap.com/lbs/static/main1119.css"/>
    <script src="http://webapi.amap.com/maps?v=1.4.2&key=您申请的key值"></script>
    <script type="text/javascript" src="http://cache.amap.com/lbs/static/addToolbar.js"></script>
    
</head>
<body>
<div id="container"></div>
<div class="button-group">
    <input type="button" class="button" value="显示热力图" onclick="heatmap.show()"/>
    <input type="button" class="button" value="关闭热力图" onclick="heatmap.hide()"/>
</div>
</body>
</html>
<script>
    var map = new AMap.Map("container", {
        resizeEnable: true,
        center: [116.418261, 39.921984],
        zoom: 11
    });
    if (!isSupportCanvas()) {
        alert('热力图仅对支持canvas的浏览器适用,您所使用的浏览器不能使用热力图功能,请换个浏览器试试~')
    }
    var heatmapData =[
'''
txt2 = '''
];
   map.plugin(["AMap.Heatmap"], function() {
        //初始化heatmap对象
        heatmap = new AMap.Heatmap(map, {
            radius: 25, //给定半径
            opacity: [0, 0.8]
            /*,gradient:{
             0.5: 'blue',
             0.65: 'rgb(117,211,248)',
             0.7: 'rgb(0, 255, 0)',
             0.9: '#ffea00',
             1.0: 'red'
             }*/
        });
        //设置数据集：该数据为北京部分“公园”数据
        heatmap.setDataSet({
            data: heatmapData,
            max: 100
        });
    });
    //判断浏览区是否支持canvas
    function isSupportCanvas() {
        var elem = document.createElement('canvas');
        return !!(elem.getContext && elem.getContext('2d'));
    }
</script>



'''
#ip_latlng = []
f.write(txt1)
def getLocal(ip):
    if type(ip) != types.StringType:
        #print ip
        return
    location = GI.record_by_addr(ip)
    if location is None:
        #print ip
        return
    lng = location['longitude']
    lat = location['latitude']
    str_temp = '{"lat":' + str(lat) + ',"lng":' + str(lng) + '},\n'
    f.write(str_temp)

if __name__ == '__main__':
    iplist = open('$DIR/iplist.csv','r')
    line = iplist.readline()
    while line:
        getLocal(line)
        line = iplist.readline()
    iplist.close()
    f.write(txt2)
