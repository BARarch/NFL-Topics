# Generated by Django 2.0.1 on 2018-06-14 20:57

from django.db import migrations, models
import oauth2client.contrib.django_util.models


class Migration(migrations.Migration):

    dependencies = [
        ('parsebot', '0002_auto_20180607_1519'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlowModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flow', oauth2client.contrib.django_util.models.FlowField(null=True)),
            ],
        ),
    ]