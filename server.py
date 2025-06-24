from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import random 
import mysql.connector
myapp = Flask(__name__)
CORS(myapp)

# mydB = mysql.connector.connect (
#      host="localhost",
#      user="root",
#      #password="",
#      #database="test"
# )

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

mycursor =mydB.cursor()

# Création des tables
mycursor.execute('''create table IF NOT EXISTS etudiants (id int primary key auto_increment, prenom varchar(50), nom varchar(50)
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
mycursor.execute('''create table IF NOT EXISTS controle(id_table int, nom_table varchar (10), implement bool default(False))
                 ''')
mydB.commit()

# Insérer les valeurs de base
mycursor.execute('''select implement from controle
                where id_table=3; ''')
isAlreadyDone = mycursor.fetchall()

if isAlreadyDone!= True:
    mycursor.execute(''' insert into controle (nom_table, implement) values
                    ('talents', False),
                    ('etudiants',False),
                    ('controle',True);''')
    mydB.commit()

mycursor.execute('''select implement from controle
                where id_table=1; ''')
isAlreadyDone = mycursor.fetchall()

if isAlreadyDone== False:
    mycursor.execute(''' insert into talents (nom) values
                    ('dev'),
                    ('musique'),
                    ('dessin'),
                    ('graphisme'),
                    ('dessin'),
                    ('3D');''')
    mydB.commit()
    mycursor.execute('''update controle set implement=True 
                    where id_table=1;''')


mycursor.execute('''select implement from controle
                where id_table=2; ''')
isAlreadyDone = mycursor.fetchall()

if isAlreadyDone== False:
    mycursor.execute(''' insert into etudiants (prenom, nom) values
                    ('Bob','leponge'),
                    ('Dora','lexploratrice'),
                    ('koro','sensei');''')
    mydB.commit()
    mycursor.execute('''update controle set implement=True 
                    where id_table=2;''')


mycursor.close()
# Fin SQL

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
        if str(liste_etudiants[i]["num_etudiant"]) == request.form["num_etud"]:
            liste_etudiants[i]["nom"] = request.form["nouv_nom"]
            liste_etudiants[i]["prenom"] = request.form["nouv_prenom"]
            break
    return affichage()