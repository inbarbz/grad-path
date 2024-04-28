from django.http import HttpRequest
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from unittest.mock import Mock
from dotenv import load_dotenv
import logging
import os
import pdb
from ..JobEnricher import job_enricher

# Create your tests here.
class TestJobEnricher(TestCase):
    """
    Unit Tests for the job_enricher.py module
    use "python manage.py test" to execute the tests
    """
    # Set up the test environment for the test cases to run in isolation from each other 
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        env_result = load_dotenv("./.env")
        logger.info(
            f"TestJobEnricher() called with: env_result: {env_result}, pwd={os.getcwd()}"
        )
    # Test the job_enricher() method in JobEnricher.py module with a sample request data set to check if the job_enricher function is able to enrich the job data
    def test_job_enricher(self):
        """
        Test the job_enricher function
        use: python manage.py test api.unit_test.test_job_enricher.TestJobEnricher.test_job_enricher
        """
        # Create a mock request
        request = Mock(spec=HttpRequest)
        # Set the method to POST
        request.method = "POST"
        # Mock the user object and its id attribute
        user = Mock(spec=AnonymousUser)
        user.id = "valid_user_id"
        # Assign the user object to the request
        request.user = user

        # pdb.set_trace()

        job_enricher(request)
