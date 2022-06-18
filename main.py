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
        #Jeder Dienst wird nun mit den Anzahl Arbeitsstunden hinterlegt.
        if request.form.get("dienst") == "CvD1":
            anzahl_stunden = 8.4

        elif request.form.get("dienst") == "CvD2":
            anzahl_stunden = 5.5

        elif request.form.get("dienst") == "CRep":
            anzahl_stunden = 8.4

        elif request.form.get("dienst") == "SpezDienst 1":
            anzahl_stunden = 8.4

        elif request.form.get("dienst") == "SpezDienst 2":
            anzahl_stunden = 4.2

        elif request.form.get("dienst") == "RSOiG":
            anzahl_stunden = 8.4

        datenspeicher_list.append({"date": arbeitstag, "dienst": dienst, "notizen": notizen, "anzahlStunden": anzahl_stunden})
        with open("datenspeicher.json", "w") as datenbank_arbeitstage:
            json.dump(datenspeicher_list, datenbank_arbeitstage, indent=4, separators=(",", ":"))
    # Daten werden der Liste arbeitstage_list hinzugefügt.
    arbeitstag_list = []
    for date in datenspeicher_list:
        arbeitstag_list.append((date["date"], date["dienst"], date["notizen"]))

        return render_template("index.html", erfasst="Du hast deinen Arbeitstag erfasst!", arbeitstag_list=arbeitstag_list)
    else:
        return render_template("index.html")


@app.route('/ueberblick', methods=['GET', 'POST'])
#Damit immer von Null aus gerechent wird, wird dies für dies für die Gesamtstunden und die jeweiligen Dienste gemacht.
def ueberblick():
    gesamtstunden = 0
    stundenCvD1 = 0
    stundenCvD2 = 0
    stundenCRep = 0
    stundenSpezDienst1 = 0
    stundenSpezDienst2 = 0
    stundenRSOiG = 0

    try:
        d = open("datenspeicher.json")
        datenspeicher_list = json.load(d)
    except FileNotFoundError:
        datenspeicher_list = []
    #Die Anzahl Stunden werden aufgrund der erfassten Tage und der zu den Diensten hinterlegten Stunden berechnet.
    for element in datenspeicher_list:
        gesamtstunden = gesamtstunden + element["anzahlStunden"]

        if element["dienst"] == "CvD1":
            stundenCvD1 = stundenCvD1 + element["anzahlStunden"]

        elif element["dienst"] == "CvD2":
            stundenCvD2 = stundenCvD2 + element["anzahlStunden"]

        elif element["dienst"] == "CRep":
            stundenCRep = stundenCRep + element["anzahlStunden"]

        elif element["dienst"] == "SpezDienst 1":
            stundenSpezDienst1 = stundenSpezDienst1 + element["anzahlStunden"]

        elif element["dienst"] == "SpezDienst 2":
            stundenSpezDienst2 = stundenSpezDienst2 + element["anzahlStunden"]

        elif element["dienst"] == "RSOiG":
            stundenRSOiG = stundenRSOiG + element["anzahlStunden"]

    #Rechnungsgrundlage mit jeweiligem Stundenansatz.
    gesamtlohn = 28 * gesamtstunden
    lohnCvD1 = 28 * stundenCvD1
    lohnCvD2 = 28 * stundenCvD2
    lohnCRep = 28 * stundenCRep
    lohnSpezDienst1 = 28 * stundenSpezDienst1
    lohnSpezDienst2 = 28 * stundenSpezDienst2
    lohnRSOiG = 28 * stundenRSOiG

    #Diagramm zeigt an, wie viele Stunden bei jedem einzelnen Dienst gearbeitet wurde.
    #Quelle: https://www.delftstack.com/de/howto/plotly/plotly-bar-chart/
    balkendiagramm_lohn = px.bar(
        x=["CvD1", "CvD2", "CRep", "SpezDienst 1", "SpezDienst 2", "RSOiG"],
        y=[stundenCvD1, stundenCvD2, stundenCRep, stundenSpezDienst1, stundenSpezDienst2, stundenRSOiG],
        labels={"x": "Dienst", "y": "Arbeitsstunden"}
    )

    div_balkendiagramm_lohn = plot(balkendiagramm_lohn, output_type="div")

    return render_template("ueberblick.html", gesamtlohn=gesamtlohn, lohnCvD1=lohnCvD1, lohnCvD2=lohnCvD2, lohnCRep=lohnCRep, lohnSpezDienst1=lohnSpezDienst1, lohnSpezDienst2=lohnSpezDienst2, lohnRSOiG=lohnRSOiG, balkendiagramm_lohn=div_balkendiagramm_lohn)


@app.route('/arbeitstage', methods=['GET', 'POST'])
def arbeitstage():

    arbeitstage_liste = []

    try:
        d = open("datenspeicher.json")
        datenspeicher_list = json.load(d)
    except FileNotFoundError:
        datenspeicher_list = []
    #Elemente aus der Liste datenspeicher_list werden der Liste arbeitstage_list hinzugefügt, damit die Elemente der Liste arbeitstage_list also Übersicht augegeben werden können.
    for element in datenspeicher_list:
        arbeitstage_liste.append([element["date"], element["dienst"], element["notizen"]])

    return render_template("/arbeitstage.html", arbeitstage_liste=arbeitstage_liste)


if __name__ == "__main__":
    app.run(debug=True, port=5000)