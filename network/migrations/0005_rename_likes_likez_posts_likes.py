# Generated by Django 4.0.2 on 2022-02-25 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_remove_posts_likes_likes'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Likes',
            new_name='Likez',
        ),
        migrations.AddField(
            model_name='posts',
            name='likes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]