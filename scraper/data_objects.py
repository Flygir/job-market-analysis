from sqlalchemy import ARRAY, Boolean, Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Job:
    def __init__(
        self,
        company: str,
        description: str,
        locations: list[str],
        home_office: bool,
        badges: list[str],
    ) -> None:
        self.company = company
        self.description = description
        self.locations = locations
        self.home_office = home_office
        self.badges = badges


class JobModel(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True)
    company = Column(String)
    description = Column(String)
    locations = Column(ARRAY(String))
    home_office = Column(Boolean)
    badges = Column(ARRAY(String))
