# Generated by Django 3.1 on 2020-09-25 02:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base_note', '0009_auto_20200924_1656'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpost',
            name='marked_answer',
        ),
        migrations.RemoveField(
            model_name='userpost',
            name='user_comment',
        ),
        migrations.CreateModel(
            name='Usercomment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marked_answer', models.URLField()),
                ('user_comment', models.CharField(max_length=1024)),
                ('post_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base_note.post')),
                ('user_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddIndex(
            model_name='usercomment',
            index=models.Index(fields=['user_key', 'post_key'], name='base_note_u_user_ke_abc902_idx'),
        ),
    ]