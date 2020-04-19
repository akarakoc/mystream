# Generated by Django 3.0.3 on 2020-04-13 15:53

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streampage', '0006_postcomments'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityStreams',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
    ]