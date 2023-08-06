import logging
import time
import requests


class ServerApi:
    def __init__(self, instance_id, spider_id):
        self.host = ''
        self.port = ''

        self.ak = 'kEdSrZxK5BhsS0iXMhxRfeBhhwIA'
        self.secret = 'ddb88604dbd74e55b86acc583f0505ea'
        self.instance_id = instance_id
        self.spider_id = spider_id

        self.data_type = ''
        self.task_id = ''
        self.old_task_id = ''
        self.task_type = ''
        self.redis_key = ''
        self.date_no = ''
        self.platform = ''
        self.store_url = ''
        self.platform = ''
        self.host_config = {
            'test': {
                'host': '10.20.16.102',
                'port': 10989,
                'store_url': 'http://10.20.16.87/api/test'
            },
            'pro': {
                'host': '10.20.20.9',
                'port': 10989,
                'store_url': 'http://10.158.0.23:18080/crawler/collect/logs'
            },
            'vps': {
                'host': '183.129.169.171',
                'port': 10989,
                'store_url': 'http://211.140.27.195:18080/crawler/collect/logs'
            }
        }

    def init_setting(self, env):
        hosts = self.host_config.get(env)
        if hosts is None:
            raise RuntimeError('未指定SDK运行环境')
        self.host = hosts['host']
        self.port = hosts['port']
        self.store_url = hosts['store_url']

    def send_heartbeat(self, status):
        """
        发送爬虫心跳
        :param status: waiting or working
        :return:
        """
        while 1:
            data = {
                "spider_id": self.spider_id,
                "instance_id": self.instance_id,
                'status': status
            }
            method = 'POST'
            url = f'http://{self.host}:{self.port}/client/instance/heartbeat'
            try:
                r = requests.request(method, url, json=data, timeout=10)
                if r.status_code == 200:
                    return
                else:
                    logging.error(f'【/client/instance/heartbeat】服务器异常，状态码: {r.text}')
            except OSError as e:
                logging.error(f'【/client/instance/heartbeat 】客户端异常: {e}')
            time.sleep(5)

    def get_data(self, key, number=1):
        if key:
            while 1:
                try:
                    url = f'http://{self.host}:{self.port}/client/data?key={key}&number={number}'
                    method = 'GET'
                    r = requests.request(method, url, timeout=10)
                    if r.status_code == 200:
                        return r.json()
                    else:
                        logging.error(f'【client/data】服务器异常,状态码：{r.json()}')
                except Exception as e:
                    logging.error(f'【client/data】客户端异常：{e}')
                time.sleep(5)
        return {}

    def task_query(self):
        while 1:
            method = 'GET'
            params = {
                'spider_id': self.spider_id,
                'instance_id': self.instance_id,
            }
            url = f'http://{self.host}:{self.port}/client/task'
            try:
                r = requests.request(method, url, params=params, timeout=10)
                if r.status_code == 200:
                    return r.json()
                else:
                    logging.error(f'【/client/task】服务器异常,状态码：{r.status_code}')
            except OSError as e:
                logging.error(f'【/client/task】客户端异常：{e}')

            time.sleep(5)

    def task_callback(self, value, is_success=True):
        """
        任务确认
        :param value: 采集数据源
        :param is_success: 数据采集是否正常
        :return:
        """
        while 1:
            params = {
                "spider_id": self.spider_id,
                "instance_id": self.instance_id,
                "task_id": self.task_id,
                "data_type": self.data_type,
                "data_value": value,
                "data_key": self.redis_key,
                "is_success": is_success,
            }
            url = f'http://{self.host}:{self.port}/client/task'
            data = params
            method = 'POST'
            try:
                r = requests.request(method, url, json=data, timeout=10)
                if r.status_code == 200:
                    logging.debug(f'【/client/task/callback】 code is 200 {r.text} instance_id: {self.instance_id}')
                    return
                else:
                    logging.error(f'【/client/task/callback】服务器异常,状态码：{r.text}')
            except OSError as e:
                logging.error(f'【/client/task/callback】客户端异常： {e}')
            time.sleep(5)

    def nginx_store_api(self, item, data_type):
        """
        data_type : 数据类型(店铺，商品，券等)
        """
        date_type_map = {
            'week': 'W',
            'month': 'M',
            'day': 'D',
            'normal': 'D',
        }
        headers = {'Content-Type': 'application/json'}
        data = {
            "header": {
                "client_id": self.spider_id,
                "task_id": self.old_task_id if self.old_task_id else self.task_id,
                "plf_id": self.platform,
                "cycle_type": date_type_map.get(self.task_type, ''),
                "data_type": data_type,
                "date_no": self.date_no
            },
            "data": item
        }
        while 1:
            try:
                r = requests.request(method='POST', url=self.store_url, headers=headers, json=data, timeout=10)
                if 200 <= r.status_code < 300:
                    logging.debug(f'【crawler/collect/logs】 code is 200 {r.text} task_id: {self.task_id}')
                    return
                else:
                    logging.error(f'【crawler/collect/logs】服务器异常：{r.text} task_id: {self.task_id}')
            except OSError as e:
                logging.error(f'【crawler/collect/logs】 客户端异常 : {e} task_id: {self.task_id}')
