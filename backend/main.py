from flask import Flask, jsonify
from api.job_service import JobService
from dto import JobDTO
import asyncio


app = Flask(__name__)
job_service = JobService()


@app.route("/jobs/<company>")
async def get_jobs_by_company(company):
    jobs_data = await job_service.get_jobs_by_company_async(company)
    job_dtos = [JobDTO(job) for job in jobs_data]
    return jsonify([job_dto.to_dict() for job_dto in job_dtos])


if __name__ == "__main__":
    app.run(debug=True)
