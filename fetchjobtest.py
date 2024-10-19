import requests
from bs4 import BeautifulSoup
import json
import time
import random
import logging

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
]

logging.basicConfig(filename='scraping_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_job_listings(job_title, location, session, retries=5):
    url = f"https://www.linkedin.com/jobs/search?keywords={requests.utils.quote(job_title)}&location={requests.utils.quote(location)}"
    jobs = []
    for i in range(retries):
        try:
            headers = {
                'User-Agent': random.choice(USER_AGENTS),
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.google.com/'
            }
            response = session.get(url, headers=headers)
            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                if retry_after:
                    wait_time = int(retry_after)
                else:
                    wait_time = (2**i + random.uniform(0, 1)) * 10  # Reduced wait time in seconds
                logging.warning(f"Rate limited. Retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)
                continue
            response.raise_for_status()
            jobs = parse_job_listings(response.content, location)
            if jobs:
                return json.dumps(jobs, indent=4)
            else:
                logging.warning("No relevant jobs found for the given location.")
                return json.dumps({'error': 'No relevant jobs found for the given location.'}, indent=4)
        except requests.exceptions.RequestException as e:
            if i == retries - 1:
                return json.dumps({'error': f"Request failed after multiple retries: {e}"}, indent=4)
            wait_time = (2**i + random.uniform(0, 1)) * 10  # Reduced wait time in seconds
            logging.error(f"Request failed. Retrying in {wait_time:.2f} seconds...")
            time.sleep(wait_time)
    return json.dumps({'error': 'Failed to retrieve job listings after multiple attempts.'}, indent=4)

def parse_job_listings(content, location):
    soup = BeautifulSoup(content, 'html.parser')
    job_listings = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
    jobs = []
    for job_listing in job_listings:
        try:
            title = job_listing.find('h3', class_='base-search-card__title')
            location_found = job_listing.find('span', class_='job-search-card__location')
            apply_link = job_listing.find('a', class_='base-card__full-link')['href']
            if title and location_found and apply_link:
                title_text = title.text.strip()
                location_text = location_found.text.strip()
                if location.lower() in location_text.lower():
                    jobs.append({
                        'title': title_text,
                        'location': location_text,
                        'apply_link': apply_link
                    })
            else:
                logging.warning(f"Missing title, location, or apply link in a job listing: {job_listing}")
        except AttributeError as e:
            logging.error(f"Parsing error: {e}")
            continue
    return jobs

if __name__ == "__main__":
    job_title = input("Enter the job title to search for: ")
    location = input("Enter the location to search in: ")
    with requests.Session() as session:
        print(get_job_listings(job_title, location, session))
