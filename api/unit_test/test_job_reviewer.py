from django.test import TestCase
from dotenv import load_dotenv
import logging
import os
from ..LLM.job_reviewer import (
    JobReviewer,
    JobParameters,
    JobLevels,
    JobTitles,
    TechnicalSkills,
    SoftSkills,
    SocialSkills,
)

# the TestJobReviewer class is used to test the job_reviewer.py module
class TestJobReviewer(TestCase):
    """
    Unit Tests for the job_reviewer.py module
    use "python manage.py test" to execute the tests
    """
# Set up the test environment for the test cases to run in isolation from each other
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        env_result = load_dotenv("./.env")
        logger.info(
            f"TestJobReviewer() called with city: env_result: {env_result}, pwd={os.getcwd()}"
        )
# Test the extract_parameters() method in JobReviewer.py module with a sample job description data set to check if the job parameters are extracted correctly
    def test_able_to_extract(self):
        jr = JobReviewer()
        job_description = """
            A new mobile network is forming, do you want to be a part of something at greenfield stage that's going to disrupt the rest of the industry and work alongside a founder who sold their previous start-up for hundreds of Millions of pounds?
              And still get equity...
              If so then this might be for you...
              As the Lead Engineer
              Hybrid working in the Covent garden office
              Have a huge impact on a product from day 1
              Work closely with a highly successful founder and leadership team on their next venture
              Be responsible for the technical delivery of the product
              Solve real-world problems using innovative and modern technologies
              You should have:
              At least 2 years of experience in a leadership position
              Strong user focus
              Experience working in a fast-paced start-up environment and building to-scale products
              Have experience working with ReactNative & Typescript (+ Next.js, Docker & Postgres is a nice to have)
              A business/entrepreneur mindset
              If this sounds of interest please send me an email at: ellis.gilbert@fewandfar.io
              or just apply on Linkedin
            """
        # Extract the job parameters from the job description using the extract_parameters() method in JobReviewer.py module and store it in the job_parameters variable
        job_parameters: JobParameters = jr.extract_parameters(job_description)
        print(job_parameters)
        self.assertEqual(job_parameters.location, "London")
        self.assertEqual(job_parameters.experience, "Mid Level")
        self.assertEqual(job_parameters.mandatory_experience_years, 2)
        self.assertEqual(job_parameters.optional_experience_years, 0)
        self.assertEqual(job_parameters.education_level, "Bachelor's Degree")
