# Generated by Django 4.2.10 on 2024-03-10 06:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0005_profile_original_image_file_name_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="resume",
            name="original_file_name",
        ),
    ]