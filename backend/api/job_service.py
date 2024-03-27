from api.arbeitsagentur_api import ArbeitsagenturAPI
import asyncio


class JobService:
    def __init__(self) -> None:
        self.arbeitsagentur = ArbeitsagenturAPI()

    async def get_jobs_by_company_async(self, company: str) -> list:
        return await self.arbeitsagentur.get_jobs_by_company(company)
