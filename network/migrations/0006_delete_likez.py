# Generated by Django 4.0.2 on 2022-02-25 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_rename_likes_likez_posts_likes'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Likez',
        ),
    ]
