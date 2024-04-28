import logging
from typing import List, Optional

from .LLM.Universities import University
from .LLM.job_reviewer import (
    JobParameters,
)
from .LLM.resume_reviewer import ResumeParameters, Education

# Create your models here.
class MatchScore:
    """
    Calculates the Match Score between the Resume and Job Description
    """
    # Constructor for MatchScore class that takes in the ResumeParameters and JobParameters as input and initializes the score to 0
    def __init__(
        self, resume_parameters: ResumeParameters, job_parameters: JobParameters
    ):
        self.resume_parameters = resume_parameters
        self.job_parameters = job_parameters
        self.score = 0
        self.university_rank = University()
        self.logger = logging.getLogger(__name__)
    # Method to calculate the Education Score based on the candidate's education
    def get_education_score(self, education: Optional[List[Education]]):
        """
        Calculate the Education Score based on the candidate's education
        """
        score = 0
        if education is None:
            return 0
        self.logger.info(f"get_education_score() education: {education}")
        for edu in education:
            if type(edu) == dict:
                if "id" in edu:
                    del edu["id"]
                edu = Education(**edu)
                chars_to_remove = ["[", "]", "'"]
                for char in chars_to_remove:
                    edu.institution_name_enum = edu.institution_name_enum.replace(
                        char, ""
                    )
            if edu.institution_name_enum is not None:
                rank = self.university_rank.get_rank(edu.institution_name_enum)
                if rank is not None:
                    if rank < 50:
                        score += 10
                    elif rank < 100:
                        score += 5
                self.logger.info(
                    f"get_education_score() University: {edu.institution_name_enum}, "
                    f"rank: {rank}, "
                    f"total score: {score}"
                )
        # round the result to 2 decimal places
        return score
    # Method to calculate the Matching Score between the Resume and Job Description
    def get_matching_score(self):
        """
        Calculate the Matching Score between the Resume and Job Description
        """
        # Check if the job_parameters and resume_parameters are not None
        if self.job_parameters is None or self.resume_parameters is None:
            return 0

        # Mandatory Experience Score
        my_experience = self.resume_parameters.get_experience_duration_years()
        if self.job_parameters.mandatory_experience_years > 0:
            experience_ratio = (
                my_experience / self.job_parameters.mandatory_experience_years
            )
        elif my_experience > 0:
            experience_ratio = 1.2
        else:
            experience_ratio = 1.0

        # Cap the experience score at 1.2
        if experience_ratio > 1.2:
            experience_ratio = 1.2
        # Log the experience ratio and mandatory experience years for debugging purposes and return the total score rounded to the nearest integer
        self.logger.info(
            f"get_matching_score(EXPERIENCE) experience_ratio: {experience_ratio}, mandatory={self.job_parameters.mandatory_experience_years}, in-resume={my_experience}"
        )

        # Optional Experience Score
        optional_experience_ratio = (
            (
                self.resume_parameters.get_experience_duration_years()
                / self.job_parameters.optional_experience_years
            )
            if self.job_parameters.optional_experience_years > 0
            else 0
        )
        # Cap the optional experience score at 1.2
        if optional_experience_ratio > 1.2:
            optional_experience_ratio = 1.2
        # Add the optional experience ratio to the experience ratio and log the result for debugging purposes and return the total score rounded to the nearest integer
        experience_ratio = experience_ratio + optional_experience_ratio
        # Log the experience ratio and mandatory experience years for debugging purposes and return the total score rounded to the nearest integer
        self.logger.info(
            f"get_matching_score(EXPERIENCE) "
            f"\n\texperience duration={self.resume_parameters.get_experience_duration_years():.2f}, "
            f"\n\tmandatory experience years={self.job_parameters.mandatory_experience_years} "
            f"\n\toptional experience years={self.job_parameters.optional_experience_years} "
            f"\n\texperience_ratio={experience_ratio:.2f}, "
        )

        # Education Score
        university_prestige_score = self.get_education_score(
            self.resume_parameters.education
        )

        # Skills match
        technical_skills_match = (
            len(
                set(self.resume_parameters.technical_skills)
                & set(self.job_parameters.technical_skills)
            )
            / len(set(self.job_parameters.technical_skills))
            if len(set(self.job_parameters.technical_skills)) > 0
            else 1
        )
        # Calculate the matching score for soft skills and social skills
        soft_skills_match = (
            len(
                set(self.resume_parameters.soft_skills)
                & set(self.job_parameters.soft_skills)
            )
            / len(set(self.job_parameters.soft_skills))
            if len(set(self.job_parameters.soft_skills)) > 0
            else 1
        )
        social_skills_match = (
            len(
                set(self.resume_parameters.social_skills)
                & set(self.job_parameters.social_skills)
            )
            / len(set(self.job_parameters.social_skills))
            if len(set(self.job_parameters.social_skills)) > 0
            else 1
        )
        skills_score = (
            technical_skills_match * 1.3 + soft_skills_match * 1.1 + social_skills_match
        ) / 3  # Weighted equally, adjust as needed

        self.logger.info(
            f"get_matching_score(SKILLS) "
            f"\n\ttechnical_skills_match={technical_skills_match:.2f}, "
            f"\n\tsoft_skills_match={soft_skills_match:.2f}, "
            f"\n\tsocial_skills_match={social_skills_match:.2f}, "
            f"\n\tskills_score={skills_score:.2f}"
        )

        # Total Score Calculation and Logging the results for debugging purposes and return the total score rounded to the nearest integer rounded to the nearest integer 
        total_score = int(
            experience_ratio * 40 + university_prestige_score + skills_score * 25
        )
        # Log the results for debugging purposes and return the total score rounded to the nearest integer
        self.logger.info(
            f"\n\tget_matching_score(OVERALL) -->"
            f"\n\texperience_ratio={experience_ratio:.2f}, "
            f"\n\tuniversity_prestige_score={university_prestige_score}, "
            f"\n\tskills_score={skills_score}, "
            f"\n\t*total_score*={total_score}"
        )

        return total_score
