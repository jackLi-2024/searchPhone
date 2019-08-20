#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:Lijiacai
Email:1050518702@qq.com
===========================================
CopyRight@JackLee.com
===========================================
"""

import os
import sys
import json

import requests

try:
    reload(sys)
    sys.setdefaultencoding("utf8")
except:
    pass

from rest_framework.views import APIView
from resource.common import output
from resource.common.util import DictToObj
from resource.extension.log import logging
from resource.common.catch_exception import catch_exception
from django.shortcuts import render
from itertools import product



class IndexView(APIView):
    @catch_exception
    def get(self, request, *args, **kwargs):
        return render(request, "index.html")

    def post(self, request, *args, **kwargs):
        data = self.request.data
        phone = data.get("phone")
        city = data.get("city")
        error = ""
        if len(phone) != 11:
            error = "手机号格式错误，必须是11位"
        try:
            int(phone[:3])
        except:
            error = "电话号码前三位必须是数字"

        try:
            int(phone[-4:])
        except:
            error = "电话号码后四位必须是数字"
        try:
            if phone[0] != str(1):
                error = "电话号码格式错误，首位必须为1"
        except:
            error = "号码不能为空"

        if error:
            return render(request, "index.html", {"error": error})

        mid_data = phone[3:7]
        result = self.filter_condition(mid_data)
        data = []
        for one in result:
            data.append(phone[:3] + one + phone[7:])
        data_list = []
        index = 0
        for one in data:
            index += 1
            try:
                url = "http://opendata.baidu.com/api.php?resource_name=guishudi&query=%s" % one
                response = requests.get(url=url).json()
                cityName = response.get("data")[0].get("city")
                province = response.get("data")[0].get("prov")
                if cityName == city or not city or city in province:
                    data_list.append({"phone": one, "city": cityName, "province": province,"index":index})
            except:
                pass

        if not data_list:
            error = "没有相关数据"

        return render(request, "index.html", {"data": data_list,"error":error})

    def filter_condition(self, mid_data="0**2"):
        length = len(mid_data)
        if not length:
            return set()
        l = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        data = product(l, repeat=length)
        result = set()
        filter_c = {}
        for i in range(len(mid_data)):
            if mid_data[i] != "*":
                filter_c[i] = mid_data[i]
        for one in data:
            a = list(one)
            for i in filter_c:
                a[i] = filter_c[i]
            a = "".join(a)
            result.add(a)
        return result
