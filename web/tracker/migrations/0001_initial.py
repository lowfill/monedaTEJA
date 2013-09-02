# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'events'
        db.create_table(u'tracker_events', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('note_id', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('tweet_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('type', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('from_user', self.gf('django.db.models.fields.CharField')(max_length=90)),
            ('to_user', self.gf('django.db.models.fields.CharField')(max_length=90)),
        ))
        db.send_create_signal(u'tracker', ['events'])

        # Adding model 'notes'
        db.create_table(u'tracker_notes', (
            ('id', self.gf('django.db.models.fields.BigIntegerField')(max_length=30, primary_key=True)),
            ('issuer', self.gf('django.db.models.fields.CharField')(max_length=90, blank=True)),
            ('bearer', self.gf('django.db.models.fields.CharField')(max_length=90, blank=True)),
            ('promise', self.gf('django.db.models.fields.CharField')(max_length=420, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('expiry', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('transferable', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('conditional', self.gf('django.db.models.fields.CharField')(max_length=420, null=True, blank=True)),
        ))
        db.send_create_signal(u'tracker', ['notes'])

        # Adding model 'trustlist'
        db.create_table(u'tracker_trust_list', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=90, blank=True)),
            ('trusted', self.gf('django.db.models.fields.CharField')(max_length=90, blank=True)),
        ))
        db.send_create_signal(u'tracker', ['trustlist'])

        # Adding model 'tags'
        db.create_table(u'tracker_tags', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'tracker', ['tags'])

        # Adding model 'tweets'
        db.create_table(u'tracker_tweets', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('tweet_id', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=90, blank=True)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=420, blank=True)),
            ('reply_to_id', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('parsed', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=420, null=True, blank=True)),
            ('display_url', self.gf('django.db.models.fields.CharField')(max_length=420, null=True, blank=True)),
            ('img_url', self.gf('django.db.models.fields.CharField')(max_length=420, null=True, blank=True)),
            ('tag_1', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('tag_2', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('tag_3', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'tracker', ['tweets'])

        # Adding model 'users'
        db.create_table(u'tracker_users', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=90, blank=True)),
            ('karma', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'tracker', ['users'])


    def backwards(self, orm):
        # Deleting model 'events'
        db.delete_table(u'tracker_events')

        # Deleting model 'notes'
        db.delete_table(u'tracker_notes')

        # Deleting model 'trustlist'
        db.delete_table(u'tracker_trust_list')

        # Deleting model 'tags'
        db.delete_table(u'tracker_tags')

        # Deleting model 'tweets'
        db.delete_table(u'tracker_tweets')

        # Deleting model 'users'
        db.delete_table(u'tracker_users')


    models = {
        u'tracker.events': {
            'Meta': {'object_name': 'events'},
            'from_user': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'to_user': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'tweet_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'tracker.notes': {
            'Meta': {'object_name': 'notes'},
            'bearer': ('django.db.models.fields.CharField', [], {'max_length': '90', 'blank': 'True'}),
            'conditional': ('django.db.models.fields.CharField', [], {'max_length': '420', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'expiry': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'max_length': '30', 'primary_key': 'True'}),
            'issuer': ('django.db.models.fields.CharField', [], {'max_length': '90', 'blank': 'True'}),
            'promise': ('django.db.models.fields.CharField', [], {'max_length': '420', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'transferable': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'tracker.tags': {
            'Meta': {'object_name': 'tags'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'tracker.trustlist': {
            'Meta': {'object_name': 'trustlist', 'db_table': "u'tracker_trust_list'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'trusted': ('django.db.models.fields.CharField', [], {'max_length': '90', 'blank': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '90', 'blank': 'True'})
        },
        u'tracker.tweets': {
            'Meta': {'object_name': 'tweets'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '90', 'blank': 'True'}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '420', 'blank': 'True'}),
            'display_url': ('django.db.models.fields.CharField', [], {'max_length': '420', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img_url': ('django.db.models.fields.CharField', [], {'max_length': '420', 'null': 'True', 'blank': 'True'}),
            'parsed': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'reply_to_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tag_1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tag_2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tag_3': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'tweet_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '420', 'null': 'True', 'blank': 'True'})
        },
        u'tracker.users': {
            'Meta': {'object_name': 'users'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'karma': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '90', 'blank': 'True'})
        }
    }

    complete_apps = ['tracker']