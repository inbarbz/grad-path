from serpapi import GoogleSearch
import os
import logging
from functional import seq
from dotenv import load_dotenv
from typing import Optional
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re


from .JobBoard import JobBoard
from .Job import Job
from api.tools.object_cache import ObjectCache

load_dotenv("../../.env")


class SerpApi(JobBoard):
    """
    Perform Google-jobs search using SerpApi
    https://serpapi.com/google-jobs-api
    """

    def __init__(self, testing: bool = False):
        self.logger = logging.getLogger(__name__)
        self.logger.info("SerpApi.__init__()")
        self.name = "serpapi"
        self.url = "https://www.google.com/search?q=jobs+near+me"
        self.logo = "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_92x30dp.png"
        self.description = "Search Jobs on Google"
        self.testing = testing
        self.max_jobs_per_search = 20

        found_env = load_dotenv("./.env")
        self.logger.info(
            f"SerpApi.__init__() current directory = {os.getcwd()}, found_env={found_env}"
        )
        super().__init__(self.name)

    def do(self, search: str, in_city: str = "London, United Kingdom") -> list[object]:
        """
        perform Google search using SerpApi
        :param search: the query to search
        :param in_city: the city to search in
        :return: Google Search results
        """
        self.logger.info(f"SerpApi.do() searching for {search}...")
        jobs = []

        # check if the data is in the cache. if so, read it from there
        cache_args = {
            "param": search,
            "in_city": in_city,
        }
        cache = ObjectCache(dict_object=cache_args)
        df = cache.load()
        if df is not None:
            self.logger.info(f"SerpApi.do() found {len(df)} jobs in the cache.")
            return df

        # https://www.google.com/search?ie=UTF-8&q=intern+jobs+in+london&oq=intern+jobs+in+london&ibp=htl;jobs&sa=X&fpstate=tldetail&fpstate=tldetail&=&hl=en
        # perform Google search using SerpApi

        self.logger.info(
            f"SerpApi.do() searching for search={search}, in_city={in_city}..."
        )

        start = 0
        while True:
            query = {
                "q": search,
                "engine": "google_jobs",
                "hl": "en",
                "location": in_city,
                "api_key": os.environ["SEP_API_KEY"],
                "safe": "active",
                "start": start,
            }
            self.logger.info(
                f"SerpApi.do() searching with offset={start} for query={query} and city={in_city}..."
            )
            google_search = GoogleSearch(query)
            self.logger.info(f"SerpApi.do() searching for query={query}...")

            result = google_search.get_dict()
            try:
                if not result["jobs_results"]:
                    break
            except Exception as e:
                self.logger.error(f"SerpApi.do() failed to get jobs_results: {e}")
                break

            try:
                google_jobs_url = result["search_metadata"]["google_jobs_url"]
            except:
                google_jobs_url = None
            for job_result in result["jobs_results"]:
                combined_info = job_result.copy()  # create a copy of the job result
                combined_info["google_jobs_url"] = (
                    google_jobs_url  # add the Google jobs URL to the new dictionary
                )
                jobs.append(combined_info)  # append the new dictionary to the jobs list
            # jobs += result["jobs_results"]
            self.logger.info(
                f"SerpApi.do() until now, found {len(jobs)} jobs. first company: {result['jobs_results'][0]['company_name']}"
            )
            start = len(jobs)
            if start > self.max_jobs_per_search:
                self.logger.info(
                    f"SerpApi.do() REACHED LIMIT of {len(jobs)} jobs BREAK!!. first company: {result['jobs_results'][0]['company_name']}"
                )
                break

        self.logger.info(f"SerpApi.do() found total of {len(jobs)} jobs.")
        if len(jobs) > 0:
            self.logger.info(f"SerpApi.do() first job {jobs[0]}.")

        # save data to the cache
        cache = ObjectCache(
            dict_object=cache_args,
            df=jobs,
        )
        self.logger.info(f"SerpApi.do() saving {len(jobs)} jobs to the cache. ")
        cache.save()

        return jobs

    def _get_post_url(self, related_links: list[dict[str, str]]) -> Optional[str]:
        if related_links is None or len(related_links) == 0:
            return None
        for u in related_links:
            link = u.get("link", None)
            if link is not None:
                if "google" in link.lower():
                    return link
        return None

    def convert_to_datetime(self, time_string):
        """
        Convert a string to a datetime object. The string can be in the format:
        "X days/weeks/months/years ago" or a date
        """
        match = re.match(r"(\d+) (day|week|month|year)s? ago", time_string)
        if match:
            amount, unit = match.groups()
            amount = int(amount)
            now = datetime.now()
            if unit.startswith("day"):
                return now - relativedelta(days=amount)
            elif unit.startswith("week"):
                return now - relativedelta(weeks=amount)
            elif unit.startswith("month"):
                return now - relativedelta(months=amount)
            elif unit.startswith("year"):
                return now - relativedelta(years=amount)
        else:
            # If the string does not match the format "X days/weeks/months/years ago",
            # try to parse it as a date.
            try:
                return datetime.strptime(time_string, "%Y-%m-%d")
            except ValueError:
                # If the string is not a date, return None.
                return None

    def get_posted_date(self, extensions: Optional[list[str]]) -> Optional[datetime]:
        if extensions is None:
            return None
        for ext in extensions:
            d = self.convert_to_datetime(ext)
            if d is not None:
                return d
        return None

    def normalize_results(self, results: list) -> list[Job]:
        """
        normalize results from SerpApi
        :param results: results from SerpApi
        :return: normalized results
        """
        # self.logger.info(
        #     f"SerpApi.normalize_results() ... results={type(results)} results[0]={type(results[0])}, {results[0]}"
        # )
        jobs = []
        if len(results) > 0:
            self.logger.info(
                f"SerpApi.normalize_results() result keys = {results[0].keys()}"
            )

        for result in results:
            job = Job(
                id=None,
                title=result.get("title", None),
                description=result.get("description", None),
                company=result.get("company_name", None),
                location=result.get("location", None),
                type=None,
                application_deadline=None,
                job_board=self.name,
                url=result.get("google_jobs_url", None),
                thumbnail=result.get("thumbnail", None),
                extracted_data=result.get("extracted_data", None),
                posted_date=self.get_posted_date(result.get("extensions", None)),
                match_score=None,
            )
            jobs.append(job)
        return jobs

    def fetch_jobs(self, in_city: str, job_description: str) -> list[Job]:
        self.logger.info(
            f"SerpApi.fetch_jobs() in_city={in_city}, job_description={job_description}..."
        )
        if in_city is None or job_description is None:
            return []
        in_city = in_city.lower()
        job_description = job_description.lower()
        results = self.do(search=job_description, in_city=in_city)
        jobs = self.normalize_results(results)
        return jobs


if __name__ == "__main__":
    from dotenv import load_dotenv
    import json

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(filename)s:%(name)s - %(levelname)s - %(message)s",
    )
    load_dotenv("../.env")
    s = SerpApi(testing=False)
    r = s.do(search="intern jobs in london", in_city="london, united kingdom")
    seq(r).for_each(
        lambda x: print(
            f"-- Company: {x['company_name']}, Title: {x['title']}, Via: {x['via']}"
        )
    )
    print("dd")
    # logging.getLogger().info(json.dumps(r, indent=2))
