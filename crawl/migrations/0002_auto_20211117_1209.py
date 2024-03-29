# Generated by Django 3.1.1 on 2021-11-17 11:09

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('crawl', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_text', models.TextField()),
                ('links_text', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='publisher',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 11, 17, 11, 9, 14, 497314, tzinfo=utc)),
            preserve_default=False,
        )
    ]
