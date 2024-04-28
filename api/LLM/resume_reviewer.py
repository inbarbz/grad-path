from dataclasses import dataclass, field, asdict
import os
import json
import logging
from typing import Optional, List
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI
from .job_reviewer import JobLevels, SoftSkills, TechnicalSkills, SocialSkills
from .Universities import University

# Define the dataclasses for the resume parameters (Experience, Education, Certificate)
@dataclass
# Define the fields for the Experience dataclass with default values as None or empty list
class Experience:  
    is_internship: Optional[bool] = field(default=None)
    company_name: Optional[str] = field(default=None)
    job_title: Optional[str] = field(default=None)
    start_date: Optional[str] = field(default=None)
    end_date: Optional[str] = field(default=None)
    responsibilities: Optional[List[str]] = field(default_factory=list)


@dataclass
# Define the fields for the Education dataclass with default values as None
class Education:
    institution_name: Optional[str] = field(default=None)
    institution_name_enum: Optional[str] = field(default=None)
    degree: Optional[str] = field(default=None)
    field_of_study: Optional[str] = field(default=None)
    graduation_date: Optional[str] = field(default=None)

    def __str__(self):
        return f"{self.institution_name_enum}"


@dataclass
# Define the fields for the Certificate dataclass with default values as None
class Certificate:
    certification_name: Optional[str] = field(default=None)
    issuing_organization: Optional[str] = field(default=None)
    date_issued: Optional[str] = field(default=None)
    expiration_date: Optional[str] = field(default=None)


@dataclass
# Define the fields for the ResumeParameters dataclass with default values as None or empty list
class ResumeParameters:
    location: Optional[str] = field(default=None)
    experience: Optional[List[Experience]] = field(default_factory=list)
    education: Optional[List[Education]] = field(default_factory=list)
    certifications: Optional[List[Certificate]] = field(default_factory=list)
    technical_skills: Optional[List[str]] = field(default_factory=list)
    social_skills: Optional[List[str]] = field(default_factory=list)
    soft_skills: Optional[List[str]] = field(default_factory=list)

    def get_education_start_date(self) -> Optional[str]:
        """
        Get the start date of the first education entry
        """
        if self.education is None or len(self.education) == 0:
            return None
        return min(education["graduation_date"] for education in self.education)

    def get_experience_duration_years(self) -> float:
        """
        Calculate the total duration of all experiences in the resume and return it in [years]
        """
        if self.experience is None:
            return 0
        total_duration_days = 0.0
        education_start_date = self.get_education_start_date()
        for experience in self.experience:
            if type(experience) == dict:
                if "id" in experience:
                    del experience["id"]
                experience = Experience(**experience)
            if experience.start_date is not None and experience.end_date is not None:
                if type(experience.start_date) == str:
                    start_date = datetime.strptime(experience.start_date, "%Y-%m-%d")
                else:
                    start_date = experience.start_date
                if type(experience.end_date) == str:
                    end_date = datetime.strptime(experience.end_date, "%Y-%m-%d")
                else:
                    end_date = experience.end_date
                experience_duration = (end_date - start_date).days
                print(
                    f"get_experience_duration_years() duration {end_date} to {education_start_date}, experience_duration={experience_duration} days"
                )
                # skip experiences that happened before the education
                if start_date <= education_start_date:
                    print(
                        f"skipping experience {start_date} as its before education started {education_start_date}"
                    )
                    continue
                total_duration_days += (end_date - start_date).days
        print(
            f"get_experience_duration_years() total_duration_days = {total_duration_days / 365.0} years"
        )
        return total_duration_days / 365.0

    def to_dict(self):
        return asdict(self)

# Define the ResumeReviewer class to extract parameters from a resume and calculate the total duration of all experiences in the resume
class ResumeReviewer:
    def __init__(self):
        self.logging = logging.getLogger(__name__)
        found_env = load_dotenv("./.env")
        self.university_list = University().get_name_list()
        self.logging.info(
            f"ResumeReviewer.__init__() current directory = {os.getcwd()}, found_env={found_env}"
        )
        self.client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"],
        )
        self.functions = [
            {
                "name": "resume_parser",
                "description": "This function automatically extracts and structures key information from users' resumes, including personal details, professional experience, educational background, skills, and certifications.There can be more that one education field and more than one education field. This structured data facilitates the matching process with job postings.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "Current or preferred employment location of the user. when missing default to Unknown",
                        },
                        "experience": {
                            "type": "array",
                            "description": "Array of Professional experience records.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "is_internship": {
                                        "type": "boolean",
                                        "description": "true if this job is an internship, false otherwise.",
                                    },
                                    "company_name": {
                                        "type": "string",
                                        "description": "Name of the company where the user worked.",
                                    },
                                    "job_title": {
                                        "type": "string",
                                        "description": "Job title held by the user.",
                                    },
                                    "start_date": {
                                        "type": "string",
                                        "format": "date",
                                        "description": "Start date of employment. use the format YYYY-MM-DD. if month is missing, assume 01. if day is missing, assume 01",
                                    },
                                    "end_date": {
                                        "type": "string",
                                        "format": "date",
                                        "description": "End date of employment, if applicable. use the format YYYY-MM-DD. if month is missing, assume 01. if day is missing, assume 01",
                                    },
                                    "responsibilities": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "Responsibilities and achievements during the employment period.",
                                    },
                                },
                                "required": [
                                    "company_name",
                                    "job_title",
                                    "start_date",
                                    "responsibilities",
                                ],
                            },
                        },
                        "education": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "institution_name": {
                                        "type": "string",
                                        "description": "Educational institution name and location",
                                    },
                                    "institution_name_enum": {
                                        "type": "array",
                                        "items": {
                                            "type": "string",
                                            "enum": self.university_list,
                                        },
                                        "description": "Educational institution name and location, matching one of the provided Enum list",
                                    },
                                    "degree": {
                                        "type": "string",
                                        "description": "Degree or certification obtained.",
                                    },
                                    "field_of_study": {
                                        "type": "string",
                                        "description": "Field of study or major.",
                                    },
                                    "graduation_date": {
                                        "type": "string",
                                        "format": "date",
                                        "description": "Graduation date or expected graduation date. use the format YYYY-MM-DD. if month is missing, assume 01. if day is missing, assume 01",
                                    },
                                },
                                "required": [
                                    "institution_name",
                                    "institution_name_enum",
                                    "degree",
                                    "field_of_study",
                                ],
                            },
                            "description": "Educational background details.",
                        },
                        "soft_skills": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": [x.value for x in list(SoftSkills)],
                            },
                            "description": "Soft skills like creativity and problem-solving and Communication with peers",
                        },
                        "technical_skills": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": [x.value for x in list(TechnicalSkills)],
                            },
                            "description": "Technical skills including programming and data analysis.",
                        },
                        "social_skills": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": [x.value for x in list(SocialSkills)],
                            },
                            "description": "Social skills such as leadership and collaboration. A position as President of a club is a good example of a Leadership skill.",
                        },
                        "certifications": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "certification_name": {
                                        "type": "string",
                                        "description": "Certification name.",
                                    },
                                    "issuing_organization": {
                                        "type": "string",
                                        "description": "Organization that issued the certification.",
                                    },
                                    "date_issued": {
                                        "type": "string",
                                        "format": "date",
                                        "description": "Date the certification was issued. use the format YYYY-MM-DD. if month is missing, assume 01. if day is missing, assume 01",
                                    },
                                    "expiration_date": {
                                        "type": "string",
                                        "format": "date",
                                        "description": "Expiration date of the certification, if any. use the format YYYY-MM-DD. if month is missing, assume 01. if day is missing, assume 01",
                                    },
                                },
                                "required": [
                                    "certification_name",
                                    "issuing_organization",
                                    "date_issued",
                                ],
                            },
                            "description": "Certifications mentioned in the resume.",
                        },
                    },
                    "required": [
                        "resume_id",
                        "personal_details",
                        "experience",
                        "education",
                        "skills",
                        "certifications",
                    ],
                },
            }
        ]

    def fix_dates(self, resume_parameters: ResumeParameters) -> ResumeParameters:
        """
        Fixes the dates in the resume_parameters to have a valid format
        :param resume_parameters: the resume parameters
        :return: the resume parameters with fixed dates
        """
        # self.logging.info(f"fix_dates() started! resume_parameters={resume_parameters}")
        for experience in resume_parameters.experience:
            if "start_date" in experience:
                experience["start_date"] = self.fix_date(experience["start_date"])
            if "end_date" in experience:
                experience["end_date"] = self.fix_date(experience["end_date"])
        for education in resume_parameters.education:
            if "graduation_date" in education:
                education["graduation_date"] = self.fix_date(
                    education["graduation_date"]
                )
        for certification in resume_parameters.certifications:
            if "date_issued" in certification:
                certification["date_issued"] = self.fix_date(
                    certification["date_issued"]
                )
            if "expiration_date" in certification:
                certification["expiration_date"] = self.fix_date(
                    certification["expiration_date"]
                )
        self.logging.info(
            f"fix_dates() returning resume_parameters={resume_parameters}"
        )
        return resume_parameters

    def fix_date(self, date_str):
        """
        Fixes a date string
        :param date_str: the date string
        :return: the fixed date string
        """
        if date_str is None:
            return None
        try:
            # Try to parse the date string as a full date (YYYY-MM-DD)
            date = datetime.strptime(date_str.split("T")[0], "%Y-%m-%d")
        except ValueError:
            try:
                # If that fails, try to parse it as a year only (YYYY-MM)
                date = datetime.strptime(date_str, "%Y-%m")
            except ValueError:
                try:
                    # If that fails, try to parse it as a year only (YYYY)
                    date = datetime.strptime(date_str, "%Y")
                except ValueError:
                    # If that also fails, return the original string
                    self.logging.warning(
                        f"fix_date() failed to parse date_str={date_str}"
                    )
                    return date_str
        # Format the date as a string in the format YYYY-MM-DD
        return date.strftime("%Y-%m-%d")

    def extract_parameters(self, resume: str) -> ResumeParameters:
        """
        Uses ChatGPT to Extracts parameters from a resume
        :param resume: the resume text
        :return: ResumeParameters
        """
        self.logging.info(f"extract_parameters() started! resume={resume}")
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": resume}],
                functions=self.functions,
                function_call="auto",
            )
            # Loading the response as a JSON object
            json_response = json.loads(
                response.choices[0].message.function_call.arguments
            )
            # self.logging.info(f"extract_parameters() json_response={json_response}")
        except Exception as e:
            self.logging.error(
                f"extract_parameters() failed with {e}. resume text: {resume}, response={response}"
            )
            return None
        # Convert the JSON response into a ResumeParameters instance
        resume_parameters = ResumeParameters(**json_response)
        self.fix_dates(resume_parameters)
        self.logging.info(
            f"extract_parameters() returning resume_parameters={resume_parameters}"
        )
        return resume_parameters
