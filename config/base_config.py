# -*- coding: utf-8 -*-
# Copyright (c) 2025 relakkes@gmail.com
#
# This file is part of MediaCrawler project.
# Repository: https://github.com/NanmiCoder/MediaCrawler/blob/main/config/base_config.py
# GitHub: https://github.com/NanmiCoder
# Licensed under NON-COMMERCIAL LEARNING LICENSE 1.1
#

# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：
# 1. 不得用于任何商业用途。
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。
# 3. 不得进行大规模爬取或对平台造成运营干扰。
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。
# 5. 不得用于任何非法或不当的用途。
#
# 详细许可条款请参阅项目根目录下的LICENSE文件。
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。

# Basic configuration
PLATFORM = "bili"  # Platform, xhs | dy | ks | bili | wb | tieba | zhihu

# 是否使用海外版小红书 (rednote.com)
# 开启后 API 走 webapi.rednote.com，cookie 域使用 .rednote.com
XHS_INTERNATIONAL = False

KEYWORDS = "编程副业,编程兼职"  # Keyword search configuration, separated by English commas
LOGIN_TYPE = "qrcode"  # qrcode or phone or cookie
COOKIES = ""
CRAWLER_TYPE = "creator"  # Crawling type, search (keyword search) | detail (post details) | creator (creator homepage data)
# Whether to enable IP proxy
ENABLE_IP_PROXY = False

# Number of proxy IP pools
IP_PROXY_POOL_COUNT = 2

# Proxy IP provider name
IP_PROXY_PROVIDER_NAME = "kuaidaili"  # kuaidaili | wandouhttp

# Setting to True will not open the browser (headless browser)
# Setting False will open a browser
# If Xiaohongshu keeps scanning the code to log in but fails, open the browser and manually pass the sliding verification code.
# If Douyin keeps prompting failure, open the browser and see if mobile phone number verification appears after scanning the QR code to log in. If it does, manually go through it and try again.
HEADLESS = False

# Whether to save login status
SAVE_LOGIN_STATE = True

# ==================== CDP (Chrome DevTools Protocol) 配置 ====================
# Whether to enable CDP mode
ENABLE_CDP_MODE = False

# Whether to enable crawling media mode (including image or video resources)
ENABLE_GET_MEIDAS = True

# Data saving type option configuration, supports: csv, db, json, jsonl, sqlite, excel, postgres. It is best to save to DB, with deduplication function.
SAVE_DATA_OPTION = "jsonl"  # csv or db or json or jsonl or sqlite or excel or postgres

# Data saving path, if not specified by default, it will be saved to the data folder.
SAVE_DATA_PATH = "H:/C#/tool/MediaCrawler/data"

# Browser file configuration cached by the user's browser
USER_DATA_DIR = "%s_user_data_dir"  # %s will be replaced by platform name

# The number of pages to start crawling starts from the first page by default
START_PAGE = 1

# Control the number of crawled videos/posts
CRAWLER_MAX_NOTES_COUNT = 100

# Controlling the number of concurrent crawlers
MAX_CONCURRENCY_NUM = 1

# Whether to enable comment crawling mode. Comment crawling is enabled by default.
ENABLE_GET_COMMENTS = True

# Control the number of crawled first-level comments (single video/post)
CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES = 10

# Whether to enable the mode of crawling second-level comments. By default, crawling of second-level comments is not enabled.
# If the old version of the project uses db, you need to refer to schema/tables.sql line 287 to add table fields.
ENABLE_GET_SUB_COMMENTS = False

# word cloud related
# Whether to enable generating comment word clouds
ENABLE_GET_WORDCLOUD = False
# Custom words and their groups
# Add rule: xx:yy where xx is a custom-added phrase, and yy is the group name to which the phrase xx is assigned.
CUSTOM_WORDS = {
    "零几": "年份",  # Recognize "zero points" as a whole
    "高频词": "专业术语",  # Example custom words
}

# Deactivate (disabled) word file path
STOP_WORDS_FILE = "./docs/hit_stopwords.txt"

# Chinese font file path
FONT_PATH = "./docs/STZHONGS.TTF"

# Crawl interval
CRAWLER_MAX_SLEEP_SEC = 2

# 是否禁用 SSL 证书验证。仅在使用企业代理、Burp Suite、mitmproxy 等会注入自签名证书的中间人代理时设为 True。
# 警告：禁用 SSL 验证将使所有流量暴露于中间人攻击风险，请勿在生产环境中开启。
DISABLE_SSL_VERIFY = False

from .bilibili_config import *
from .xhs_config import *
from .dy_config import *
from .ks_config import *
from .weibo_config import *
from .tieba_config import *
from .zhihu_config import *

# ==================== 动态加载用户自定义配置 (user_settings.json) ====================
def load_user_settings():
    import json
    import os
    import re
    json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "user_settings.json")
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                content = f.read()
                try:
                    user_settings = json.loads(content)
                except json.JSONDecodeError:
                    # 自动修复 Windows 路径常见的单反斜杠问题
                    # 规则：匹配反斜杠 \，且其后不是有效的 JSON 转义字符 (\\, \", \/, \b, \f, \n, \r, \t, \u)
                    fixed_content = re.sub(r'\\(?![\\"/bfnrtu])', '/', content)
                    user_settings = json.loads(fixed_content)
                    print(f"[Config] 检测到 user_settings.json 格式错误（路径单反斜杠），已自动修正加载")
                
                for key, value in user_settings.items():
                    # 将 JSON 中的配置注入到全局变量中
                    globals()[key] = value
                print(f"[Config] 已从 user_settings.json 成功加载自定义配置")
        except Exception as e:
            print(f"[Config] 加载 user_settings.json 失败: {e}")

load_user_settings()
