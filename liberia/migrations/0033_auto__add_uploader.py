# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Uploader'
        db.create_table(u'liberia_uploader', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('docfile', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('sit_rep_date', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('month_format', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'liberia', ['Uploader'])


    def backwards(self, orm):
        # Deleting model 'Uploader'
        db.delete_table(u'liberia_uploader')


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
        u'liberia.document': {
            'Meta': {'object_name': 'Document'},
            'docfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month_format': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'sit_rep_date': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'liberia.location': {
            'Meta': {'ordering': "['name']", 'object_name': 'Location'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'weekly_cases': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'weekly_deaths': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'liberia.locationsitrep': {
            'CFR': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'Meta': {'ordering': "['-date']", 'object_name': 'LocationSitRep'},
            'admission_cum': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'admission_new': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'auto_new_deaths': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
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
            'is_copy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'week_of_year': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['liberia.WeekOfYear']", 'null': 'True', 'blank': 'True'})
        },
        u'liberia.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'liberia.uploader': {
            'Meta': {'object_name': 'Uploader'},
            'docfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month_format': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'sit_rep_date': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
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