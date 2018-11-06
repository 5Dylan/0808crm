# Generated by Django 2.1 on 2018-10-23 20:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(db_column='user_name', max_length=20)),
                ('password', models.CharField(max_length=100)),
                ('truename', models.CharField(db_column='true_name', max_length=20, null=True)),
                ('email', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=20, null=True)),
                ('is_valid', models.IntegerField(default=1, max_length=4)),
                ('create_date', models.DateTimeField(default=datetime.datetime(2018, 10, 23, 20, 37, 0, 237163))),
                ('update_date', models.DateTimeField(null=True)),
                ('code', models.CharField(max_length=255, null=True)),
                ('status', models.BooleanField(default=0, max_length=1)),
                ('timestamp', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 't_user',
            },
        ),
    ]