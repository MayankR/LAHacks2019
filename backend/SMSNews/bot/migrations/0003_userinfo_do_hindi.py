# Generated by Django 2.1.7 on 2019-03-31 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_userinfo_topic_idx'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='do_hindi',
            field=models.IntegerField(default=-1),
        ),
    ]
