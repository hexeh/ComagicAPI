# -*- coding: utf-8 -*-

try:
	import urllib
	import json
	import datetime
	import requests
	import sys
except ImportError:
	sys.exit(
		'''Please install following packages using pip:
		urllib
		'''
	)

class CMInstance:
	def __init__(self, config):
		self.base = 'http://api.comagic.ru'
		self.config = config
		self.message = []
		session_query = {
			'login': self.config['login'],
			'password': self.config['password']
		}
		session_start = requests.post(
			self.base + '/api/login/',
			headers = { 'Accept': 'application/json'},
			data = session_query
		)
		if session_start.status_code == 200:
			response = json.loads(session_start.text)
			if response['success']:
				self.session_key = response['data']['session_key']
				self.message.append({
					'source': 'comagic',
					'date': str(datetime.datetime.now()),
					'action': 'session_key',
					'details': {
						'session_key': self.session_key,
						'expires_in': 10800000,
						'expires_on': str(datetime.datetime.now() + datetime.timedelta( hours = 3))
					},
					'state': 'OK'
				})
			else:
				self.message.append({
					'source': 'comagic',
					'date': str(datetime.datetime.now()),
					'action': 'session_key',
					'details': response,
					'state': 'ERROR'
				})
				msg = 'Server Closed Connection with info: ' + response
				raise Exception(msg)
		else:
			self.message.append({
				'source': 'comagic',
				'date': str(datetime.datetime.now()),
				'action': 'session_key',
				'details': session_start.text,
				'state': 'ERROR'
			})
			msg = 'Server Closed Connection with info: ' + session_start.text
			raise Exception(msg)

	def getMessages(self):
		return(self.message)

	def getClients(self):

		clients_list = requests.get(self.base + '/api/v1/customer_list/', headers = { 'Accept': 'application/json'}, data = { 'session_key': self.session_key })
		result = {}
		if clients_list.status_code == 200:
			clients_res = json.loads(clients_list.text)
			if clients_res['success']:
				self.message.append({
					'source': 'comagic',
					'date': str(datetime.datetime.now()),
					'action': 'clients_list',
					'details': {},
					'state': 'OK'
				})
				result = clients_res['data']
			else:
				self.message.append({
					'source': 'comagic',
					'date': str(datetime.datetime.now()),
					'action': 'clients_list',
					'details': clients_res,
					'state': 'ERROR'
				})
		else:
			self.message.append({
				'source': 'comagic',
				'date': str(datetime.datetime.now()),
				'action': 'clients_list',
				'details': clients_list.text,
				'state': 'ERROR'
			})
		return(result)

	def getSites(self):

		sites_list = requests.get(self.base + '/api/v1/site/', headers = { 'Accept': 'application/json'}, data = { 'session_key': self.session_key })
		result = {}
		if sites_list.status_code == 200:
			sites_res = json.loads(sites_list.text)
			if sites_res['success']:
				self.message.append({
					'source': 'comagic',
					'date': str(datetime.datetime.now()),
					'action': 'sites_list',
					'details': {},
					'state': 'OK'
				})
				result = sites_res['data']
			else:
				self.message.append({
					'source': 'comagic',
					'date': str(datetime.datetime.now()),
					'action': 'sites_list',
					'details': sites_res,
					'state': 'ERROR'
				})
		else:
			self.message.append({
				'source': 'comagic',
				'date': str(datetime.datetime.now()),
				'action': 'sites_list',
				'details': sites_list.text,
				'state': 'ERROR'
			})
		return(result)

	def getTags(self):

		tags_list = requests.get(self.base + '/api/v1/tag/', headers = { 'Accept': 'application/json'}, data = { 'session_key': self.session_key })
		result = {}
		if tags_list.status_code == 200:
			tags_res = json.loads(tags_list.text)
			if tags_res['success']:
				self.message.append({
					'source': 'comagic',
					'date': str(datetime.datetime.now()),
					'action': 'tags_list',
					'details': {},
					'state': 'OK'
				})
				result = tags_res['data']
			else:
				self.message.append({
					'source': 'comagic',
					'date': str(datetime.datetime.now()),
					'action': 'tags_list',
					'details': tags_res,
					'state': 'ERROR'
				})
		else:
			self.message.append({
				'source': 'comagic',
				'date': str(datetime.datetime.now()),
				'action': 'tags_list',
				'details': tags_list.text,
				'state': 'ERROR'
			})
		return(result)

	def getSummaryStats(self, siteId, dateFrom, dateTo, acId = False, customerId = False, byDate = False):
		
		summary_stats = []
		summary_query = {
			'session_key': self.session_key,
			'site_id': siteId,
			'date_from': dateFrom,
			'date_till': dateTo
		}
		if acId: summary_query['ac_id'] = acId
		if customerId: summary_query['customer_id'] = customerId
		summary_req = requests.get(
			self.base + '/api/v1/stat/',
			headers = { 'Accept': 'application/json'},
			data = summary_query
		)
		if summary_req.status_code == 200:
			summary_res = json.loads(summary_req.text)
			if summary_res['success']:
				summary_res['data'][0]['date'] = dateFrom
				summary_res['data'][0]['total'] = (not byDate)
				summary_stats.append(summary_res['data'][0])
				self.message.append({
					'source': 'comagic',
					'date': str(datetime.datetime.now()),
					'action': 'summary_stats',
					'details': {},
					'state': 'OK'
				})
			else:
				self.message.append({
					'source': 'comagic',
					'date': str(datetime.datetime.now()),
					'action': 'summary_stats',
					'details': summary_res,
					'state': 'ERROR'
				})
		else:
			self.message.append({
				'source': 'comagic',
				'date': str(datetime.datetime.now()),
				'action': 'summary_stats',
				'details': summary_req.text,
				'state': 'ERROR'
			})
		if byDate:
			newDate = datetime.datetime.strptime(dateFrom, '%Y-%m-%d').date() + datetime.timedelta(1)
			if newDate <= datetime.datetime.strptime(dateTo, '%Y-%m-%d').date():
				summary_stats += self.getSummaryStats(siteId, newDate.strftime('%Y-%m-%d'), dateTo, acId, customerId, byDate)
		return(summary_stats)

	def getCommunicationStats(self, siteId, dateFrom, dateTo, acId = False, tagId = False, showNotGoal = False, onlyFirst = False):

		dateTo = (datetime.datetime.strptime(dateTo, '%Y-%m-%d').date() + datetime.timedelta(1)).strftime('%Y-%m-%d')
		comm_stats = []
		comm_query = {
			'session_key': self.session_key,
			'site_id': siteId,
			'date_from': dateFrom,
			'date_till': dateTo
		}
		if acId: comm_query['ac_id'] = acId
		if tagId: comm_query['tag_id'] = tagId
		if showNotGoal: comm_query['show_not_goal'] = showNotGoal
		if onlyFirst: comm_query['only_first'] = onlyFirst
		comm_req = requests.get(
			self.base + '/api/v1/communication/',
			headers = { 'Accept': 'application/json'},
			data = comm_query
		)
		if comm_req.status_code == 200:
			comm_res = json.loads(comm_req.text)
			if comm_res['success']:
				comm_stats = comm_res['data']
				self.message.append({
					'source': 'comagic',
					'date': str(datetime.datetime.now()),
					'action': 'communication_stats',
					'details': {},
					'state': 'OK'
				})
			else:
				self.message.append({
					'source': 'comagic',
					'date': str(datetime.datetime.now()),
					'action': 'communication_stats',
					'details': comm_res,
					'state': 'ERROR'
				})
		else:
			self.message.append({
				'source': 'comagic',
				'date': str(datetime.datetime.now()),
				'action': 'communication_stats',
				'details': comm_req.text,
				'state': 'ERROR'
			})
		return(comm_stats)

	def getGoalStats(self, siteId, dateFrom, dateTo, acId = False, customerId = False, goalId = False, visitorId = False, tagId = False):

		dateTo = (datetime.datetime.strptime(dateTo, '%Y-%m-%d').date() + datetime.timedelta(1)).strftime('%Y-%m-%d')
		goal_stats = []
		goal_query = {
			'session_key': self.session_key,
			'site_id': siteId,
			'date_from': dateFrom,
			'date_till': dateTo
		}
		if acId: goal_query['ac_id'] = acId
		if tagId: goal_query['tag_id'] = tagId
		if customerId: goal_query['customer_id'] = customerId
		if goalId: goal_query['id'] = goalId
		if visitorId: goal_query['visitor_id'] = visitorId

		goal_req = requests.get(
			self.base + '/api/v1/goal/',
			headers = { 'Accept': 'application/json'},
			data = goal_query
		)
		if goal_req.status_code == 200:
			goal_res = json.loads(goal_req.text)
			if goal_res['success']:
				goal_stats = goal_res['data']
				self.message.append({
					'source': 'comagic',
					'date': str(datetime.datetime.now()),
					'action': 'goal_stats',
					'details': {},
					'state': 'OK'
				})
			else:
				self.message.append({
					'source': 'comagic',
					'date': str(datetime.datetime.now()),
					'action': 'goal_stats',
					'details': goal_res,
					'state': 'ERROR'
				})
		else:
			self.message.append({
				'source': 'comagic',
				'date': str(datetime.datetime.now()),
				'action': 'goalunication_stats',
				'details': goal_req.text,
				'state': 'ERROR'
			})
		return(goal_stats)

	def getCallStats(self, dateFrom, dateTo, siteId = False, acId = False, customerId = False, callId = False, visitorId = False, tagId = False, direction = False, numa = False, numb = False, returnRecordUrls = False):

		dateTo = (datetime.datetime.strptime(dateTo, '%Y-%m-%d').date() + datetime.timedelta(1)).strftime('%Y-%m-%d')
		call_stats = []
		records = []
		result = []
		call_query = {
			'session_key': self.session_key,
			'date_from': dateFrom,
			'date_till': dateTo
		}
		if siteId: call_query['site_id'] = siteId
		if acId: call_query['ac_id'] = acId
		if tagId: call_query['tag_id'] = tagId
		if customerId: call_query['customer_id'] = customerId
		if callId: call_query['id'] = callId
		if visitorId: call_query['visitor_id'] = visitorId
		if direction: call_query['direction'] = direction
		if numa: call_query['numa'] = numa
		if numb: call_query['numb'] = numb

		call_req = requests.get(
			self.base + '/api/v1/call/',
			headers = { 'Accept': 'application/json'},
			data = call_query
		)
		if call_req.status_code == 200:
			call_res = json.loads(call_req.text)
			if call_res['success']:
				call_stats = call_res['data']
				if returnRecordUrls:
					records = [{'id': v['id'], 'link': v['file_link'][0].replace('//app', 'https://app')} for v in call_stats if len(v['file_link']) != 0]
					result = {'call_stats': call_stats, 'records': records}
				else:
					result = call_stats
				self.message.append({
					'source': 'comagic',
					'date': str(datetime.datetime.now()),
					'action': 'call_stats',
					'details': {},
					'state': 'OK'
				})
			else:
				self.message.append({
					'source': 'comagic',
					'date': str(datetime.datetime.now()),
					'action': 'call_stats',
					'details': call_res,
					'state': 'ERROR'
				})
		else:
			self.message.append({
				'source': 'comagic',
				'date': str(datetime.datetime.now()),
				'action': 'callunication_stats',
				'details': call_req.text,
				'state': 'ERROR'
			})
		return(result)

	def endSession(self):
		session_end = requests.get(self.base + '/api/logout/', headers = { 'Accept': 'application/json' }, data = { 'session_key': self.session_key })
		if session_end.status_code == 200:
			self.message.append({
				'source': 'comagic',
				'date': str(datetime.datetime.now()),
				'action': 'session_end',
				'details': {},
				'state': 'OK'
			})
		else:
			self.message.append({
				'source': 'comagic',
				'date': str(datetime.datetime.now()),
				'action': 'session_end',
				'details': {'status_code': session_end.status_code, 'text': session_end.text },
				'state': 'OK'
			})
