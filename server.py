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

@myapp.route("/")
def accueil():
    return render_template('accueil.html')

@myapp.route("/liste_etudiants")
def affichage():
    return render_template("affichage_etud.html")


@myapp.route("/ajout")
def ajout():
    return affichage()

@myapp.route("/suppression")
def suppression():
    return affichage()