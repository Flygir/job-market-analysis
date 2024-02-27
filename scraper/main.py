from scraper import GetInItScraper
from handler import DatabaseHandler


connection_string = "postgresql://job-analysis:1234@localhost:5432/job-analysis"
scraper = GetInItScraper(DatabaseHandler(connection_string))
scraper.scrape_jobs()
