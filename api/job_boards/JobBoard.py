from .Job import Job
from abc import ABC, abstractmethod
import dataclasses


@dataclasses.dataclass
class JobBoard(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def fetch_jobs(self, in_city: str, job_description: str) -> list[Job]:
        pass

    def get_name(self) -> str:
        return self.name

    def __str__(self):
        return f"<JobBoard {self.name}>"
