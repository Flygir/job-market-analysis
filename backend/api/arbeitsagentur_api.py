import requests, json, math


class ArbeitsagenturAPI:
    url = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs"
    auth_header = {"X-API-Key": "c003a37f-024f-462a-b36d-b001be4cd24a"}

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

    def get_jobs_by_company(self, company: str) -> list:
        entry_count = self.get_entry_count({"arbeitgeber": company})
        page = 1
        all_jobs = []

        while page <= self._calculate_total_pages(entry_count, 200):
            params = {"arbeitgeber": company, "size": 200, "page": page}

            response = requests.get(self.url, headers=self.auth_header, params=params)
            if response.status_code == 200:
                data = response.json()["stellenangebote"]
                all_jobs.extend(data)
                page += 1
            else:
                print(
                    f"Fehler beim Abrufen der Stellenangebote für Firma {company}. Status-Code:",
                    response.status_code,
                )
        return all_jobs

    def _write_job_data(self, data: str):
        with open("jobs.json", "a") as file:
            file.write(json.dumps(data, indent=4))


agentur = ArbeitsagenturAPI()

response = requests.get(agentur.url, headers=agentur.auth_header)

with open("response.json", "w") as file:
    file.write(json.dumps(response.json(), indent=4))
