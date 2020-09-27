# Generated by Django 3.1 on 2020-09-26 22:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base_note', '0013_auto_20200926_1821'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='bucket',
            name='base_note_b_bucket__a5bad2_idx',
        ),
        migrations.AddField(
            model_name='bucket',
            name='owner',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AddIndex(
            model_name='bucket',
            index=models.Index(fields=['bucket_name', 'owner'], name='base_note_b_bucket__c1bf72_idx'),
        ),
    ]