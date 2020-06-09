# Generated by Django 2.2.4 on 2020-04-15 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parsers', '0012_auto_20200415_0434'),
    ]

    operations = [
        migrations.AddField(
            model_name='parsingtask',
            name='var_name',
            field=models.CharField(max_length=36, null=True, verbose_name='variable name'),
        ),
        migrations.AlterField(
            model_name='parsingtask',
            name='desc',
            field=models.TextField(blank=True, editable=False),
        ),
    ]