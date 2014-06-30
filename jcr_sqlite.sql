create table if not exists `journals` (
	jid integer primary key,
	issn text,
	name text,
	abbrev text,
	isoAbbrev text,
	jcrAbbrev text,
	factor real,
	fiveFactor real,
	issue integer,
	articles integer,
	cites integer,
	halflife text,
	immediacyIndex real, 
	eigenfactor real, 
	influenceScore real,
	lid integer,
	coid integer,
	pid integer,
	views integer
);

create table if not exists `languages` (
	lid integer primary key,
	name text,
	journals integer
);

create table if not exists `countries` (
	coid integer primary key,
	name text,
	abbrev text,
	journals integer
);

create table if not exists `categories` (
	caid integer primary key,
	name text,
	cites integer,
	medianFactor real,
	aggregateFactor real,
	immediacyIndex real,
	halflife text,
	journals integer,
	articles integer
);

create table if not exists `relations` (
	rid integer primary key,
	jid integer,
	caid integer,
	rank integer,
	quartile text
);

create table if not exists `publishers` (
	pid integer primary key,
	name text,
	address text,
	journals integer
);

create table if not exists `factors` (
	fid integer primary key,
	jid integer,
	year integer,
	factor real
);