# Generated by Django 2.0.1 on 2018-06-07 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parsebot', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TeamArticle',
            new_name='Article',
        ),
    ]