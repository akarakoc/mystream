# Generated by Django 3.0.3 on 2020-05-16 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streampage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcomments',
            name='commentText',
            field=models.CharField(help_text='Enter name of type', max_length=2000, null=True),
        ),
    ]
