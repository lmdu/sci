#!/usr/bin/evn python
#-*- coding: utf-8 -*-

try:
	import sqlite3
except ImportError:
	from pysqlite2 import dbapi2 as sqlite3

class Row(dict):
	def __getattr__(self, name):
		try:
			return self[name]
		except KeyError:
			raise AttributeError(name)

	def __setattr__(self, name, value):
		self[name] = value

def row_factory(cursor, row):
	column_names = [col[0] for col in cursor.description]
	return Row(zip(column_names, row))

class Connection(object):
	def __init__(self, db, level=None):
		self.level = level
		self.conn = sqlite3.connect(db, isolation_level=level)
		self.conn.row_factory = row_factory

	def __del__(self):
		self.conn.close()

	def _execute(self, cursor, sql, args, kwargs):
		return cursor.execute(sql, args or kwargs)

	def query(self, sql, *args, **kwargs):
		cursor = self.conn.cursor()
		try:
			self._execute(cursor, sql, args, kwargs)
			return cursor.fetchall()
		finally:
			cursor.close()

	def iter(self, sql, *args, **kwargs):
		cursor = self.conn.cursor()
		try:
			self._execute(cursor, sql, args, kwargs)
			for row in cursor:
				yield row
		finally:
			cursor.close()

	def get(self, sql, *args, **kwargs):
		cursor = self.conn.cursor()
		try:
			self._execute(cursor, sql, args, kwargs)
			return cursor.fetchone()
		finally:
			cursor.close()

	def execute(self, sql, *args, **kwargs):
		cursor = self.conn.cursor()
		try:
			self._execute(cursor, sql, args, kwargs)
		finally:
			cursor.close()

	def insert(self, sql, *args, **kwargs):
		cursor = self.conn.cursor()
		try:
			self._execute(cursor, sql, args, kwargs)
			return cursor.lastrowid
		finally:
			if self.level is not None:
				self.conn.commit()
			cursor.close()

	def update(self, sql, *args, **kwargs):
		cursor = self.conn.cursor()
		try:
			self._execute(cursor, sql, args, kwargs)
		finally:
			if self.level is not None:
				self.conn.commit()
			cursor.close()
