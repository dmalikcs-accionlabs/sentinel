# Generated by Django 2.2.4 on 2020-04-06 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0002_auto_20200403_0524'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailcollection',
            name='email_to',
            field=models.CharField(default='defaut_to@xyz.com', max_length=256),
        ),
        migrations.AlterField(
            model_name='emailcollection',
            name='email_from',
            field=models.CharField(default='defaut_from@xyz.com', max_length=256),
        ),
    ]
