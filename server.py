from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import random 
import mysql.connector
import request_sql
myapp = Flask(__name__)
CORS(myapp)

pswd = ""
database_name = "test"

default = {"num_etudiant": 1, "nom": "Dupont", "prenom": "Jean"}
test = {"num_etudiant": 2, "nom": "Leclerc", "prenom": "Charles"}
controle = {"num_etudiant": 3, "nom": "ctrl", "prenom": "ctrl"}
liste_etudiants = [default,test,controle]

liste_talents = ["Web", "3D", "Dev", "Montage", "Musique", "Dessin"]
liste_etudiants_talents = [
    {"num_etudiant": 1, "talent": liste_talents[1]},
    {"num_etudiant": 1, "talent": liste_talents[2]},
    {"num_etudiant": 2, "talent": liste_talents[1]},
    {"num_etudiant": 3, "talent": liste_talents[3]},
]

request_sql.init_database(pswd,database_name)
###### Fin SQL ######

@myapp.route("/")
def accueil():
    return render_template('accueil.html')

@myapp.route("/liste_etudiants")
def affichage():
    return render_template('affichage_etud.html', liste_etudiants=liste_etudiants , liste_etudiants_talents = liste_etudiants_talents)


@myapp.route("/ajout", methods=['GET', 'POST'])
def ajout():
    num_etudiant = int(request.form["num_etudiant"])
    nom = request.form["nom"]
    prenom = request.form["prenom"]

    etudiant = {
        "num_etudiant": num_etudiant,
        "nom": nom,
        "prenom": prenom
    }
    liste_etudiants.append(etudiant)
    return affichage()

@myapp.route("/traitement")
def traitement():
    return render_template("ajout.html")

@myapp.route("/suppression/<int:value>")
def suppression(value):
    for i in range(len(liste_etudiants)):
        if liste_etudiants[i]["num_etudiant"] == value:
            liste_etudiants.pop(i)
            break
    return affichage()

@myapp.route("/modification/<int:value>")
def modification(value):
    etudiant = {}
    for i in range(len(liste_etudiants)):
        if liste_etudiants[i]["num_etudiant"] == value:
            etudiant = liste_etudiants[i]
            break
    return render_template("modification_page.html", etudiant = etudiant)

@myapp.route("/changement", methods=['POST'])
def changement():
    for i in range(len(liste_etudiants)):
        # if str(liste_etudiants[i]["num_etudiant"]) == request.form["num_etud"]:
            liste_etudiants[i]["nom"] = request.form["nouv_nom"]
            liste_etudiants[i]["prenom"] = request.form["nouv_prenom"]
            break
    return affichage()

@myapp.route("/modification_talents/<int:value>")
def modification_talents(value):
    liste_possede = []
    for talents in liste_etudiants_talents:
        if talents["num_etudiant"] == value:
            liste_possede.append(talents["talent"])
    return render_template("modification_talents.html", num_etud = value, liste_talents = liste_talents, liste_possede = liste_possede)

@myapp.route("/changement_talents", methods=['POST'])
def changement_talents():
    liste_nouv_talents = []
    liste_autre_talents = []
    for i in range(len(request.form.getlist("talents"))):
        liste_nouv_talents.append({"num_etudiant": int(request.form["num_etud"]), "talent": request.form.getlist("talents")[i]})
    for i in range(len(liste_etudiants_talents)):
        if str(liste_etudiants_talents[i]["num_etudiant"]) != request.form["num_etud"]:
            liste_autre_talents.append(liste_etudiants_talents[i])
    liste_etudiants_talents.clear()
    for i in range(len(liste_autre_talents)):
        liste_etudiants_talents.append(liste_autre_talents[i])
    for i in range(len(liste_nouv_talents)):
        liste_etudiants_talents.append(liste_nouv_talents[i])
    return affichage()