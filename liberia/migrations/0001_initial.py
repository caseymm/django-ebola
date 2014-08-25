# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DateStats'
        db.create_table(u'liberia_datestats', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_date', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('total_cases', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('total_suspected_cases', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('total_probable_cases', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('total_confirmed_cases', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('new_cases', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('new_suspected_cases', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('new_probable_cases', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('new_confirmed_cases', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('news_contacts', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('contacts_completed_observation', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('contacts_lost_followup', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('total_deaths_all', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('total_deaths_suspected', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('total_deaths_probable', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('total_deaths_confirmed', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('today_deaths_all', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('today_deaths_suspected', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('today_deaths_probable', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('today_deaths_confirmed', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal(u'liberia', ['DateStats'])


    def backwards(self, orm):
        # Deleting model 'DateStats'
        db.delete_table(u'liberia_datestats')


    models = {
        u'liberia.datestats': {
            'Meta': {'object_name': 'DateStats'},
            'contacts_completed_observation': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'contacts_lost_followup': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_cases': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'new_confirmed_cases': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'new_probable_cases': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'new_suspected_cases': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'news_contacts': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'original_date': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'today_deaths_all': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'today_deaths_confirmed': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'today_deaths_probable': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'today_deaths_suspected': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'total_cases': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'total_confirmed_cases': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'total_deaths_all': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'total_deaths_confirmed': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'total_deaths_probable': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'total_deaths_suspected': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'total_probable_cases': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'total_suspected_cases': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['liberia']