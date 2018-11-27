# Generated by Django 2.1.2 on 2018-10-31 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddpush_android', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='deviceModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dev_andId', models.CharField(max_length=128)),
                ('dev_imei', models.CharField(max_length=12)),
                ('dev_isRt', models.CharField(max_length=10)),
                ('dev_name', models.CharField(max_length=25)),
                ('dev_sdk', models.CharField(max_length=10)),
                ('app_ver', models.CharField(max_length=10)),
                ('dev_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='taskModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dev_andId', models.CharField(max_length=128)),
                ('task_id', models.CharField(max_length=10)),
                ('task_type', models.CharField(max_length=10)),
                ('task_state', models.CharField(max_length=10)),
                ('task_crt_date', models.DateField()),
                ('task_fish_date', models.DateField()),
            ],
        ),
    ]
