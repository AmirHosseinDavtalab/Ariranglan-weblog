# Generated by Django 5.0.4 on 2024-06-08 20:54

import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0015_alter_image_image_file"),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="image_file",
            field=django_resized.forms.ResizedImageField(
                crop=["middle", "center"],
                force_format="jpg",
                keep_meta=True,
                quality=-1,
                scale=None,
                size=[300, 400],
                upload_to="post_images/",
            ),
        ),
    ]
