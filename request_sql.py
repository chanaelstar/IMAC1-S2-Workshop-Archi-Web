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
    mycursor.execute('''create table IF NOT EXISTS groupe (id_grp int primary key auto_increment, nb_membres int
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

    # Insérer les valeurs de base
    mycursor.execute('''select implement from controle
                    where id_table=3; ''')
    isAlreadyDone = mycursor.fetchone()
    if isAlreadyDone is None :
        isAlreadyDone = False

    if not isAlreadyDone :
        mycursor.execute(''' insert into controle (nom_table, implement) values
                        ('talent', False),
                        ('etudiant',False),
                        ('controle',True);''')
        mydB.commit()

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

    mycursor.execute('''select implement from controle
                    where id_table=2; ''')
    isAlreadyDone = mycursor.fetchone()[0]

    if not isAlreadyDone:
        mycursor.execute(''' insert into etudiant (prenom, nom) values
                        ('Bob','leponge'),
                        ('Dora','lexploratrice'),
                        ('koro','sensei');''')
        mydB.commit()
        
        mycursor.execute('''update controle set implement=True 
                        where id_table=2;''')
        mydB.commit()

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