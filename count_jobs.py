import json

jobs_list = []

# Öffne und lese die JSON-Datei
with open("jobs.json") as json_file:
    data = json.load(json_file)

    # Iteriere über die Jobs in der JSON-Datei und füge die Jobtitel der Liste hinzu
    for job in data:
        if job["refnr"] in jobs_list:
            pass
        else:
            jobs_list.append(job["refnr"])

# Ausgabe der Liste mit den Jobtiteln
print(len(jobs_list))
