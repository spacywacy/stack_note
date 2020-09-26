# Generated by Django 3.1 on 2020-09-24 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_note', '0008_post_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpost',
            name='marked_answer',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userpost',
            name='user_comment',
            field=models.CharField(default='', max_length=1024),
            preserve_default=False,
        ),
    ]
