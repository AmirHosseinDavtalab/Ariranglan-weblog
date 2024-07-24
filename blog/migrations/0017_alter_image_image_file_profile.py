# Generated by Django 5.0.4 on 2024-07-22 17:28

import django.db.models.deletion
import django_jalali.db.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0016_alter_image_image_file"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="image_file",
            field=models.ImageField(upload_to="post_images/"),
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date_of_birth",
                    django_jalali.db.models.jDateField(
                        blank=True, null=True, verbose_name="تاریخ تولد"
                    ),
                ),
                ("bio", models.TextField(blank=True, null=True, verbose_name="بایو")),
                (
                    "photo",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="profile_images/",
                        verbose_name="تصویر پروفایل",
                    ),
                ),
                ("job", models.CharField(blank=True, null=True, verbose_name="شغل")),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "پروفایل",
                "verbose_name_plural": "پروفایل ها",
            },
        ),
    ]
