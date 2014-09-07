# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'DateStats'
        db.delete_table(u'liberia_datestats')

        # Adding model 'WeekOfYear'
        db.create_table(u'liberia_weekofyear', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('week', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('new_cases', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('new_deaths', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal(u'liberia', ['WeekOfYear'])

        # Adding field 'SitRep.week_of_year'
        db.add_column(u'liberia_sitrep', 'week_of_year',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['liberia.WeekOfYear'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'DateStats'
        db.create_table(u'liberia_datestats', (
            ('contacts_completed_observation', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('original_date', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('contacts_lost_followup', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('news_contacts', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('total_deaths_probable', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('new_suspected_cases', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('today_deaths_probable', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('total_cases', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('total_probable_cases', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('new_cases', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('today_deaths_confirmed', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('new_probable_cases', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('total_confirmed_cases', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('total_deaths_confirmed', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('total_deaths_suspected', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('new_confirmed_cases', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('total_suspected_cases', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('today_deaths_all', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('total_deaths_all', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('today_deaths_suspected', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal(u'liberia', ['DateStats'])

        # Deleting model 'WeekOfYear'
        db.delete_table(u'liberia_weekofyear')

        # Deleting field 'SitRep.week_of_year'
        db.delete_column(u'liberia_sitrep', 'week_of_year_id')


    models = {
        u'liberia.author': {
            'Meta': {'object_name': 'Author'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'liberia.crisisnetentry': {
            'Meta': {'ordering': "['createdAt', 'is_geocoded', 'author', 'source']", 'object_name': 'CrisisNetEntry'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['liberia.Author']", 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'createdAt': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_geocoded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'lifespan': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'publishedAt': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'remoteID': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['liberia.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'updatedAt': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'})
        },
        u'liberia.location': {
            'Meta': {'ordering': "['name']", 'object_name': 'Location'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'liberia.locationsitrep': {
            'CFR': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'Meta': {'ordering': "['-date']", 'object_name': 'LocationSitRep'},
            'admission_cum': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'admission_new': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'cases_cum': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'cases_cum_confirmed': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'cases_cum_probable': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'cases_cum_suspected': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'cases_new_confirmed': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'cases_new_probable': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'cases_new_suspected': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'cases_new_total': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'date_span': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'deaths': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'formatted_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'hc_workers': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'hcw_cases_cum': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'hcw_cases_new': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'hcw_deaths_cum': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'hcw_deaths_new': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_treatment': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['liberia.Location']", 'null': 'True', 'blank': 'True'}),
            'new_deaths_confirmed': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'new_deaths_probable': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'new_deaths_suspected': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'sit_rep': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['liberia.SitRep']", 'null': 'True', 'blank': 'True'}),
            'total_deaths_all': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'total_deaths_confirmed': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'total_deaths_probable': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'total_deaths_suspected': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'total_discharges': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'liberia.sitrep': {
            'Meta': {'ordering': "['-date']", 'object_name': 'SitRep'},
            'date': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'date_span': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'day_of_year': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'formatted_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'week_of_year': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['liberia.WeekOfYear']", 'null': 'True', 'blank': 'True'})
        },
        u'liberia.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'liberia.weekofyear': {
            'Meta': {'ordering': "['-week', '-year']", 'object_name': 'WeekOfYear'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_cases': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'new_deaths': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'week': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['liberia']