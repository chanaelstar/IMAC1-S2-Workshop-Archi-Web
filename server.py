from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import random 
import mysql.connector
import request_sql
myapp = Flask(__name__)
CORS(myapp)

pswd = "636cxp77"
database_name = "test"

# default = {"num_etudiant": 1, "nom": "Dupont", "prenom": "Jean"}
# test = {"num_etudiant": 2, "nom": "Leclerc", "prenom": "Charles"}
# controle = {"num_etudiant": 3, "nom": "ctrl", "prenom": "ctrl"}
liste_etudiants = []

liste_talents = []
""" liste_etudiants_talents = [
    {"num_etudiant": 1, "talent": liste_talents[1]},
    {"num_etudiant": 1, "talent": liste_talents[2]},
    {"num_etudiant": 2, "talent": liste_talents[1]},
    {"num_etudiant": 3, "talent": liste_talents[3]},
] """

liste_etudiants_talents = []

request_sql.init_database(pswd,database_name)
request_sql.init_liste_talents(pswd, database_name, liste_talents)
###### Fin SQL ######

@myapp.route("/")
def accueil():
    return render_template('accueil.html')

@myapp.route("/liste_etudiants")
def affichage():
    request_sql.get_students_info(pswd, database_name, liste_etudiants,liste_etudiants_talents)
    return render_template('affichage_etud.html', liste_etudiants=liste_etudiants , liste_etudiants_talents = liste_etudiants_talents)


@myapp.route("/ajout", methods=['GET', 'POST'])
def ajout():
    """ num_etudiant = int(request.form["num_etudiant"])
    nom = request.form["nom"]
    prenom = request.form["prenom"]

    etudiant = {
        "num_etudiant": num_etudiant,
        "nom": nom,
        "prenom": prenom
    }
    liste_etudiants.append(etudiant) """
    request_sql.add_student(pswd,database_name,request)
    return affichage()

@myapp.route("/traitement")
def traitement():
    return render_template("ajout.html")

@myapp.route("/suppression/<int:value>")
def suppression(value):
    # for i in range(len(liste_etudiants)):
    #     if liste_etudiants[i]["num_etudiant"] == value:
    #         liste_etudiants.pop(i)
    #         break
    request_sql.suppression(pswd, database_name, value)
    return affichage()

@myapp.route("/modification/<int:value>")
def modification(value):
    etudiant = {}
    for i in range(len(liste_etudiants)):
        if liste_etudiants[i]["num_etudiant"] == value:
            etudiant = liste_etudiants[i]
            break
    return render_template("modification_page.html", etudiant = etudiant, liste_etudiants_talents = liste_etudiants_talents)

@myapp.route("/changement/<int:num_etud>", methods=['POST'])
def changement(num_etud):

    request_sql.changement_infos_etud(pswd, database_name, num_etud, request)
    # for i in range(len(liste_etudiants)):
    #     if liste_etudiants[i]["num_etudiant"] == num_etud:
    #         liste_etudiants[i]["nom"] = request.form["nouv_nom"]
    #         liste_etudiants[i]["prenom"] = request.form["nouv_prenom"]
    #         break

    return affichage()

@myapp.route("/modification_talents/<int:value>")
def modification_talents(value):
    liste_possede = []
    """ for talents in liste_etudiants_talents:
        if talents["num_etudiant"] == value:
            liste_possede.append(talents["talent"]) """
    request_sql.students_current_talents(pswd, database_name, value, liste_possede)
    return render_template("modification_talents.html", num_etud = value, liste_talents = liste_talents, liste_possede = liste_possede)

@myapp.route("/changement_talents", methods=['POST'])
def changement_talents():
    liste_nouv_talents = []
    liste_anciens_talents = []
    """ for i in range(len(request.form.getlist("talents"))):
        liste_nouv_talents.append({"num_etudiant": int(request.form["num_etud"]), "talent": request.form.getlist("talents")[i]})
    for i in range(len(liste_etudiants_talents)):
        if str(liste_etudiants_talents[i]["num_etudiant"]) != request.form["num_etud"]:
            liste_anciens_talents.append(liste_etudiants_talents[i])
    liste_etudiants_talents.clear()
    for i in range(len(liste_anciens_talents)):
        liste_etudiants_talents.append(liste_anciens_talents[i])
    for i in range(len(liste_nouv_talents)):
        liste_etudiants_talents.append(liste_nouv_talents[i]) """
    request_sql.modifiy_students_talents(pswd,database_name, request, liste_nouv_talents, liste_anciens_talents)
    return affichage()