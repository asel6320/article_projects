# Generated by Django 5.0.6 on 2024-07-09 05:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Created at')),
                ('name', models.CharField(max_length=31, verbose_name='Tag')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
                'db_table': 'tags',
            },
        ),
        migrations.CreateModel(
            name='ArticleTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Created at')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags_articles', to='webapp.article', verbose_name='Article')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles_tags', to='webapp.tag', verbose_name='Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(related_name='articles', through='webapp.ArticleTag', to='webapp.tag', verbose_name='Tags'),
        ),
    ]
