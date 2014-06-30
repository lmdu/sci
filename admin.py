#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.web
from utils import encrypt_password,join_path

class BaseHandler(tornado.web.RequestHandler):
	@property
	def db(self):
		return self.application.db

	def get_current_user(self):
		admin_id = self.get_secure_cookie("admin")
		if not admin_id: return None
		return self.db.get("SELECT uid,email,name,type FROM user WHERE uid=?", int(admin_id))

	def get_login_url(self):
		return '/admin/login'

	def get_template_path(self):
		template_path = self.application.settings.get("template_path")
		return join_path(template_path, 'admin')


class AdminHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		self.render('index.html')

	def get_login_url(self):
		return '/admin/login'

class LoginHandler(BaseHandler):
	def get(self):
		self.render('login.html')

	def post(self):
		if self.get_current_user():
			raise tornado.web.HTTPError(403)
		name = self.get_argument('name')
		pwd = self.get_argument('password')
		if name == '' or pwd == '':
			self.write('用户名和密码不能为空!')
			return
		pwd = encrypt_password(pwd)
		sql = "SELECT uid FROM user WHERE name=? AND password=? AND type>=10 LIMIT 1"
		user = self.db.get(sql, name, pwd)
		print user
		if user:
			self.set_secure_cookie("admin", str(user.uid))
			self.redirect(self.get_argument('next', '/admin'))
		else:
			self.write('用户名或密码不正确!')

class LogoutHandler(BaseHandler):
	def get(self):
		self.clear_cookie("admin")
		self.redirect(self.get_argument('next', '/admin'))


adminUrls = [
	(r'/admin', AdminHandler),
	(r'/admin/login', LoginHandler),
	(r'/admin/logout', LogoutHandler)
]