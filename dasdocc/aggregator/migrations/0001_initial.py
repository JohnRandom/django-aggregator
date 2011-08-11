# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'SourceCategory'
        db.create_table('aggregator_sourcecategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('aggregator', ['SourceCategory'])

        # Adding model 'Feed'
        db.create_table('aggregator_feed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('etag', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('date_parsed', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('valid', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('trashed_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('content_expiration', self.gf('django.db.models.fields.SmallIntegerField')(default=7)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aggregator.SourceCategory'], null=True, blank=True)),
        ))
        db.send_create_signal('aggregator', ['Feed'])

        # Adding model 'ParsingError'
        db.create_table('aggregator_parsingerror', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aggregator.Feed'])),
            ('error_message', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_raised', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('aggregator', ['ParsingError'])

        # Adding model 'Entry'
        db.create_table('aggregator_entry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_published', self.gf('django.db.models.fields.DateTimeField')()),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aggregator.Feed'])),
        ))
        db.send_create_signal('aggregator', ['Entry'])

        # Adding model 'StaticContent'
        db.create_table('aggregator_staticcontent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('source', self.gf('django.db.models.fields.URLField')(max_length=255)),
            ('date_parsed', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aggregator.SourceCategory'], null=True, blank=True)),
        ))
        db.send_create_signal('aggregator', ['StaticContent'])

        # Adding model 'Selector'
        db.create_table('aggregator_selector', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aggregator.StaticContent'])),
            ('css_selector', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('bound_content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('aggregator', ['Selector'])

        # Adding model 'StaticContentError'
        db.create_table('aggregator_staticcontenterror', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aggregator.StaticContent'])),
            ('error', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_raised', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('aggregator', ['StaticContentError'])


    def backwards(self, orm):
        
        # Deleting model 'SourceCategory'
        db.delete_table('aggregator_sourcecategory')

        # Deleting model 'Feed'
        db.delete_table('aggregator_feed')

        # Deleting model 'ParsingError'
        db.delete_table('aggregator_parsingerror')

        # Deleting model 'Entry'
        db.delete_table('aggregator_entry')

        # Deleting model 'StaticContent'
        db.delete_table('aggregator_staticcontent')

        # Deleting model 'Selector'
        db.delete_table('aggregator_selector')

        # Deleting model 'StaticContentError'
        db.delete_table('aggregator_staticcontenterror')


    models = {
        'aggregator.entry': {
            'Meta': {'ordering': "('-date_published',)", 'object_name': 'Entry'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date_published': ('django.db.models.fields.DateTimeField', [], {}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aggregator.Feed']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'aggregator.feed': {
            'Meta': {'object_name': 'Feed'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aggregator.SourceCategory']", 'null': 'True', 'blank': 'True'}),
            'content_expiration': ('django.db.models.fields.SmallIntegerField', [], {'default': '7'}),
            'date_parsed': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'etag': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'trashed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'aggregator.parsingerror': {
            'Meta': {'ordering': "('-date_raised',)", 'object_name': 'ParsingError'},
            'date_raised': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'error_message': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aggregator.Feed']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'aggregator.selector': {
            'Meta': {'object_name': 'Selector'},
            'bound_content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'css_selector': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aggregator.StaticContent']"})
        },
        'aggregator.sourcecategory': {
            'Meta': {'object_name': 'SourceCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'aggregator.staticcontent': {
            'Meta': {'object_name': 'StaticContent'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aggregator.SourceCategory']", 'null': 'True', 'blank': 'True'}),
            'date_parsed': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'source': ('django.db.models.fields.URLField', [], {'max_length': '255'})
        },
        'aggregator.staticcontenterror': {
            'Meta': {'ordering': "('-date_raised',)", 'object_name': 'StaticContentError'},
            'date_raised': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'error': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aggregator.StaticContent']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        }
    }

    complete_apps = ['aggregator']
