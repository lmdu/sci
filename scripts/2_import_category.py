#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import sys

from pysqlite2 import dbapi2 as sqlite3

reload(sys)
sys.setdefaultencoding('UTF-8')

conn = sqlite3.connect("jcr.db")

cursor = conn.cursor()

path = "../category"

def check(val):
	if val == u"\u00a0" or val== u"\xa0":
		val = None
	return val

for j in os.listdir(path):
	p = os.path.join(path, j)
	
	if os.path.isdir(p):
		continue
	
	with open(p) as fp:
		cats = json.load(fp)

	for c in cats:
		vs = [None]
		for k in ('category','mfactor', 'afactor', 'aindex', 'ahalf', 'cites', 'articles'):
			vs.append(check(c[k].strip()))
		cursor.execute("INSERT INTO subject(sid,name,medianFactor,aggregateFactor,immediacyIndex,halfLife,cites,articles) VALUES (?,?,?,?,?,?,?,?)", vs)
		
conn.commit()
conn.close()