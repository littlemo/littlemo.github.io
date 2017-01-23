#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = '小貘'
SITENAME = '幻冥极地'
SITEURL = ''

THEME = "../pelican-themes/Flex"
PLUGIN_PATHS = ['../pelican-plugins']
PLUGINS = [
    'related_posts',    # 相关post
    'post_stats',       # post统计
    'sitemap',          # 站点地图
    # 'i18n_subsites',    # 国际化
    'tag_cloud',        # 标签云
]

PATH = 'content'
OUTPUT_PATH = '/Users/moore/ServerData/test/mnt/html/'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = 'zh'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    # ('Git私服', 'https://git.mojia.date/'),
    # ('Pypi私服', 'https://pypi.mojia.date/'),
)

# Social widget
SOCIAL = (
    # ('weibo', 'http://weibo.com/moorehy'),
    # ('github', 'https://github.com/littlemo'),
    # ('twitter', 'https://twitter.com/LittleMotwo'),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True


ARTICLE_PATHS = ['articles']
_ARTICLE_PREFIX = 'posts/{date:%Y}/{date:%m}/'
ARTICLE_URL = _ARTICLE_PREFIX + '{slug}.html'
ARTICLE_SAVE_AS = _ARTICLE_PREFIX + '{slug}.html'
ARTICLE_LANG_URL = _ARTICLE_PREFIX + '{slug}-{lang}.html'
ARTICLE_LANG_SAVE_AS = _ARTICLE_PREFIX + '{slug}-{lang}.html'

USE_FOLDER_AS_CATEGORY = False

# PYGMENTS_RST_OPTIONS = {'linenos': 'table'}

# Sitemap插件
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.6,
        'indexes': 0.6,
        'pages': 0.5,
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    },
    'exclude': ['tag/', 'category/'],
}

# 标签云插件
TAG_CLOUD_ENABLED = True  # 开启标签云插件
TAG_CLOUD_STEPS = 4  # Count of different font sizes in the tag cloud.
TAG_CLOUD_MAX_ITEMS = 100  # Maximum number of tags in the cloud.
TAG_CLOUD_SORTING = 'size'  # The tag cloud ordering scheme. Valid values: random, alphabetically, alphabetically-rev, size and size-rev
TAG_CLOUD_BADGE = True  # Optionnal setting : can bring badges, which mean say : display the number of each tags present on all articles.

# 访问量统计支持(Base on LeanCloud)
PAGE_VIEW_ENABLED = True
PAGE_VIEW_APP_ID = 'wxkPfkOzYFWCWLSG7hDkIgIw-gzGzoHsz'
PAGE_VIEW_KEY = 'VwaBlqSBLoUTjRL6E94vjF8T'
PAGE_VIEW_COUNTER_NAME = 'PageViewCounter'

# Flex主题相关配置
# 参考: https://github.com/alexandrevicenzi/blog/blob/master/pelicanconf.py
SITETITLE = AUTHOR
SITESUBTITLE = '逝者如斯夫，不舍昼夜'
SITEDESCRIPTION = '开发,编程,软件,Python,码农,Blog,工程师,程序员'
SITELOGO = '//s.gravatar.com/avatar/cb7df89c872ae4af496b6b9e94520ffe?s=80'
FAVICON = SITEURL + '/images/logo_128x128.png'

BROWSER_COLOR = '#333'
PYGMENTS_STYLE = 'monokai'  # 备选: fruity

ROBOTS = 'index, follow'

# Enable i18n plugin.
# PLUGINS = ['i18n_subsites']
# Enable Jinja2 i18n extension used to parse translations.
# JINJA_EXTENSIONS = ['jinja2.ext.i18n']

# Translate to German.
# DEFAULT_LANG = 'de'
# OG_LOCALE = 'zh_CN'
# LOCALE = 'zh_CN'

# Default theme language.
I18N_TEMPLATES_LANG = 'en'

DATE_FORMATS = {
    'en': '%B %d, %Y',
    'zh': '%Y-%m-%d',
}

MAIN_MENU = True
MENUITEMS = (('归档', '/archives.html'),
             ('分类', '/categories.html'),
             ('标签', '/tags.html'),)

CC_LICENSE = {
    'name': 'Creative Commons Attribution-ShareAlike',
    'version': '4.0',
    'slug': 'by-sa'
}

COPYRIGHT_YEAR = 2016

DEFAULT_PAGINATION = 10

ADD_THIS_ID = 'ra-588421ee4f962fa3'
# DISQUS_SITENAME = 'mojia'
DUOSHUO_SITENAME = 'mojia'

BAIDU_TONGJI = 'e5adea2cf336e2e74a60b7b318074ae4'
# GOOGLE_ANALYTICS = 'UA-1234-5678'
# GOOGLE_TAG_MANAGER = 'GTM-ABCDEF'

# Google广告
# GOOGLE_ADSENSE = {
#     'ca_id': 'ca-pub-1234567890',    # Your AdSense ID
#     'page_level_ads': True,          # Allow Page Level Ads (mobile)
#     'ads': {
#         'aside': '1234561',          # Side bar banner (all pages)
#         'main_menu': '1234562',      # Banner before main menu (all pages)
#         'index_top': '1234563',      # Banner after main menu (index only)
#         'index_bottom': '1234564',   # Banner before footer (index only)
#         'article_top': '1234565',    # Banner after article title (article only)
#         'article_bottom': '1234566', # Banner after article content (article only)
#     }
# }

# STATUSCAKE = {
#     'trackid': 'SL0UAgrsYP',
#     'days': 7,
#     'rumid': 6852,
#     'design': 6,
# }

STATIC_PATHS = ['images', 'extra', 'fonts']

EXTRA_PATH_METADATA = {
    'extra/custom.css': {'path': 'static/custom.css'},
    'extra/theme.css.map': {'path': 'static/theme.css.map'},
    'extra/theme.css': {'path': 'static/theme.css'},
}
CUSTOM_CSS_BEFORE_THEME = [
    'static/theme.css',
]
CUSTOM_CSS = [
    'static/custom.css',
]

USE_LESS = True
