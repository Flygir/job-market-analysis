from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from data_objects import Job, JobModel

Base = declarative_base()


class DatabaseHandler:
    def __init__(self, connection_string: str) -> None:
        self.engine = create_engine(connection_string)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_job(self, job: Job) -> None:
        session = self.Session()
        job_data = JobModel(
            company=job.company,
            description=job.description,
            locations=job.locations,
            home_office=job.home_office,
            badges=job.badges,
        )
        session.add(job_data)
        session.commit()
        session.close()
