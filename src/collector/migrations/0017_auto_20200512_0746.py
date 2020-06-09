# Generated by Django 2.2.4 on 2020-05-12 12:46

import django.contrib.postgres.fields.hstore
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parsers', '0016_template_desination'),
        ('collector', '0016_auto_20200505_0711'),
    ]

    operations = [
        migrations.AddField(
            model_name='sbemailparsing',
            name='is_published',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='sbemailparsing',
            name='meta',
            field=django.contrib.postgres.fields.hstore.HStoreField(null=True, verbose_name='Extracted data'),
        ),
        migrations.AddField(
            model_name='sbemailparsing',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='parsers.Template'),
        ),
        migrations.AddField(
            model_name='sbemailparsing',
            name='template_match_status',
            field=models.CharField(choices=[('NEW', 'New'), ('MULTIPLE_MATCH', 'Multiple template match found'), ('NOT_MATCH', 'No template match found'), ('MATCH_FOUND', 'Template matched')], default='NEW', max_length=15),
        ),
    ]