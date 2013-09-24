# Twitter Configuration
TWITTER_CONSUMER_KEY              = ''
TWITTER_CONSUMER_SECRET           = ''
ISSUER_ACCOUNT                    = ''

TW_ACCESS_KEY = ''
TW_ACCESS_SECRET = ''

SOCIAL_AUTH_CREATE_USERS          = True
SOCIAL_AUTH_FORCE_RANDOM_USERNAME = False
SOCIAL_AUTH_DEFAULT_USERNAME      = 'socialauth_user'
SOCIAL_AUTH_COMPLETE_URL_NAME     = 'socialauth_complete'
#LOGIN_ERROR_URL                   = '/login/error/'

#SOCIAL_AUTH_USER_MODEL = 'tracker.Users'

LOGIN_URL          = '/login-form/'
LOGIN_REDIRECT_URL = '/finish_login/'
LOGIN_ERROR_URL    = '/error/'

SOCIAL_AUTH_FORCE_POST_DISCONNECT = True

#SOCIAL_AUTH_PIPELINE = (
#    'social_auth.backends.pipeline.social.social_auth_user',
#    'social_auth.backends.pipeline.associate.associate_by_email',
#    'social_auth.backends.pipeline.misc.save_status_to_session',
#    'social_auth.backends.pipeline.user.create_user',
#    'social_auth.backends.pipeline.social.associate_user',
#    'social_auth.backends.pipeline.social.load_extra_data',
#    'social_auth.backends.pipeline.user.update_user_details',
#)
