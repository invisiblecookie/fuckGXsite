# Generated by Django 3.2.18 on 2023-03-22 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classics', '0002_author_book_subtitle'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='comment',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
