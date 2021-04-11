# Generated by Django 3.1.7 on 2021-04-10 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20210407_2302'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='watchlist',
            options={'get_latest_by': 'watchList_id'},
        ),
        migrations.AddField(
            model_name='watchlist',
            name='watchList_name',
            field=models.CharField(default='', max_length=15),
        ),
    ]