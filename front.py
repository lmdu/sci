#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import hashlib
import time
import codecs
import tornado.escape
import tornado.web
import tornado.gen
from config import UPLOAD_PATH
from utils import xdict, QQGraphMixin

class BaseHandler(tornado.web.RequestHandler):
	@property
	def db(self):
		return self.application.db

	def get_current_user(self):
		user_id = self.get_secure_cookie("user")
		if not user_id: return None
		return self.db.get("SELECT uid,email,name FROM user WHERE uid=?", int(user_id))

	def get_template_path(self):
		return os.path.join(self.application.settings.get("template_path"), "front")

	def write_error(self, status_code, **kwargs):
		if status_code == 404:
			self.render('404.html')
		elif status_code == 500:
			self.render('500.html')
		else:
			super(BaseHandler, self).write_error(status_code, **kwargs)

class LoginHandler(BaseHandler, QQGraphMixin):
	@tornado.web.asynchronous
	@tornado.gen.coroutine
	def get(self):
		#next = self.get_argument('next', '/')
		#if self.get_current_user():
		#	self.redirect(next)
		#else:
		#	self.render('login.html', msg=None, next=next)
		redirect_uri = 'http://sci.elegantr.com/login'
		code = self.get_argument('code', False)
		if code:
			user = yield self.get_authenticated_user(
				redirect_uri=redirect_uri,
				client_id=self.settings['qq_app_id'],
				client_secret=self.settings['qq_app_key'],
				code=self.get_argument("code")
			)
			self.finish(user)
		else:
			yield self.authorize_redirect(
				redirect_uri=redirect_uri,
				client_id=self.settings['qq_app_id'],
				extra_params=dict(response_type="code")
			)

	def post(self):
		if self.get_current_user():
			raise tornado.web.HTTPError(403)
		email = self.get_argument('email')
		pwd = self.get_argument('password')
		pwd = hashlib.sha1(pwd).hexdigest()
		user = self.db.get("SELECT uid FROM user WHERE email=? AND password=?", email, pwd)
		if user:
			self.set_secure_cookie("user", str(user.uid))
			self.redirect(self.get_argument('next', '/'))
		else:
			self.render('login.html', msg="邮箱或密码错误")

class LogoutHandler(BaseHandler):
	def get(self):
		self.clear_cookie("user")
		self.redirect(self.get_argument('next', '/'))

class RegisterHandler(BaseHandler):
	def get(self):
		self.render('register.html', msg=None)

	def post(self):
		email = self.get_argument('email')
		name = self.get_argument('name')
		pwd = self.get_argument('password')
		res = self.db.get("SELECT 1 FROM user WHERE email=? LIMIT 1", email)
		if res:
			self.render('register.html', msg="邮箱已存在!")
			return
		res = self.db.get("SELECT 1 FROM user WHERE name=? LIMIT 1", name)
		if res:
			self.render('register.html', msg="用户名已存在!")
			return
		pwd = hashlib.sha1(pwd).hexdigest()
		date = int(time.time())
		sql = "INSERT INTO user(email,name,password,type,created) VALUES (?,?,?,?,?)"
		self.db.insert(sql, email, name, pwd, 1, date)
		self.redirect('/login')

class MainHandler(BaseHandler):
	def get(self):
		'''Display the index page.'''
		mostViewed = self.db.query("SELECT jid,title,views FROM journal ORDER BY views DESC LIMIT 10")
		views = self.db.get("SELECT SUM(views) AS views FROM journal")['views']
		journalNum = self.db.get("SELECT COUNT(1) AS total FROM journal")['total']
		subjectNum = self.db.get("SELECT COUNT(1) AS subject FROM subject")['subject']
		languageNum = self.db.get("SELECT COUNT(1) AS language FROM language")['language']
		countryNum = self.db.get("SELECT COUNT(1) AS country FROM country")['country']
		mosts = self.db.query("SELECT jid,title,factor FROM journal ORDER BY factor DESC LIMIT 10")
		self.render('index.html',
			hots=mostViewed, 
			views=views,
			journalNum=journalNum, 
			subjectNum=subjectNum, 
			languageNum=languageNum, 
			countryNum=countryNum, 
			mosts=mosts
		)

	def post(self):
		'''Do ajax search for index search input auto complete.'''
		term = '"%s*"' % self.get_argument('s')
		sql = (
			"SELECT docid,snippet(search) AS target,factor FROM search,journal"
			" WHERE search MATCH ? AND docid=jid ORDER BY target LIMIT 10"
		)
		content = ""
		for r in self.db.query(sql, term):
			content += '<li><a href="/journal/%s">%s</a><strong>%s</strong></li>' \
				% (r.docid, r.target, r.factor)
		self.write(content)

class SearchHandler(BaseHandler):
	def post(self):
		term = self.get_argument('s')
		sql = (
			"SELECT j.jid, s.title, s.abbrev, s.issn, j.factor FROM search s,journal j"
			" WHERE search MATCH ? AND s.docid=j.jid ORDER BY snippet(search)"
		)
		res = self.db.query(sql, '"%s*"' % term)
		self.render("search.html", mags = res, term=term)

class JournalHandler(BaseHandler):
	def get(self, jid):
		jid = int(jid)
		sql = "SELECT * FROM journal WHERE jid=? LIMIT 1"
		journal = self.db.get(sql, jid)
		
		if journal is None:
			self.render('error.html')
			return

		#get category information
		sql = (
			"SELECT s.sid,name,translate FROM subject s, relationship r"
			" WHERE s.sid=r.sid AND r.jid=?"
		)
		journal.category = [
			xdict(
				sid=row.sid,
				name=row.name,
				tr=row.translate,
				rank=self.get_rank(row.sid, jid)
			)
			for row in self.db.query(sql, jid)
		]
		
		#get language information
		sql = "SELECT lid,name,translate AS tr FROM language WHERE lid=?"
		journal.language = self.db.get(sql, journal.lid)
		
		#get country information
		sql = "SELECT cid,name,translate AS tr FROM country WHERE cid=?"
		journal.country = self.db.get(sql, journal.cid)
		
		#get publisher information
		sql = "SELECT pid,name,address FROM publisher WHERE pid=?"
		journal.publisher = self.db.get(sql, journal.pid)

		#get history data
		sql = (
			"SELECT year,factor,fiveFactor,articles,cites FROM history"
			" WHERE jid=? ORDER BY year"
		)
		res = self.db.query(sql, jid)
		journal.history = xdict({
			k: ",".join([str(row[k]) if row[k] else 'null' for row in res])
			for k in ('year', 'factor', 'fiveFactor','articles', 'cites')
		})

		#get journal clicked or view number
		sql = "SELECT views FROM journal WHERE jid=?"
		clickNum = self.db.get(sql, jid).views or 0
		
		#get comments information of a journal
		comment = self.get_comments(jid)
		
		self.render('journal.html',
			j=journal,
			clickNum = clickNum,
			acceptRate = comment[0],
			monthAvg = comment[1],
			commentNum = comment[2],
			comments = comment[3]
		)

		self.db.update("UPDATE journal SET views=views+1 WHERE jid=?", jid)

	def get_rank(self, catId, jid):
		sql = (
			"SELECT j.jid,factor FROM journal j, relationship r"
			" WHERE j.jid=r.jid AND r.sid=? ORDER BY factor DESC"
		)
		for rank,j in enumerate(self.db.query(sql, catId)):
			if j.jid == jid:
				if j.factor is None: return "暂无"
				return rank + 1

	def get_comments(self, jid):
		sql = (
			"SELECT c.content,c.review,c.submit,c.doi,c.created,u.uid,u.name"
			" FROM comment c, user u WHERE c.uid=u.uid AND c.jid=?"
			" ORDER BY c.created DESC"
		)
		res = self.db.query(sql, jid)
		if not res: return 0, 0, 0, None
		monthes, accepts = 0, 0
		for r in res:
			if r.submit == 1:
				accepts += 1
			monthes += r.review
		commentNum = len(res)
		acceptRate = round(float(accepts)/commentNum*100, 2)
		monthAvg = int(float(monthes)/commentNum)
		return acceptRate, monthAvg, commentNum, res

class CategoryHandler(BaseHandler):
	def get(self, catId=None):
		if catId:
			category = self.db.get("SELECT * FROM subject WHERE sid=?", catId)
			sql = (
				"SELECT j.jid,issn,title,abbrev,factor FROM journal j,"
				" relationship r WHERE r.jid=j.jid AND r.sid=?"
			)
			res = self.db.query(sql, catId)
			self.render('subject.html', mags=res, cat=category)
		else:
			sql = "SELECT sid,name,translate,medianFactor,immediacyIndex,count FROM subject"
			res = self.db.query(sql)
			self.render('subjects.html', cats=res)

class CountryHandler(BaseHandler):
	def get(self, cid=None):
		if cid:
			country = self.db.get("SELECT translate FROM country WHERE cid=?", cid)
			if not country:
				raise tornado.web.HTTPError(404)
			sql = (
				"SELECT jid,issn,title,abbrev,factor"
				" FROM journal WHERE cid=?"
			)
			res = self.db.query(sql, cid)
			self.render('category.html', mags=res, title="%sSCI期刊" % country.translate)
		else:
			res = self.db.query("SELECT * FROM country ORDER BY count DESC")
			self.render('countries.html', countries=res)

class LanguageHandler(BaseHandler):
	def get(self, lid=None):
		if lid:
			language = self.db.get("SELECT translate FROM language WHERE lid=?", lid)
			if not language:
				raise tornado.web.HTTPError(404)
			sql = (
				"SELECT jid,issn,title,abbrev,factor"
				" FROM journal WHERE lid=?"
			)
			res = self.db.query(sql, lid)
			self.render('category.html', mags=res, title="%sSCI期刊" % language.translate)
		else:
			res = self.db.query("SELECT * FROM language ORDER BY count DESC")
			self.render('languages.html', languages=res)

class PublisherHandler(BaseHandler):
	def get(self, pid=None):
		if pid:
			publisher = self.db.get("SELECT name FROM publisher WHERE pid=?", pid)
			if not publisher:
				raise tornado.web.HTTPError(404)
			sql = (
				"SELECT jid,issn,title,abbrev,factor"
				" FROM journal WHERE pid=?"
			)
			res = self.db.query(sql, pid)
			self.render('category.html', mags=res, title="%s SCI期刊" % publisher.name)
		else:
			res = self.db.query("SELECT * FROM publisher ORDER BY count DESC")
			self.render('publishers.html', publishers=res)

class CommentHandler(BaseHandler):
	def post(self):
		if self.current_user is None:
			self.redirect('/login')
			return
		accept = self.get_argument('accept')
		month = self.get_argument('month')
		doi = self.get_argument('doi', None)
		content = self.get_argument('content')
		jid = self.get_argument('jid')
		user = self.current_user.uid
		ip = self.request.remote_ip
		agent = self.request.headers.get('User-Agent', None)
		date = int(time.time())
		sql = (
			"INSERT INTO comment(jid,uid,content,ip,agent,review,submit,doi,created,approved)" 
			" VALUES (?,?,?,?,?,?,?,?,?,?)"
		)
		self.db.insert(sql, jid, user, content, ip, agent, month, accept, doi, date, 0)
		self.redirect(self.get_argument('next', '/'))

class PersonalHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self, action=None):
		if action is None:
			self.render("person.html", msg=None)
		elif action == 'password':
			self.render("password.html", msg=None)
		else:
			self.render('person.html', msg=None)


class AvatarHandler(BaseHandler):
	@tornado.web.authenticated
	def post(self):
		if not self.request.files:
			self.render('person.html', msg="未选择图片")
			return
		avatar = self.request.files['avatar'][0]
		fileext = os.path.splitext(avatar.filename)[1]
		if fileext not in ['.png', '.gif', '.jpg', '.jpeg']:
			self.render('person.html', msg="图片格式不对")
			return
		upload = os.path.join(UPLOAD_PATH, "avatar/%s%s" % (self.current_user.uid, fileext))
		with open(upload, "wb") as fw:
			fw.write(avatar["body"])
		self.redirect(self.get_argument('next', '/'))

class ArchiveHandler(BaseHandler):
	def get(self, action=None):
		self.write("开发中...")

class PageHandler(BaseHandler):
	def get(self, page):
		if page == 'fadeback':
			self.render('fadeback.html')
		elif page == 'about':
			self.render('about.html')
		elif page == 'contact':
			self.render('contact.html')
		else:
			self.write('开发中...')

class BaiduHandler(BaseHandler):
	def get(self):
		self.render("baiduapp.html")

	def post(self):
		term = self.get_argument('s')
		action = self.get_argument('a', None)
		if action == 'suggest':
			res = self.db.search_for_ajax(term)
			content = ""
			if res:
				content = "\n".join(['<li><a href="#">' + str(r[1]) + '</a></li>' for r in res])
			self.write(content)
		else:
			res = self.db.search_for_baidu(term)
			
			if res:
				table = '<table class="width-100 table-bordered"><tbody>%s</tbody></table>'
				inner = '<tr><td><strong>期刊名称:</strong></td><td><a href="/journal/%s.html">%s</a></td></tr>' % (res[0], res[1])
				inner += '<tr><td><strong>名称缩写:</strong></td><td>%s</td></tr>' % res[2]
				inner += '<tr><td><strong>ISSN:</strong></td><td>%s</td></tr>' % res[3]
				inner += '<tr><td><strong>影响因子:</strong></td><td>%s</td></tr>' % res[4]
				content = table % inner
			else:
				content = "未查询到"
			
			self.write(content)

class QQHandler(BaseHandler):
	def get(self):
		jid = self.get_argument('jid', None)
		if jid is None:
			sql = (
				"SELECT jid,title,abbrev,issn,issue,factor,fiveFactor,halfLife"
				" FROM journal ORDER BY views DESC LIMIT 1"
			)
		else:
			sql = (
				"SELECT jid,title,abbrev,issn,issue,factor,fiveFactor,halfLife"
				" FROM journal WHERE jid=%s" % jid 
			)

		journal = self.db.get(sql)
		self.render("qq-index.html", j=journal)

	def post(self):
		term = '"%s*"' % self.get_argument('s')
		sql = (
			"SELECT docid,snippet(search) AS target,factor FROM search,journal"
			" WHERE search MATCH ? AND docid=jid ORDER BY target LIMIT 10"
		)
		content = ""
		for r in self.db.query(sql, term):
			content += '<li><a href="/qq?jid=%s">%s</a><strong>%s</strong></li>' \
				% (r.docid, r.target, r.factor)
		self.write(content)


frontUrls = [
	(r'/', MainHandler),
	(r'/search', SearchHandler),
	(r'/category/*(.*)', CategoryHandler),
	(r'/country/*(.*)', CountryHandler),
	(r'/publisher/*(.*)', PublisherHandler),
	(r'/language/*(.*)', LanguageHandler),
	(r'/journal/(.*)', JournalHandler),
	(r'/page/(.*)', PageHandler),
	(r'/archive/(.*)', ArchiveHandler),
	(r'/login', LoginHandler),
	(r'/logout', LogoutHandler),
	(r'/register', RegisterHandler),
	(r'/comment', CommentHandler),
	(r'/scientist/*(.*)', PersonalHandler),
	(r'/avatar', AvatarHandler),
	(r'/baidu', BaiduHandler),
	(r'/qq', QQHandler)
] 
