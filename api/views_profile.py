import os
from datetime import datetime
from django.http import HttpRequest, JsonResponse, FileResponse
import logging
from django.db import models
from typing import Union
from .models import Profile, Skills
from .resume_processing import ResumeProcessing

# Create a logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# the profile() function is used to return the profile of the user or update the profile of the user
def profile(request: HttpRequest) -> JsonResponse:
    """
    Return the profile of the user or update the profile of the user
    """
    # Get the user id from the request
    user_id = request.user.id
    logger.info(f"profile() called with Method={request.method}, user id = {user_id}")
#     # Check if the user is logged in
    if user_id is None:
        return JsonResponse({"error": "User not logged in"}, status=400)
    # If the request method is GET, return the profile of the user
    if request.method == "GET":
        try:
            logger.info(f"profile() GET with user id = {request.user.id}")
            user_profile = Profile.objects.get(user_id=user_id)
            all_skills = user_profile.skills.all()
            skill_names = [skill.name for skill in all_skills]
        except Profile.DoesNotExist:
            logger.error(
                f"profile() GET, got Profile.DoesNotExist for user_id={user_id}"
            )
            return JsonResponse({"error": "Profile not found"}, status=400)
        try:
            resume_processing = ResumeProcessing(user=request.user)
            resume_parameters = resume_processing.get_resume_parameters()
        except Exception as e:
            logger.info(
                f"profile() GET, got exception when calling resume_processing.get_resume_parameters = {e}"
            )
            resume_parameters = None
        # Create a dictionary to store the profile data
        profile_dict = {
            "user": user_profile.user.username,
            "name": user_profile.name,
            "university": user_profile.university,
            "degree": user_profile.degree,
            "gpa": user_profile.gpa,
            "graduation_date": user_profile.graduation_date,
            "intern_work_experience_years": user_profile.intern_work_experience_years,
            "full_time_work_experience_years": user_profile.full_time_work_experience_years,
            "skills": skill_names,
            "resume_parameters": (
                resume_parameters.to_dict() if resume_parameters else None
            ),
            "original_resume_file_name": user_profile.original_resume_file_name,
            "original_image_file_name": user_profile.original_image_file_name,
            # "profile_image": user_profile.profile_image.url
            # "resume": user_profile.resume.url,
        }
        # Return the profile data as a JsonResponse
        logger.info(f"profile() /profile GET returning profile_dict={profile_dict}")
        return JsonResponse(profile_dict, safe=False)
    # If the request method is POST, update the profile of the user
    elif request.method == "POST":
        logger.info(
            f"profile() POST, current-folder={os.getcwd()}, got POST={request.POST}, FILES={request.FILES}"
        )
        logger.info(f"profile() POST, got POST.name={request.POST.get('name')}")
        logger.info(f"profile() POST, got POST.gpa={request.POST.get('gpa')}")

        logger.info(
            f"profile() POST, resume={'resume' in request.FILES}, profileImage={'profileImage' in request.FILES}"
        )

        # save the file "resume" to disk into the folder name "resumes"
        resume_filename = None
        if "resume" in request.FILES:
            logger.info(f"profile() POST, got resume={request.FILES['resume']}")
            resume_filename = f"resumes/{user_id}.pdf"
            with open(resume_filename, "wb") as f:
                resume_data = request.FILES["resume"].read()
                f.write(resume_data)
                logger.info(f"profile() POST, saved resume to {resume_filename}")
            resume_processing = ResumeProcessing(
                user=request.user, pdf_file_path=resume_filename
            )
            resume_processing.save(resume_processing.extract_info())

        # save the profile image to disk into the folder name "profile_images"
        profile_image_filename = None
        if "profileImage" in request.FILES:
            logger.info(
                f"profile() POST, got profileImage={request.FILES['profileImage']}"
            )
            profile_image_filename = f"profile_images/{user_id}.jpeg"
            with open(profile_image_filename, "wb") as f:
                f.write(request.FILES["profileImage"].read())
                logger.info(
                    f"profile() POST, saved profileImage to {profile_image_filename}"
                )

        # Get the user profile
        user_profile = Profile.objects.get(user_id=request.user.id)

        # Update the fields in the Profile model
        user_profile.name = request.POST.get("name")
        user_profile.university = request.POST.get("university", "Unknown")
        user_profile.degree = request.POST.get("degree", "Unknown")
        user_profile.gpa = (
            float(request.POST.get("gpa", 0.0)) if request.POST.get("gpa") else 0.0
        )
        # Update the profile_image field in the Profile model
        user_profile.profile_image = profile_image_filename
        user_profile.resume = resume_filename
        user_profile.original_resume_file_name = (
            request.FILES["resume"] if "resume" in request.FILES else ""
        )
        user_profile.original_image_file_name = (
            request.FILES["profileImage"] if "profileImage" in request.FILES else ""
        )

        try:
            graduation_date = datetime.strptime(
                request.POST.get("graduationDate"), "%Y-%m-%d"
            )
        except ValueError:
            logger.error(
                f"profile() POST, got invalid graduationDate={request.POST.get('graduationDate')}"
            )
            graduation_date = datetime(2024, 1, 1)  # Default date

        try:
            intern_work_experience_years = float(
                request.POST.get("intern_work_experience_years", 0.0)
            )
        except ValueError:
            logger.error(
                f"profile() POST, got invalid intern_work_experience_years={request.POST.get('intern_work_experience_years')}"
            )
            intern_work_experience_years = 0.0

        try:
            full_time_work_experience_years = float(
                request.POST.get("full_time_work_experience_years", 0.0)
            )
        except ValueError:
            logger.error(
                f"profile() POST, got invalid full_time_work_experience_years={request.POST.get('full_time_work_experience_years')}"
            )
            full_time_work_experience_years = 0.0

        logger.info(
            f'profile() POST, got graduationDate={request.POST.get("graduationDate")}, f"{graduation_date}"'
        )
        user_profile.graduation_date = graduation_date
        user_profile.intern_work_experience_years = intern_work_experience_years
        user_profile.full_time_work_experience_years = full_time_work_experience_years

        # Get the skills array from the POST data
        skills_array = request.POST.get("skills").split(",")
        logger.info(f"profile() POST, got skills_array={skills_array}")
        # Get or create Skills objects for each skill name
        skills_objects = [
            Skills.objects.get_or_create(name=skill_name)[0]
            for skill_name in skills_array
        ]
        # Add the skills to the user's profile
        user_profile.skills.set(skills_objects)

        # Save the updated profile
        user_profile.save()

        return JsonResponse({"status": "ok"})

# the get_profile_image() function is used to return the profile image of the user
def get_profile_image(request: HttpRequest) -> Union[FileResponse, JsonResponse]:
    """
    Return the profile image of the user
    """
    user_id = request.user.id
    logger.info(
        f"get_profile_image() called with Method={request.method}, user id = {user_id}"
    )
    # Check if the user is logged in and if the profile image exists for the user in the database and return the profile image as a FileResponse
    if user_id is None:
        logger.error(f"get_profile_image() Error! user_id is None!!")
        return JsonResponse({"error": "User not logged in"}, status=400)
    try:
        user_profile = Profile.objects.get(user_id=user_id)
    except Profile.DoesNotExist:
        logger.error(
            f"get_profile_image() Error! Profile.DoesNotExist for user_id={user_id}"
        )
        return JsonResponse({"error": "Profile not found"}, status=400)
    try:
        profile_image_path = f"profile_images/{user_id}.jpeg"
        # check if image exists
        if not os.path.exists(profile_image_path):
            return JsonResponse({"error": "Profile image not found"}, status=400)
    except:
        logger.error(
            f"get_profile_image() Error! Profile image not found for user_id={user_id}, profile_image_path={profile_image_path}"
        )
        return JsonResponse({"error": "Profile image not found"}, status=400)
    logger.info(
        f"get_profile_image() called with user_id={user_id}, with path={profile_image_path}"
    )
    return FileResponse(open(profile_image_path, "rb"), content_type="image/jpeg")
