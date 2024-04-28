import base64
import io
import logging
import os
import re
import time
from typing import Optional
# from django.http import HttpRequest, JsonResponse, FileResponse
from django.contrib.auth.models import User
from PyPDF2 import PdfReader
import pdfplumber
# from .models import Profile, Skills
from .models import (
    Resume,
    Certificate,
    Experience,
    Education,
    SoftSkills,
    TechnicalSkills,
    SocialSkills,
)
from .LLM.resume_reviewer import ResumeReviewer, ResumeParameters

# the ResumeProcessing class is used to process the resume of the user
class ResumeProcessing:
    def __init__(
        self,
        user: User,
        pdf_file_path: Optional[str] = None,
    ):
        """
        Constructor for ResumeProcessing
        :param pdf_resume: Optional str containing the content of the resume in pdf format
        :param txt_resume: Optional str containing the content of the resume in txt format
        :param pdf_file_path: Optional str containing the path to the pdf file
        """
        # Initialize the user, logger, and pdf_file_path attributes of the ResumeProcessing class
        self.user = user
        self.logger = logging.getLogger(__name__)
        self.pdf_file_path = pdf_file_path
        if pdf_file_path:
            with pdfplumber.open(pdf_file_path) as pdf:
                self.logger.info(
                    f"ResumeProcessing() got pdf={pdf}, pdf_file_path={pdf_file_path}, pages={len(pdf.pages)}"
                )
                self.txt_resume = ""
                for page in pdf.pages:
                    self.txt_resume += page.extract_text() or ""
            self.txt_resume = re.sub("^\s*$", "\n", self.txt_resume, flags=re.MULTILINE)
            self.logger.info(f"ResumeProcessing() got txt_resume={self.txt_resume}")
        else:
            self.txt_resume = None
    # Method to save the resume data to the database
    def save(self, resume_data: ResumeParameters):
        """
        Save the resume data to the database
        """
        self.logger.info(f"save() called with resume_data={resume_data}")
        if resume_data is None:
            return False

        # Create and save PersonalDetails
        soft_skills = (
            [SoftSkills.objects.create(name=skill) for skill in resume_data.soft_skills]
            if resume_data.soft_skills
            else []
        )
        technical_skills = (
            [
                TechnicalSkills.objects.create(name=skill)
                for skill in resume_data.technical_skills
            ]
            if resume_data.technical_skills
            else []
        )
        social_skills = (
            [
                SocialSkills.objects.create(name=skill)
                for skill in resume_data.social_skills
            ]
            if resume_data.social_skills
            else []
        )

        # Create and save Education, Experience, and Certificate
        education = [Education.objects.create(**edu) for edu in resume_data.education]
        experience = [
            Experience.objects.create(**exp) for exp in resume_data.experience
        ]
        certificate = [
            Certificate.objects.create(**cert) for cert in resume_data.certifications
        ]

        # Create and save Resume
        resume, created = Resume.objects.update_or_create(user=self.user)

        resume.soft_skills.set(soft_skills)
        resume.technical_skills.set(technical_skills)
        resume.social_skills.set(social_skills)
        resume.education.set(education)
        resume.experience.set(experience)
        resume.certificate.set(certificate)
        resume.save()

        return True

    def get_resume_parameters(self) -> Optional[ResumeParameters]:
        """
        Get the resume parameters from the database
        """
        self.logger.info(f"get_resume_parameters() called")
        try:
            resume = Resume.objects.get(user=self.user)

            # Create ResumeParameters object
            resume_parameters = ResumeParameters()

            # Fill ResumeParameters with data from Resume
            resume_parameters.soft_skills = list(
                resume.soft_skills.values_list("name", flat=True)
            )
            resume_parameters.technical_skills = list(
                resume.technical_skills.values_list("name", flat=True)
            )
            resume_parameters.social_skills = list(
                resume.social_skills.values_list("name", flat=True)
            )
            resume_parameters.education = list(resume.education.values())
            resume_parameters.experience = list(resume.experience.values())
            resume_parameters.certifications = list(resume.certificate.values())

            self.logger.info(
                f"get_resume_parameters() returning resume_parameters={resume_parameters}"
            )

            return resume_parameters
        except Exception as e:
            return None
    # Method to extract the resume info from the resume using LLM and return the resume parameters 
    def extract_info(self) -> ResumeParameters:
        """
        Extract the resume info from the resume using LLM
        """
        self.logger.info(f"extract_info() called")
        resume_reviewer = ResumeReviewer()
        # time the following function, and add a log of the time it took it to run
        start_time = time.time()
        resume_parameters: ResumeParameters = resume_reviewer.extract_parameters(
            self.txt_resume
        )
        end_time = time.time()
        self.logger.info(
            f"extract_info() took {end_time - start_time} seconds, with resume_parameters={resume_parameters}"
        )
        # do some processing
        return resume_parameters
