from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import random 
import mysql.connector
import request_sql
myapp = Flask(__name__)
CORS(myapp)

pswd = "636cxp77"
database_name = "test"

### listes pour traitement globale
liste_etudiants = []
liste_talents = []
liste_etudiants_talents = []
liste_groupes = []
liste_groupes_talents = []
liste_projets = []

###### Initialisation SQL ######
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
    request_sql.add_student(pswd,database_name,request)
    return affichage()

@myapp.route("/traitement")
def traitement():
    return render_template("ajout.html")

@myapp.route("/suppression/<int:value>")
def suppression(value):
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
    return affichage()

@myapp.route("/modification_talents/<int:value>")
def modification_talents(value):
    liste_possede = []
    request_sql.students_current_talents(pswd, database_name, value, liste_possede)
    return render_template("modification_talents.html", num_etud = value, liste_talents = liste_talents, liste_possede = liste_possede)

@myapp.route("/changement_talents", methods=['POST'])
def changement_talents():
    liste_nouv_talents = []
    liste_anciens_talents = []
    request_sql.modifiy_students_talents(pswd,database_name, request, liste_nouv_talents, liste_anciens_talents)
    request_sql.init_liste_talents(pswd, database_name, liste_talents)

    print(liste_talents)
    return affichage()

@myapp.route("/liste_groupes")
def affichage_groupes():
    request_sql.get_groups_info(pswd, database_name, liste_groupes, liste_groupes_talents, liste_projets) 
    return render_template('affichage_groupe.html', liste_groupes=liste_groupes , liste_groupes_talents = liste_groupes_talents, liste_projets = liste_projets)

@myapp.route("/ajout_groupe", methods=['GET', 'POST'])
def ajout_groupe():
    request_sql.add_group(pswd, database_name, request)
    return affichage_groupes()

@myapp.route("/traitement_groupe")
def traitement_groupe():
    return render_template("ajout_groupe.html")

@myapp.route("/modification_grp/<int:id_grp>")
def modif_groupe (id_grp):
    groupe = {}
    for i in range(len(liste_groupes)):
        if liste_groupes[i]["num_groupe"] == id_grp:
            groupe = liste_groupes[i]
            break
    return render_template("modification_groupe_page.html", groupe = groupe, liste_projets = liste_projets)

@myapp.route("/changement_grp/<int:num_grp>", methods=['POST'])
def changement_grp(num_grp):
    request_sql.changement_infos_grp(pswd, database_name, num_grp, request)
    return affichage_groupes()


### API (inutilisée pour le moment)
## students & students_talents
@myapp.route("/api/v1/students", methods=['GET'])
def api_get_students():
    request_sql.get_students_info(pswd,database_name,liste_etudiants,liste_etudiants_talents)
    return jsonify({'students':liste_etudiants, 'students_talents':liste_etudiants_talents})

@myapp.route("/api/v1/students", methods=['POST'])
def api_add_students():
    if not request.json or not 'nom' in request.json  or not 'prenom' in request.json or (not 'nom' in request.json  and not 'prenom' in request.json):
        return jsonify({'error': 'Bad request'}), 400

    new_id = max(student['num_etudiant'] for student in liste_etudiants) + 1 if liste_etudiants else 1
    
    new_student = {
        'num_etudiant': new_id,
        'prenom': request.json['prenom'],
        'nom': request.json['nom'],
        'groupe': 1
    }
    liste_etudiants.append(new_student)
    return jsonify({'new_student': new_student}), 201

@myapp.route("/api/v1/students/<int:id_stud>", methods = ['GET'])
def api_get_one_student(id_stud):
    student = next((student for student in liste_etudiants if student['num_etud'] == id_stud), None)
    if student:
        return jsonify({'student': student})
    return jsonify({'error': 'Not found'}), 404

@myapp.route("/api/v1/students/<int:id_stud>", methods = ['PUT'])
def api_modify_one_student(id_stud):
    student = next((student for student in liste_etudiants if student['num_etud'] == id_stud), None)
    if not student:
        return jsonify({'error': 'Not found'}), 404
    
    student['nom'] = request.json.get('nom',student['nom'])
    student['prenom'] = request.json.get('prenom',student['prenom'])
    student['groupe'] = request.json.get('groupe',student['groupe'])

    return jsonify({'student': student})

@myapp.route("/api/v1/students/<int:id_stud>", methods = ['DELETE'])
def api_delete_one_student(id_stud):
    global liste_etudiants
    global liste_etudiants_talents
    liste_etudiants = [student for student in liste_etudiants if student['num_etud'] != id_stud]
    liste_etudiants_talents = [student_talent for student_talent in liste_etudiants_talents if student_talent["num_etudiant"] != id_stud]

    return jsonify({'result' : True})

## groups
@myapp.route("/api/v1/groups", methods = ['GET'])
def api_get_groups():
    return 0

@myapp.route("/api/v1/groups", methods = ['POST'])
def api_add_groups():
    return 0

@myapp.route("/api/v1/groups/<int:id_grp>", methods = ['GET'])
def api_get_one_group(id_grp):
    return 0

@myapp.route("/api/v1/groups/<int:id_grp>", methods = ['PUT'])
def api_modify_one_group(id_grp):
    return 0

@myapp.route("/api/v1/groups/<int:id_grp>", methods = ['DELETE'])
def api_delete_one_group(id_grp):
    return 0

## talents
@myapp.route("/api/v1/talents", methods = ['GET'])
def api_get_talents():
    return 0

@myapp.route("/api/v1/talents", methods = ['POST'])
def api_add_talents():
    return 0

@myapp.route("/api/v1/talents/<int: id_talent>", methods = ['GET'])
def api_get_one_talent(id_talent):
    return 0

@myapp.route("/api/v1/talents/<int: id_talent>", methods = ['PUT'])
def api_modify_one_talent(id_talent):
    return 0

@myapp.route("/api/v1/talents/<int: id_talent>", methods = ['DELETE'])
def api_delete_one_talent(id_talent):
    return 0

## projects
@myapp.route("/api/v1/projects", methods = ['GET'])
def api_get_projects():
    return 0

@myapp.route("/api/v1/projects", methods = ['POST'])
def api_add_projects():
    return 0

@myapp.route("/api/v1/projects/<int: id_proj>", methods = ['GET'])
def api_get_one_project(id_proj):
    return 0

@myapp.route("/api/v1/projects/<int: id_proj>", methods = ['PUT'])
def api_modify_one_project(id_proj):
    return 0

@myapp.route("/api/v1/projects/<int: id_proj>", methods = ['DELETE'])
def api_delete_one_project(id_proj):
    return 0