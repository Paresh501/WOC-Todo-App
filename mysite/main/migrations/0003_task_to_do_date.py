# Generated by Django 2.2.9 on 2019-12-29 18:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_task_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='to_do_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
