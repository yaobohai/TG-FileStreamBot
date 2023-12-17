import re
import requests
import logging

logger = logging.getLogger(__name__)

def download_task(url):

    resource_url = url.replace("https://tele-stream-bot.init.ac:443/", "http://tele-stream-bot.private.svc.cluster.local:443/")
    resource_name = re.search(r'\/([^\/]+)\?', url).group(1)

    resource_name = resource_name.split('?')[0]
    headers = {
        'cookie': 'connect.sid=s%3AXDax-Pgemsnj4yMvOcBJjb2biCwKTlrt.4ZfR0TCYlwUogvrPlEnxKLdRj91Ws9fzvHTQBR4ABak'
    }
    data = {
        'name': resource_name,
        'URL': resource_url
    }

    response = requests.post('https://init.ac/api/tasks', headers=headers, json=data)

    if response.status_code == 200:
        logger.info(f"提交下载任务成功: {resource_name},状态码: {response.status_code}")
    else:
        logger.info(f"提交下载任务失败: {resource_name},状态码: {response.status_code}")
