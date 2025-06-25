import mysql.connector

def init_database(pswd, database_name):
    mydB = mysql.connector.connect (
     host="localhost",
     user="root",
     password = pswd,
     database= database_name
    )

    mycursor =mydB.cursor()

    # Création des tables
    mycursor.execute('''create table IF NOT EXISTS talent (id_tal int primary key auto_increment, nom varchar(50)
                    )''')
    mydB.commit()
    mycursor.execute('''create table IF NOT EXISTS groupe (id_grp int primary key auto_increment, nom varchar(50), nb_membres int
                    )''')
    mydB.commit()
    mycursor.execute('''create table IF NOT EXISTS etudiant (id_num int primary key auto_increment, prenom varchar(50), nom varchar(50), id_groupe int (10),
                    foreign key(id_groupe) references groupe(id_grp)
                    )''')
    mycursor.execute('''create table IF NOT EXISTS projet (id_prj int primary key auto_increment, nom varchar(50), id_groupe int(10),
                    foreign key(id_groupe) references groupe (id_grp)
                    )''')
    mydB.commit()
    mycursor.execute('''create table IF NOT EXISTS possede (id_etud int, id_talent int, primary key(id_etud, id_talent),
                    foreign key(id_etud) references etudiant(id_num), foreign key(id_talent) references talent(id_tal)
                    )''')
    mydB.commit()
    mycursor.execute('''create table IF NOT EXISTS controle(id_table int primary key auto_increment, nom_table varchar (10), implement bool default(False))
                    ''')
    mydB.commit()

    ### Insérer les valeurs de base ###
    # CONTROLE
    mycursor.execute('''select implement from controle
                    where id_table=3; ''')
    isAlreadyDone = mycursor.fetchone()
    if isAlreadyDone is None :
        isAlreadyDone = False
    if not isAlreadyDone :
        mycursor.execute(''' insert into controle (nom_table, implement) values
                        ('talent',False),
                        ('etudiant',False),
                        ('controle',True),
                        ('groupe',False),
                        ('possede',False),
                        ('projet', False);''')
        mydB.commit()

    # TALENT
    mycursor.execute('''select implement from controle
                    where id_table=1; ''')
    isAlreadyDone = mycursor.fetchone()[0]
    if not isAlreadyDone:
        mycursor.execute(''' insert into talent (nom) values
                        ('dev'),
                        ('musique'),
                        ('dessin'),
                        ('graphisme'),
                        ('dessin'),
                        ('3D'),
                        ('Montage');''')
        mydB.commit()
        mycursor.execute('''update controle set implement=True 
                        where id_table=1;''')
        mydB.commit()

    # GROUPE
    mycursor.execute('''select implement from controle
                    where id_table=4; ''')
    isAlreadyDone = mycursor.fetchone()[0]
    if not isAlreadyDone:
        mycursor.execute(''' insert into groupe (nom, nb_membres) values ('movieStars', 3);''')
        mydB.commit()
        mycursor.execute('''update controle set implement=True 
                        where id_table=4;''')
        mydB.commit()

    # ETUDIANT
    mycursor.execute('''select implement from controle
                    where id_table=2; ''')
    isAlreadyDone = mycursor.fetchone()[0]
    if not isAlreadyDone:
        mycursor.execute(''' insert into etudiant (prenom, nom, id_groupe) values
                        ('Bob','leponge', 1),
                        ('Dora','lexploratrice', 1),
                        ('koro','sensei', 1);''')
        mydB.commit()
        mycursor.execute('''update controle set implement=True 
                        where id_table=2;''')
        mydB.commit()

    # POSSEDE
    mycursor.execute('''select implement from controle
                    where id_table=5; ''')
    isAlreadyDone = mycursor.fetchone()[0]
    if not isAlreadyDone:
        mycursor.execute(''' insert into possede (id_etud, id_talent) values 
                         (1,2),
                         (1,4), 
                         (2,6);''')
        mydB.commit()
        mycursor.execute('''update controle set implement=True 
                        where id_table=5;''')
        mydB.commit()

    # PROJET
    mycursor.execute('''select implement from controle
                    where id_table=6; ''')
    isAlreadyDone = mycursor.fetchone()[0]
    if not isAlreadyDone:
        mycursor.execute(''' insert into projet (nom, id_groupe) values 
                         ('Collab', 1);''')
        mydB.commit()
        mycursor.execute('''update controle set implement=True 
                        where id_table=6;''')
        mydB.commit()

    ### Affichage initial dans concole ###
    mycursor.execute('''select * from etudiant''')
    etud=mycursor.fetchall()
    print(etud)

    mycursor.execute('''select * from talent''')
    tal=mycursor.fetchall()
    print(tal)

    mycursor.execute('''select * from groupe''')
    grp=mycursor.fetchall()
    print(grp)

    mycursor.execute('''select * from projet''')
    prj=mycursor.fetchall()
    print(prj)

    mycursor.execute('''select * from controle''')
    ctrl=mycursor.fetchall()
    print(ctrl)

    mycursor.execute('''select * from possede''')
    pssd=mycursor.fetchall()
    print(pssd)

    mycursor.close()

def init_liste_talents(pswd,database_name, liste_talents):
    mydB = mysql.connector.connect (
     host="localhost",
     user="root",
     password = pswd,
     database= database_name
    ) 
    mycursor = mydB.cursor()

    mycursor.execute('''select * from talent;''')
    for i in mycursor.fetchall():
        liste_talents.append(i)
    mycursor.close()

def get_students_info(pswd,database_name, liste_etudiants, liste_etudiants_talents):
    mydB = mysql.connector.connect (
     host="localhost",
     user="root",
     password = pswd,
     database= database_name
    ) 

    mycursor = mydB.cursor()
    
    liste_etudiants_talents.clear()
    liste_etudiants.clear()

    mycursor.execute('''select * from etudiant''')
    for i in mycursor.fetchall():
        etudiant = {}
        etudiant["num_etudiant"] = i[0]
        etudiant["prenom"] = i[1]
        etudiant["nom"] = i[2]
        etudiant["groupe"] = i[3]
        
        liste_etudiants.append(etudiant)

    mycursor.execute('''select etudiant.id_num, talent.id_tal, talent.nom from talent
                     join possede on talent.id_tal = possede.id_talent
                     join etudiant on possede.id_etud = etudiant.id_num''')
    for i in mycursor.fetchall():
        etudiant_talent = {}
        etudiant_talent["num_etudiant"] = i[0]
        etudiant_talent["id_talent"] = i[1]
        etudiant_talent["nom_talent"] = i[2]
        liste_etudiants_talents.append(etudiant_talent)

    mycursor.close()

def add_student(pswd, database_name, request):
    mydB = mysql.connector.connect (
     host="localhost",
     user="root",
     password = pswd,
     database= database_name
    )

    mycursor = mydB.cursor()

    mycursor.execute('''insert into etudiant (prenom, nom) values (+"''' 
                     + request.form["prenom"] + '''","''' 
                     + request.form["nom"] + '''");'''  )
    mydB.commit()

    mycursor.close()

def students_current_talents(pswd, database_name, num_etud, liste_possede):
    mydB = mysql.connector.connect (
     host="localhost",
     user="root",
     password = pswd,
     database= database_name
    )

    mycursor = mydB.cursor()
    
    mycursor.execute('''select id_talent from possede
                        where id_etud  = ''' + str(num_etud) + ''';''')
    for talent in mycursor.fetchall():
        liste_possede.append(talent[0])
    mycursor.close()

def modifiy_students_talents(pswd, database_name, request, liste_nouv_talents, liste_anciens_talents):
    mydB = mysql.connector.connect (
     host="localhost",
     user="root",
     password = pswd,
     database= database_name
    )

    mycursor = mydB.cursor()
    
    for i in range(len(request.form.getlist("talents"))):
        liste_nouv_talents.append((int(request.form["num_etud"]),int(request.form.getlist("talents")[i])))

    mycursor.execute('''select * from possede
                     where id_etud = ''' + request.form["num_etud"] + ''';''')
    liste_anciens_talents = mycursor.fetchall()
    
    liste_selection = []
    #trie entre les nouveaux talents et les anciens 
    for talent in liste_anciens_talents:
        if talent in liste_nouv_talents:
            liste_selection.append((talent[0], talent[1], "present"))
        else:
            liste_selection.append((talent[0], talent[1], "delete"))
    #vérifie si un nouveau talent doit être ajouté 
    for talent in liste_nouv_talents:
        if talent not in liste_anciens_talents:
            liste_selection.append((talent[0],talent[1], "add"))

    for talent in liste_selection:
        if talent[2] == "delete":
            mycursor.execute('''delete from possede where id_talent= ''' + str(talent[1]) + ''';''')
            mydB.commit()
        elif talent[2] == "add":
            mycursor.execute('''insert into possede (id_etud,id_talent) values
                             (''' + str(talent[0]) + ''', ''' + str(talent[1]) + ''');''')
            mydB.commit()
    mycursor.close()

def suppression(pswd, database_name, value):
    mydB = mysql.connector.connect (
     host="localhost",
     user="root",
     password=pswd,
     database=database_name
    )
    mycursor =mydB.cursor()

    mycursor.execute('''delete from possede
                     where id_etud=''' + str(value) + ''';'''
                     )
    mycursor.execute('''update groupe 
                     join etudiant on id_grp = id_groupe
                     set nb_membres = nb_membres-1
                     where id_num=''' + str(value) + ''';'''
                     )
    mycursor.execute('''delete from etudiant
                     where id_num=''' + str(value)
                     )
    mydB.commit()
    mycursor.close()

def changement_infos_etud(pswd, database_name, num_etud, request):
    mydB = mysql.connector.connect (
     host="localhost",
     user="root",
     password=pswd,
     database=database_name
    )
    mycursor =mydB.cursor()

    # mycursor.execute('''select * from etudiant where id_num=''' + str(num_etud) + ''';''')
    # print(type(mycursor.fetchone()[2]))
    # mydB.commit()

    mycursor.execute('''update etudiant set nom= "''' + request.form["nouv_nom"] +
                     '''" where id_num=''' + str(num_etud) + 
                     ''';'''
                     )
    mycursor.execute('''update etudiant set prenom= "''' + request.form["nouv_prenom"] +
                     '''" where id_num=''' + str(num_etud)
                    )
    mydB.commit()
    
    # mycursor.execute('''select * from etudiant where id_num=''' + str(num_etud) + ''';''')
    # print(mycursor.fetchone())
    # mydB.commit()
    mycursor.close()

def get_groups_info(pswd, database_name, liste_groupes, liste_groupes_talents, liste_projets):
    mydB = mysql.connector.connect (
    host="localhost",
    user="root",
    password=pswd,
    database=database_name
    )
    mycursor =mydB.cursor()

    liste_groupes_talents.clear()
    liste_groupes.clear()
    liste_projets.clear()

    mycursor.execute('''select * from groupe;''')
    for i in mycursor.fetchall():
        groupe = {}
        groupe["num_groupe"] = i[0]
        groupe["nom"] = i[1]
        groupe["membres"] = i[2]

        liste_groupes.append(groupe)

    mycursor.execute('''select projet.nom from projet
                     join groupe on projet.id_groupe = groupe.id_grp
                     order by id_groupe;''')
    for i in mycursor.fetchall():
        projet = i[0]
        liste_projets.append(projet)

    mycursor.execute('''select distinct groupe.id_grp, talent.nom from talent
                     join possede on talent.id_tal = possede.id_talent
                     join etudiant on possede.id_etud = etudiant.id_num
                     join groupe on etudiant.id_groupe = groupe.id_grp''')
    for i in mycursor.fetchall():
        groupe_talent = {}
        groupe_talent["num_groupe"] = i[0]
        groupe_talent["talent"] = i[1]

        liste_groupes_talents.append(groupe_talent)
    
    mycursor.close()