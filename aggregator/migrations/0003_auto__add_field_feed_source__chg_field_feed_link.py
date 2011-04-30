# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding field 'Feed.source'
        db.add_column('aggregator_feed', 'source', self.gf('django.db.models.fields.URLField')(default=1, max_length=255), keep_default=False)

        # Changing field 'Feed.link'
        db.alter_column('aggregator_feed', 'link', self.gf('django.db.models.fields.URLField')(max_length=255, null=True))


    def backwards(self, orm):

        # Deleting field 'Feed.source'
        db.delete_column('aggregator_feed', 'source')

        # Changing field 'Feed.link'
        db.alter_column('aggregator_feed', 'link', self.gf('django.db.models.fields.URLField')(default=1, max_length=255))


    models = {
        'aggregator.feed': {
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

    complete_apps = ['aggregator']
