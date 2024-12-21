import logging
from jobspy import scrape_jobs
import pymongo
from datetime import datetime, date

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("crawler.log"), logging.StreamHandler()]
)

# MongoDB setup
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["shopify_jobs"]
collection = db["job_List"]

# Headers for the request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
}

# Configurable parameters
CONFIG = {
    "search_term": "Shopify",
    "location": "India",
    "results_wanted": 50, # number of job results to retrieve for each site specified in 'site_name'
    "hours_old": 72,  # Fetch jobs posted within the last 72 hours
    "site_name": ["linkedin", "indeed", "zip_recruiter", "glassdoor", "google"], # Multiple sources
    "description_format": "markdown",
    "linkedin_fetch_description": True,
}

# Function to scrape jobs using python-jobspy
def scrape_and_store_jobs():
    try:
        logging.info(f"Starting job scraping...")

        # Scrape jobs using jobspy
        jobs = scrape_jobs(
            site_name=CONFIG["site_name"],
            search_term=CONFIG["search_term"],
            location=CONFIG["location"],
            results_wanted=CONFIG["results_wanted"],
            hours_old=CONFIG["hours_old"],
            description_format=CONFIG["description_format"],
            linkedin_fetch_description=CONFIG["linkedin_fetch_description"],
            headers=HEADERS,
        )

        logging.info(f"Found {len(jobs)} jobs")

        # Store filtered jobs in MongoDB
        for job in jobs.to_dict(orient="records"):
            # Handle missing or null date_posted
            if "date_posted" in job:
                if isinstance(job["date_posted"], date):
                    filtered_date_posted = job["date_posted"].strftime("%d/%m/%Y")
                else:
                    # Handle missing or invalid date format
                    filtered_date_posted = "Unknown"
                    logging.warning(f"Missing or invalid date for job: {job['title']} at {job['company']}")
            else:
                filtered_date_posted = "Unknown"
                logging.warning(f"Missing date_posted field for job: {job['title']} at {job['company']}")

            # Filtered job dictionary
            filtered_job = {
                "title": job.get("title"),
                "company": job.get("company"),
                "location": job.get("location"),
                "description": job.get("description"),
                "application_link": job.get("job_url"),
                "date_posted": filtered_date_posted,
                "source": job.get("site")
            }

            if not collection.find_one({"title": filtered_job["title"], "company": filtered_job["company"], "location": filtered_job["location"]}):
                filtered_job["scraped_at"] = datetime.now()
                collection.insert_one(filtered_job)
                logging.info(f"Stored job: {filtered_job['title']} at {filtered_job['company']}")
            else:
                logging.info(f"Duplicate job skipped: {filtered_job['title']} at {filtered_job['company']}")

        logging.info(f"Total jobs stored: {collection.count_documents({})}")

    except Exception as e:
        logging.error(f"Error during job scraping or storing: {e}")

if __name__ == "__main__":
    scrape_and_store_jobs()