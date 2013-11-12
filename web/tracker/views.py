from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.messages.api import get_messages
from django.db.models import Q
from django.utils.translation import ugettext as _
from django.utils import simplejson


from tracker.models import *
from tracker.utils import *
from operator import itemgetter
from itertools import chain
#import re
import operator

from social_auth.models import UserSocialAuth
from social_auth import __version__ as version
from local_settings import ISSUER_ACCOUNT

# Create your views here.

def error(request):
    """Error view"""
    messages = get_messages(request)
    return render_to_response('error.html', {'version': version,
                                             'messages': messages},
                              RequestContext(request))

def disconnect(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/tracker')

def finish_login(request):
    if request.user:
        saveUser(request.user.username)
        
    return HttpResponseRedirect('/tracker')

def home(request):
    return HttpResponseRedirect('/tracker')

def dashboard(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/user/'+request.user.username)
    else:
        return HttpResponseRedirect('/tracker')
    
def user_suggest(request, username):
    term = request.GET['term']
    suggested = users.objects.filter(username__startswith=term)
    resp = []
    if len(suggested) > 0:
        for user in suggested:
            resp.append(user.username)
    
    return HttpResponse(simplejson.dumps(resp),mimetype='text/json')

def event_suggest(request):
    term = request.GET['term']
    suggested = tags.objects.filter(tag__startswith=term)
    resp = []
    if len(suggested) > 0:
        for tag in suggested:
            resp.append(tag.tag)
    
    return HttpResponse(simplejson.dumps(resp),mimetype='text/json')

def verify(request,event):
    resp = verify_payment(request.user,event)        
    print resp    
    return HttpResponse(simplejson.dumps(resp),mimetype='text/json')

def tracker(request, tag_1 = None, tag_2 = None, tag_3 = None):

    # convert tags to ids and get related tags
    
    tag_ids = []
    tag_slug = ''
    for tag in [tag_1, tag_2, tag_3]:
        if tag is not None:
            t = tags.objects.get(tag = tag)
            tag_id = int(t.id)
            tag_ids.append(tag_id)  
        
            tag_slug += tag + '/'

    variables = {
        'page':'ticker',
        'tag_1':tag_1,
        'tag_2':tag_2,
        'tag_3':tag_3,
        'tag_slug' : tag_slug,
    }

    # Related tags
    related_tags = relatedTags(tag_ids)
    
    if related_tags is not None:
        variables['related_tags'] = related_tags
    
    

    return render_to_response('tracker.html', variables,RequestContext(request))


def ticker(
        request, 
        max=50, 
        type=None, 
        username=None, 
        noteid=None, 
        tag_1=None, 
        tag_2=None, 
        tag_3=None,
    ):

    # limit max to 200
    max = int(max)
    if max > 200:
        max = 200
        
    # Convert tags to ids
    filters = []
    
    if tag_1 is not None:
        tag_1 = tags.objects.get(tag = tag_1)
        filters.append(int(tag_1.id))

    if tag_2 is not None:
        tag_2 = tags.objects.get(tag = tag_2)
        filters.append(int(tag_2.id))
        
    if tag_3 is not None:
        tag_3 = tags.objects.get(tag = tag_3)
        filters.append(int(tag_3.id))
    
    
    
    new_events = []

    # Filter by tags
    if len(filters) > 0:
    
        if type is not None:
            raw_events = events.objects.filter(
                Q(type=type)
            ).order_by('-timestamp')[:max]
        else:
            raw_events = events.objects.all().order_by('-timestamp')[:max]
    
        
        for event in raw_events:
            note_id = event.note_id
            note = notes.objects.get(note_id)
                         
            try:
                tweet = tweets.objects.get(tweet_id = note_id)
                tweet_tags = [tweet.tag_1, tweet.tag_2, tweet.tag_3]
                tweet_tags = [int(tag) for tag in tweet_tags if tag is not None]

                if len(filters) == 1:
                    if filters[0] in tweet_tags:
                        new_events.append(event)

                if len(filters) == 2:
                
                    if filters[0] in tweet_tags and filters[1] in tweet_tags:
                        new_events.append(event)
                        
                if len(filters) == 3:
                    if filters[0] in tweet_tags and filters[1] in tweet_tags and filters[2] in tweet_tags:
                        new_events.append(event)
            except:
                pass

    # filter by type and/or username if given
    elif type is not None and username is not None:
        if type == '10':
            new_events = events.objects.filter(
                Q(type=type),
                Q(from_user=username) 
                ).order_by('-timestamp')[:max]
        elif type == '3':
            #new_events = events.objects.filter(
            #    Q(type=type),
            #    Q(to_user=username) 
            #    ).order_by('-timestamp')[:max]
            #TODO Add relationship to tables to avoid this raw query
            query = "SELECT e.*,n.status FROM tracker_events e JOIN tracker_notes n ON e.note_id=n.id AND n.status!=1 WHERE to_user=%s AND e.type=%s"
            query+=" ORDER BY timestamp"
            new_events = events.objects.raw(query,[username,type])[:max]
        else:
            new_events = events.objects.filter(
                Q(type=type),
                Q(to_user=username) | Q(from_user=username)
                ).order_by('-timestamp')[:max]    
               
    elif type is not None and username is None:
        new_events = events.objects.filter(
            Q(type=type)
            ).order_by('-timestamp')[:max]
    elif type is None and username is not None:
        new_events = events.objects.filter(
            Q(from_user=username) | Q(to_user=username)
            ).order_by('-timestamp')[:max]
    elif noteid is not None:
        new_events = events.objects.filter(
            Q(note_id=noteid)
            ).order_by('-timestamp')[:max]
    else:
        new_events = events.objects.all().order_by('-timestamp')[:max]

        
    # get new notes
    new_notes = notes.objects.all()    
    result_list = []
    
    for event in new_events:
        note = notes.objects.filter(id=event.note_id)[0]
        
        if int(note.status) != 0 and type is not None:
            #if int(type) == 4 or int(type) == 5:
            if int(type) == 5:
                continue
        
        # Turn tags into hyperlinks in promise
        note_id = event.note_id
        tweet = tweets.objects.get(tweet_id = note_id)
        tag_ids = [tweet.tag_1, tweet.tag_2, tweet.tag_3]
        tag_ids = [int(tag) for tag in tag_ids if tag is not None]
        
        tags_final = []
        for tag_id in tag_ids:
            try:
                t = tags.objects.get(id = tag_id)
                if t is not None:
                    tag = str(t.tag)
                    tags_final.append(tag)
            except:
                pass
            
        if event.note_id == note.id:
            
            result_list.append({
                'promise':note.promise,
                'timestamp':event.timestamp,
                'from_user':event.from_user,
                'to_user':event.to_user,
                'type':event.type,
                'note_id':event.note_id,
                'tweet_id':event.tweet_id,
                'tags':tags_final,
            })
    
    final = sorted(result_list, key=itemgetter('timestamp'), reverse=True)
    
    show_arrow = True
    
    variables = {
        'events':final,
        'show_arrow':show_arrow,
        'username':username,
        'user':request.user
    }

    return render_to_response('ticker.html', variables)    
    
def shownet(request):

    trust_list = trustlist.objects.all()
    
    variables = {
        'trustlist':trust_list,
        'page':'trustlist',
    }
    
    return render_to_response('trustnet.html', variables,RequestContext(request))   
    
def about(request):
    
    return render_to_response('about.html', {'page':'about'},RequestContext(request))  
    
def faq(request):
    
    return render_to_response('faq.html', {},RequestContext(request))    

def user(request, username):
    

    requests=events.objects.filter(to_user=username,type=10).count()
    received=events.objects.filter(to_user=username,type=3).count()
    verified=events.objects.filter(from_user=username,type=1).count()
    withproblems=events.objects.filter(to_user=username,type=4).count()
    expired = events.objects.filter(to_user=username,type=12).count()

    requests_received=events.objects.filter(from_user=username,type=10).count()
    sent=events.objects.filter(from_user=username,type=3).count()
    validated =events.objects.filter(to_user=username,type=1).count()
    sentwithproblems=events.objects.filter(from_user=username,type=4).count()
    expired_to = events.objects.filter(from_user=username,type=12).count()

    balance = (requests - verified) - (requests_received - validated) - expired + expired_to         

    notes_bearer = notes.objects.filter(bearer=username).filter(status=0)
    notes_issuer = notes.objects.filter(issuer=username).filter(status=0)
    events_from = events.objects.filter(from_user=username)[:10]
    events_to = events.objects.filter(to_user=username)[:10]
 
    events_all = chain(events_from,events_to)
    
    result_list = []
    
    for event in events_all:
        note = notes.objects.filter(id=event.note_id)[0]
        if event.note_id == note.id:
        
            result_list.append({
                'promise':note.promise,
                'timestamp':event.timestamp,
                'from_user':event.from_user,
                'to_user':event.to_user,
                'type':event.type,
                'note_id':event.note_id,
                'tweet_id':event.tweet_id,
            })
    
    final = sorted(result_list, key=itemgetter('timestamp'), reverse=True)
    
    # Find number of people who trust this user
    trusters = trustlist.objects.filter(trusted=username)    
    trust_num = len(trusters)

    # Add trusters to list
    trusters_list = []
    for truster in trusters:
        trusters_list.append(truster.user)

    # Arbitrary, for now
    top_trusters = trusters_list[:1]

    # generate slug
    slug = username
    
    # karma
    karma = getKarma(username)

    user = saveUser(username=username) 
        
    # combine events
    variables = {
        'username':username,
        'notes_held':notes_bearer,
        'notes_issued':notes_issuer,
        'events':final,
        'trust':trust_num,
        'trusters':trusters_list,
        'top_trusters':top_trusters,
        'karma':karma,
        'user_icon':user.icon_url,
        'about':user.about,
        'requests':requests,
        'received':received,
        'verified':verified,
        'withproblems':withproblems,
        'expired':expired,
        'requests_received':requests_received,
        'sent':sent,
        'validated':validated,
        'sentwithproblems':sentwithproblems,
        'expired_to':expired_to,
        'balance':balance,         

    }
    
    # return all
    return render_to_response('user.html', variables,RequestContext(request))
    

def getnote(request, noteid):

    note = notes.objects.get(id=noteid)
    new_events = events.objects.filter(note_id=noteid).order_by('timestamp')
    new_events = new_events.reverse()
    
    tweet = tweets.objects.get(tweet_id=noteid)
    
    id = str(note.id)
    
    promise = note.promise
    
    # Replace pronouns with opposites
    variables = {}
    
    if note.type == 5 or note.type == 10:
        reply_promise = promise.replace(' my ', ' your ')
        reply_promise = reply_promise.replace(' me ', ' you ')
        reply_promise = reply_promise.replace(' i ', ' you ')
        variables['reply_promise'] = reply_promise
    
    raw_tags = [tweet.tag_1, tweet.tag_2, tweet.tag_3]
    tags_final = []
    for tag_id in raw_tags:
        if tag_id != None:
            t = tags.objects.get(id = tag_id)
            tags_final.append(t.tag)
    
    variables = {
        'events' : new_events,
        'note' : note,
        'content' : tweet.content,
        'url' : tweet.url,
        'display_url' : tweet.display_url,
        'id' : id,
        'img_url' : tweet.img_url,
        'tags' : tags_final,
    }
    
    if note.type == 0:
        template = 'note.html'
    elif note.type == 4:
        template = 'offer.html'
    elif note.type == 5:
        template = 'need.html'
    elif note.type == 1:
        template = 'thanks.html'
    elif note.type == 10:
        template = 'request.html'
    
    return render_to_response(template, variables,RequestContext(request))
    
    
def printer(request):
    variables = {
        'page':'printer',
        'issuer':ISSUER_ACCOUNT
    }
    return render_to_response('printer.html', variables,RequestContext(request))

def pay(request,target=None):
    variables = {
        'page':'pay',
        'issuer':ISSUER_ACCOUNT,
        'target':target
    }
        
    return render_to_response('pay_printer.html', variables,RequestContext(request))
    
def generate_debt(request):
    error = ''
    if request.method == 'POST':
        if request.FILES.has_key('recipients'):
            file = request.FILES['recipients'] 
            if file.content_type == 'text/csv':
                generate_debt_from_file(request.user,file)
            else:
                error = _("The attached file doesn't have the right format. Please review it and try again.")
        else:
                error = _('Please attach a file.')    
        
    variables = {
        'page':'printer',
        'issuer':ISSUER_ACCOUNT,
        'error' : error
    }
    
    return render_to_response('printer.html', variables,RequestContext(request))

def help(request):
    variables = {
        'page':'help',
    }
    return render_to_response('help.html', variables,RequestContext(request))

# [!] Check if for non-note ids too
def search(request, term=None):

    # Attempt to resolve to username first
    try:
        user = users.objects.get(username=term)
        url = '/user/' + term
    except:
        # Otherwise, resolve to tags
        tags = term.split(' ')
        
        url = '/t/'
        
        for tag in tags:
            url += tag + '/'
        
    return HttpResponse(url)


# Returns user_info for trustnet sidebar   
def user_info(request, username):

    # Find number of people who trust this user
    trusted_by = trustlist.objects.filter(trusted=username)    
    trusted_num = len(trusted_by)

    # Add trusters to list
    trusted_list = []
    for t in trusted_by:
        trusted_list.append(t.user)

    # Find number of people who this user trusts
    trusts = trustlist.objects.filter(user=username)    
    trusts_num = len(trusts)
    
    # Add people user trusts to list
    trusts_list = []
    for t in trusts:
        trusts_list.append(t.trusted)
    
    karma = getKarma(username)
    
    user = saveUser(username);
    
    # Return variables
    variables = {
        'karma':karma,
        'username':username,
        'user_icon':user.icon_url
    }
    
    return render_to_response('user_info.html', variables,RequestContext(request))
    
