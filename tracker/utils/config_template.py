#!/usr/bin/python

"""

monedaTeja 0.1 :: Configuration File

"""

# COMMUNITY
'''
Currency hashtag, name of trustlist and seed_user to crawl from (no '@'). Must be lowercase!

Please use a different hashtag for testing.

'''

HASHTAG = '#monedateja'
ALT_HASHTAG = '#1T'
ISSUER_ACCOUNT = 'lowfill_devel'


# TWITTER API CREDENTIALS
'''
Register an app with read/write access at http://dev.twitter.com.
'''

TW_CONSUMER_KEY = 'z9ipY0MY6OO2XeoubfMg'
TW_CONSUMER_SECRET = '3E8AF38oXQSeIZEDRCWrkzQ32n58rcaYnexAVkLSA'

TW_ACCESS_KEY = '1291767895-uCC4HPJZzfcdQeAALKhvI7B63vOO8QHJaNcNgns'
TW_ACCESS_SECRET = 'GFYCMTSgfLbIEXJTgLB26RWOy87Idxxl1ucwRvs'

# LOG PATH
'''
Absolute path to a log file in /tracker/logs
'''

LOG_PATH = 'logs/tracker.log'


# MYSQL DATABASE
'''
MySQL database credentials. Socket locations can vary depending on the system.
'''

MYSQL_HOST = 'localhost'
MYSQL_USER = 'lowfill'
MYSQL_DATABASE = 'monedateja'
MYSQL_PASSWORD = 'mko09ijn'
MYSQL_SOCKET = '/tmp/mysql.sock'


# SETTINGS
'''
Set tweet to true to tweet syntax errors via the main Twitter account.
Set debug to true to log debug messages
TWIPM tweets a weekly summary of activity in the tracker.
'''

SETTINGS = {
    'tweet' : False,
    'debug' : False,
    'twipm' : False,
}
