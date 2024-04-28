from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from .views_profile import profile, get_profile_image
from .views_user import user_login, user_signup, user_logout
from .views import skills, search_jobs
import logging

urlpatterns = [
    path("search_jobs/<str:city>/<str:role>/", search_jobs, name="search_jobs"),
    path("profile/", profile, name="profile"),
    path("login", user_login, name="login"),
    path("profile_image", get_profile_image, name="profile_image"),
    path("signup", user_signup, name="register"),
    path("logout", user_logout, name="logout"),
    path("skills/", skills, name="skills"),
    # path("healthcheck/", views.healthcheck, name="healthcheck"),
    path("accounts/", include("django.contrib.auth.urls")),  # Add this line
    # The root path for your SPA
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
    # Catch-all pattern for SPA - ensures that any non-defined route is handled by Vue.js
    # re_path(r"^.*/$", TemplateView.as_view(template_name="index.html")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(
    f"Grad-Path settings.DEBUG={settings.DEBUG} URL={settings.STATIC_URL} root={settings.STATIC_ROOT} urlpatterns: {urlpatterns}"
)
