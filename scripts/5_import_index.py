#!/usr/bin/env python

import os
import json
import sys

from pysqlite2 import dbapi2 as sqlite3

reload(sys)
sys.setdefaultencoding('UTF-8')

conn = sqlite3.connect("jcr.db")
cur = conn.cursor()

sql = """
	CREATE INDEX issn_idx ON journal(issn);
	CREATE INDEX title_idx ON journal(title);
	CREATE INDEX abbrev_idx on journal(abbrev);
	CREATE INDEX factor_idx on journal(factor);
	CREATE INDEX factor5_idx on journal(fiveFactor);
	CREATE INDEX article_idx on journal(articles);
	CREATE INDEX cite_idx on journal(cites);
	CREATE INDEX imme_idx on journal(immediacyIndex);
	CREATE INDEX relate_idx on relationship(jid,sid);
	CREATE INDEX his_idx on history(jid, year);
"""
cur.executescript(sql)
cur.execute("create virtual table search using fts3(issn,title,abbrev)")
cur.execute("SELECT jid,issn,title,abbrev FROM journal")
for row in cur.fetchall():
	cur.execute("INSERT INTO search(docid,issn,title,abbrev) VALUES(?,?,?,?)", tuple(row))

conn.commit()
conn.close()