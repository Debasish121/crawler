# Shopify Job Scraper

This project is a Python-based job scraper that collects job listings related to Shopify from multiple sources like LinkedIn, Indeed, Glassdoor, ZipRecruiter, Google Jobs etc. The scraped data is stored in a MongoDB database for further analysis and usage.


--


## Features

- Scrapes job postings from multiple job boards.
- Configurable search parameters such as location, job title, and time range.
- Captures essential job details like title, company, location, description, application link, and date posted.
- Uses MongoDB for storing job data.
- Headers included for better scraping reliability.
- Effective logging and error handling.


---


## How It Works

1. The script uses the `python-jobspy` library to scrape job data from the specified job boards.
2. Headers are included to simulate a browser request for reliable scraping.
3. Job data is cleaned and transformed before being stored in MongoDB.
4. The script ensures no duplicate entries are stored by checking existing records.


## Prerequisites

Before setting up the project, ensure the following are installed:

- **Python 3.8 or above**
- **MongoDB** (running locally or accessible remotely)
- **pip** (Python package installer)


---


## Setup Instructions

### 1. Clone the Repository

```bash
$ git clone <repository_url>
$ cd shopify-job-scraper
```

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
$ python -m venv venv
$ venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies

Install all required Python packages:

```bash
$ pip install -r requirements.txt
```

---


### 4. Configure MongoDB

1. Ensure MongoDB is running on your local machine or a remote server.
2. The project uses a MongoDB connection string:
   ```python
   mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
   ```
   Modify the connection string in the code if needed (e.g., for remote databases).

### 5. Run the Scraper

Execute the script to scrape job postings and store them in MongoDB:

```bash
$ python scraper.py
```

---


## Configuration

The scraper is highly configurable through the `CONFIG` dictionary in the script. Below are the configurable parameters:

```python
CONFIG = {
    "search_term": "Shopify",
    "location": "India",
    "results_wanted": 50, # number of job results to retrieve for each site specified in 'site_name'
    "hours_old": 72,  # Fetch jobs posted within the last 72 hours
    "site_name": ["linkedin", "indeed", "zip_recruiter", "glassdoor", "google"], # Multiple sources
    "description_format": "markdown",
    "linkedin_fetch_description": True,
}
```

You can modify these parameters to adjust search terms, location, job boards, and more.

---

## MongoDB Database Structure

The scraped data is stored in the `shopify_jobs` database within the `job_List` collection. Each job document has the following structure:

```json
{
  "title": "Shopify Developer",
  "company": "Example Corp",
  "location": "Bangalore, India",
  "description": "Job description in markdown format",
  "application_link": "https://example.com/job",
  "date_posted": "21/12/2024",
  "source": "LinkedIn",
  "scraped_at": "2024-12-21T12:34:56"
}
```

### MongoDB Dashboard Example

I have included screenshots of the MongoDB dashboard showcasing stored job data for better clarity.
![s-2](https://github.com/user-attachments/assets/5734cb37-0722-4216-9475-97bb42998176)
![s-1](https://github.com/user-attachments/assets/b44a9412-54be-4d78-abda-e50d9e8d5e0f)

---

## Logging

All activity is logged in the `crawler.log` file and displayed in the console. Logs include:

- Scraping start and completion times.
- Number of jobs scraped.
- Jobs successfully stored or skipped due to duplication.
- Warnings and errors.

---

## Error Handling

- **Network Errors**: Logs any network-related issues during scraping.
- **Invalid Data**: Handles missing or malformed data gracefully and logs warnings.
- **Duplicate Jobs**: Skips storing duplicate jobs by checking the database.

---

## Future Improvements

- Add more job boards for wider coverage.
- Integrate email notifications for new job postings.
- Implement a web-based dashboard to visualize job data.

---

Debasish Vishal
