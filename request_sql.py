import mysql.connector

def init_database(config_database):
    mydB = mysql.connector.connect (
     host= config_database['host'],
     user= config_database['user'],
     password = config_database['password'],
     database= config_database['database']
    )

    mycursor =mydB.cursor()

    # Création des tables
    mycursor.execute('''create table IF NOT EXISTS talent (id_tal int primary key auto_increment, nom varchar(50)
                    )''')
    mydB.commit()
    mycursor.execute('''create table IF NOT EXISTS groupe (id_grp int primary key auto_increment, nom varchar(50), nb_membres int default(0)
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
                        ('Dev'),
                        ('Musique'),
                        ('Dessin'),
                        ('Graphisme'),
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
        mycursor.execute(''' insert into groupe (nom, nb_membres) values
                         ('sans groupe', 0), 
                         ('movieStars', 3),
                         ('movies', 2);''')
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
                        ('Bob','leponge', 2),
                        ('Dora','lexploratrice', 2),
                        ('koro','sensei', 2),
                        ('Scream', '2', 3),
                        ('Gladiator', 'II', 3);''')
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
                         (2,6),
                         (4,1),
                         (4,3),
                         (5,1);''')
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
                         ('Aucun', 1),
                         ('Collab', 2),
                         ('Sequel', 3);''')
        mydB.commit()
        mycursor.execute('''update controle set implement=True 
                        where id_table=6;''')
        mydB.commit()

    ### Affichage initial dans console ###
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

def init_liste_talents(config_database, liste_talents):
    mydB = mysql.connector.connect (
     host= config_database['host'],
     user= config_database['user'],
     password = config_database['password'],
     database= config_database['database']
    ) 
    mycursor = mydB.cursor()
    liste_talents.clear()

    mycursor.execute('''select * from talent;''')
    for i in mycursor.fetchall():
        liste_talents.append(i)
    mycursor.close()

def get_students_info(config_database, liste_etudiants, liste_etudiants_talents):
    mydB = mysql.connector.connect (
     host= config_database['host'],
     user= config_database['user'],
     password = config_database['password'],
     database= config_database['database']
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

def add_student(config_database, request):
    mydB = mysql.connector.connect (
     host= config_database['host'],
     user= config_database['user'],
     password = config_database['password'],
     database= config_database['database']
    )

    mycursor = mydB.cursor()

    mycursor.execute('''insert into etudiant (prenom, nom, id_groupe) values (+"''' 
                     + request.form["prenom"] + '''","''' 
                     + request.form["nom"] + '''", ''' 
                     + "1" + ''');'''  )
    mycursor.execute('''update groupe set nb_membres = nb_membres + 1
                     where id_grp = 1 ;''')
    mydB.commit()

    mycursor.close()

def students_current_talents(config_database, num_etud, liste_possede):
    mydB = mysql.connector.connect (
     host= config_database['host'],
     user= config_database['user'],
     password = config_database['password'],
     database= config_database['database']
    )

    mycursor = mydB.cursor()
    
    mycursor.execute('''select id_talent from possede
                        where id_etud  = ''' + str(num_etud) + ''';''')
    for talent in mycursor.fetchall():
        liste_possede.append(talent[0])
    mycursor.close()

def modifiy_students_talents(config_database, request, liste_nouv_talents, liste_anciens_talents, value):
    mydB = mysql.connector.connect (
     host= config_database['host'],
     user= config_database['user'],
     password = config_database['password'],
     database= config_database['database']
    )

    mycursor = mydB.cursor()
    print(request.form["talent_autre"])
    for i in request.form["talent_autre"]:
        if i != "":
            mycursor.execute('''insert into talent (nom) values ("'''
                            + request.form["talent_autre"] + '''");'''  )
            mydB.commit()
            break

    for i in range(len(request.form.getlist("talents"))):
        liste_nouv_talents.append((value,int(request.form.getlist("talents")[i])))

    mycursor.execute('''select * from possede
                     where id_etud = ''' + str(value) + ''';''')
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
    
    mycursor.execute('''select max(id_tal) from talent ;''')
    id_talent_autre = mycursor.fetchone()[0]

    mycursor.execute('''insert into possede (id_etud, id_talent) values ('''
                     + str(value) + ''', '''
                     + str(id_talent_autre) + ''');''')
    mydB.commit()

    mycursor.close()

def suppression(config_database, value):
    mydB = mysql.connector.connect (
     host= config_database['host'],
     user= config_database['user'],
     password = config_database['password'],
     database= config_database['database']
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

def changement_infos_etud(config_database, num_etud, request):
    mydB = mysql.connector.connect (
     host= config_database['host'],
     user= config_database['user'],
     password = config_database['password'],
     database= config_database['database']
    )
    mycursor =mydB.cursor()

    mycursor.execute('''update etudiant set nom= "''' + request.form["nouv_nom"] +
                     '''" where id_num=''' + str(num_etud) + 
                     ''';'''
                     )
    mycursor.execute('''update etudiant set prenom= "''' + request.form["nouv_prenom"] +
                     '''" where id_num=''' + str(num_etud)+ 
                     ''';'''
                    )
    mydB.commit()

    mycursor.execute('''select max(id_grp) from groupe;''')
    max_id_grp = mycursor.fetchone()[0]
    if int(request.form["nouv_grp"]) > 0 and int(request.form["nouv_grp"]) <= max_id_grp:
        mycursor.execute('''update groupe
                     join etudiant on groupe.id_grp = etudiant.id_groupe 
                     set nb_membres = nb_membres - 1
                     where etudiant.id_num =  ''' + str(num_etud) + ''';''')
        mycursor.execute('''update groupe set nb_membres = nb_membres + 1 
                     where id_grp = "''' + request.form["nouv_grp"] +'''" ; ''')
        mycursor.execute('''update etudiant 
                    set id_groupe = "''' + request.form["nouv_grp"] +'''"
                    where  id_num =  ''' + str(num_etud) + ''';''')
    mydB.commit()
    
    mycursor.close()

def get_groups_info(config_database, liste_groupes, liste_groupes_talents, liste_projets):
    mydB = mysql.connector.connect (
     host= config_database['host'],
     user= config_database['user'],
     password = config_database['password'],
     database= config_database['database']
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
    projets_nom = mycursor.fetchall()
    mycursor.execute('''select projet.id_prj from projet
                            join groupe on projet.id_groupe = groupe.id_grp
                            order by id_groupe;''')
    projets_id = mycursor.fetchall()
    n=0
    for i in projets_nom:
        projet = i[0]
        if n != 0 :
            if (projets_id[n][0] - projets_id[n-1][0]) > 1 : # Permet de compenser si un groupe a été supprimé
                k=0
                while k < (projets_id[n][0] - projets_id[n-1][0] - 1) :
                    liste_projets.append((projets_id[n][0] - projets_id[n-1][0])-k)
                    k=k+1
            
        n=n+1
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

def add_group(config_database, request):
    mydB = mysql.connector.connect (
     host= config_database['host'],
     user= config_database['user'],
     password = config_database['password'],
     database= config_database['database']
    )
    mycursor = mydB.cursor()

    mycursor.execute('''insert into groupe (nom) values (+"''' 
                      + request.form["nom"] + '''");'''  )
    mydB.commit()

    mycursor.execute('''select max(id_grp) from groupe;''')
    max_id_grp = mycursor.fetchone()[0]

    mycursor.execute('''insert into projet (nom, id_groupe) values (+"''' 
                    + request.form["projet"] + '''", '''
                    + str(max_id_grp) + ''');'''  )
    mydB.commit()
    mycursor.close()

def changement_infos_grp(config_database, num_grp, request, liste_nouv_membres, liste_anciens_membres):
    mydB = mysql.connector.connect (
     host= config_database['host'],
     user= config_database['user'],
     password = config_database['password'],
     database= config_database['database']
    )
    mycursor = mydB.cursor()

    mycursor.execute('''update groupe set nom= "''' + request.form["nouv_nom"] +
                     '''" where id_grp=''' + str(num_grp) + ''';'''
                     )
    mycursor.execute('''update projet set nom= "''' + request.form["nouv_projet"] +
                     '''" where id_groupe=''' + str(num_grp) + ''';'''
                     )
    
    mydB.commit()
    
    for i in range(len(request.form.getlist("etudiants"))):
        mycursor.execute('''select id_groupe from etudiant
                         where id_num =''' + request.form.getlist("etudiants")[i] + ''';''')
        membre_groupe = mycursor.fetchone()[0]
        liste_nouv_membres.append((int(request.form.getlist("etudiants")[i]), membre_groupe)) 

    mycursor.execute('''select id_num,id_groupe from etudiant
                     where id_groupe = ''' + str(num_grp) + ''';''')
    liste_anciens_membres = mycursor.fetchall()

    #trie entre les nouveaux membres et les anciens
    for membre in liste_anciens_membres:
        if membre not in liste_nouv_membres:
            mycursor.execute('''update etudiant set id_groupe=1
                             where id_num= ''' + str(membre[0]) + ''';''')
            mycursor.execute('''update groupe set nb_membres = nb_membres-1
                             where id_grp = ''' + str(num_grp) + ''';''')
            mycursor.execute('''update groupe set nb_membres = nb_membres+1
                             where id_grp =1;''')
            mydB.commit()
    #vérifie si un nouveau talent doit être ajouté 
    for membre in liste_nouv_membres:
        if membre not in liste_anciens_membres:
            mycursor.execute('''update etudiant set id_groupe=''' + str(num_grp) +
                             ''' where id_num= ''' + str(membre[0]) + ''';''')
            mycursor.execute('''update groupe set nb_membres = nb_membres +1
                             where id_grp = ''' + str(num_grp) + ''';''')
            mycursor.execute('''update groupe set nb_membres = nb_membres -1
                             where id_grp =''' + str(membre[1]) + ''' ;''')
            mydB.commit()

    mycursor.close()

def suppression_groupe(config_database, num_grp, request):
    mydB = mysql.connector.connect (
     host= config_database['host'],
     user= config_database['user'],
     password = config_database['password'],
     database= config_database['database']
    )
    mycursor = mydB.cursor()

    mycursor.execute('''delete from projet
                     where id_groupe=''' + str(num_grp) + ''';'''
                     )
    mycursor.execute('''update etudiant set id_groupe=1
                     where id_groupe= ''' + str(num_grp) + ''';''')
    
    mycursor.execute('''select nb_membres from groupe
                     where id_grp = ''' + str(num_grp) + ''';''')
    nb_membres_grp = mycursor.fetchone()[0]
    mycursor.execute('''update groupe set nb_membres = nb_membres + ''' + str(nb_membres_grp) +
                    ''' where id_grp =1;''')
    
    mycursor.execute('''delete from groupe
                     where id_grp=''' + str(num_grp) + ''';'''
                     )
    mydB.commit()

    mycursor.close()