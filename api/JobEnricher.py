import logging
import os

from django.http import HttpRequest, JsonResponse

from .LLM.job_reviewer import JobReviewer
from .tools.object_cache import ObjectCache

# Create your views here.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# the maximum number of jobs to enrich per category is set to 10 for testing purposes only
max_jobs_to_enrich_per_category = 10

# the job_enricher() function is used to review all the cached Jobs, extract additional data from their description, and enrich the cached data with that
def job_enricher(request: HttpRequest) -> JsonResponse:
    """
    review all the cached Jobs, extract additional data from their description, and enrich the cached data with that
    """
    user_id = request.user.id
    logger.info(
        f"job_enricher() called with Method={request.method}, user id = {user_id}"
    )

    if user_id is None:
        return JsonResponse({"error": "User not logged in"}, status=400)
    if request.method == "POST":
        # list all files in cache/*.pkl, and for each file, call CacheObject.load_from_file()
        # to retrieve the json
        cache_dir = "cache"
        cache_files = os.listdir(cache_dir)
        # Use the filter function to filter out .pkl files
        pkl_files = list(filter(lambda file: file.endswith(".pkl"), cache_files))
        # logger.info(f"job_enricher() POST, cache_files={pkl_files}")
        # concatenate the path cache_dir with the file name pkl_files[0]
        full_path = os.path.join(cache_dir, pkl_files[0])
        logger.info(
            f"job_enricher() POST, first job file={pkl_files[0]} == {ObjectCache.load_from_file(full_path)[0].keys()}"
        )

        # each file contains a list of jobs for a specific search criteria
        for search_criteria_jobs_filename in pkl_files:
            search_criteria_jobs = ObjectCache.load_from_file(
                os.path.join(cache_dir, search_criteria_jobs_filename)
            )
            # for each job in the list, call JobReviewer.extract_skills()
            job_reviewer = JobReviewer()
            for i, job in enumerate(search_criteria_jobs):
                if not (
                    "extracted_data" in job.keys() and job["extracted_data"] is not None
                ):
                    if i > max_jobs_to_enrich_per_category:
                        break
                    parameters = job_reviewer.extract_parameters(str(job))
                    search_criteria_jobs[i]["extracted_data"] = parameters
                else:
                    logger.info(
                        f"job_enricher() POST, skipping already enriched data in {search_criteria_jobs_filename}"
                    )
            # save the enriched data back to the cache
            logger.info(
                f"job_enricher() POST, saving enriched data to {search_criteria_jobs_filename}"
            )
            # save the enriched data back to the cache
            ObjectCache(df=search_criteria_jobs).save(
                to_file_name=search_criteria_jobs_filename
            )
