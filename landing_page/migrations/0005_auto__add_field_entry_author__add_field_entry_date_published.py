# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Entry.author'
        db.add_column('landing_page_entry', 'author', self.gf('django.db.models.fields.CharField')(default='unknown', max_length=255), keep_default=False)

        # Adding field 'Entry.date_published'
        db.add_column('landing_page_entry', 'date_published', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 4, 30, 1, 11, 58, 544933)), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Entry.author'
        db.delete_column('landing_page_entry', 'author')

        # Deleting field 'Entry.date_published'
        db.delete_column('landing_page_entry', 'date_published')


    models = {
        'landing_page.entry': {
            'Meta': {'object_name': 'Entry'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date_published': ('django.db.models.fields.DateTimeField', [], {}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['landing_page.Feed']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'landing_page.feed': {
            'Meta': {'object_name': 'Feed'},
            'date_parsed': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'etag': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['landing_page']
