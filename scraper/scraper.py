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
        self.driver_path = "../chromedriver.exe"
        self.url = "https://www.get-in-it.de/jobsuche"
        self.http_content = self.scrape_jobs_html()
        self.soup = BeautifulSoup(self.http_content, "html.parser")

    def get_jobs(self) -> Job:
        job_search = self.soup.find("main", class_="jobsuche")
        job_overview = job_search.findNext("div", class_="row")
        job_cards = job_overview.findAll(
            "div", class_="col-12 col-lg-6 col-xl-4 mb-1-5"
        )

        jobs = []
        for job_card in job_cards:
            company_name = job_card.findNext(
                "div",
                class_="my-0-5 font-size-15 font-weight-bold no-overflow text-color-default",
            ).text
            job_description = job_card.findNext(
                "div", class_="CardJob_jobTitle__9UY_h"
            ).text
            jobs.append(Job(company_name, job_description))
        return jobs

    def scrape_jobs_html(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        driver = webdriver.Chrome(options=options)

        driver.get(self.url)

        self.declineCookies(driver)
        self.pressShowMore(driver)

        html_content = driver.page_source

        driver.quit()

        return html_content

    def declineCookies(self, webdriver):
        try:

            reject_cookies_button = WebDriverWait(webdriver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@data-cy='cookieRejectOptional']")
                )
            )

            reject_cookies_button.click()
        except (NoSuchElementException, TimeoutException):
            print("Cookie-Popup oder Ablehnungsbutton nicht gefunden.")

    def pressShowMore(self, webdriver):
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
