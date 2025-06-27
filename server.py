from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import random 
import mysql.connector
import request_sql
import utils
myapp = Flask(__name__)
CORS(myapp)

config_database ={
    'host': 'localhost',
    'user': 'root',
    'password': '$W1shm3str$',
    'database': 'test'
}

### listes pour traitement globale
liste_etudiants = []
liste_talents = []
liste_etudiants_talents = []
liste_groupes = []
liste_groupes_talents = []
liste_projets = []

###### Initialisation SQL ######
request_sql.init_database(config_database)
request_sql.init_liste_talents(config_database, liste_talents)
###### Fin SQL ######

@myapp.route("/")
def accueil():
    return render_template('accueil.html')

@myapp.route("/liste_etudiants")
def affichage():
    request_sql.get_students_info(config_database, liste_etudiants,liste_etudiants_talents)
    return render_template('affichage_etud.html', liste_etudiants=liste_etudiants , liste_etudiants_talents = liste_etudiants_talents)


@myapp.route("/ajout", methods=['GET', 'POST'])
def ajout():
    request_sql.add_student(config_database,request)
    return affichage()

@myapp.route("/traitement")
def traitement():
    return render_template("ajout.html")

@myapp.route("/suppression/<int:value>")
def suppression(value):
    request_sql.suppression(config_database, value)
    return affichage()

@myapp.route("/modification/<int:value>")
def modification(value):
    etudiant = utils.selection_etudiant(liste_etudiants,value)    
    return render_template("modification_page.html", etudiant = etudiant, liste_etudiants_talents = liste_etudiants_talents)

@myapp.route("/changement/<int:num_etud>", methods=['POST'])
def changement(num_etud):
    request_sql.changement_infos_etud(config_database, num_etud, request)
    return affichage()

@myapp.route("/modification_talents/<int:value>")
def modification_talents(value):
    liste_possede = []
    request_sql.students_current_talents(config_database, value, liste_possede)
    return render_template("modification_talents.html", num_etud = value, liste_talents = liste_talents, liste_possede = liste_possede)

@myapp.route("/changement_talents/<int:value>", methods=['POST'])
def changement_talents(value):
    liste_nouv_talents = []
    liste_anciens_talents = []
    request_sql.modifiy_students_talents(config_database, request, liste_nouv_talents, liste_anciens_talents, value)
    request_sql.init_liste_talents(config_database, liste_talents)

    print(liste_talents)
    return affichage()

@myapp.route("/liste_groupes")
def affichage_groupes():
    request_sql.get_groups_info(config_database, liste_groupes, liste_groupes_talents, liste_projets) 
    return render_template('affichage_groupe.html', liste_groupes=liste_groupes , liste_groupes_talents = liste_groupes_talents, liste_projets = liste_projets)

@myapp.route("/ajout_groupe", methods=['GET', 'POST'])
def ajout_groupe():
    request_sql.add_group(config_database, request)
    return affichage_groupes()

@myapp.route("/traitement_groupe")
def traitement_groupe():
    return render_template("ajout_groupe.html")

@myapp.route("/modification_grp/<int:id_grp>")
def modif_groupe (id_grp):
    groupe = utils.selection_groupe(liste_groupes,id_grp)   
    request_sql.get_students_info(config_database, liste_etudiants, liste_etudiants_talents)

    return render_template("modification_groupe_page.html", groupe = groupe, liste_projets = liste_projets, liste_etudiants=liste_etudiants)

@myapp.route("/changement_grp/<int:num_grp>", methods=['POST'])
def changement_grp(num_grp):
    liste_nouv_membres = []
    liste_anciens_membres = []
    request_sql.changement_infos_grp(config_database, num_grp, request,liste_nouv_membres, liste_anciens_membres)
    return affichage_groupes()

@myapp.route("/suppression_grp/<int:num_grp>")
def suppr_grp(num_grp):
    request_sql.suppression_groupe(config_database, num_grp, request)
    return affichage_groupes()


### API (inutilisée pour le moment)
## students & students_talents
@myapp.route("/api/v1/students", methods=['GET'])
def api_get_students():
    request_sql.get_students_info(config_database,liste_etudiants,liste_etudiants_talents)
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
    request_sql.get_groups_info(config_database, liste_groupes, liste_groupes_talents, liste_projets)
    return jsonify({'groups': liste_groupes, 'groups_talents': liste_groupes_talents})

@myapp.route("/api/v1/groups", methods = ['POST'])
def api_add_groups():
    if not request.json or not 'nom' in request.json:
        return jsonify({'error': 'Bad request'}), 400
    
    new_id = max((grp['num_groupe'] for grp in liste_groupes), default=0) + 1
    new_groupe = {
        'num_groupe': new_id,
        'nom': request.json['nom'],
        'nb_membres': 0
    }
    liste_groupes.append(new_groupe)
    return jsonify({'new_groupe': new_groupe}), 201

@myapp.route("/api/v1/groups/<int:id_grp>", methods = ['GET'])
def api_get_one_group(id_grp):
    groupe = next((grp for grp in liste_groupes if grp['num_groupe'] == id_grp), None)
    if groupe:
        return jsonify({'groupe': groupe})
    return jsonify({'error': 'Not found'}), 404

@myapp.route("/api/v1/groups/<int:id_grp>", methods = ['PUT'])
def api_modify_one_group(id_grp):
    groupe = next((grp for grp in liste_groupes if grp['num_groupe'] == id_grp), None)
    if not groupe:
        return jsonify({'error': 'Not found'}), 404
    
    groupe['nom'] = request.json.get('nom', groupe['nom'])
    return jsonify({'groupe': groupe})

@myapp.route("/api/v1/groups/<int:id_grp>", methods = ['DELETE'])
def api_delete_one_group(id_grp):
    global liste_groupes
    liste_groupes = [grp for grp in liste_groupes if grp['num_groupe'] != id_grp]
    return jsonify({'result': True})

## talents
@myapp.route("/api/v1/talents", methods = ['GET'])
def api_get_talents():
    request_sql.init_liste_talents(config_database, liste_talents)
    return jsonify({'talents': liste_talents})

@myapp.route("/api/v1/talents", methods = ['POST'])
def api_add_talents():
    if not request.json or not 'nom' in request.json:
        return jsonify({'error': 'Bad request'}), 400
    
    new_id = max(talent['id_tal'] for talent in liste_talents) + 1 if liste_talents else 1
    new_talent = {
        'id_tal': new_id,
        'nom': request.json['nom'],
    }
    liste_talents.append(new_talent)
    return jsonify({'new_talent': new_talent}), 201

@myapp.route("/api/v1/talents/<int:id_talent>", methods = ['GET'])
def api_get_one_talent(id_talent):
    talent = next((talent for talent in liste_talents if talent['id_tal'] == id_talent), None)
    if talent:
        return jsonify({'talent': talent})
    return jsonify({'error': 'Not found'}), 404

@myapp.route("/api/v1/talents/<int:id_talent>", methods = ['PUT'])
def api_modify_one_talent(id_talent):
    talent = next((talent for talent in liste_talents if talent['id_tal'] == id_talent), None)
    if not talent:
        return jsonify({'error': 'Not found'}), 404
    
    talent['nom'] = request.json.get('nom', talent['nom'])
    return jsonify({'talent': talent})

@myapp.route("/api/v1/talents/<int:id_talent>", methods = ['DELETE'])
def api_delete_one_talent(id_talent):
    global liste_talents
    liste_talents = [talent for talent in liste_talents if talent['id_talent'] != id_talent]
    return jsonify({'result': True})


## projects
@myapp.route("/api/v1/projects", methods = ['GET'])
def api_get_projects():
    request_sql.get_groups_info(config_database, liste_groupes, liste_groupes_talents, liste_projets)
    return jsonify({'projects': liste_projets})

@myapp.route("/api/v1/projects", methods = ['POST'])
def api_add_projects():
    if not request.json or not 'nom' in request.json:
        return jsonify({'error': 'Bad request'}), 400
    
    new_id = max((proj['id_prj'] for proj in liste_projets), default=0) + 1
    new_project = {
        'id_prj': new_id,
        'nom': request.json['nom'],
    }
    liste_projets.append(new_project)
    return jsonify({'new_project': new_project}), 201

@myapp.route("/api/v1/projects/<int:id_proj>", methods = ['GET'])
def api_get_one_project(id_proj):
    projet = next((projet for projet in liste_projets if projet['id_prj'] == id_proj), None)
    if projet:
        return jsonify({'projet': projet})
    return jsonify({'error': 'Not found'}), 404

@myapp.route("/api/v1/projects/<int:id_proj>", methods = ['PUT'])
def api_modify_one_project(id_proj):
    projet = next((projet for projet in liste_projets if projet['id_prj'] == id_proj), None)
    if not projet:
        return jsonify({'error': 'Not found'}), 404
    
    projet['nom'] = request.json.get('nom', projet['nom'])
    return jsonify({'projet': projet})

@myapp.route("/api/v1/projects/<int:id_proj>", methods = ['DELETE'])
def api_delete_one_project(id_proj):
    global liste_projets
    liste_projets = [projet for projet in liste_projets if projet['id_proj'] != id_proj]
    return jsonify({'result': True})
