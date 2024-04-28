from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpRequest, JsonResponse
import json
import logging

from django.views.decorators.http import require_POST, require_http_methods

from api.models import Profile

# Create your views here.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@require_http_methods(["POST", "OPTIONS"])
def user_login(request):
    """
    Log in a user
    """
    if request.method == "OPTIONS":
        logger.info(f"user_login() called with request.method={request.method}")
        return JsonResponse({"status": "ok"})
    else:
        logger.info(f"user_login() called with request.body={request.body}")
        data = json.loads(request.body)
        # username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        logger.info(f"user_login() called with email={email}, password={password}")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            logger.info(f"user_login() DEBUG 1")
            login(request, user)
            request.session.save()  # Save the session
            logger.info(f"user_login() DEBUG 2")
            return JsonResponse({"status": "ok"})
        else:
            return JsonResponse({"error": "Invalid login credentials"}, status=400)


def user_logout(request: HttpRequest) -> JsonResponse:
    """
    Log out a user
    """
    logger.info(f"user_logout() called with request.method={request.method}")
    logout(request)
    request.session.flush()
    return JsonResponse({"status": "ok"})


# @csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def user_signup(request):
    """
    Create a new user
    """
    logger.info(f"user_signup() called with request.body={request.body}")
    if request.method == "OPTIONS":
        logger.info(f"user_signup() called with request.method={request.method}")
        return JsonResponse({"status": "ok"})
    else:
        logger.info(f"user_signup() called with request.body={request.body}")
        data = json.loads(request.body)
        # username = data.get("username")
        email = data.get("email")
        username = email
        password = data.get("password")
        logger.info(f"user_login() called with email={email}, password={password}")
        user = User.objects.create_user(username, email, password)
        user.save()

        # Create a new Profile instance and associate it with the new User
        profile = Profile(user=user)
        profile.save()

        return JsonResponse({"status": "ok"})
