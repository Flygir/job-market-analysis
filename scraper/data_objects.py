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
