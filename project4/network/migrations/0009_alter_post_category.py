# Generated by Django 5.1.6 on 2025-02-22 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0008_post_likes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="category",
            field=models.CharField(
                blank=True,
                choices=[
                    ("computer_graphics", "Computer Graphics"),
                    ("graphic_designs", "Graphic Designs"),
                    ("3d_models", "3D Models"),
                    ("painting", "Painting"),
                    ("photography", "Photography"),
                    ("music", "Music"),
                ],
                max_length=20,
                null=True,
            ),
        ),
    ]
