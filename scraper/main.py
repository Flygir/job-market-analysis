from scraper import GetInItScraper 

scraper = GetInItScraper()
for job in scraper.get_jobs():
    print(f"{job.company} {job.description}")
