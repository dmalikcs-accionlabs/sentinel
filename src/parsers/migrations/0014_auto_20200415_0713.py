# Generated by Django 2.2.4 on 2020-04-15 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parsers', '0013_auto_20200415_0444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parsingtask',
            name='template',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parsers', to='parsers.Template'),
        ),
    ]
