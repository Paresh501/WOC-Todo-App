# Generated by Django 2.2.9 on 2019-12-29 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_task_to_do_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='to_do_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
