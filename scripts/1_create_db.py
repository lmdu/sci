#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pysqlite2 import dbapi2 as sqlite3

sql = '''
CREATE TABLE IF NOT EXISTS `journal` (
	`jid` INTEGER PRIMARY KEY,
	`issn` TEXT,
	`title` TEXT,
	`abbrev` TEXT,
	`isoAbbrev` TEXT,
	`jcrAbbrev` TEXT,
	`factor` REAL,
	`fiveFactor` REAL,
	`issue` INTEGER,
	`articles` INTEGER,
	`cites` INTEGER,
	`halfLife` TEXT,
	`immediacyIndex` REAL,
	`eigenFactor` REAL,
	`influenceScore` REAL,
	`homepage` TEXT,
	`guideLink` TEXT,
	`lid` INTEGER,
	`cid` INTEGER,
	`pid` INTEGER,
	`views` INTEGER
);

CREATE TABLE IF NOT EXISTS `language` (
	`lid` INTEGER PRIMARY KEY,
	`name` TEXT,
	`translate` TEXT,
	`count` INTEGER
);

CREATE TABLE IF NOT EXISTS `country` (
	`cid` INTEGER PRIMARY KEY,
	`name` TEXT,
	`translate` TEXT,
	`abbrev` TEXT,
	`count` INTEGER
);

CREATE TABLE IF NOT EXISTS `publisher` (
	`pid` INTEGER PRIMARY KEY,
	`name` TEXT,
	`address` TEXT,
	`count` INTEGER
);

CREATE TABLE IF NOT EXISTS `subject` (
	`sid` INTEGER PRIMARY KEY,
	`name` TEXT,
	`translate` TEXT,
	`medianFactor` REAL,
	`aggregateFactor` REAL,
	`immediacyIndex` REAL,
	`halfLife` TEXT,
	`cites` INTEGER,
	`articles` INTEGER,
	`count` INTEGER
);

CREATE TABLE IF NOT EXISTS `relationship` (
	`jid` INTEGER,
	`sid` INTEGER
);

CREATE TABLE IF NOT EXISTS `history` (
	`jid` INTEGER,
	`year` INTEGER,
	`factor` REAL,
	`fiveFactor` REAL,
	`immediacyIndex` REAL,
	`eigenFactor` REAL,
	`influenceScore` REAL,
	`halfLife` TEXT,
	`articles` INTEGER,
	`cites` INTEGER
);

CREATE TABLE IF NOT EXISTS `user` (
	`uid` INTEGER PRIMARY KEY,
	`email` TEXT,
	`name` TEXT,
	`password` TEXT,
	`type` INTEGER,
	`created` INTEGER
);

CREATE TABLE IF NOT EXISTS `comment` (
	`cid` INTEGER PRIMARY KEY,
	`jid` INTEGER,
	`uid` INTEGER,
	`content` TEXT,
	`ip` TEXT,
	`approved` INTEGER,
	`agent` TEXT,
	`review` INTEGER,
	`submit` INTEGER,
	`doi` INTEGER,
	`created` INTEGER
);

CREATE TABLE IF NOT EXISTS `focus` (
	`uid` INTEGER,
	`jid` INTEGER,
	`created` INTEGER
);
'''

conn = sqlite3.connect("jcr.db")
cursor = conn.cursor()
cursor.executescript(sql)

conn.commit()
conn.close()