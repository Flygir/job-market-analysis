from bs4 import BeautifulSoup
import requests
from data_objects import Job


class GetInItScraper:
    
    def __init__(self) -> None:
        self.driver_path = "../chromedriver.exe"
        self.url = "https://www.get-in-it.de/jobsuche"
        self.http_content = self.scrape_jobs_html()
        self.soup = BeautifulSoup(self.http_content, "html.parser")
    
    def get_jobs(self) -> Job:
        job_search = self.soup.find("main", class_ = "jobsuche")
        job_overview = job_search.findNext("div", class_ = "row")
        job_cards = job_overview.findAll("div", class_ = "col-12 col-lg-6 col-xl-4 mb-1-5")
    
        jobs = []
        for job_card in job_cards:
            company_name = job_card.findNext("div", class_ = "my-0-5 font-size-15 font-weight-bold no-overflow text-color-default").text
            job_description = job_card.findNext("div", class_ = "CardJob_jobTitle__9UY_h").text
            jobs.append(Job(company_name, job_description))
        return jobs
    
