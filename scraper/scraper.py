from bs4 import BeautifulSoup
import requests
from data_objects import Job
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
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
        # options.add_argument("--start-fullscreen")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        driver = webdriver.Chrome(options=options)
        driver.get(self.url)

        self.declineCookies(driver)

        for job_url in self.job_urls:
            driver.get(job_url)
            # self.pressShowMore(driver)
            job_cards = self.find_job_cards(driver)

            for job_card in job_cards:
                job_card.click()
                driver.switch_to.window(driver.window_handles[-1])
                driver.current_url
                self.save_jobs(driver.page_source)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                driver.current_url

        driver.quit()

    def save_jobs(self, html: str) -> None:
        soup = BeautifulSoup(html, "html.parser")

        company_name = soup.find(
            "p",
            class_="JobHeaderRegular_companyTitle__Q1svI",
        ).text
        job_description = soup.find(
            "h1", class_="JobHeaderRegular_jobTitle__DS4V4"
        ).text
        job_location = soup.find(
            "div", class_="JobHeaderRegular_jobLocation__MFauy"
        ).text
        job_home_office = soup.find("div", class_="JobHeaderRegular_homeOffice__zVhgn")
        if not job_home_office:
            job_home_office = "kein Home-Office"
        else:
            job_home_office = job_home_office.text
        job_badges = soup.find_all("div", class_="JobHeaderRegular_jobBadge__58OzR")
        job_badges_names = []

        for job_badge in job_badges:
            job_badges_names.append(job_badge.text)

        print(
            company_name,
            "\n",
            job_description,
            "\n",
            job_location,
            "\n",
            job_home_office,
            "\n",
            job_badges_names,
        )

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

    def find_job_cards(self, webdriver: webdriver.Chrome) -> list[WebElement]:
        WebDriverWait(webdriver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div.col-12.col-lg-6.col-xl-4.mb-1-5")
            )
        )
        return webdriver.find_elements(
            By.CSS_SELECTOR, "div.col-12.col-lg-6.col-xl-4.mb-1-5"
        )

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
