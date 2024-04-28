from django.test import TestCase
from dotenv import load_dotenv
import logging
import os
from ..MatchScore import MatchScore
from ..LLM.resume_reviewer import ResumeParameters, Education, Experience
from ..LLM.job_reviewer import (
    JobReviewer,
    JobParameters,
    JobLevels,
    JobTitles,
    TechnicalSkills,
    SoftSkills,
    SocialSkills,
)

logger = logging.getLogger(__name__)

# Create your tests here.
class TestMatchScore(TestCase):
    """
    Unit Tests for the MatchScore.py module
    use "python manage.py test api.unit_test.test_matchscore.TestMatchScore.test_match_score" to execute the tests
    """

    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        env_result = load_dotenv("./.env")
        logger.info(f"TestMatchScore() env_result: {env_result}, pwd={os.getcwd()}")

    # Test the get_matching_score() method in MatchScore.py module with a sample resume and job description data set to check if the matching score is greater than 70
    def test_match_score(self):
        resume_parameters = ResumeParameters(
            location="London",
            experience=[
                Experience(
                    is_internship=True,
                    company_name="Google",
                    job_title="Product Manager",
                    start_date="2021-01-01",
                    end_date="2021-06-01",
                    responsibilities=[],
                )
            ],
            education=[
                Education(
                    institution_name="Imperial College London",
                    institution_name_enum="Imperial College London",
                    degree="Bachelor's Degree",
                    field_of_study="Computer Science",
                    graduation_date="2021-01-01",
                )
            ],
            certifications=None,
            technical_skills=[
                TechnicalSkills.DataAnalysis.value,
                TechnicalSkills.SQL.value,
            ],
            social_skills=[
                SocialSkills.ConflictResolution.value,
            ],
            soft_skills=[
                SoftSkills.Communication.value,
                SoftSkills.Creativity.value,
                SoftSkills.AttentionToDetail.value,
            ],
        )
        job_parameters = JobParameters(
            location="London",
            experience="Mid Level",
            mandatory_experience_years=0.4,
            optional_experience_years=0,
            education_level="Bachelor's Degree",
            technical_skills=[
                TechnicalSkills.Programming.value,
                TechnicalSkills.SQL.value,
                TechnicalSkills.DataAnalysis.value,
            ],
            soft_skills=[
                SoftSkills.Communication.value,
                SoftSkills.Creativity.value,
                SoftSkills.ProblemSolving.value,
                SoftSkills.TimeManagement.value,
            ],
            social_skills=[],
            job_title="Product Manager",
            job_level="",
            education_field="",
            min_salary=0,
            max_salary=10000,
            benefits=[],
            responsibilities=[],
        )
        # Create a MatchScore object and get the matching score between the resume and job description data sets
        score_match = MatchScore(resume_parameters, job_parameters)
        score = score_match.get_matching_score()
        logger.info(f"test_match_score() score: {score}")
        self.assertGreater(score, 70)
