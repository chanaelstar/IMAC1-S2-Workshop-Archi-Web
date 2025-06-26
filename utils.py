def selection_etudiant(liste_etudiants,value):
    for i in range(len(liste_etudiants)):
        if liste_etudiants[i]["num_etudiant"] == value:
            return liste_etudiants[i]

def selection_groupe(liste_groupes,id_grp):
    for i in range(len(liste_groupes)):
        if liste_groupes[i]["num_groupe"] == id_grp:
            return liste_groupes[i]