from flask import Flask, request, render_template
import plotly.express as px
from plotly.offline import plot
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

    arbeitstag_list = []
    for date in datenspeicher_list:
        arbeitstag_list.append((date["date"], date["dienst"], date["notizen"]))

        arbeitstag_list = sorted(arbeitstag_list, key=lambda x: x[0], reverse=True)
        arbeitstag_list = arbeitstag_list[:3]

        return render_template("index.html", erfasst="Du hast deinen Arbeitstag erfasst!", arbeitstag_list=arbeitstag_list)

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
    lohnSpezialdienst2 = 28 * stundenSpezialdienst2
    lohnRSOiG = 28 * stundenRSOiG


    balkendiagramm_lohn = px.bar(
        x=["CvD1", "CvD2", "CRep", "Spezialdienst 1", "Spezialdienst 2", "RSOiG"],
        y=[stundenCvD1, stundenCvD2, stundenCRep, stundenSpezialdienst1, stundenSpezialdienst2, stundenRSOiG],
        labels={"x": "Dienst", "y": "Arbeitsstunden"}
    )

    div_balkendiagramm_lohn = plot(balkendiagramm_lohn, output_type="div")

    return render_template("ueberblick.html", gesamtlohn=gesamtlohn, lohnCvD1=lohnCvD1, lohnCvD2=lohnCvD2, lohnCRep=lohnCRep, lohnSpezialdienst1=lohnSpezialdienst1, lohnSpezialdienst2=lohnSpezialdienst2, lohnRSOiG=lohnRSOiG, balkendiagramm_lohn=div_balkendiagramm_lohn)


@app.route('/arbeitstage', methods=['GET', 'POST'])
def arbeitstage():

    arbeitstage_liste = []

    try:
        d = open("datenspeicher.json")
        datenspeicher_list = json.load(d)
    except FileNotFoundError:
        datenspeicher_list = []

    for element in datenspeicher_list:
        arbeitstage_liste.append([element["date"], element["dienst"], element["notizen"]])


    return render_template("/arbeitstage.html", arbeitstage_liste=arbeitstage_liste)


if __name__ == "__main__":
    app.run(debug=True, port=5000)