# Generated by Django 2.2.9 on 2019-12-30 19:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_task_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='content',
        ),
    ]