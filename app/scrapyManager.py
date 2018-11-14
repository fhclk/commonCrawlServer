#!/usr/bin/env python
#-*-coding:utf-8-*-

from .util import http
import config
import requests
import time, datetime
from .util.http import *


class JobPriority():
    LOW, NORMAL, HIGH, HIGHEST = range(-1, 3)


class JobRunType():
    ONETIME = 'onetime'
    PERIODIC = 'periodic'

class SpiderStatus():
    PENDING, RUNNING, FINISHED, CANCELED = range(4)

class ScrapyManager(object):

    def __init__(self):
        self._scrapyd_url = 'http://' + config.SCRAPYD_SERVER_IP + ':' + str(config.SCRAPYD_SERVER_PORT)
        self._project_name = config.CRAWLER_PROJECT
        self.spider_status_name_dict = {
            SpiderStatus.PENDING: 'pending',
            SpiderStatus.RUNNING: 'running',
            SpiderStatus.FINISHED: 'finished'
        }


    def daemonstatus(self):
        pass


    def addversion(self, file_path):
        with open(file_path, 'rb') as f:
            eggdata = f.read()
        res = requests.post(self._scrapyd_url + '/addversion.json', data={
            'project': self._project_name,
            'version': int(time.time()),
            'egg': eggdata,
        })
        return res.text if res.status_code == 200 else None
        pass

    def schedule(self,spider_name,arguments, download_delay=None):
        post_data = dict(project=self._project_name, spider=spider_name)

        if download_delay:
            try:
                post_data.setting = 'DOWNLOAD_DELAY=' + str(download_delay)
            except Exception as e:
                pass

        if spider_name == 'regexSpider':
            pass
        if spider_name == 'regexLoginedSpider':
            pass
        if spider_name == 'universalSpider':
            pass
        if spider_name == 'universalProxySpider':
            pass
        if spider_name == 'universalLoginedSpider':
            pass
        if spider_name == 'universalSplashSpider':
            pass

        post_data.update(arguments)
        data = request("post", self._scrapyd_url + "/schedule.json", data=post_data, return_type="json")
        return data['jobid'] if data and data['status'] == 'ok' else None

    def cancel(self,job_id):
        post_data = dict(project=self._project_name, job=job_id)
        data = request("post", self._scrapyd_url + "/cancel.json", data=post_data, return_type="json")
        return data != None

    def listprojects(self):
        pass

    def listversions(self):
        pass

    def listspiders(self):
        data = request("get", self._scrapyd_url + "/listspiders.json?project=%s" % self._project_name,
                       return_type="json")
        result = []
        if data and data['status'] == 'ok':
            for spider_name in data['spiders']:
                spider_instance = dict()
                spider_instance.spider_name = spider_name
                result.append(spider_instance)
        return result

    def listjobs(self, spider_status=None):
        data = request("get", self._scrapyd_url + "/listjobs.json?project=%s" % self._project_name,
                       return_type="json")
        result = {SpiderStatus.PENDING: [], SpiderStatus.RUNNING: [], SpiderStatus.FINISHED: []}
        if data and data['status'] == 'ok':
            for _status in self.spider_status_name_dict.keys():
                for item in data[self.spider_status_name_dict[_status]]:
                    start_time, end_time = None, None
                    if item.get('start_time'):
                        start_time = datetime.datetime.strptime(item['start_time'], '%Y-%m-%d %H:%M:%S.%f')
                    if item.get('end_time'):
                        end_time = datetime.datetime.strptime(item['end_time'], '%Y-%m-%d %H:%M:%S.%f')
                    result[_status].append(dict(id=item['id'], start_time=start_time, end_time=end_time))
        return result if not spider_status else result[spider_status]

    def delversion(self):
        pass

    def delproject(self):
        pass

    def log(self, spider_name, job_id):
        return self._scrapyd_url + '/logs/%s/%s/%s.log' % (self._project_name, spider_name, job_id)

    pass