#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = ''
RELATIVE_URLS = False

# FEED_ALL_ATOM = 'feeds/all.atom.xml'
# CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

#DISQUS_SITENAME = ""
#GOOGLE_ANALYTICS = ""

# 百度爬虫自动推送使能
SPIDER_BAIDU_ENABLED = True

# 百度统计
BAIDU_TONGJI = 'e5adea2cf336e2e74a60b7b318074ae4'

# 访问量统计支持(Base on LeanCloud)
PAGE_VIEW_ENABLED = True
PAGE_VIEW_APP_ID = 'wxkPfkOzYFWCWLSG7hDkIgIw-gzGzoHsz'
PAGE_VIEW_KEY = 'VwaBlqSBLoUTjRL6E94vjF8T'
PAGE_VIEW_COUNTER_NAME = 'PageViewCounter'
