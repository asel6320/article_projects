# Generated by Django 5.0.6 on 2024-07-29 06:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_alter_article_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='author',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
    ]
