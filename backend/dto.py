class JobDTO:
    def __init__(self, json_data: dict):
        self.job_name = json_data.get("beruf", "")
        self.title = json_data.get("titel", "")
        self.company = json_data.get("arbeitgeber", "")
        self.refnr = json_data.get("refnr", "")
        self.location = LocationDTO(json_data.get("arbeitsort", {}))

    def to_dict(self):
        return {
            "job_name": self.job_name,
            "title": self.title,
            "company": self.company,
            "refnr": self.refnr,
            "location": self.location.to_dict(),
        }


class LocationDTO:
    def __init__(self, json_data: dict):
        self.city = json_data.get("ort", "")
        self.plz = json_data.get("plz", "")
        self.region = json_data.get("region", "")
        self.country = json_data.get("land", "")
        self.coordinates = CoordinatesDTO(json_data.get("koordinaten", {}))

    def to_dict(self):
        return {
            "city": self.city,
            "plz": self.plz,
            "region": self.region,
            "country": self.country,
            "coordinates": self.coordinates.to_dict(),
        }


class CoordinatesDTO:
    def __init__(self, json_data: dict):
        self.lat = json_data.get("lat", "")
        self.lon = json_data.get("lon", "")

    def to_dict(self):
        return {"lat": self.lat, "lon": self.lon}


data = {
    "beruf": "Betriebswirt/in (Hochschule)",
    "titel": "Praktikum im Bereich Product Lifecycle Management",
    "refnr": "15986-1208883-1-S",
    "arbeitsort": {
        "plz": "74232",
        "ort": "Abstatt",
        "region": "Baden-W\u00fcrttemberg",
        "land": "Deutschland",
        "koordinaten": {"lat": 49.0719876, "lon": 9.2987459},
    },
    "arbeitgeber": "Robert Bosch GmbH",
    "aktuelleVeroeffentlichungsdatum": "2024-03-21",
    "modifikationsTimestamp": "2024-03-21T14:16:47.374",
    "eintrittsdatum": "2024-03-22",
    "kundennummerHash": "iZ1qVUSwSUBsMgarpsprvZYrvnsj_BfNcQt_jaCgINA=",
}
