from django.db import models
from adaptor.model import CsvModel
from adaptor.fields import CharField, IntegerField

class events(models.Model):
    id = models.AutoField(primary_key=True)
    note_id = models.BigIntegerField(null=True, blank=True)
    tweet_id = models.BigIntegerField()
    type = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField()
    from_user = models.CharField(max_length=90)
    to_user = models.CharField(max_length=90)
    class Meta:
        db_table = u'tracker_events'

class notes(models.Model):
    id = models.BigIntegerField(max_length=30, primary_key=True)
    issuer = models.CharField(max_length=90, blank=True)
    bearer = models.CharField(max_length=90, blank=True)
    promise = models.CharField(max_length=420, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    expiry = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
    transferable = models.IntegerField(null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    conditional = models.CharField(max_length=420, null=True, blank=True)
    class Meta:
        db_table = u'tracker_notes'

class trustlist(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=90, blank=True)
    trusted = models.CharField(max_length=90, blank=True)
    class Meta:
        db_table = u'tracker_trust_list'
        
class tags(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=30)
    class Meta:
        db_table = u'tracker_tags'
        
class tweets(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    tweet_id = models.BigIntegerField(null=True, blank=True)
    author = models.CharField(max_length=90, blank=True)
    content = models.CharField(max_length=420, blank=True)
    reply_to_id = models.BigIntegerField(null=True, blank=True)
    parsed = models.CharField(max_length=1, null=True, blank=True)
    url = models.CharField(max_length=420, null=True, blank=True)
    display_url = models.CharField(max_length=420, null=True, blank=True)
    img_url = models.CharField(max_length=420, null=True, blank=True)
    tag_1 = models.IntegerField(null=True, blank=True)
    tag_2 = models.IntegerField(null=True, blank=True)
    tag_3 = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'tracker_tweets'

class users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=90, blank=True)
    karma = models.IntegerField(null=True, blank=True)
    lastlogin = models.DateTimeField()
    is_active = models.BooleanField()
    class Meta:
        db_table = u'tracker_users'
        
class DebtModel(CsvModel):
    name = CharField()
    ammount = IntegerField(null=True,default=1)
    event = CharField()
    expiration = IntegerField(null=True,default=30)
    class Meta:
        delimiter = ","
        silent_failure = False