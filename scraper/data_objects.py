class Job:
    def __init__(self, company, description) -> None:
        self.company = company
        self.description = description


class CategoryCheckbox:
    def __init__(self, checkbox, name) -> None:
        self.checkbox = checkbox
        self.name = name
        self.isActive = False

    def pressCheckbox(self):
        self.checkbox.click()
        self.isActive = not self.isActive
