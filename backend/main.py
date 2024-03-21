from flask import Flask, jsonify
from api.arbeitsagentur_api import ArbeitsagenturAPI
from dto import JobDTO


app = Flask(__name__)
job_service = ArbeitsagenturAPI()


@app.route("/jobs/<company>")
def get_jobs_by_company(company):
    jobs_data = job_service.get_jobs_by_company(company)
    job_dtos = [JobDTO(job) for job in jobs_data]
    return jsonify([job_dto.to_dict() for job_dto in job_dtos])


if __name__ == "__main__":
    app.run(debug=True)
