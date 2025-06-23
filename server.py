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

mycursor =mydB.cursor()

# Création des tables
mycursor.execute('''create table IF NOT EXISTS etudiants (id int primary key auto_increment, nom varchar(50)
                 )''')
mydB.commit()
mycursor.execute('''create table IF NOT EXISTS talents (id int primary key auto_increment, nom varchar(50)
                 )''')
mydB.commit()
mycursor.execute('''create table IF NOT EXISTS groupes (id int primary key auto_increment, id_membre int(10)
                 )''')
mydB.commit()
mycursor.execute('''create table IF NOT EXISTS projets (id int primary key auto_increment, nom varchar(50), id_groupe int(10)
                 )''')
mydB.commit()
mycursor.execute('''create table IF NOT EXISTS possede (id_etud int, id_talent int , primary key(id_etud, id_talent)
                 )''')
mydB.commit()
mycursor.execute('''create table IF NOT EXISTS forme (id_etud int, id_groupe int , primary key(id_etud, id_groupe)
                 )''')
mydB.commit()

# Insérer les valeurs de base
mycursor.execute(''' insert into talents values
                 ('dev'),
                 ('musique'),
                 ('dessin'),
                 ('graphisme'),
                 ('dessin'),
                 ('3D')''')
mydB.commit()

mycursor.execute(''' insert into etudiants values
                 ('Bob leponge'),
                 ('Dora lexploratrice'),
                 ('koro-sensei')''')
mydB.commit()


mycursor.close()
# Fin SQL


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