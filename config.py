#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

#sqlite database file
DB_FILE = os.path.join(os.path.dirname(__file__), "jcr.db")

#template path
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'template')

#static file path
STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static')

#upload directory
UPLOAD_PATH = os.path.join(STATIC_PATH, 'upload')

#QQ connection and login
QQ_APP_ID = '101105313'
QQ_APP_KEY = 'b7c4b643ae6dd6d257deb9c8376825f0'
