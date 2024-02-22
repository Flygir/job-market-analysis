from bs4 import BeautifulSoup
import requests
from data_objects import Job
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class GetInItScraper:

    def __init__(self) -> None:
        self.driver_path: str = "../chromedriver.exe"
        self.url: str = "https://www.get-in-it.de/jobsuche"
        self.job_urls: list[str] = [
            "https://www.get-in-it.de/jobsuche?thematicPriority=36",
            "https://www.get-in-it.de/jobsuche?thematicPriority=38",
            "https://www.get-in-it.de/jobsuche?thematicPriority=37",
            "https://www.get-in-it.de/jobsuche?thematicPriority=39",
            "https://www.get-in-it.de/jobsuche?thematicPriority=45",
            "https://www.get-in-it.de/jobsuche?thematicPriority=44",
            "https://www.get-in-it.de/jobsuche?thematicPriority=51",
            "https://www.get-in-it.de/jobsuche?thematicPriority=41",
            "https://www.get-in-it.de/jobsuche?thematicPriority=3",
            "https://www.get-in-it.de/jobsuche?thematicPriority=24",
            "https://www.get-in-it.de/jobsuche?thematicPriority=40",
            "https://www.get-in-it.de/jobsuche?thematicPriority=35",
            "https://www.get-in-it.de/jobsuche?thematicPriority=47",
            "https://www.get-in-it.de/jobsuche?thematicPriority=5",
        ]
        self.jobs: list[Job] = []

    def scrape_jobs(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-fullscreen")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        driver = webdriver.Chrome(options=options)
        driver.get(self.url)

        self.declineCookies(driver)

        for job_url in self.job_urls:
            driver.get(job_url)
            self.pressShowMore(driver)
            self.save_jobs(driver.page_source)

        driver.quit()

    def save_jobs(self, html: str) -> None:
        soup = BeautifulSoup(html, "html.parser")
        job_search = soup.find("main", class_="jobsuche")
        job_overview = job_search.findNext("div", class_="row")
        job_cards = job_overview.findAll(
            "div", class_="col-12 col-lg-6 col-xl-4 mb-1-5"
        )

        for job_card in job_cards:
            company_name = job_card.findNext(
                "div",
                class_="my-0-5 font-size-15 font-weight-bold no-overflow text-color-default",
            ).text
            job_description = job_card.findNext(
                "div", class_="CardJob_jobTitle__9UY_h"
            ).text
            self.jobs.append(Job(company_name, job_description))

    def declineCookies(self, webdriver: webdriver.Chrome) -> None:
        try:
            reject_cookies_button = WebDriverWait(webdriver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@data-cy='cookieRejectOptional']")
                )
            )

            reject_cookies_button.click()
        except (NoSuchElementException, TimeoutException):
            print("Cookie-Popup oder Ablehnungsbutton nicht gefunden.")

    def pressShowMore(self, webdriver: webdriver.Chrome) -> None:
        while True:
            try:
                mehr_anzeigen_button = WebDriverWait(webdriver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//button[@data-cy='showMore']")
                    )
                )
                mehr_anzeigen_button.click()
            except NoSuchElementException:
                print("Button nicht gefunden.")
                break
            except TimeoutException:
                print("Timeout beim Warten auf den Button.")
                break
