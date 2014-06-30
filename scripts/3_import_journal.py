#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import json
import warnings

from pysqlite2 import dbapi2 as sqlite3

reload(sys)
sys.setdefaultencoding('UTF-8')

conn = sqlite3.connect('jcr.db')
cur = conn.cursor()

def get_lang_id(name):
	cur.execute("SELECT lid FROM language WHERE name=? LIMIT 1", (name,))
	row = cur.fetchone()
	if row is None:
		cur.execute("INSERT INTO language(name) VALUES (?)", (name,))
		return cur.lastrowid
	else:
		return row[0]

def get_pub_id(name, address):
	cur.execute("SELECT pid FROM publisher WHERE name=? LIMIT 1", (name,))
	row = cur.fetchone()
	if row is None:
		cur.execute("INSERT INTO publisher(name,address) VALUES (?, ?)", (name, address))
		return cur.lastrowid
	else:
		return row[0]

def get_con_id(name):
	cur.execute("SELECT cid FROM country WHERE name=? LIMIT 1", (name,))
	row = cur.fetchone()
	if row is None:
		cur.execute("INSERT INTO country(name) VALUES (?)", (name,))
		return cur.lastrowid
	else:
		return row[0]

def get_cat_id(name):
	cur.execute("SELECT sid FROM subject WHERE name=? LIMIT 1", (name,))
	row = cur.fetchone()
	return row[0]

def check(val):
	if val == u"\u00a0" or val== u"\xa0":
		val = None
	return val

error = 1

path = "../journal"

sql = "INSERT INTO journal(jid,issn,title,abbrev,isoAbbrev,jcrAbbrev,factor, \
	fiveFactor,issue,articles,cites,halfLife,immediacyIndex,eigenFactor, \
	influenceScore,lid,cid,pid) VALUES (%s)" % ",".join(["?"]*18)

country = {}
publisher = {}
language = {}
category = {}

for js in os.listdir(path):
	if not js.endswith(".json"): 
		continue
	
	with open(os.path.join(path, js)) as fh:
		mags = json.load(fh)

	for m in mags:
		
		infos = [None]
		
		if m['issn'] == '****-****':
			with open("../details/error%s.json" % error) as fh:
				d = json.load(fh)
				error += 1
		else:
			with open("../details/%s.json" % m['issn']) as fh:
				d = json.load(fh)

		infos.append(m['issn'])
		infos.append(d['full_title'])
		infos.append(m['abbr'])
		infos.append(d['iso_abbrev'])
		infos.append(d['jcr_abbrev'])
		infos.append(check(m['factor']))
		infos.append(check(m['5year']))
		infos.append(check(d['issues']))
		infos.append(check(m['articles']))
		infos.append(check(m['cites']))
		infos.append(check(m['half']))
		infos.append(check(m['index']))
		infos.append(check(m['efs']))
		infos.append(check(m['ais']))
		
		lid = get_lang_id(d['language'])
		infos.append(lid)
		
		try:
			language[lid] += 1
		except KeyError:
			language[lid] = 1

		cid = get_con_id(d['country'])
		infos.append(cid)

		try:
			country[cid] += 1
		except KeyError:
			country[cid] = 1

		pid = get_pub_id(d['publisher'], d['address'])
		infos.append(pid)

		try:
			publisher[pid] += 1
		except KeyError:
			publisher[pid] = 1

		cur.execute(sql, infos)

		jid = cur.lastrowid

		for cat in d['category']:
			cid = get_cat_id(cat)
			cur.execute("INSERT INTO relationship(jid, sid) VALUES (?,?)", (jid, cid))
			try:
				category[cid] += 1
			except KeyError:
				category[cid] = 1

for ID in publisher:
	cur.execute("UPDATE publisher SET count=? WHERE pid=?", (publisher[ID], ID))

for ID in country:
	cur.execute("UPDATE country SET count=? WHERE cid=?", (country[ID], ID))

for ID in language:
	cur.execute("UPDATE language SET count=? WHERE lid=?", (language[ID], ID))

for ID in category:
	cur.execute("UPDATE subject SET count=? WHERE sid=?", (category[ID], ID))

conn.commit()
conn.close()