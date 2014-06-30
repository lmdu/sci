#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import sys
reload(sys)
sys.setdefaultencoding("utf8")

import litedb
import tornado.autoreload
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.httpserver
from tornado.options import options, define

import config

from admin import adminUrls
from front import frontUrls

define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
	def __init__(self):
		settings = dict(
			debug = True,
			gzip = True,
			#xsrf_cookies = True,
			template_path = config.TEMPLATE_PATH,
			static_path = config.STATIC_PATH,
			qq_app_id = config.QQ_APP_ID,
			qq_app_key = config.QQ_APP_KEY,
			
			#generate secret base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
			cookie_secret = 'DZeGSPAMSFucHmx3PxntevoZxQJvbUUmlJrUSmyhF3I=',
			login_url = '/login'
		)

		super(Application, self).__init__(adminUrls + frontUrls, **settings)

		self.db = litedb.Connection(config.DB_FILE)

class NotFound(tornado.web.RequestHandler):
	def get(self):
		raise tornado.web.HTTPError(404)

if __name__ == '__main__':
	http_server = tornado.httpserver.HTTPServer(Application(), xheaders=True)
	tornado.options.parse_command_line()
	tornado.web.ErrorHandler = NotFound
	http_server.listen(options.port)
	loop = tornado.ioloop.IOLoop.instance()
	tornado.autoreload.start(loop)
	loop.start()