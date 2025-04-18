# Generated by Django 5.1.6 on 2025-02-22 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0004_rename_followed_following_followers_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="category",
            field=models.CharField(
                choices=[
                    ("computer_graphics", "Computer Graphics"),
                    ("painting", "Painting"),
                    ("photography", "Photography"),
                    ("3d_models", "3D Models"),
                    ("graphic_design", "Graphic Design"),
                    ("music", "Music"),
                ],
                default="computer_graphics",
                max_length=50,
            ),
        ),
    ]
