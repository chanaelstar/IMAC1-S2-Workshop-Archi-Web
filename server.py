from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import random 
import mysql.connector
myapp = Flask(__name__)

mydB = mysql.connector.connect (
    host="localhost",
    user="root",
    #password="",
    #database="test"
)

default = {"Numéro étudiant": "1", "Nom": "Dupont", "Prénom": "Jean"}

@myapp.route("/")
def accueil():
    return render_template('accueil.html')

@myapp.route("/liste_etudiants")
def affichage():
    return render_template("affichage_etud.html", 
                           etudiants=[default, default, default, default])



@myapp.route("/ajout", methods=['GET', 'POST'])
def ajout():
    num_etudiant = request.form["num_etudiant"]
    nom = request.form["nom"]
    prenom = request.form["prenom"]

    return affichage()

@myapp.route("/suppression")
def suppression():
    return affichage()