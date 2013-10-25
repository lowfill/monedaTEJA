from django.conf.urls.defaults import patterns, include, url

js_info_dict = {
    'packages': ('tracker','conf'),
}

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'tracker.views.home', name='home'),
    
    url(r'^tracker/$', 'tracker.views.tracker', name='tracker'),
    
    url(r'^t/(?P<tag_1>\w+)/$', 'tracker.views.tracker', name='tracker'),
    url(r'^t/(?P<tag_1>\w+)/(?P<tag_2>\w+)/$', 'tracker.views.tracker', name='tracker'),
    url(r'^t/(?P<tag_1>\w+)/(?P<tag_2>\w+)/(?P<tag_3>\w+)/$', 'tracker.views.tracker', name='tracker'),
    
    # ticker url patterns
    # max (optional) < user (optional) < type (optional) < note (optional)
    
    url(r'^ticker/$', 'tracker.views.ticker', name='ticker'),
    url(r'^ticker/max/(?P<max>\d+)/user/(?P<username>\w+)/type/(?P<type>\d+)/$', 'tracker.views.ticker', name='ticker'),
    url(r'^ticker/max/(?P<max>\d+)/type/(?P<type>\d+)/$', 'tracker.views.ticker', name='ticker'),
    url(r'^ticker/user/(?P<username>\w+)/type/(?P<type>\d_)/$', 'tracker.views.ticker', name='ticker'),
    url(r'^ticker/max/(?P<max>\d+)/user/(?P<username>\w+)/$', 'tracker.views.ticker', name='ticker'),
    url(r'^ticker/max/(?P<max>\d+)/$', 'tracker.views.ticker', name='ticker'),
    url(r'^ticker/user/(?P<username>\w+)/$', 'tracker.views.ticker', name='ticker'),
    url(r'^ticker/type/(?P<type>\d+)$', 'tracker.views.ticker', name='ticker'),
    url(r'^ticker/note/(?P<noteid>\d+)$', 'tracker.views.ticker', name='ticker'),
    
    # Tags only
    
    url(r'^ticker/tags/(?P<tag_1>\w+)/$', 'tracker.views.ticker', name='ticker'),
    url(r'^ticker/tags/(?P<tag_1>\w+)/(?P<tag_2>\w+)/$', 'tracker.views.ticker', name='ticker'),
    url(r'^ticker/tags/(?P<tag_1>\w+)/(?P<tag_2>\w+)/(?P<tag_3>\w+)/$', 'tracker.views.ticker', name='ticker'),
    
    # Type with tags
    
    url(r'^ticker/type/(?P<type>\d+)/tags/(?P<tag_1>\w+)/$', 'tracker.views.ticker', name='ticker'),
    url(r'^ticker/type/(?P<type>\d+)/tags/(?P<tag_1>\w+)/(?P<tag_2>\w+)/$', 'tracker.views.ticker', name='ticker'),
    url(r'^ticker/type/(?P<type>\d+)/tags/(?P<tag_1>\w+)/(?P<tag_2>\w+)/(?P<tag_3>\w+)/$', 'tracker.views.ticker', name='ticker'),

    # search
    url(r'^search/(?P<term>.*)$', 'tracker.views.search', name='search'),
    
    # Static pages
    # Press
    url(r'^about/$', 'tracker.views.about', name='about'),
    url(r'^faq/$', 'tracker.views.faq', name='faq'),
    url(r'^help/$', 'tracker.views.help', name='help'),

    # other patterns
    
    url(r'^network/$', 'tracker.views.shownet', name='network'),
    url(r'^print/$', 'tracker.views.printer', name='showlist'),
    url(r'^generate_debt/$', 'tracker.views.generate_debt', name='generateDebt'),
    url(r'^user/(?P<username>\w+)$', 'tracker.views.user', name='user'),
    url(r'^note/(?P<noteid>\w+)$', 'tracker.views.getnote', name='note'),
    
    # trust list
    url(r'^graph/$', 'tracker.views.trustnet', name='graph'),
    url(r'^user_info/(?P<username>\w+)$', 'tracker.views.user_info', name='user_info'),
    
    #django-social-auth
    url(r'^error/$', 'tracker.views.error', name='error'),
    url(r'^finish_login/$', 'tracker.views.finish_login', name='error'),
    url(r'^disconnect/$', 'tracker.views.disconnect', name='user'),
    url(r'', include('social_auth.urls')),
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
    #(r'^jsi18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog'),    
)
