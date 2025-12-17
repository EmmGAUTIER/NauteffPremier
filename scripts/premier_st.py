##############################################################################
#                                                                            #
# Présentation du premier essai du pilote automatique Nauteff                #
#                                                                            #
##############################################################################

import streamlit         as st
import pandas            as pd
import numpy             as np
import matplotlib.pyplot as plt
import seaborn           as sns

import ipywidgets as widgets
from ipywidgets import interact

rep_raw = "data/raw/"
rep_processed = "data/processed/"
df = None
instantDebut = None
instantFin = None

##############################################################################
# Lecture du jeu de données                                                  #
#
# Ce jeu de données est réduit à une heure et ne contient que les données
# d'orientation : cap, roulis et tangage au cours du temps.
#
##############################################################################

# Le décorateur st.cache_data permet de faire un seul appel à la fonction
# de lecture. 
@st.cache_data
def read_df():

    df_lu = None
    ideb = None
    ifin = None

    try:
        df_lu = pd.read_csv(rep_processed + "premier_att.csv", sep=',')

        # Les fonctions trigonométriques utilisent des angles en radians.
        # Les marin ne connaissent que les angles en degrés, convertissons.
        df_lu["heading_deg"]  =  - (df_lu["heading"] * (180. / np.pi) ) + 90
        df_lu["roll_deg"]  = df_lu["roll"] * (180. / np.pi)
        df_lu["pitch_deg"]  = df_lu["pitch"] * (180. / np.pi)
        ideb = df_lu["instant"].min()
        ifin = df_lu["instant"].max()

    except Exception as e:
        st.error(f"Erreur lors du chargement du jeu de données : {str(e)}")

    return df_lu, ideb, ifin

st.sidebar.title("Sommaire")

pages=["Nauteff, un projet novateur", # 0
       "Le matériel et le logiciel",  # 1
       "Premier essai en mer",        # 2
       "Des premiers résultats",      # 3
       "Et après ?"]                  # 4
page=st.sidebar.radio("", pages)                #
st.sidebar.write("Emmanuel Gautier")
st.sidebar.write("The Nauteff Project")

##############################################################################
#
# En-tête : Titre du projet
#
##############################################################################

st.title ("Nauteff")

##############################################################################
#                                                                            #
# Page : Présentation du projet                                              #
#                                                                            #
##############################################################################

if page == pages[0] :
    st.header("Présentation du projet")
    st.write(
"""
Les bateaux utilisent de plus en plus l'électronique pour aider les navigateurs.
Le pilote automatique permet de barrer pendant des heures et libérer l'équipage
d'une tâche prenante. Il s'avère être un auxiliaire indispensable pour le navigateur
solitaire en lui permettant de lacher la barre et de faire des manœuvre ou se reposer.

Nauteff est un projet de pilote automatique.
Nous voulons que Nauteff soit un pilote automatique moderne, performant
et qu'il s'intègre dans les systèmes existants.

Avec ce projet, nous apportons aux navigateurs un outil qui ne cache rien
et qu'ils peuvent adapter.
C'est la plateforme de développement pour ceux qui veulent aller plus loin.

"""
)

##############################################################################
#                                                                            #
# Page de présentation matériel et logiciel                                  #
#                                                                            #
##############################################################################

if page == pages[1] :
    st.header("Présentation du projet")
    st.subheader("Des composants modernes")
    st.write(
"""
Nauteff est architecturé autour d'un puissant microcontrôleur STM32L4.
C'est le cerveau du pilote automatique. Il allie performances et économie d'énergie.
Il contient aussi de nombreux périphériques pour communiquer avec l'extérieur.

Des capteurs Mems dans un minuscule boîtier (LSM9DS1) fournissent les informations d'orientation
du navire, ces information comprennent un magnétomètre un accéléromètre et un gyromètre.

L'action sur la barre est réalisée au moyen d'un vérin électrique commandé par un circuit spécifique
pour assurer sa commande et son contrôle.
"""
)

    st.subheader("Un logiciel adapté à l'embarqué")
    st.write(
"""
L'actuel logiciel est conçu et architecturé avec soin pour assurer un fonctionnement fiable.

Le logiciel réalise la fusion des capteurs et détermine le cap du navire. 
Il compare ce cap à la consigne donnée par le navigateur et 
envoie les ordres appropiés au verin électrique attelé à la barre pour maintenir le cap.

Le logiciel en cours de développement,
son code comporte des parties expérimentales,
mais, même en expérimentation, il a l'obligation d'être fiable et robuste.

Il est aussi conçu pour permettre d'accéder sans limitation aux informations et être facilement modifiable.

"""
)

##############################################################################
#                                                                            #
# Page Premier essai                                                         #
#                                                                            #
##############################################################################

if page == pages[2] :
    st.header("Premier essai en mer")
    st.subheader("Des conditions \"agitées\"")
    st.write(
"""
Ce premier essai a été réalisé le 28 novembre 2025, pendant l'après-midi à bord de Kreiz Avel.
Kreiz Avel est un un voilier de 9m de type arpège.
Il naviguait vers le entre le NNE et le N, vers le large avec son génois seul.
Fin novembre oblige, la mer est souvent "agitée" avec des coups de vent et de la pluie.
L'essai a été réalisé entre deux BMS (Bulletin météo spécial).
Le vent était modéré et de travers, il venait de bâbord (venant de la gauche du bateau).
La houle était significative, elle venait du nord ouest,
était courte et avait une amplitude de l'ordre de 1m.
Elle augmentait au fur et à mesure
que Kreiz Avel faisait route vers le large.

Ces conditions de mer étaient difficiles et pourtant le pilote a permis de maintenir le cap
du bateau pendant une heure.
"""
)

##############################################################################
#                                                                            #
# Page Résultats avec graphiques.                                            #
#                                                                            #
##############################################################################

if page == pages[3] :
    st.header("Des résultats encourageants")
    st.subheader("Un cap tenu pendant une heure dans une mer formée")
    st.write(
"""
le pilote automatique a tenu le cap pendant une heure sans défaillir
dans une mer formée.

Les graphes suivants montrent le cap, le roulis et le tangage au cours du temps.

Le graphe du cap montre deux corrections réalisées
pour éviter le plateau des Duons, puis,
pour passer à l'Est de la balise Pot de Fer. 
Il montre aussi les écarts de cap.
Ces écarts de cap augmentaient avec la houle du large.
Les dernières variation sont le début du retour. 

Le roulis est le mouvement d'inclinaison du bateau vers le côté.
Le roulis était important et augmentait aussi avec la houle du large.
Recevant le vent de bâbord,
il avait une gîte (inclinaison) moyenne vers tribord (à gauche) de quelques degrés. 
Le mouvement de roulis était important et explique en partie les écarts de cap.

Le tangage est le mouvement d'inclinaison du bateau vers l'avant ou l'arrière.
Le tangage est resté modéré et à peu près constant en amplitude.

L'enregistrement de ces données sert au développement
et à la mise au point du pilote.
L'enregistrement de ces données pourra aussi être 
une aide à la formation ou à l'entraînement.

"""
        )

    df, instantDebut, instantFin = read_df()

    # Curseur horizontal pour le début
    st.write("### Sélectionnez la période d'affichage")
    instantDebut = st.slider(
        "Début :",
        min_value=instantDebut,
        max_value=instantFin - 10,  # Écart minimal de 10
        value=instantDebut,
        step=10.0,
        key="start_slider",
    )

    # Curseur horizontal pour la borne supérieure
    instantFin = st.slider(
        "Fin :",
        min_value=instantDebut + 10,  # Écart minimal de 10
        max_value=instantFin,
        value=instantFin,
        step=10.0,
        key="end_slider",
    )

    # Vérification de la cohérence
    #if instantFin <= instantDebut:
    #    instantFin = instantDebut + 10

    df_plage = df[(df["instant"] >= instantDebut) & (df["instant"] <= instantFin)]

    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    # Tracer y1
    axes[0].plot(df_plage["instant"], df_plage["heading_deg"], label="heading (degrés)",  color="blue")
    axes[0].set_ylabel("Cap")
    axes[0].set_ylim(-45, +5)
    axes[2].set_xlabel("temps")
    axes[0].grid(True)

    # Tracer y2
    axes[1].plot(df_plage["instant"], df_plage["roll_deg"], label="roll (degrés)",  color="orange")
    axes[1].set_ylabel("Roulis")
    axes[2].set_xlabel("temps")
    axes[1].set_ylim(-25,10)
    axes[1].grid(True)

    # Tracer y3
    axes[2].plot(df_plage["instant"], df_plage["pitch_deg"], label="pitch (degrés)", color="green")
    axes[2].set_ylabel("tangage")
    axes[2].set_xlabel("temps (s)")
    axes[2].set_ylim(-25,10)
    axes[2].grid(True)

    # Titre global
    fig.suptitle("Cap, roulis et tangage au cours du temps")
    plt.tight_layout()
    st.pyplot(fig)

    # La matrice de corrélation est désactivée car elle ralentit
    # l'affichage et ne montre pas de corrélation significative entre les valeurs
    #matcorr = df_plage[["heading_deg", "roll_deg", "pitch_deg"]].corr()
    #matcorr = matcorr.rename(
    #    columns={
    #        "heading": "Cap",
    #        "roll": "Roulis",
    #        "pitch": "Tangage",
    #    },
    #    index={
    #        "heading": "Cap",
    #        "roll": "Roulis",
    #        "pitch": "Tangage",
    #        }
    #    )
    #st.write(matcorr)

    #fig = plt.figure(figsize=(4, 4))
    #sns.heatmap(
    #    matcorr,
    #    annot=True,  # Affiche les valeurs dans les cases
    #    cmap="coolwarm",  # Palette de couleurs
    #    center=0,  # Centre la palette sur 0
    #    vmin=-1,  # Valeur minimale de la palette
    #    vmax=1,   # Valeur maximale de la palette
    #)
    #plt.title("Matrice de corrélation")
    #st.pyplot(fig)

##############################################################################
#                                                                            #
# Page et après ?                                                            #
#                                                                            #
##############################################################################

if page == pages[4] :
    st.header("Et Après ? ")
    st.markdown(
"""
Les premiers essais sont encourageants,
le pilote nécessite encore un long travail de mise au point et d'améliorations.
"""
)
    st.subheader("Développements immédiats")
    st.markdown(
"""
Ces essais ont permis d'enregistrer un important volume de données.
Leur dépouillement et leur analyse permettront d'améliorer
le logiciel et ses réglages.

D'autres tests seront encore nécessaires pour continuer d'améliorer
les performances.

"""
        )

    st.subheader("plus tard")
    st.markdown(
"""
 - Industrialisation pour un matériel adapté au milieu marin;
 - Connectivité avec d'autres appareils;
 - Favoriser l'exploitation de données issues des capteurs;
 - Machine learning;
 - ... 

"""
        )
