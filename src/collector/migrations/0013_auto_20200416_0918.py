# Generated by Django 2.2.4 on 2020-04-16 14:18

import django.contrib.postgres.fields.hstore
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0012_auto_20200416_0912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailcollection',
            name='meta',
            field=django.contrib.postgres.fields.hstore.HStoreField(default=dict, null=True, verbose_name='Extracted data'),
        ),
    ]