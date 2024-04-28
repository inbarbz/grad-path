from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


@dataclass
class Job:
    id: Optional[int]
    title: str
    description: str
    company: str
    location: str
    type: Optional[str]
    posted_date: Optional[datetime]
    application_deadline: Optional[datetime]
    job_board: str
    url: str
    thumbnail: Optional[str]
    extracted_data: Optional[dict]
    match_score: Optional[float]

    def to_dict(self):
        job_dict = asdict(self)
        for key, value in job_dict.items():
            if isinstance(value, datetime):
                job_dict[key] = value.date().isoformat()
        return job_dict
