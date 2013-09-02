# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'users.first_name'
        db.add_column(u'tracker_users', 'first_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=1, blank=True),
                      keep_default=False)

        # Adding field 'users.last_name'
        db.add_column(u'tracker_users', 'last_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=1, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'users.first_name'
        db.delete_column(u'tracker_users', 'first_name')

        # Deleting field 'users.last_name'
        db.delete_column(u'tracker_users', 'last_name')


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
            'about': ('django.db.models.fields.CharField', [], {'max_length': '600', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'icon_url': ('django.db.models.fields.CharField', [], {'max_length': '420', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'karma': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '90', 'blank': 'True'})
        }
    }

    complete_apps = ['tracker']