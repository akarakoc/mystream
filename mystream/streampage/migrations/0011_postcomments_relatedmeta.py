# Generated by Django 3.0.3 on 2020-04-13 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('streampage', '0010_auto_20200413_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcomments',
            name='relatedMeta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='streampage.PostsMetaHash'),
        ),
    ]