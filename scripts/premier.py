
import pandas as pd

nblig = 0  # Nbre de lignes du fichier d'origine
nbligp = 0 # Nbre de lignes retenues
##instantDebut =0
lignes = []

with open("data/raw/data-2025_11_27.log", "rt") as fin, open("data/processed/premier.log", "wt") as fout :
    for ligne in fin:
        nblig += 1
        champs = ligne.split(" ")
        try :
            if len (champs) > 2 :
                #if ligne.find("APCMD")  >= 0 :
                #    print ("----> APCMD")
                if champs[1] > "16:13:25" and champs[1] < "17:15:55" and ligne.find("APCMD") < 0:
                    partiesInstant = champs[1].split(":")
                    heures = int(partiesInstant[0])
                    minutes = int(partiesInstant[1])
                    secondes = float(partiesInstant[2].replace(',', '.'))
                    instant = heures * 3600. + minutes * 60. + secondes

                    del(champs[0])
                    champs [0] = f"{instant:.3f}"
                    if champs[2] == "?" :
                        del (champs[2])
                    ligne = " ".join(champs[3:])
                    lignes.append([instant, champs[2], ligne])
                    nbligp += 1
        except :
            pass

    lignes.sort()

    instantDebut = lignes[0][0]
    instantFin = lignes[0][0]
    for ligne in lignes :
        if instantDebut > ligne[0] :
            instantDebut = ligne[0]
        if instantFin < ligne[0] :
            instantFin = ligne[0]

    print (f"Début : {instantDebut:10.3f}")
    print (f"Fin   : {instantFin:10.3f}")
    print (f"Durée : {instantFin-instantDebut:10.3f}")


    for ligne in lignes :
        fout.write(f"{(ligne[0]-instantDebut):.3f} {ligne[1]} {ligne[2]}")

    df = pd.DataFrame(lignes, columns=["instant", "categorie", "ligne"])



with open ("data/processed/premier_att.csv", "wt") as fout :
    fout.write("instant,heading,roll,pitch\n")
    for ligne in lignes :
        if ligne[1] == "ATTITUDE" :
            l = f"{(ligne[0]-instantDebut):.3f},{ligne[2].replace(' ', ',')}"
            fout.write(l)

print (f"Nombre de lignes d'origine : {nblig:7d} ")
print (f"Nombre de lignes retenues  : {nbligp:7d} ")
