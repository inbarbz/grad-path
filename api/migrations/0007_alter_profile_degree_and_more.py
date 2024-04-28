# Generated by Django 4.2.10 on 2024-03-17 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0006_remove_resume_original_file_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="degree",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="full_time_work_experience_years",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="gpa",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="graduation_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="intern_work_experience_years",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="university",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]