#!/usr/bin/env python
#-*-coding:utf-8-*-

import pymongo
import json
from .scrapyManager import SpiderStatus
from .util import util
from datetime import datetime

class Job(object):


    def __init__(self, db, scrapyManager):
        self.db = db
        self.scrapyManager = scrapyManager
        pass


    @classmethod
    def updateJobStatus(cls, db, scrapyManager):
        format = '%Y-%m-%d %H:%M:%S'
        jobsDict = scrapyManager.listjobs()
        for (status, jobs) in jobsDict.items():
            if status == SpiderStatus.PENDING:
                for job in jobs:
                    db['job'].update({'scrapy_job_id':job["id"]},
                                     {"$set":{'status': 'pending'}})
            if status == SpiderStatus.RUNNING:
                cls.updateJobNotRunningStatus(db, jobs)
                now = datetime.now()
                for job in jobs:
                    db['job'].update({'scrapy_job_id':job["id"]},
                                     {"$set":{'status': 'running',
                                              'start_time': job.get('start_time',now).strftime(format),
                                              'run_time': util.calculateDuration(job.get('start_time',now), now)}})
            if status == SpiderStatus.FINISHED:
                for job in jobs:
                    cancel_job = db['job'].find({'scrapy_job_id':job["id"], 'status':'canceled'})
                    if cancel_job.count() == 0:
                        db['job'].update({'scrapy_job_id': job["id"]},
                                         {"$set": {'status': 'finished',
                                                   'start_time': job.get('start_time').strftime(format),
                                                   'end_time': job.get('end_time').strftime(format),
                                                   'run_time': util.calculateDuration(job.get('start_time'),
                                                                                      job.get('end_time'))}})
                    else:
                        db['job'].update({'scrapy_job_id': job["id"]},
                                         {"$set": {'start_time': job.get('start_time').strftime(format),
                                                   'end_time': job.get('end_time').strftime(format),
                                                   'run_time': util.calculateDuration(job.get('start_time'),
                                                                                      job.get('end_time'))}})
            # if status == SpiderStatus.CANCELED:
            #     for job in jobs:
            #         db['job'].update({'scrapy_job_id':job["id"]},
            #                          {"$set":{'status': 'canceled',
            #                                   'start_time': job.get('start_time').strftime(format),
            #                                   'end_time': job.get('end_time').strftime(format),
            #                                   'run_time': util.calculateDuration(job.get('start_time'), job.get('end_time'))}})

    @classmethod
    def updateJobNotRunningStatus(cls, db, runningJobs):
        pass
        # jobs = db['job'].find({'status':'running'})
        # for job in jobs:
        #     has = False
        #     for runningJob in runningJobs:
        #         if job['scrapy_job_id'] == runningJob['id']:
        #             has = True
        #             break
        #     if not has:
        #         db['job'].update({'scrapy_job_id': job["scrapy_job_id"]},
        #                          {"$set": {'status': 'canceled',
        #                                    'except': True}})

