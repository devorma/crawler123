# Generated by Django 3.1.1 on 2021-11-17 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('crawl', '0009_delete_publisher'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('links', models.CharField(max_length=200)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('file_size', models.FloatField()),
                ('content_type', models.CharField(max_length=200)),
                ('last_modified', models.DateTimeField()),
                ('expiry_date', models.DateTimeField()),
                ('cache_control', models.CharField(max_length=200)),
                ('server', models.CharField(max_length=200)),
            ],
        ),
    ]
