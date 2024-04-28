from django.db import models
from django.contrib.auth.models import User

#
# all the following Models, are filled with data extracted from the Resume
#


class Certificate(models.Model):
    certification_name = models.CharField(max_length=255, null=True, blank=True)
    issuing_organization = models.CharField(max_length=255, null=True, blank=True)
    date_issued = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.certification_name


class Experience(models.Model):
    is_internship = models.BooleanField(null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    job_title = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    responsibilities = models.TextField(
        null=True, blank=True
    )  # Store as comma-separated values

    def __str__(self):
        return self.company_name


class Education(models.Model):
    institution_name = models.CharField(max_length=255, null=True, blank=True)
    institution_name_enum = models.CharField(max_length=255, null=True, blank=True)
    degree = models.CharField(max_length=255, null=True, blank=True)
    field_of_study = models.CharField(max_length=255, null=True, blank=True)
    graduation_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.institution_name


class SoftSkills(models.Model):
    name = models.CharField(max_length=50)


class TechnicalSkills(models.Model):
    name = models.CharField(max_length=50)


class SocialSkills(models.Model):
    name = models.CharField(max_length=50)


class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    education = models.ManyToManyField(Education, null=True, blank=True)
    experience = models.ManyToManyField(Experience, null=True, blank=True)
    certificate = models.ManyToManyField(Certificate, null=True, blank=True)
    soft_skills = models.ManyToManyField(SoftSkills, null=True, blank=True)
    technical_skills = models.ManyToManyField(TechnicalSkills, null=True, blank=True)
    social_skills = models.ManyToManyField(SocialSkills, null=True, blank=True)

    def __str__(self):
        return f"Resume : {self.user.email} - {self.education} - {self.experience} - {self.certificate} - {self.soft_skills} - {self.technical_skills} - {self.social_skills}"


class Skills(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    university = models.CharField(max_length=100, null=True, blank=True)
    degree = models.CharField(max_length=100, null=True, blank=True)
    gpa = models.FloatField(null=True, blank=True)
    graduation_date = models.DateField(null=True, blank=True)
    intern_work_experience_years = models.FloatField(null=True, blank=True)
    full_time_work_experience_years = models.FloatField(null=True, blank=True)
    skills = models.ManyToManyField(Skills, blank=True)
    profile_image = models.ImageField(
        upload_to="profile_images/", default="profile_images/default.jpg"
    )
    resume = models.FileField(upload_to="resumes/", default="resumes/default.pdf")
    original_resume_file_name = models.CharField(max_length=255, null=True, blank=True)
    original_image_file_name = models.CharField(max_length=255, null=True, blank=True)
