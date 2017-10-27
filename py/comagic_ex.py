# -*- coding: utf-8 -*-

import pprint
import requests
from comagic_def import CMInstance

if __name__ == '__main__':

	config = {
		'login': 'USER_EMAIL',
		'password': 'USER_PASSWORD'
	}
	cm = CMInstance(config)
	pp = pprint.PrettyPrinter(indent = 4)
	
	sitesList = cm.getSites()
	pp.pprint(sitesList)
	
	statSummary = cm.getSummaryStats(sitesList[0]['id'], '2017-10-01', '2017-10-02', byDate = True)
	statCalls = cm.getCallStats('2017-10-01', '2017-10-02', siteId = vid_gorod, returnRecordUrls = True)
	pp.pprint(stats['records'])
	record = requests.get(statCalls['records'][2]['link'], headers = { 'Accept': 'application/json' }, stream = True)
	
	print(stats['records'][2]['link'])
	if record.status_code == 200:
		rec = record.content
		with open('record.mp3', 'wb') as r:
			r.write(rec)
		print('call record has been saved')
	else:
		print(record.status_code)
	pp.pprint(cm.getMessages())
	cm.endSession()
