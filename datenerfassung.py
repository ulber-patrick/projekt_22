import json

arbeitstage_dict = {
    "Arbeitstag": ["date"],
    "Dienst": ["dienst"],
    "Notizen": ["notizen"],
}

print(arbeitstage_dict)


with open("datenspeicher.json", "w") as datenbank_arbeitstage:
    json.dump(arbeitstage_dict, datenbank_arbeitstage, indent=4, separators=(",", ":"))