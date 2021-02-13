# !/usr/bin/env python
# -*- coding:utf-8 -*-

import re
from sql import query_rule
#from rexrules import Rules


class Detect:
    """
    检测web攻击行为
    user-agent, cookies, uri, body
    匹配特征
    """

    def __init__(self, http_data):
        self.uri = str(http_data.uri)
        user_agent_data = http_data.headers.get("user-agent", False)
        if user_agent_data:
            self.user_agent = str(http_data.headers["user-agent"])
        else:
            self.user_agent = ""
        if http_data.headers.get("cookie"):
            self.cookie = str(http_data.headers["cookie"])
        else:
            self.cookie = ""
        if http_data.body:
            self.body = str(http_data.body)
        else:
            self.body = ""

    def run(self):
        '''检查url user-agent cookie body'''
        result = {
            "status": False,
            "type": [],
            "url": ""
        }
        #print("uri ", self.uri)
        result["url"] = self.uri
        Rules = query_rule()
        for rule in Rules:
            res = re.compile(Rules[rule]["rex"], re.IGNORECASE).findall(self.uri)
            # print("1: ", res)
            if res:
                # print(self.uri)
                result["status"] = result["status"] or True
                result["type"].append(Rules[rule]["name"])

            res = re.compile(Rules[rule]["rex"],
                             re.IGNORECASE).findall(self.user_agent)
            # print("2: ", res)
            if res:
                result["status"] = result["status"] or True
                result["type"].append(Rules[rule]["name"])

            res = re.compile(Rules[rule]["rex"],
                             re.IGNORECASE).findall(self.cookie)
            # print("3: ", res)
            if res:
                result["status"] = result["status"] or True
                result["type"].append(Rules[rule]["name"])

            res = re.compile(Rules[rule]["rex"],
                             re.IGNORECASE).findall(self.body)
            # print("4: ", res)

            if res:
                # print(self.body)
                result["status"] = result["status"] or True
                result["type"].append(Rules[rule]["name"])

        return result
