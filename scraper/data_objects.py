class Job:
    def __init__(
        self,
        company: str,
        description: str,
        location: list[str],
        home_office: bool,
        badges: list[str],
    ) -> None:
        self.company = company
        self.description = description
        self.location = location
        self.home_office = home_office
        self.badges = badges
