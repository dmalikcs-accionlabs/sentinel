# Generated by Django 2.2.4 on 2020-05-05 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0014_auto_20200416_0921'),
    ]

    operations = [
        migrations.CreateModel(
            name='SBEmailParsing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('ClientId', models.IntegerField(verbose_name='ClientId')),
                ('UniqueIdentifier', models.CharField(max_length=128, verbose_name='UniqueIdentifier')),
                ('InboxUsername', models.CharField(max_length=128, verbose_name='InboxUsername')),
                ('Subject', models.CharField(blank=True, max_length=128, verbose_name='Subject')),
                ('BodyPlainText', models.TextField(blank=True, verbose_name='BodyPlainText')),
                ('BodyHtmlContent', models.TextField(blank=True, verbose_name='BodyHtmlContent')),
                ('FromAddress', models.EmailField(max_length=254, verbose_name='FromAddress')),
                ('ToAddresses', models.EmailField(max_length=254, verbose_name='ToAddresses')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]