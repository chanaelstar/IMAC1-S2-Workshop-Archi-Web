from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import random 
import mysql.connector
myapp = Flask(__name__)
CORS(myapp)

mydB = mysql.connector.connect (
     host="localhost",
     user="root",
     #password="",
     #database="test"
)

default = {"num_etudiant": 1, "nom": "Dupont", "prenom": "Jean"}
test = {"num_etudiant": 2, "nom": "Leclerc", "prenom": "Charles"}
liste_etudiants = [default,test]

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
mycursor.execute('''create table IF NOT EXISTS controle(id_table int, nom_table varchar (10), implement bool default(0))
                 )''')
mydB.commit()

# Insérer les valeurs de base
mycursor.execute('''select implement from controle;
                where nom_table='etudiants'; ''')
isAlreadyDone = mycursor.fetchall()

if isAlreadyDone!= True:
    mycursor.execute(''' insert into controle values
                    ('talents','False'),
                    ('etudiants','False'),
                    ('controle','True'),''')
    mydB.commit()
    mycursor.execute('''update controle set implement=True 
                    where nom_table='etudiants';''')

mycursor.execute('''select implement from controle;
                where nom_table='talents'; ''')
isAlreadyDone = mycursor.fetchall()

if isAlreadyDone== False:
    mycursor.execute(''' insert into talents values
                    ('dev'),
                    ('musique'),
                    ('dessin'),
                    ('graphisme'),
                    ('dessin'),
                    ('3D')''')
    mydB.commit()
    mycursor.execute('''update controle set implement=True 
                    where nom_table='talents';''')


mycursor.execute('''select implement from controle;
                where nom_table='etudiants'; ''')
isAlreadyDone = mycursor.fetchall()

if isAlreadyDone== False:
    mycursor.execute(''' insert into etudiants values
                    ('Bob leponge'),
                    ('Dora lexploratrice'),
                    ('koro-sensei')''')
    mydB.commit()
    mycursor.execute('''update controle set implement=True 
                    where nom_table='etudiants';''')


mycursor.close()
# Fin SQL

@myapp.route("/")
def accueil():
    return render_template('accueil.html')

@myapp.route("/liste_etudiants")
def affichage():
    return render_template('affichage_etud.html', liste_etudiants=liste_etudiants)


@myapp.route("/ajout", methods=['GET', 'POST'])
def ajout():
    num_etudiant = request.form["num_etudiant"]
    nom = request.form["nom"]
    prenom = request.form["prenom"]

    return affichage()

@myapp.route("/suppression/<int:value>")
def suppression(value):
    for i in range(len(liste_etudiants)):
        if (liste_etudiants[i]["num_etudiant"] == value):
            liste_etudiants.pop(i)
            break
    return affichage()

