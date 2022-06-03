from flask import Flask, request, render_template
from datetime import date
from datetime import datetime
import json


app = Flask("Hello Patrick")


@app.route('/', methods=['GET', 'POST'])
def home():
    #Daten werden von datenspeicher.json in datenspeicher_list übernommen
    try:
        d = open("datenspeicher.json")
        datenspeicher_list = json.load(d)
    except FileNotFoundError:
        datenspeicher_list = []

    #Daten, welche im Formular eingegeben wurden und in JSON gespeichert sind, werden nun abgefragt.
    if request.method == 'POST':
        arbeitstag = request.form.get("date")
        dienst = request.form.get("dienst")
        notizen = request.form.get("notizen")

        if request.form.get("dienst") == "CvD1":
            anzahl_stunden = 8.4
        elif request.form.get("dienst") == "CvD2":
            anzahl_stunden = 5.5

        elif request.form.get("dienst") == "CRep":
            anzahl_stunden = 8.4

        elif request.form.get("dienst") == "Spezialdienst 1":
            anzahl_stunden = 8.4

        elif request.form.get("dienst") == "Spezialdienst 2":
            anzahl_stunden = 4.2

        elif request.form.get("dienst") == "RSOiG":
            anzahl_stunden = 8.4

        datenspeicher_list.append({"date": arbeitstag, "dienst": dienst, "notizen": notizen, "anzahlStunden": anzahl_stunden})
        with open("datenspeicher.json", "w") as datenbank_arbeitstage:
            json.dump(datenspeicher_list, datenbank_arbeitstage, indent=4, separators=(",", ":"))

        return render_template("index.html", erfolgreich="Du hast deinen Arbeitstag erfasst!")

    else:
        return render_template("index.html")


@app.route('/ueberblick', methods=['GET', 'POST'])
def ueberblick():
    gesamtstunden = 0
    stundenCvD1 = 0
    stundenCvD2 = 0
    stundenCRep = 0
    stundenSpezialdienst1 = 0
    stundenSpezialdienst2 = 0
    stundenRSOiG = 0

    try:
        d = open("datenspeicher.json")
        datenspeicher_list = json.load(d)
    except FileNotFoundError:
        datenspeicher_list = []

    for element in datenspeicher_list:
        gesamtstunden = gesamtstunden + element["anzahlStunden"]

        if element["dienst"] == "CvD1":
            stundenCvD1 = stundenCvD1 + element["anzahlStunden"]

        elif element["dienst"] == "CvD2":
            stundenCvD2 = stundenCvD2 + element["anzahlStunden"]

        elif element["dienst"] == "CRep":
            stundenCRep = stundenCRep + element["anzahlStunden"]

        elif element["dienst"] == "Spezialdienst 1":
            stundenSpezialdienst1 = stundenSpezialdienst1 + element["anzahlStunden"]

        elif element["dienst"] == "Spezialdeinst 2":
            stundenSpezialdienst2 = stundenSpezialdienst2 + element["anzahlStunden"]

        elif element["dienst"] == "RSOiG":
            stundenRSOiG = stundenRSOiG + element["anzahlStunden"]


    gesamtlohn = 28 * gesamtstunden
    lohnCvD1 = 28 * stundenCvD1
    lohnCvD2 = 28 * stundenCvD2
    lohnCRep = 28 * stundenCRep
    lohnSpezialdienst1 = 28 * stundenSpezialdienst1
    lohnSpezieldienst2 = 28 * stundenSpezialdienst2
    lohnRSOiG = 28 * stundenRSOiG


    return render_template("ueberblick.html", gesamtlohn=gesamtlohn, lohnCvD1=lohnCvD1, lohnCvD2=lohnCvD2, lohnCRep=lohnCRep, lohnSpezialdienst1=lohnSpezialdienst1, lohnSpezieldienst2=lohnSpezieldienst2, lohnRSOiG=lohnRSOiG)


@app.route('/arbeitstage', methods=['GET', 'POST'])
def arbeitstage():
    try:
        d = open("datenspeicher.json")
        datenspeicher_list = json.load(d)
    except FileNotFoundError:
        datenspeicher_list = []

    datum = datum
    notizen = notizen

    return render_template("arbeitstage.html", datum=datum, notizen=notizen)


if __name__ == "__main__":
    app.run(debug=True, port=5000)