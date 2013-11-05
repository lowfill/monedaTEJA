# -*- coding: utf-8 -*-
"""

PunkMoney 0.2 :: parser.py 

Main class for interpreting #PunkMoney statements.

"""

from mysql import Connection
from tejaharvester import Harvester
from config import HASHTAG, ALT_HASHTAG,ISSUER_ACCOUNT, SETTINGS
from objects import Event

import re
from datetime import datetime
from dateutil.relativedelta import *
import time
import sys

'''
TejaParser class 
'''

class Parser(Harvester):

    #TODO Make this i18n
    types_map = {'promise':[u'se comprometió con',
                            u'se enredó con'],
                      'thanks':['@(\w+) gracias|gracias! (por)?(.*)']}
    def __init__(self):
        self.setupLogging()
        self.connectDB()
        self.TW = self.connectTwitter()
    
    '''
    Parse new tweets
    '''
    
    def parseNew(self):  
        
        # Process new tweets
        for tweet in self.getTweets():
            try:
                # If tweet contains 'RT' (e.g. is a retweet), skip
                retweet = False
                for w in tweet['content'].split():
                    if w == 'RT':
                        self.setParsed(tweet['tweet_id'])
                        raise Exception("Tweet is a retweet")
                        
                # Save tweet author to user database
                self.saveUser(tweet['author'])
                
                # Determine tweet type
                tweet_type = None
                operation = None
                for message_type in self.types_map:
                    for expression in self.types_map[message_type]:
                        operation = re.search(expression,tweet['content'],re.IGNORECASE|re.UNICODE)
                        if operation:
                            tweet_type = message_type
                
                #transfer = re.search('transfer @(\w+)(.*)', tweet['content'], re.IGNORECASE)
                #thanks = re.search('@(\w+) thanks|redeemed (for)?(.*)', tweet['content'], re.IGNORECASE)
                #new_thanks = re.search('thanks @(\w+) (for)?(.*)', tweet['content'], re.IGNORECASE)
                
                # strip urls from text
                r = re.search("(.*)(?P<url>https?://[^\s]+)(.*)", tweet['content'], re.IGNORECASE)
                if r:
                    tweet['content'] = r.group(1) + ' ' + r.group(3) 
                
                # Processing the tweet
                if  tweet_type == 'promise':
                    self.parsePromise(tweet)
                elif tweet_type == 'thanks':
                    if operation.group(2):
                        if operation.group(2).lower() == 'por':
                            tweet['message'] = operation.group(3)
                    else:
                        tweet['message'] = ''
                
                    self.parseThanks(tweet)
                else:
                    self.parsePayment(tweet)
                    #self.setParsed(tweet['tweet_id'], '-')
                
#                else:
#                    self.setParsed(tweet['tweet_id'], '-')
#                    raise Exception("Tweet was not recognised")
               
            except Exception, e:
                self.logWarning("Parsing tweet %s failed: %s" % (tweet['tweet_id'], e))
                #self.setParsed(tweet['tweet_id'], '-')
                continue  
                 
    '''
    Parser functions
    '''
    
    # parsePromise
    # parses and saves a new promise
    def parsePromise(self, tweet):

        expressions = self.types_map['promise']
        
        for expression in expressions:
            try:
                # Tweet flag default true
                tweet_errors = True
    
                # Strip out user accout
                h = re.search('(.*)(@%s)(.*)'% (ISSUER_ACCOUNT), tweet['content'], re.IGNORECASE)
                
                if h:
                    statement = h.group(1) + h.group(3)
                else:
                    raise Exception("Issuer not found")
                
                tweet['transferable'] = False
            
                # Check expiry (optional)
                ''' 'Expires in' syntax '''
                
                e = re.match('(.*) Expira en (\d+) (\w+)(.*)', statement, re.IGNORECASE|re.UNICODE)
                if e:
                    num = e.group(2)
                    unit = e.group(3)
                    tweet['expiry'] = self.getExpiry(tweet['created'], num, unit)
                    statement = e.group(1) + e.group(4)
                else:
                    tweet['expiry'] = None
                    
                
                # Get condition
                c = re.match('(.*)( if )(.*)', statement, re.IGNORECASE)
                
                if c:
                    tweet['condition'] = c.group(3)
                else:
                    tweet['condition'] = None
            
                # Get promise
                p = re.match('(.*)(%s)(.*)con(.*)' % expression, statement, re.IGNORECASE)
                
                if p:
                    print p.groups()
                    if p.group(1).strip().lower() == 'i':
                        promise = p.group(3)
                    else:
                        promise = p.group(1).strip() + p.group(3)
                else:
                    continue
                    

                # Get bearer
                r = re.search('@(\w+)(.*)', promise)
                
                if r:
                    tweet['recipient'] = tweet['author'] #The recipient for the debt is the author of the tweet 
                    tweet['author'] = r.group(1)
                    promise = r.group(2).strip()
                    self.saveUser(tweet['author'], intro=True)
                    
                else:
                    # (Don't tweet this as an error)
                    tweet_errors = False;
                    raise Exception("Recipient not found")
                 
                # Check not to self
                if tweet['recipient'] == tweet['author']:
                    raise Exception("Issuer and recipient are the same")
                    
                
                # Clean up promise 
                '''
                Remove trailing white space, full stop and word 'you' (if found)
                '''
                
                promise = promise.strip()
                
                while promise[-1] == '.':
                    promise = promise[:-1]
            
                if promise[0:4] == 'you ':
                    promise = promise[4:]
                tweet['promise'] = promise
            except Exception, e:
                raise e
          
            if promise:  
                # Processing promise
                try:
                    self.setParsed(tweet['tweet_id'])
                    self.createNote(tweet)
                    
                    self.sendWelcome(tweet['author'], tweet['recipient'],tweet['tweet_id'])
                    
                    E = Event(tweet['tweet_id'], tweet['tweet_id'], 10, tweet['created'], tweet['author'], tweet['recipient'])
                    E.save()
        
                    self.sendTweet('@%s %s @%s %s http://www.punkmoney.org/note/%s' % (expression ,tweet['author'], tweet['recipient'], tweet['promise'], tweet['tweet_id']))
                    self.logInfo('[P] @%s %s @%s %s.' % (expression, tweet['author'], tweet['recipient'], tweet['tweet_id']))
                    break
                except Exception, e:
                    self.logWarning("Processing promise %s failed: %s" % (tweet['tweet_id'], e))
                    if tweet_errors is not False:
                        self.sendTweet('@%s Sorry, your promise [%s] didn\'t parse. Try again: http://www.punkmoney.org/print/' % (tweet['author'], tweet['tweet_id']))
                    self.setParsed(tweet['tweet_id'], '-')
            else:
                raise Exception("Promise not found")
                        
            
    #parsePayment
    #parse and save payments
    def parsePayment(self,tweet):
        try:
            self.logInfo("Parsing tweet %s [payment]" % tweet['tweet_id'])
                            # Strip out user accout
            h = re.search('(.*)(@%s)(.*)'% (ISSUER_ACCOUNT), tweet['content'], re.IGNORECASE)
            
            if h:
                statement = h.group(1) + h.group(3)
            else:
                raise Exception("Issuer not found")
            
            r = re.search('@(\w+)(.*)', statement)
                
            if r:
                recipient = r.group(1)
            else:
                raise Exception("Recipient not found")
                 
            # Check not to self
            if recipient == tweet['author']:
                raise Exception("Issuer and recipient are the same")
            
            tags = tweet['tags']
            #TODO Check if the number of tejas payed match the tejas issued
            
            for tag in tags:
                query = "SELECT e.* \
                        FROM tracker_events e, tracker_tweets t \
                        WHERE (t.tag_1 = %(tag)d OR t.tag_2 = %(tag)d OR t.tag_3=%(tag)d ) \
                        AND t.tweet_id = e.tweet_id \
                        AND to_user='%(recipient)s' and from_user = '%(author)s'" % {'tag':tag,'recipient':recipient,'author':tweet['author']}
                for recipient_event in self.getRows(query):
                    note = self.getNote(recipient_event[2])
                    
                    if tweet['author'].lower() != note['issuer']:
                        raise Exception("Close attempt by non-issuer")
                        
                    if note['status'] != 10 and note['status']!=4:
                        raise Exception("Note already closed")
                    
                    if tweet['url'] is None or tweet['url']=='':
                        self.updateNote(note['id'], 'status', 4)
                        code = 4 #payment with error it is marked as offer
                    else:
                        self.updateNote(note['id'], 'status', 3)
                        code = 3 #payment correct it is a transfer
                        
                    # Create event
                    E = Event(note['id'], tweet['tweet_id'], code, tweet['created'], tweet['author'], recipient)
                    E.save()
                    
                    # Log event
                    self.logInfo("[X] '%s' closed note %s" % (tweet['author'], note['id']))
                    self.setParsed(tweet['tweet_id'])
        except Exception, e:
            self.logWarning("Processing payment %s failed: %s" % (tweet['tweet_id'], e))
            self.setParsed(tweet['tweet_id'], '-')
            
    # parseThanks
    # parse and save thanks
    def parseThanks(self, tweet):
        try:
            self.logInfo("Parsing tweet %s [thanks]" % tweet['tweet_id'])
            from_user = tweet['author']
            # If tweet has no reply to id
            if tweet['reply_to_id'] is None:

                h = re.search('(.*)(@%s)(.*)'% (ISSUER_ACCOUNT), tweet['content'], re.IGNORECASE)
                
                if h:
                    statement = h.group(1) + h.group(3)
                else:
                    raise Exception("Issuer not found")

                r = re.search('@(\w+)(.*)', statement)
                    
                if r:
                    tweet['recipient'] = r.group(1)
                else:
                    raise Exception("Recipient not found")
                
                self.createThanks(tweet)
                
                if tweet['message'] != '':
                    tweet['message'] = 'for ' + tweet['message']
                self.saveUser(tweet['recipient'], intro=True)
                
                # Log thanks
                message = '[Thanks] @%s thanked @%s %s' % (tweet['author'], tweet['recipient'], tweet['message'])
                self.logInfo(message)
                self.sendTweet('@%s thanked @%s %s http://www.punkmoney.org/note/%s' % (tweet['author'], tweet['recipient'], tweet['message'], tweet['tweet_id']))
                self.setParsed(tweet['tweet_id'])

            # If tweet has a reply_to_id, parse as redemption
            else:
                original_id = self.findOriginal(tweet['reply_to_id'], tweet['tweet_id'])
                note = self.getNote(original_id)
                
                to_user = note['issuer']
                
                # Check original exists
                if note is False:
                    raise Exception("Original note not found")
                
                # Check tweet author is current bearer
                if note['bearer'] != from_user:
                    raise Exception("User is not the current note bearer")
                    
                # Check note is open (i.e. not expired or redeemed)
                if note['status'] != 10:
                    if note['status'] == 1:
                        raise Exception("Note has already been redeemed")
                    if note['status'] == 2:
                        raise Exception("Note has expired")
                        
                message = note['promise']
                    
                # Process thanks
                self.updateNote(note['id'], 'status', 1)
                
                E = Event(note['id'], tweet['tweet_id'], 1, tweet['created'], from_user, to_user)
                E.save()
                
                # Log thanks
                self.logInfo('[T] @%s thanked @%s for %s' % (to_user, from_user, message))
                
                # Tweet event
                self.sendTweet('@%s thanked @%s for %s http://www.punkmoney.org/note/%s' % (from_user, to_user, note['promise'], note['id']))
                self.setParsed(tweet['tweet_id'])
                
        except Exception, e:
            self.logWarning("Processing thanks %s failed: %s" % (tweet['tweet_id'], e))
            self.setParsed(tweet['tweet_id'], '-')

    

    '''
    Helper functions
    '''
    # getTweets
    # Get unparsed tweets from database
    def getTweets(self):
        try:
            tweets = []
            for tweet in self.getRows("SELECT timestamp, tweet_id, author, content, reply_to_id,tag_1,tag_2,tag_3,url FROM tracker_tweets WHERE parsed is Null ORDER BY timestamp ASC"):
                tweet = {
                    'created' : tweet[0], 
                    'tweet_id' : tweet[1], 
                    'author' : tweet[2], 
                    'content' : tweet[3], 
                    'reply_to_id' : tweet[4],
                    'tags':[tweet[5],tweet[6],tweet[7]],
                    'url':tweet[8]
                }
                
                tags_ids = (",".join(str(v) for v in tweet['tags'] if v is not None))
                tags = []
                if tags_ids:
                    for tag in self.getRows("SELECT id,tag FROM tracker_tags WHERE id IN (%s)" % tags_ids):
                        if not re.match('(\d)T',tag[1],re.IGNORECASE|re.UNICODE):
                            tags.append(tag[0])
                    
                tweet['tags'] = tags
                tweets.append(tweet)
        except Exception, e:
            raise Exception("Getting tweets from database failed: %s" % e)
            return tweets
        else:
            return tweets
    
    # setParsed
    # Set parsed flag to 1 if successful, or '-' if not
    def setParsed(self, tweet_id, val=1):
        if SETTINGS.get('debug', False) == True:
            return False
        try:
            query = "UPDATE tracker_tweets SET parsed = %s WHERE tweet_id = %s"
            self.queryDB(query, (val, tweet_id))
        except Exception, e:
            raise Exception("Setting parsed flag for tweet %s failed: %s" % (tweet_id, e))
        else:
            return True
            
    # getExpiry
    # Takes created date time, a number and unit (day, week, month, year,) & returns expiry datetime
    def getExpiry(self, created, num, unit):
        try:
            num = int(num)
            if unit == 'minutes' or unit == 'minute' or unit == 'minutos':
                expiry = created + relativedelta(minutes=+num)
            if unit == 'hours' or unit == 'hour':
                expiry = created + relativedelta(hours=+num)
            if unit == 'days' or unit == 'day' or unit == 'dias' or unit == u'días':
                expiry = created + relativedelta(days=+num)
            if unit == 'weeks' or unit == 'week':
                expiry = created + relativedelta(days=+7*num)
            if unit == 'months' or unit == 'month':
                expiry = created + relativedelta(months=+num)
            if unit == 'years' or unit == 'year':
                expiry = created + relativedelta(years=+num)
        except Exception, e:
            raise Exception("Calculating expiry date failed: %s" % e)
        else:
            return expiry
    
    # findOriginal
    # Given a reply_to_id, finds the original 
    def findOriginal(self, reply_to_id, tweet_id):
        tweet = {}
        def getLast(reply_to_id):
            #query = "SELECT created, id, issuer, promise, type FROM tracker_notes WHERE id = %s" % reply_to_id
            query = "SELECT created, id, issuer, promise, type FROM tracker_notes WHERE id = (SELECT note_id FROM tracker_events WHERE tweet_id = %s)" % reply_to_id
            tweet = self.getRows(query)[0]
            return tweet
        try:
            note_types = [0, 4, 5, 10]
            
            while int(getLast(reply_to_id)[4]) not in note_types:
                reply_to_id = getLast(reply_to_id)[4]
            else:
                tweet = getLast(reply_to_id)
        except Exception, e:
            raise Exception("Original note for id %s not found" % tweet_id)
        else:
            return tweet[1]
    
    # createNote
    # Create a new note from a parsed tweet
    def createNote(self, tweet):
        try:
            query = "SELECT id FROM tracker_notes WHERE id = '%s'" % tweet['tweet_id']        
            if self.getSingleValue(query) is None:            
                query = "INSERT INTO tracker_notes(id, issuer, bearer, promise, created, expiry, status, transferable, type, conditional) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                params = (tweet['tweet_id'], tweet['author'].lower(), tweet['recipient'].lower(), tweet['promise'], tweet['created'], tweet['expiry'], 10, tweet['transferable'], 10, tweet['condition'])
                self.queryDB(query, params)
            else:
                self.logWarning('Note %s already exists' % tweet['tweet_id'])
                return False
        except Exception, e:
            raise Exception("Creating note from tweet %s failed: %s" % (tweet['tweet_id'], e))
        else:
            return True
            
            
    # createThanks
    # Create a thanks note
    def createThanks(self, tweet):
        try:
            query = "SELECT id FROM tracker_notes WHERE id = '%s'" % tweet['tweet_id']        
            if self.getSingleValue(query) is None:            
                query = "INSERT INTO tracker_notes(id, issuer, bearer, promise, created, expiry, status, transferable, type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                params = (tweet['tweet_id'], tweet['author'].lower(), tweet['recipient'].lower(), tweet['message'], tweet['created'], None, 0, 0, 1)
                self.queryDB(query, params)
                
                # Create an event
                E = Event(tweet['tweet_id'],1,1,tweet['created'],tweet['author'], tweet['recipient'])
                E.save()
            else:
                self.logWarning('Note %s already exists' % tweet['tweet_id'])
                return False
        except Exception, e:
            raise Exception("Creating thanks note from tweet %s failed: %s" % (tweet['tweet_id'], e))
        else:
            return True
    
    # getNote
    # Return a note given its id    
    def getNote(self, note_id):
        try:
            query = "SELECT id, issuer, bearer, promise, created, expiry, status, transferable, type FROM tracker_notes WHERE id = %s" % note_id
            note = self.getRows(query)[0]
            note = {'id' : note[0], 'issuer' : note[1], 'bearer' : note[2], 'promise' : note[3], 'created' : note[4], 'expiry' : note[5], 'status' : note[6], 'transferable' : note[7], 'type' : note[8]}
        except Exception, e:
            raise Exception("Original note %s not found" % (note_id, e))
            return False
        else:
            return note
    
    # updateNote
    # Update a note
    def updateNote(self, note_id, field, value):
        try:
            query = "UPDATE tracker_notes SET %s = %s where id = %s" % (field, '%s', '%s')
            params = (value, note_id)
            self.queryDB(query, params)
        except Exception, e:
            raise Exception("Updating note %s failed: %s" % (note_id, e))
        else:
            return True

    # saveUser
    # Check user exists
    def saveUser(self, username, intro = False):
        username = username.lower()
        try:
            query = "SELECT id FROM tracker_users WHERE username = '%s'" % username.lower()
            r = self.getSingleValue(query)
        except Exception, e:
            self.logError("Checking user exists failed: %s" % e)
            return False
        try:
            if r:
                return True
            else:
                self.logInfo("Saving new user %s" % username)
                api = self.connectTwitter()
                tuser = api.get_user(username.lower())
                icon_url = tuser.profile_image_url
                name = tuser.name
                about = tuser.description

                query = "INSERT INTO tracker_users (username,icon_url,name,about,last_login,date_joined) VALUES (%s,%s,%s,%s,NOW(),NOW())"
                params = (username.lower(),icon_url,name,about)
                self.queryDB(query, params)
                
                # Send intro tweet
                if intro == True:
                    try:
                        message = '@' + username + ' Hi there. Someone just sent you #PunkMoney. Here\'s how to get started: http://is.gd/bezeyu' 
                        self.sendTweet(message)
                    except:
                        pass
                
                # Follow user
                try:
                    if self.TW.exists_friendship('punk_money', username) is False:
                        self.TW.create_friendship(username)
                except:
                    pass
        except Exception, e:
            raise Exception("Creating new user failed: %s" % e)
        else:
            return True
        
    # updateExpired
    # Update status of any expired notes
    def updateExpired(self):
        try:
            self.logInfo("Checking for expirations")
            query = "SELECT id, bearer, issuer, type FROM tracker_notes WHERE expiry < now() AND status = 10"
            for note in self.getRows(query):
            
                self.logInfo('Note %s expired' % note[0])
                self.updateNote(note[0], 'status', 12)
                
                # promise
                if note[3] == 0:
                    code = 2
                # offer
                elif note[3] == 4:
                    code = 8
                # need
                elif note[3] == 5:
                    code = 9
                # request
                elif note[3] == 10:
                    code = 12
                
                # Create event
                E = Event(note[0], 0, code, datetime.now(), note[2], note[1])
                E.save()
                
        except Exception, e:
            raise Exception("Cleaning database failed: %s" % e)
            
    # sendTweet
    # Tweet a message from the main account
    def sendTweet(self, message):
        if SETTINGS.get('tweet', False) is True:
            try:
                self.TW.update_status(message)
            except:
                self.logError("Tweeting message failed (%s)" % message)      

    def sendWelcome(self,author,recipient,note):
        #self.sendTweet('@%s %s @%s %s http://www.punkmoney.org/note/%s' % (expression ,tweet['author'], tweet['recipient'], tweet['promise'], tweet['tweet_id']))
        #Buscar si el usuario es nuevo
        try:
            query = "SELECT count(*) from tracker_events where from_user = '%s'" % author
            print query
            u = self.getSingleValue(query)
            print u
            message = u"@%s Haz adquirido un compromiso con @%s por favor visita http://www.monedateja.net/ para gestionarlo." % (author, recipient, note)

            if u == 0:
                print message
                self.TW.update_status(message)
        except Exception, e:
            self.logError("Tweeting message failed (%s)" % e)
                            
    # checkTrusted
    # Check if there is a trust path between two users
    def checkTrusted(self,from_user, to_user):
        try:
            query = "SELECT COUNT(*) FROM tracker_events WHERE type = 1 AND from_user = '%s' AND to_user = '%s'" % (from_user, to_user)
            u = self.getSingleValue(query)
            print u
            if u > 0:
                return True
            else:
                return False
        except Exception, e:
            raise Exception('Checking TrustList for user %s failed: %s' % (username,e))