from dataclasses import dataclass
import os
import json
import logging
from enum import Enum
from typing import Optional
from openai import OpenAI

#the job titles enum class is used to define the job titles that can be extracted from a job description
@dataclass
class JobTitles(Enum):
    ProductManager = "Product Manager"
    SoftwareEngineer = "Software Engineer"
    ProjectManager = "Project Manager"
    MarketingSpecialist = "Marketing Specialist"
    DataAnalyst = "Data Analyst"
    DataScientist = "Data Scientist"
    ProjectCoordinator = "Project Coordinator"
    UXDesigner = "UX Designer"
    GraphicDesigner = "Graphic Designer"
    BusinessAnalyst = "Business Analyst"
    

    def __str__(self):
        return self.value

#the job levels enum class is used to define the job levels that can be extracted from a job description
@dataclass
class JobLevels(Enum):
    Graduate = "Graduate"
    Junior = "Junior"
    Associate = "Associate"
    EntryLevel = "Entry Level"
    MidLevel = "Mid Level"
    SeniorLevel = "Senior Level"

    def __str__(self):
        return self.value

#the soft skills enum class is used to define the soft skills that can be extracted from a job description
@dataclass
class SoftSkills(Enum):
    Creativity = "Creativity"
    Adaptability = "Adaptability"
    TimeManagement = "Time Management"
    Curiosity = "Curiosity"
    CriticalThinking = "Critical Thinking"
    AnalyticalThinking = "Analytical Thinking"
    AttentionToDetail = "Attention to Detail"
    VerbalSkills = "Verbal Skills"
    WrittenSkills = "Written Skills"
    OrganisationalSkills = "Organisational skills"
    MultiTaskingSkills = "Multi-tasking Skills"
    Communication = "Good Communication"
    Teamwork = "Teamwork"
    Leadership = "Leadership"
    EmotionalIntelligence = "Emotional Intelligence"
    Negotiation = "Negotiation"
    ConflictResolution = "Conflict Resolution"
    Networking = "Networking"
    Persuasion = "Persuasion"
    DecisionMaking = "Decision Making"
    StressManagement = "Stress Management"
    Flexibility = "Flexibility"
    ProblemSolving = "Problem Solving"
    CustomerService = "Customer Service"
    Sales = "Sales"
    Marketing = "Marketing"
    PublicSpeaking = "Public Speaking"
    PresentationSkills = "Presentation Skills"
    InterpersonalSkills = "Interpersonal Skills"
    Empathy = "Empathy"
    Patience = "Patience"
    Resilience = "Resilience"
    SelfMotivation = "Self-Motivation"
    SelfConfidence = "Self-Confidence"
    SelfAwareness = "Self-Awareness"
    SelfRegulation = "Self-Regulation"


    def __str__(self):
        return self.value

#the technical skills enum class is used to define the technical skills that can be extracted from a job description
class TechnicalSkills(Enum):
    Programming = "Programming"
    DataAnalysis = "Data Analysis"
    WebDevelopment = "Web Development"
    DatabaseManagement = "Database Management"
    MachineLearning = "Machine Learning"
    Sketching = "Sketching"
    Prototyping = "Prototyping"
    ABTesting = "A/B Testing"
    PYTHON = "Python Programming"
    JAVA = "Java Programming"
    JAVASCRIPT = "Javascript Programming"
    SCALA = "Scala Programming"
    AWS = "AWS Cloud"
    Jira = "Jira"
    Figma = "Figma"
    HTML = "HTML"
    CSS = "CSS"
    SQL = "SQL"
    ABtesting = "A/B Testing"
    AI = "Artificial Intelligence"
    Database= "Database"
    NLP = "Natural Language Processing"
    LLM = "Large Language Models"
    C = "C++"
    Scala= "Scala"
    Agile = "Agile"
    Scrum = "Scrum"
    Unity = "Unity"
    Django = "Django"
    Vue= "Vue"
    React = "React"
    Typescript = "Typescript"
    Excel = "Excel"
    Tableau = "Tableau"
    PowerBI = "PowerBI"
    GoogleAnalytics = "Google Analytics"
    AdobePhotoshop = "Adobe Photoshop"
    AdobeIllustrator = "Adobe Illustrator"
    AdobeXD = "Adobe XD"
    AdobePremiere = "Adobe Premiere"
    AdobeAfterEffects = "Adobe After Effects"
    AdobeInDesign = "Adobe InDesign"
    AdobeLightroom = "Adobe Lightroom"
    AdobeSpark = "Adobe Spark"
    AdobeAudition = "Adobe Audition"
    AdobeAnimate = "Adobe Animate"
    AdobeCharacterAnimator = "Adobe Character Animator"
    AdobeDimension = "Adobe Dimension"
    AdobeFresco = "Adobe Fresco"
    AdobeInCopy = "Adobe InCopy"
    CyberSecurity = "Cyber Security"
    Scratch = "Scratch"
    DesignThinking = "Design Thinking"
    

    def __str__(self):
        return self.value

#the social skills enum class is used to define the social skills that can be extracted from a job description
class SocialSkills(Enum):
    Leadership = "Leadership"
    Collaboration = "Collaboration"
    Teamwork = "Teamwork"
    ConflictResolution = "Conflict Resolution"
    Networking = "Networking"
    EmotionalIntelligence = "Emotional Intelligence"
    Communication = "Communication"
    

    def __str__(self):
        return self.value

#the JobParameters class is used to define the parameters that can be extracted from a job description
@dataclass
class JobParameters:
    experience: str
    mandatory_experience_years: float
    optional_experience_years: float
    job_title: str
    job_level: str
    education_level: str
    education_field: str
    soft_skills: list[str]
    technical_skills: list[str]
    social_skills: list[str]
    location: str
    min_salary: int
    max_salary: int
    benefits: list[str]
    responsibilities: list[str]

#the JobReviewer class is used to extract and structure key job characteristics such as skills, experiences, and preferences from a job description
class JobReviewer:
    #initializes the JobReviewer class
    def __init__(self):
        #initializes the logger
        self.logging = logging.getLogger(__name__)
        #initializes the OpenAI client
        self.client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"],
        )
        #initializes the functions
        self.functions = [
            {
                "name": "job_reviewer",
                "description": "process and evaluate job postings. It extracts and structures key job characteristics such as skills, experiences, and preferences.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "experience": {
                            "type": "string",
                            "enum": ["Entry Level", "Mid Level", "Senior Level"],
                            "description": "The required professional experience level for the job, categorized into Entry Level (may have some intern level experience, but no full time experience), Mid Level (0-2 years), or Senior Level (3+ years).",
                        },
                        "mandatory_experience_years": {
                            "type": "integer",
                            "description": "The minimum, mandatory number of years of experience required for the job. This is a numeric value. For example, 3 years of experience.",
                        },
                        "optional_experience_years": {
                            "type": "integer",
                            "description": "The non-mandatory, number of years of experience required for the job. This is a numeric value. For example, 3 years of experience is a plus.",
                        },
                        "job_title": {
                            "type": "string",
                            "enum": [x.value for x in list(JobTitles)],
                            "description": "The title of the job, indicating the role and responsibilities. Product manager, may also be called Product Owner. UX-Designer may also be called User-Experience or UX/UI",
                        },
                        "job_level": {
                            "type": "string",
                            "enum": [x.value for x in list(JobLevels)],
                            "description": "The level of the job within the organization, reflecting the hierarchy and seniority.",
                        },
                        "education_level": {
                            "type": "string",
                            "enum": [
                                "High School Diploma",
                                "Bachelor's Degree",
                                "Master's Degree",
                                "MBA",
                                "Doctorate",
                            ],
                            "description": "The minimum required education level for the job candidate.",
                        },
                        "education_field": {
                            "type": "string",
                            "enum": [
                                "Computer Science",
                                "Engineering",
                                "Business Administration",
                                "Marketing",
                                "Data Science",
                                "Graphic Design",
                            ],
                            "description": "The field of study that is most relevant to the job.",
                        },
                        "soft_skills": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": [x.value for x in list(SoftSkills)],
                            },
                            "description": "Key soft skills that are beneficial for the job. do not make up. only pick ones mentioned in the job post",
                        },
                        "technical_skills": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": [x.value for x in list(TechnicalSkills)],
                            },
                            "description": "Specific technical skills required or preferred for the job. do not make up. only pick from the job post",
                        },
                        "social_skills": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": [x.value for x in list(SocialSkills)],
                            },
                            "description": "Social skills that contribute to effective teamwork and communication. do not make up. only pick from the job post",
                        },
                        "location": {
                            "type": "string",
                            "enum": ["London", "Remote", "USA", "Unknown"],
                            "description": "The location of the job, which could be a specific city or remote. if not exists, then its Unknown",
                        },
                        "min_salary": {
                            "type": "number",
                            "description": "The minimum salary offered for the job.",
                        },
                        "max_salary": {
                            "type": "number",
                            "description": "The maximum salary offered for the job.",
                        },
                        "benefits": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": [
                                    "Health Insurance",
                                    "Retirement Plans",
                                    "Flexible Work Schedule",
                                    "Professional Development Opportunities",
                                    "Gym Memberships",
                                ],
                            },
                            "description": "The benefits provided by the employer. do not make up. only pick from the job post",
                        },
                        "responsibilities": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "The main responsibilities and tasks associated with the job.do not make up. only pick from the job post",
                        },
                    },
                    "required": [
                        "experience",
                        "mandatory_experience_years",
                        "optional_experience_years",
                        "job_title",
                        "job_level",
                        "education_level",
                        "education_field",
                        "soft_skills",
                        "technical_skills",
                        "social_skills",
                        "location",
                        "salary",
                        "benefits",
                        "responsibilities",
                    ],
                },
            }
        ]
        #logs the initialization of the JobReviewer class
        self.logging.info(f"JobReviewer() initialized! functions={self.functions}")

    #extracts job parameters from a job description
    def extract_parameters(self, job_description: str) -> Optional[JobParameters]:
        """
        Uses ChatGPT to Extracts job parameters from a job description
        :param job_description: the job description
        :return: JobParameters
        """
        self.logging.info(
            f"extract_parameters() job_description={job_description[:40]}..."
        )
        # Calls the OpenAI API to extract job parameters from the job description
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": job_description}],
            functions=self.functions,
            function_call="auto",
        )
        # Loading the response as a JSON object
        try:
            json_response = json.loads(
                response.choices[0].message.function_call.arguments
            )
        except AttributeError:
            return None

        # self.logging.info(f"extract_parameters() json_response={json_response}")
        return JobParameters(
            experience=json_response.get("experience", "Unknown"),
            mandatory_experience_years=json_response.get(
                "mandatory_experience_years", 0
            ),
            optional_experience_years=json_response.get("optional_experience_years", 0),
            job_title=json_response.get("job_title", "Unknown"),
            job_level=json_response.get("job_level", "Unknown"),
            education_level=json_response.get("education_level", "Unknown"),
            education_field=json_response.get("education_field", "Unknown"),
            soft_skills=json_response.get("soft_skills", []),
            technical_skills=json_response.get("technical_skills", []),
            social_skills=json_response.get("social_skills", []),
            location=json_response.get("location", "Unknown"),
            min_salary=json_response.get("min_salary", 0),
            max_salary=json_response.get("max_salary", 0),
            benefits=json_response.get("benefits", []),
            responsibilities=json_response.get("responsibilities", []),
        )
