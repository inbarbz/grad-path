from django.test import TestCase
from dotenv import load_dotenv
import logging
import os
from ..LLM.resume_reviewer import ResumeReviewer, ResumeParameters

# the TestResumeReviewer class is used to test the ResumeReviewer class 
class TestResumeReviewer(TestCase):
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
            f"TestResumeReviewer() called with: env_result: {env_result}, pwd={os.getcwd()}"
        )
# Test the extract_parameters() method in ResumeReviewer.py module with a sample resume description data set to check if the resume parameters are extracted correctly
    def test_able_to_extract(self):
        jr = ResumeReviewer()
        resume_description = """
INBAR BEN ZUK

+44-7950973675
www.linkedin.com/in/inbarbenzuk
inbarbenzuk@gmail.com

Achievements
Queen Mary University
Received the Global Excellence
Scholarship for my bachelor’s degree
studies in Queen Mary University of
London
National Service
Received an excellence award as a
research analyst
FLL Robotics
As the head of research in my FLL
(https://bit.ly/3fP0XtD) international
robotic competition, received the first
national prize and chosen to present
our research in the US embassy and at
the national TV & Radio stations

Languages & Skills
• Hebrew – first language
• English – High level
• OFFICE skills
• Basic Figma skills
• Jira
• Python fundamentals
• JavaScript fundamentals
• HTML and CSS
• Basic SQL

Product Manager intern (April-Sep 2023)
Manatal, Thailand
During my 6-month internship I managed my own features throughout
their lifecycle, from customer research and design to development,
A/B testing and iteration.
I collaborated with cross-functional teams, including design, marketing,
and engineering (participating in the scrum ceremonies), and
contributed to core product metrics including conversion and retention.

BSc (Eng) Creative Computing (2021 – 2024)
Queen Mary University of London
Currently on my final year, studying towards a bachelor’s degree in
creative computing. As part of this degree program, I focus on
programming fundamentals as well as user centred design practices.

Professional Business English Diploma (2021)
Kaplan Higher Education Institute, Singapore
Completed with High Distinction a diploma in Professional Business
English at Kaplan Higher Education Institute in Singapore, improving
both my English verbal and written skills.

National Service (2018 – 2021)
IDF, Israel
As an Israeli citizen, I attended the National Service for 3 years as a
research analyst. Independently leading the research in my domain,
analysing information, and formulating conclusions and
recommendations. I presented my findings in written form and verbally
for high-ranking officers, working under extreme pressure with high
national responsibility.
            """
        # Extract the resume parameters from the resume description using the extract_parameters() method in ResumeReviewer.py module and store it in the resume_parameters variable
        resume_parameters: ResumeParameters = jr.extract_parameters(resume_description)
        print(resume_parameters)
        self.assertEqual(resume_parameters.location, "London")
        found_manatal = False
        for experience in resume_parameters.experience:
            if experience.get("company_name", "Unknown") == "Manatal":
                found_manatal = True
                self.assertEqual(
                    experience.get("position", "Unknown"), "Product Manager intern"
                )
                self.assertEqual(experience.get("start_date", "Unknown"), "2023-04-01")
                self.assertEqual(experience.get("is_internship", "Unknown"), True)
        self.assertEqual(found_manatal, True)
