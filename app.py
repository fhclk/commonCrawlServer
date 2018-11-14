#!/usr/bin/env python
#-*-coding:utf-8-*-

from flask import Flask
from flask import render_template, url_for, redirect, request, jsonify

import pymongo
import json
import requests

import config
from app.scrapyManager import ScrapyManager
from app.job import Job
from datetime import datetime

app = Flask(__name__)
app.jinja_env.variable_start_string = '%%'
app.jinja_env.variable_end_string = '%%'

app.config.from_object(config)

mongoConn = pymongo.MongoClient('127.0.0.1', 27017)
mongoDb = mongoConn['common_crawler']


scrapyManager = ScrapyManager()


RULE_SPIDERS_NAME = {"常规" : "regexSpider",
                     "模拟登录" : "regexLoginedSpider"}
NORMAL_SPIDERS_NAME = {"常规" : "universalSpider",
                       "代理" : "universalProxySpider",
                       "模拟登录" : "universalLoginedSpider",
                       "模拟浏览器" : "universalSplashSpider"}

@app.route('/')
def index():
    # return render_template('createTask.html')
    return redirect(url_for('openFile', fileName='createTask.html'))

@app.route('/crawlSetting/<fileName>')
def openFile(fileName):
    return render_template(fileName)


@app.route('/crawlSetting/saveTaskConfig', methods=['POST'])
def saveTaskConfig():
    if request.method == 'POST':
        userId = request.form.get('userId', '')
        taskConfig = request.form.get('taskConfig', '')
        result = {'result':False, 'message':''}
        if userId and taskConfig:
            conf = json.loads(taskConfig)
            conf['user_id'] = userId
            task_no = conf.get('task_no','')
            has_records = mongoDb['task_temp'].find({'user_id': userId, 'task_no':task_no})
            if has_records and has_records.count() > 0:
                result['result'] = False
                result['message'] = '已经有任务编号为'+conf.get('task_no','')+'的任务配置'
            else:
                mongoDb['task_temp'].insert(conf)
                result['result'] = True
                result['message'] = '保存成功'
        else:
            result['result'] = False
            result['message'] = '保存失败'
        return jsonify(result)


@app.route('/crawlSetting/createTaskConfig', methods=['POST'])
def createTaskConfig():
    if request.method == 'POST':
        userId = request.form.get('userId', '')
        taskConfig = request.form.get('taskConfig', '')
        result = {'result':False, 'message':''}
        if userId and taskConfig:
            conf = json.loads(taskConfig)
            conf['user_id'] = userId
            task_no = conf.get('task_no','')
            has_records = mongoDb['task_temp'].find({'user_id': userId, 'task_no':task_no})
            if has_records and has_records.count() > 0:
                result['result'] = False
                result['message'] = '已经有任务编号为'+conf.get('task_no','')+'的任务配置'
            else:
                mongoDb['task_temp'].insert(conf)
                result['result'] = True
                result['message'] = '保存成功'
        else:
            result['result'] = False
            result['message'] = '保存失败'
        return jsonify(result)


@app.route('/crawlSetting/dashboard/loadAllTasks', methods=['POST'])
def loadAllTasks():
    if request.method == 'POST':
        userId = request.form.get('userId', '')
        result = {'result':False, 'message':'', 'data': []}
        if userId:
            records = mongoDb['task_temp'].find({'user_id': userId})
            for record in records:
                task = {}
                task['task_no'] = record['task_no']
                task['task_type'] = record.get('task_type', '')
                result['data'].append(task)
            result['result'] = True
            result['message'] = '获取成功'
        else:
            result['result'] = False
            result['message'] = '获取失败'
        return jsonify(result)

@app.route('/crawlSetting/dashboard/loadWaitingTasks', methods=['POST'])
def loadWaitingTasks():
    if request.method == 'POST':
        Job.updateJobStatus(mongoDb, scrapyManager)
        userId = request.form.get('userId', '')
        result = {'result':False, 'message':'', 'data': []}
        if userId:
            records = mongoDb['job'].find({'user_id': userId, "$or":[{'status':'waiting'},{'status':'pending'}]})
            # records = mongoDb['job'].find({'user_id': userId, 'status':'waiting'})
            for record in records:
                del record['_id']
                task = mongoDb['task_temp'].find_one({'task_no': record['task_no']})
                if task:
                    record["task_type"] = task.get('task_type','')
                result['data'].append(record)
            result['result'] = True
            result['message'] = '获取成功'
        else:
            result['result'] = False
            result['message'] = '获取失败'
        return jsonify(result)


@app.route('/crawlSetting/dashboard/loadRunningTasks', methods=['POST'])
def loadRunningTasks():
    if request.method == 'POST':
        userId = request.form.get('userId', '')
        result = {'result':False, 'message':'', 'data': []}
        if userId:
            records = mongoDb['job'].find({'user_id': userId, 'status':'running'})
            for record in records:
                del record['_id']
                task = mongoDb['task_temp'].find_one({'task_no': record['task_no']})
                if task:
                    record["task_type"] = task.get('task_type','')
                result['data'].append(record)
            result['result'] = True
            result['message'] = '获取成功'
        else:
            result['result'] = False
            result['message'] = '获取失败'
        return jsonify(result)


@app.route('/crawlSetting/dashboard/loadFinishedTasks', methods=['POST'])
def loadFinishedTasks():
    if request.method == 'POST':
        userId = request.form.get('userId', '')
        result = {'result':False, 'message':'', 'data': []}
        if userId:
            records = mongoDb['job'].find({'user_id': userId, "$or":[{'status':'finished'},{'status':'canceled'}]})
            for record in records:
                del record['_id']
                task = mongoDb['task_temp'].find_one({'task_no': record['task_no']})
                if task:
                    record["task_type"] = task.get('task_type','')
                result['data'].append(record)
            result['result'] = True
            result['message'] = '获取成功'
        else:
            result['result'] = False
            result['message'] = '获取失败'
        return jsonify(result)

@app.route('/crawlSetting/dashboard/getTaskConfig', methods=['POST'])
def getTaskConfig():
    if request.method == 'POST':
        userId = request.form.get('userId', '')
        taskNo = request.form.get('taskNo', '')
        result = {'result':False, 'message':'', 'data': []}
        if userId and taskNo:
            find_record = mongoDb['task_temp'].find_one({'user_id': userId, 'task_no':taskNo})
            if find_record:
                if '_id' in find_record:
                    del find_record['_id']
                if 'task_type' in find_record:
                    del find_record['task_type']
                if 'user_id' in find_record:
                    del find_record['user_id']
                result['data'] = find_record
                result['result'] = True
                result['message'] = '获取成功'
            else:
                result['result'] = False
                result['message'] = '获取失败'
        else:
            result['result'] = False
            result['message'] = '用户编号或任务编号为空'
        return jsonify(result)


@app.route('/crawlSetting/dashboard/runTask', methods=['POST'])
def runTask():
    if request.method == 'POST':
        userId = request.form.get('userId', '')
        taskNo = request.form.get('taskNo', '')
        crawlNo = request.form.get('crawlNo', '')
        taskType = request.form.get('taskType', '')
        spiderType = request.form.get('spiderType', '')
        priority = request.form.get('priority', '0')
        downloadDelay = request.form.get('downloadDelay', None)
        result = {'result': False, 'message': '', 'data': []}
        if not userId:
            result['result'] = False
            result['message'] = '用户编号编号不能为空'
        elif not taskNo:
            result['result'] = False
            result['message'] = '任务编号不能为空'
        elif not crawlNo:
            result['result'] = False
            result['message'] = '任务运行编号不能为空'
        elif not taskType:
            result['result'] = False
            result['message'] = '任务类型不能为空'
        elif not spiderType:
            result['result'] = False
            result['message'] = '任务运行方式不能为空'
        else:
            spiderName = None
            if taskType == "rule_spider":
                spiderName = RULE_SPIDERS_NAME.get(spiderType, '')
            if taskType == "normal_spider":
                spiderName = NORMAL_SPIDERS_NAME.get(spiderType, '')
            if spiderName:
                scrapyJobId = scrapyManager.schedule(spiderName,{'taskNo': taskNo, 'crawlNo': crawlNo} ,downloadDelay)
                if scrapyJobId:
                    job = {}
                    job["user_id"] = userId
                    job["task_no"] = taskNo
                    job["crawl_no"] = crawlNo
                    job["task_type"] = taskType
                    job["spider_name"] = spiderName
                    job["spider_type"] = spiderType
                    job["priority"] = priority
                    job["status"] = "waiting"
                    job['scrapy_job_id'] = scrapyJobId
                    job['download_delay'] = downloadDelay
                    mongoDb['job'].insert(job)
                    result['result'] = True
                    result['message'] = '运行任务成功'
                else:
                    result['result'] = False
                    result['message'] = '任务运行失败'
            else:
                result['result'] = False
                result['message'] = '任务运行方式错误'
        return jsonify(result)

@app.route('/crawlSetting/dashboard/stopTask', methods=['POST'])
def stopTask():
    if request.method == 'POST':
        userId = request.form.get('userId', '')
        jobId = request.form.get('jobId', '')
        scrapyJobId = request.form.get('scrapyJobId', '')
        result = {'result': False, 'message': '', 'data': []}
        if not userId:
            result['result'] = False
            result['message'] = '用户编号编号不能为空'
        elif not jobId:
            result['result'] = False
            result['message'] = '任务执行编号不能为空'
        elif not scrapyJobId:
            result['result'] = False
            result['message'] = '爬虫执行编号不能为空'
        else:
            if scrapyManager.cancel(scrapyJobId):
                mongoDb['job'].update({'scrapy_job_id': scrapyJobId},
                                 {"$set": {'status': 'canceled'}})
                result['result'] = True
                result['message'] = '停止任务成功'
            else:
                result['result'] = False
                result['message'] = '停止任务失败'
        return jsonify(result)

@app.route("/crawlSetting/dashboard/getJobLog", methods=['POST'])
def getJobLog():
    if request.method == 'POST':
        userId = request.form.get('userId', '')
        spiderName = request.form.get('spiderName', '')
        scrapyJobId = request.form.get('scrapyJobId', '')
        result = {'result': False, 'message': '', 'data': []}
        if not userId:
            result['result'] = False
            result['message'] = '用户编号编号不能为空'
        elif not spiderName:
            result['result'] = False
            result['message'] = '爬取类型不能为空'
        elif not scrapyJobId:
            result['result'] = False
            result['message'] = '爬虫执行编号不能为空'
        else:
            try:
                raw = requests.get(scrapyManager.log(spiderName, scrapyJobId)).text or ""
            except Exception:
                result['result'] = False
                result['message'] = '获取日志失败'
            else:
                result['result'] = True
                result['message'] = '获取日志成功'
                result['data'] = raw.split('\n')
        return jsonify(result)

@app.route("/crawlSetting/dashboard/getJobResult", methods=['POST'])
def getJobResult():
    if request.method == 'POST':
        userId = request.form.get('userId', '')
        taskNo = request.form.get('taskNo', '')
        crawlNo = request.form.get('jobId', '')
        result = {'result': False, 'message': '', 'data': []}
        if not userId:
            result['result'] = False
            result['message'] = '用户编号编号不能为空'
        elif not taskNo:
            result['result'] = False
            result['message'] = '任务不能为空'
        elif not crawlNo:
            result['result'] = False
            result['message'] = '任务执行编号不能为空'
        else:
            task = mongoDb['task_temp'].find_one({'user_id':userId, 'task_no':taskNo})
            if task:
                if task["task_type"] == 'normal_spider':
                    result['task_type'] = 'normal_spider'
                    for follow in task.get('follows',[]):
                        if 'columns' in follow:
                            follow_item = {}
                            follow_item['ord'] = follow["ord"]
                            follow_item['type'] = follow["type"]
                            follow_item['data'] = []
                            items = mongoDb[follow.get('type')].find({'crawl_no':crawlNo, 'follow_ord':follow["ord"]})
                            for item in items:
                                del item['_id']
                                if 'crawl_no' in item:
                                    del item['crawl_no']
                                if 'follow_ord' in item:
                                    del item['follow_ord']
                                if 'image_urls' in item:
                                    del item['image_urls']
                                if 'o_image_urls' in item:
                                    del item['o_image_urls']
                                follow_item['data'].append(item)
                            result['data'].append(follow_item)
                if task["task_type"] == 'rule_spider':
                    result['task_type'] = 'rule_spider'
                    for rule in task.get('url_rules',[]):
                        if 'columns' in rule:
                            rule_item = {}
                            rule_item['ord'] = rule["ord"]
                            rule_item['type'] = ''
                            rule_item['data'] = []
                            items = mongoDb['rules_content'].find({'crawl_no':crawlNo, 'rule_id':rule["ord"]})
                            for item in items:
                                del item['_id']
                                rule_item['data'].append(item)
                            result['data'].append(rule_item)
            result['result'] = True
            result['message'] = '获取结果成功'
        return jsonify(result)

@app.route('/crawlSetting/manageTask/deleteTask', methods=['POST'])
def deleteTask():
    if request.method == 'POST':
        userId = request.form.get('userId', '')
        taskNo = request.form.get('taskNo', '')
        result = {'result':False, 'message':'', 'data': []}
        if userId and taskNo:
            mongoDb['task_temp'].remove({'user_id': userId, 'task_no':taskNo})
            result['result'] = True
            result['message'] = '删除成功'
        else:
            result['result'] = False
            result['message'] = '删除失败'
        return jsonify(result)

@app.route('/crawlSetting/manageTask/resetTask', methods=['POST'])
def resetTask():
    if request.method == 'POST':
        userId = request.form.get('userId', '')
        taskConfig = request.form.get('taskConfig', '')
        result = {'result': False, 'message': ''}
        if userId and taskConfig:
            conf = json.loads(taskConfig)
            conf['user_id'] = userId
            task_no = conf.get('task_no', '')
            has_records = mongoDb['task_temp'].find({'user_id': userId, 'task_no': task_no})
            if has_records and has_records.count() > 0:
                mongoDb['task_temp'].remove({'user_id': userId, 'task_no': task_no})
                mongoDb['task_temp'].insert(conf)
                result['result'] = True
                result['message'] = '修改成功'
            else:
                result['result'] = False
                result['message'] = '修改失败'
        else:
            result['result'] = False
            result['message'] = '修改失败'
        return jsonify(result)

@app.route('/crawlSetting/googleExtension/getExTaskConfig', methods=['POST'])
def getExTaskConfig():
    if request.method == 'POST':
        taskNo = request.form.get('taskNo', '')
        result = {'result':False, 'message':'', 'data': []}
        if taskNo:
            find_record = mongoDb['task_temp'].find_one({'task_no':taskNo})
            if find_record:
                if '_id' in find_record:
                    del find_record['_id']
                if 'user_id' in find_record:
                    del find_record['user_id']
                result['data'] = find_record
                result['result'] = True
                result['message'] = '获取成功'
            else:
                result['result'] = False
                result['message'] = '获取失败'
        else:
            result['result'] = False
            result['message'] = '任务编号为空'
        return jsonify(result)

@app.route('/crawlSetting/googleExtension/resetExTaskConfig', methods=['POST'])
def resetExTaskConfig():
    if request.method == 'POST':
        taskNo = request.form.get('taskNo', '')
        followsStr = request.form.get('followList', '{}')
        follows = json.loads(followsStr)
        result = {'result':False, 'message':'', 'data': []}
        if taskNo and follows:
            mongoDb['task_temp'].update({'task_no':taskNo}, {"$set":{"follows": follows}})
            result['result'] = True
            result['message'] = '设置成功'
        else:
            result['result'] = False
            result['message'] = '设置失败'
        return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5600)
