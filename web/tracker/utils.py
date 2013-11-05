# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.utils import simplejson
from django.db.models import Q

from social_auth.models import UserSocialAuth

import operator

from tracker.models import *
from local_settings import TWITTER_CONSUMER_KEY,TWITTER_CONSUMER_SECRET,ISSUER_ACCOUNT,TW_ACCESS_KEY, TW_ACCESS_SECRET
import tweepy


'''
API Methods
'''

# Return trustnet as JSON
def trustnet_old(request):

    all_nodes = trustlist.objects.all()
    
    nodes = []
    checked = []
    for n in all_nodes:
        if n.user not in checked:
            nodes.append({"name":n.user, "group":1})
            checked.append(n.user)
        if n.trusted not in checked:
            nodes.append({"name":n.trusted, "group":1})
            checked.append(n.trusted)


    links = []
    for n in all_nodes:
        
        source = checked.index(n.user)
        target = checked.index(n.trusted)
    
        links.append({"source" : source, "target" : target, "value" : 1})
        
    graph = {"nodes" : nodes, "links" : links}
    
    data = simplejson.dumps(graph)
    
    return HttpResponse(data, mimetype='application/javascript')
    
# Return trustnet as JSON
def trustnet(request):

    all_nodes = events.objects.filter(Q(type=1)).order_by('-timestamp')
    
    # Minimum karma for graph inclusion
    
    nodes = []
    checked = []
    min_karma = 10
    
    for n in all_nodes:
    
        if n.from_user not in checked:
        
            karma = getKarma(n.from_user)

            nodes.append({"name":n.from_user, "group":int(round(karma/10,0)), "karma":karma})
            checked.append(n.from_user)
            
        if n.to_user not in checked:
        
            karma = getKarma(n.to_user)
            
            nodes.append({"name":n.to_user, "group":int(round(karma/10,0)), "karma":karma})
            checked.append(n.to_user)


    links = []
    for n in all_nodes:
        
        source = checked.index(n.from_user)
        target = checked.index(n.to_user)

        links.append({"source" : source, "target" : target, "value" : 1})
    
    
        
    graph = {"nodes" : nodes, "links" : links}
    
    data = simplejson.dumps(graph)

    return HttpResponse(data, mimetype='application/javascript')


    
''' HELPERS '''

# getKarma
# fethes and returns a user's karma, based on in-bound thanks statements

def getKarma(username):

    # Disabled for now

    '''
    try:
        user = users.objects.get(username=username)
        
        if user.karma is None:
            return 1
        else:
            return int(user.karma)
    except:
        return 1
    '''
    
    return 50


# relatedTags
# gets frequently associated tags to the supplied tags list

def relatedTags(base_tags = None):

    all_tweets = []
    # If no tag is specified, return most popular tags
    if base_tags is None or base_tags == []:
        all_tweets = tweets.objects.filter(parsed = 1)
    else:
        raw_tweets = []
        for tag_id in base_tags:
            raw_tweets += tweets.objects.filter(
                Q(tag_1 = tag_id)|Q(tag_2 = tag_id)|Q(tag_3 = tag_id)
            )

        # Filter out tweets where tags don't co-occur
        for tweet in raw_tweets:
        
            tweet_tags = [tweet.tag_1, tweet.tag_2, tweet.tag_3]
            tweet_tags = [int(tag) for tag in tweet_tags if tag is not None]
            
            insert = True
            for tag in base_tags:
                if tag not in tweet_tags:
                    insert = False
                    break

            if insert == True:
                all_tweets.append(tweet)

    # Get and rank all tags
    all_tags = {}
    for tweet in all_tweets:
    
        tweet_tags = [tweet.tag_1, tweet.tag_2, tweet.tag_3]
        tweet_tags = [int(tag) for tag in tweet_tags if tag is not None]
        
        for tag in tweet_tags:
        
            if all_tags.has_key(tag) is False:
                all_tags[tag] = 1
            else:
                all_tags[tag] = all_tags[tag] + 1

    
    # Get names for all tags
    tags_final = {}
    
    for tag_id, count in all_tags.items():
        try:
            if base_tags is not None:
                if tag_id not in base_tags:         
                    t = tags.objects.get(id = tag_id)
                    tag = str(t.tag)
                    tags_final[tag] = count
            else:
                t = tags.objects.get(id = tag_id)
                tag = str(t.tag)
                tags_final[tag] = count
        except Exception, e:
            print e
            
    # Sort dict by count, limit to first 20
    
    tags_final = sorted(tags_final.iteritems(), key=operator.itemgetter(1))
    tags_final.reverse()

    
    # Return tags    
    return tags_final
    
def connectTwitter():
        try:
            auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
            auth.set_access_token(TW_ACCESS_KEY, TW_ACCESS_SECRET)
            api = tweepy.API(auth)
        except Exception, e:
            raise Exception("Error connecting to Twitter API: %s" % e)
        else:
            return api
    

def generate_debt_from_file(user,fileObject):
    try:
        api = connectTwitter(user)
        print api
        csv = DebtModel.import_from_file(file=fileObject)
        for debt in csv:
            event = debt.event.replace(' ','').lower()
            name = debt.name.replace('@','')
            tweet = "@%s se enredó con #%dT por #%s. Expira en %d días. @%s " % (name , debt.ammount, event , debt.expiration,ISSUER_ACCOUNT)
            api.update_status(status=tweet)
            
    except Exception, e:
        print e
        #raise Exception("Error connecting to Twitter API: %s" % e)
        return False
        
def saveUser(username):
    username = username.lower()
    try:
        user = users.objects.get(username=username)
    except:
        user = users.objects.create_user_by_username(username=username)
    
    if user.icon_url == "":    
        api = connectTwitter()
        tuser = api.get_user(username)
        user.icon_url = tuser.profile_image_url
        user.name = tuser.name
        user.about = tuser.description
        user.save()

    return user