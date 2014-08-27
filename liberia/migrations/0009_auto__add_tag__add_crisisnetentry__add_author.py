# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'liberia_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal(u'liberia', ['Tag'])

        # Adding model 'CrisisNetEntry'
        db.create_table(u'liberia_crisisnetentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['liberia.Location'], null=True, blank=True)),
            ('publishedAt', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('lifespan', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('updatedAt', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('geo', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('createdAt', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
        ))
        db.send_create_signal(u'liberia', ['CrisisNetEntry'])

        # Adding M2M table for field tags on 'CrisisNetEntry'
        m2m_table_name = db.shorten_name(u'liberia_crisisnetentry_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('crisisnetentry', models.ForeignKey(orm[u'liberia.crisisnetentry'], null=False)),
            ('tag', models.ForeignKey(orm[u'liberia.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['crisisnetentry_id', 'tag_id'])

        # Adding model 'Author'
        db.create_table(u'liberia_author', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal(u'liberia', ['Author'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table(u'liberia_tag')

        # Deleting model 'CrisisNetEntry'
        db.delete_table(u'liberia_crisisnetentry')

        # Removing M2M table for field tags on 'CrisisNetEntry'
        db.delete_table(db.shorten_name(u'liberia_crisisnetentry_tags'))

        # Deleting model 'Author'
        db.delete_table(u'liberia_author')


    models = {
        u'liberia.author': {
            'Meta': {'object_name': 'Author'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'liberia.crisisnetentry': {
            'Meta': {'object_name': 'CrisisNetEntry'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['liberia.Location']", 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'createdAt': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'geo': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lifespan': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'publishedAt': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['liberia.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'updatedAt': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'})
        },
        u'liberia.datestats': {
            'Meta': {'ordering': "['date']", 'object_name': 'DateStats'},
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
        },
        u'liberia.location': {
            'Meta': {'ordering': "['name']", 'object_name': 'Location'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'liberia.locationsitrep': {
            'CFR': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'Meta': {'ordering': "['location']", 'object_name': 'LocationSitRep'},
            'cases_cum': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'cases_cum_confirmed': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'cases_cum_probable': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'cases_cum_suspected': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'date_span': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'deaths': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'hc_workers': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'hcw_cases_cum': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'hcw_deaths_cum': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['liberia.Location']", 'null': 'True', 'blank': 'True'}),
            'num': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'sit_rep': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['liberia.SitRep']", 'null': 'True', 'blank': 'True'}),
            'total_deaths_all': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'total_deaths_confirmed': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'total_deaths_suspected': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'total_probable_deaths': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'liberia.sitrep': {
            'Meta': {'ordering': "['num']", 'object_name': 'SitRep'},
            'date': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'date_span': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'liberia.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        }
    }

    complete_apps = ['liberia']