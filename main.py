import requests
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

class Job:
    def __init__(self, title, company, location, salary, qualifications, description, sentiment):
        self.title = title
        self.company = company
        self.location = location
        self.salary = salary
        self.qualifications = qualifications
        self.description = description
        self.sentiment = sentiment

    def print_job_details(self):
        print("Job Title:", self.title)
        print("Company:", self.company)
        print("Location:", self.location)
        print("Salary:", self.salary)
        print("Qualifications:")
        for qualification in self.qualifications:
            print("-", qualification)
        print("Sentiment Score:", self.sentiment)

class JobScraper:
    def __init__(self, websites, search_keywords):
        self.websites = websites
        self.search_keywords = search_keywords
        self.sia = SentimentIntensityAnalyzer()
        nltk.download('vader_lexicon')

    def scrape_jobs(self, website, keyword):
        url = f"{website}/jobs?q={keyword}"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            job_listings = soup.find_all("div", class_="job-listing")

            for job in job_listings:
                job_details = self.extract_job_details(job)
                job_obj = Job(*job_details)
                job_obj.print_job_details()

    def extract_job_details(self, job):
        job_title = job.find("h2").text.strip()
        company_name = job.find("h3").text.strip()
        location = job.find("span", class_="location").text.strip()
        salary = job.find("span", class_="salary").text.strip()

        qualifications_list = job.find("ul").find_all("li")
        qualifications = [qualification.text.strip() for qualification in qualifications_list]

        job_description = job.find("p").text.strip()

        sentiment_score = self.sia.polarity_scores(job_description)
        sentiment = sentiment_score["compound"]

        return job_title, company_name, location, salary, qualifications, job_description, sentiment

    def scrape_all_jobs(self):
        for website in self.websites:
            for keyword in self.search_keywords:
                self.scrape_jobs(website, keyword)

def main():
    # Define the websites to scrape
    websites = [
        "https://www.indeed.com",
        "https://www.linkedin.com",
        "https://www.glassdoor.com"
    ]

    # Define the job search keywords
    search_keywords = [
        "Data Scientist",
        "Software Engineer",
        "Product Manager"
    ]

    scraper = JobScraper(websites, search_keywords)
    scraper.scrape_all_jobs()

if __name__ == "__main__":
    main()