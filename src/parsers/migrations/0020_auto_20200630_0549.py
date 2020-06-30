# Generated by Django 2.2.4 on 2020-06-30 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parsers', '0019_pdfparsingtask_pdftemplate'),
    ]

    operations = [
        migrations.AddField(
            model_name='parsingtask',
            name='get_multiple_values',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='template',
            name='event_split_string',
            field=models.CharField(blank=True, max_length=75),
        ),
        migrations.AddField(
            model_name='template',
            name='multiple_events',
            field=models.BooleanField(default=False),
        ),
    ]
