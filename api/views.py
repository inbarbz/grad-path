import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, JsonResponse
import json
import logging

from dotenv import load_dotenv

from api.resume_processing import ResumeProcessing
from .LLM.job_reviewer import JobParameters
from .LLM.resume_reviewer import ResumeParameters
from .MatchScore import MatchScore
from .job_boards.SerpApi import SerpApi
from .job_boards.Job import Job
from .models import Profile, Skills, Resume

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Grad-Path API views.py loaded!!!")


def get_resume_parameters(user: User) -> ResumeParameters:
    resume_processing = ResumeProcessing(user=user)
    resume_parameters = resume_processing.get_resume_parameters()
    return resume_parameters


def get_job_parameters(job: Job) -> JobParameters:
    pass


@login_required
def search_jobs(request: HttpRequest, city: str, role: str) -> JsonResponse:
    logger.info(f"search_jobs() called with city: {city}, role: {role}")
    env_result = load_dotenv("./.env")
    logger.info(
        f"search_jobs() called with city: env_result: {env_result}, pwd={os.getcwd()}"
    )
    s = SerpApi()
    r = s.fetch_jobs(in_city=city, job_description=role)
    # fetch the match score using the class MatchScore for the logged-in user and the job.match_score
    enriched_r = []
    for job in r:
        match_score = MatchScore(
            get_resume_parameters(request.user), job.extracted_data
        )
        job.match_score = match_score.get_matching_score()
        enriched_r.append(job)
    logger.info(f"search_jobs() returning TYPE {type(enriched_r[0])} ")
    post_list = json.dumps([obj.to_dict() for obj in enriched_r])
    return JsonResponse(post_list, safe=False)


def skills(request: HttpRequest) -> JsonResponse:
    """
    Return a list of all the skills in the database
    """
    # get the list of skill names from the Skill model
    skills_list = [skill.name for skill in Skills.objects.all()]
    return JsonResponse(skills_list, safe=False)


def healthcheck(request: HttpRequest) -> JsonResponse:
    logger.info("healthcheck() ok")
    return JsonResponse({"status": "ok"})


if __name__ == "__main__":
    x = get_resume_parameters(1)
