# Generated by Django 4.0.5 on 2022-06-22 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web01', '0006_alter_userinfo_gender_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='levl',
        ),
        migrations.AddField(
            model_name='task',
            name='level',
            field=models.SmallIntegerField(choices=[(3, '临时'), (1, '紧急'), (2, '重要')], default=1, verbose_name='级别'),
        ),
    ]
