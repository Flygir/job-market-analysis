from collections import deque
from datetime import datetime, timedelta
from aiohttp import ClientSession, ClientResponse
import requests, json, math
import asyncio


class ArbeitsagenturAPI:

    def __init__(self):
        self.url = (
            "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs"
        )
        self.auth_header = {"X-API-Key": "c003a37f-024f-462a-b36d-b001be4cd24a"}

    def _calculate_total_pages(self, total_entries: int, size: int) -> int:
        return math.ceil(total_entries / size)

    def get_entry_count(self, param: str) -> int:
        response = requests.get(self.url, headers=self.auth_header, params=param)
        return response.json()["maxErgebnisse"]

    def get_companies(self) -> dict:
        param = {"size": 1}
        response = requests.get(self.url, headers=self.auth_header, params=param)
        return response.json()["facetten"]["arbeitgeber"]["counts"]

    def get_cities(self) -> dict:
        param = {"size": 1}
        response = requests.get(self.url, headers=self.auth_header, params=param)
        return response.json()["facetten"]["arbeitsort"]["counts"]

    def get_occupational_field(self) -> dict:
        param = {"size": 1}
        response = requests.get(self.url, headers=self.auth_header, params=param)
        return response.json()["facetten"]["berufsfeld"]["counts"]

    def get_occupation(self) -> dict:
        param = {"size": 1}
        response = requests.get(self.url, headers=self.auth_header, params=param)
        return response.json()["facetten"]["beruf"]["counts"]

    async def get_job_data(self, session: ClientSession, params):
        data = await self._async_request("GET", params)
        return data["stellenangebote"]

    async def get_jobs_by_company(self, company: str) -> list:
        entry_count = self.get_entry_count({"arbeitgeber": company})
        total_pages = self._calculate_total_pages(entry_count, 200)
        params_list = [
            {"arbeitgeber": company, "size": 200, "page": page}
            for page in range(1, total_pages + 1)
        ]

        all_jobs = []
        async with ClientSession() as session:
            tasks = [self.get_job_data(session, params) for params in params_list]
            for task in asyncio.as_completed(tasks):
                data = await task
                all_jobs.extend(data)

        return all_jobs

    async def _async_request(self, method, params=None):
        async with ClientSession() as session:
            async with session.request(
                method, self.url, params=params, headers=self.auth_header
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    print(
                        f"Fehler beim Abrufen der Stellenangebote. Status-Code: {response.status}"
                    )
                    return None

    def _write_job_data(self, data: str):
        with open("jobs.json", "a") as file:
            file.write(json.dumps(data, indent=4))


agentur = ArbeitsagenturAPI()

response = requests.get(agentur.url, headers=agentur.auth_header)

with open("response.json", "w") as file:
    file.write(json.dumps(response.json(), indent=4))
