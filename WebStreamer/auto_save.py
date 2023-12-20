# This file is a module integrated into TG FileStreamBot
# Used to submit the generated file URL to a third-party platform for automatic file download
# Applicable platforms: https://github.com/ordosx/remote-downloader

import re
import json
import logging
import hashlib
import requests
from urllib.parse import unquote
# load varsfile
from WebStreamer.vars import Var

logger = logging.getLogger(__name__)

def login():
    '''
    input env :  SAVE_SERVER(remote-downloader服务地址)
    input env :  SAVE_SERVER_PASSWORD(remote-downloader服务密码)
    output: connect.sid
    '''

    # 获取盐值
    salt_response = requests.get(f'{Var.SAVE_SERVER}/api/salt')
    try:
        salt_data = salt_response.json()
    except json.JSONDecodeError:
        logger.error('没有返回有效的JSON数据,请检查服务地址是否正确')
        logger.error(f'请求状态码: {salt_response.status_code} 返回响应体:\n{salt_response.text}')
        return 1

    salt_id = salt_data['saltID']
    salt = salt_data['salt']

    # 使用盐值散列密码
    password = Var.SAVE_SERVER_PASSWORD
    salted_password = hashlib.sha256((password + salt).encode()).hexdigest()

    # 构造登录数据
    login_data = {
        'saltID': salt_id,
        'password': salted_password
    }

    # 发送登录请求
    session_response = requests.post(f'{Var.SAVE_SERVER}/api/session', json=login_data)

    # 提取登录信息
    session_data = session_response.json()
    connect_sid = session_response.cookies.get('connect.sid', None)

    if session_data.get('code') == 0:
        return connect_sid
    else:
        logger.error('登录失败,请检查密码或服务地址是否正确');return 1

def download_task(url):
    '''
    input: url
    output: None
    '''

    # 提交下载任务
    connect_sid = login()
    resource_url = url.replace("https://tele-stream-bot.init.ac:443/", "http://tele-stream-bot.private.svc.cluster.local:443/")

    # 防止url中包含中文乱码导致下载失败
    resource_name = re.search(r'\/([^\/]+)\?', url).group(1)
    resource_name = unquote(resource_name.split('?')[0])

    headers = {
        'cookie': f'connect.sid={connect_sid}'
    }

    data = {
        'name': resource_name,
        'URL': resource_url
    }

    response = requests.post(f'{Var.SAVE_SERVER}/api/tasks', headers=headers, json=data)
    if response.status_code == 200:
        logger.info(f"提交下载任务成功: {resource_name},状态码: {response.status_code}")
    else:
        logger.error(f"提交下载任务失败: {resource_name},状态码: {response.status_code}")