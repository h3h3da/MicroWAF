#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
from datetime import datetime
from threading import Thread
from config import *
from parse import Request
from detect import Detect
from log import log_block


def filter(r, addr):
    """检测web攻击，返回检测结果"""
    # uri黑白名单检测
    uri = r.uri.split('?')[0]
    if WHITE_URI_SWITCH:
        if uri not in WHITE_URI_LIST:
            return {"status": True, "type": 'not-white-uri'}
    if uri in BLACK_URI_LIST and not WHITE_URI_SWITCH:
        return {"status": True, "type": 'in-black-uri'}

    # 规则匹配
    det_data = Detect(r)
    result = det_data.run()

    # ip白名单允许连接
    if result["status"] and WHITE_IP_SWITCH:
        if addr[0] in WHITE_IP_LIST:
            return {"status": False}

    # result = {"status": False}
    # print("result: ", result)
    return result


def connecting(conn, addr):
    """使用反向代理模式提供waf功能，阻止web攻击"""
    # 阻挡ip黑名单连接
    if addr[0] in BLACK_IP_LIST:
        conn.close()
        print("Blocked in black")
        return

    # 接受客户端请求内容
    req = b''
    while True:
        buf = conn.recv(2048)
        req += buf
        if len(buf) < 2048:
            break
    if not req:
        conn.close()
        return

    # 解析http请求，拦截攻击，记录拦截行为
    try:
        r = Request(req)
    except Exception as e:
        conn.close()
        print(e)
        return

    result = filter(r, addr)
    log_block(addr, result)
    if result["status"]:
        conn.close()
        return

    # 向web服务器转发请求，将web服务器返回内容送回客户端
    req = req.replace(WAF_IP.encode("utf-8"), ('{}:{}'.format(WEB_IP, WEB_PORT)).encode("utf-8")) \
        .replace('keep-alive'.encode("utf-8"), 'close'.encode("utf-8")) \
        .replace('gzip'.encode("utf-8"), b'')
    #print(req)
    s1 = socket.socket()
    try:
        s1.connect((WEB_IP, WEB_PORT))
        s1.sendall(req)
    except Exception as e:
        print(e)
        s1.close()
        conn.close()
        return
    resp = b''
    while True:
        try:
            buf = s1.recv(2048)
        except socket.timeout as e:
            print("err ", e)
            break
        if not buf: # or buf.startswith('WebSocket') and buf.endswith('\r\n\r\n'):
            break
        resp += buf
    s1.close()

    resp = resp.replace(bytes(WEB_IP, encoding='utf-8'), bytes(WAF_IP, encoding='utf-8'))
    conn.send(resp)
    conn.close()


def run():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 80))
    s.listen(5)
    try:
        while 1:
            conn, addr = s.accept()

            t = Thread(target=connecting, args=(conn, addr))
            t.start()

    finally:
        s.close()


if __name__ == '__main__':
    run()
