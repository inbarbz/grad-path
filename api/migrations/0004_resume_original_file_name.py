# Generated by Django 4.2.10 on 2024-03-10 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_certificate_education_experience_socialskills_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="resume",
            name="original_file_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
