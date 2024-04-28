from django.contrib import admin
from .models import (
    Certificate,
    Experience,
    Education,
    SoftSkills,
    TechnicalSkills,
    SocialSkills,
    Resume,
    Skills,
    Profile,
)

# the following lines register the models with the Django admin site so that they can be viewed and edited in the admin interface
admin.site.register(Certificate)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(SoftSkills)
admin.site.register(TechnicalSkills)
admin.site.register(SocialSkills)
admin.site.register(Resume)
admin.site.register(Skills)
admin.site.register(Profile)
