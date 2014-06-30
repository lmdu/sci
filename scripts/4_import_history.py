#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
import sys

from pysqlite2 import dbapi2 as sqlite3

err_log = open("error.log", "w")

reload(sys)
sys.setdefaultencoding('UTF-8')

conn = sqlite3.connect("jcr.db")
cur = conn.cursor()

IDS = {}
errors = []
error = 0

nofound = 0

def check(val):
	if val == u"\u00a0" or val== u"\xa0":
		val = None
	return val

cur.execute("SELECT jid,issn FROM journal")

for row in cur.fetchall():
	if row[1] == '****-****':
		errors.append(row[0])
	else:
		IDS[row[1]] = row[0]

for folder in range(2003, 2013):
	for js in os.listdir("../" + str(folder)):
		if not js.endswith(".json"): 
			continue

		with open("../%s/%s" % (str(folder), js)) as fh:
			factors = json.load(fh)

		for item in factors:
			
			if item['issn'] == "****-****": 
				continue
			
			try:
				jid = IDS[item['issn']]
			except KeyError:
				err_log.write("%s\t%s\n" % (item['issn'], folder))
				continue

			if folder >= 2007:
				info = (jid, folder, check(item.get('factor')), check(item.get('5year')), check(item.get('index')), check(item.get('efs')), check(item.get('ais')), check(item.get('half')), check(item.get('articles')), check(item.get('cites')))
			else:
				info = (jid, folder, check(item.get('factor')), None, check(item.get('5year')), None, None, check(item.get('articles')), check(item.get('index')), check(item.get('cites')))
			
			cur.execute("INSERT INTO history VALUES (?,?,?,?,?,?,?,?,?,?)", info)
				
conn.commit()
conn.close()