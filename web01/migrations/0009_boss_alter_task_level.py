# Generated by Django 4.0.5 on 2022-06-25 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web01', '0008_alter_task_level_alter_userinfo_gender_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boss',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('age', models.IntegerField(verbose_name='年龄')),
                ('img', models.CharField(max_length=128, verbose_name='头像')),
            ],
        ),
        migrations.AlterField(
            model_name='task',
            name='level',
            field=models.SmallIntegerField(choices=[(3, '临时'), (1, '紧急'), (2, '重要')], default=1, verbose_name='级别'),
        ),
    ]
