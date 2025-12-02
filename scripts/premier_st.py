import streamlit         as st
import pandas            as pd
import numpy             as np
import matplotlib.pyplot as plt
import seaborn           as sns

#import mplcursors  # Pour les annotations interactives
import ipywidgets as widgets
from ipywidgets import interact

#import joblib
#from st_demo import st_demo
#import os

rep_raw = "data/raw/"
rep_processed = "data/processed/"
df = None
instantDebut = None
instantFin = None

st.sidebar.title("Sommaire")

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

pages=["Nauteff, un projet novateur",      # 0
       "Le matériel et le logiciel",    # 1
       "Premier essai en mer",     # 2
       "Des premiers résultats",     # 3
       "Et après ?"]     # 4
page=st.sidebar.radio("Aller vers", pages)                #
st.sidebar.write("Emmanuel Gautier")

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
    st.subheader("Notre philosophie")
    st.write(
"""
Les bateaux utilisent de plus en plus l'électronique pour aider le navigateur.
Le pilote automatique permet de barrer pendant des heures et libérer le navigateur
d'une tâche prenante. Il s'avère iêtre un auxiliaire indispensable pour le navigateur
solitaire pour permettre à celui-ci de faire des manœuvre et de se reposer.

Nauteff est un projet de pilote automatique. L'électronique d'aujourd'hui permet
des réalisations performantes, fiables, économes en énergie et même d'envisager
de l'apprentissage.

Nous voulons que Nauteff soit un pilote automatique moderne et performant et aussi
une plateforme de développement pour ceux qui veulent aller plus loin.

Avec ce projet, nous apportons aux navigateurs un outil qui ne cache rien et qu'ils peuvent adapter.
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
Nauteff utilise un puissant microcontrôleur STM32L4.
C'est le cerveau du pilote automatique. Il allie performances et économie d'énergie.
Il contient aussi de nombreux périphériques pour communiquer avec l'extérieur.

Des capteurs Mems dans un minuscule boîtier fournissent les informations d'orientation du bateau
et surtout, le plus important, le cap.

L'action sur la barre est réalisée au moyent d'un vérin électrique commandé par un circuit spécifique
pour assurer sa commande et sa protection.
"""
)

    st.subheader("Un logiciel adapté à l'embarqué")
    st.write(
"""
L'actuel logiciel est conçu et architecturé avec soin pour assurer un fonctionnement fiable.

Il est en cours de développement est son code comporte des sondes et des parties expérimentales
mais il doit, même en expérimentation, être fiable.

Il est aussi conçu pour permettre d'accéder sans barrière aux informations et être facilement modifiable.

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
Fin novembre oblige, la mer est "agitée"  avec coups de vent et pluies.
L'essai a été réalisé entre deux BMS (Bulletin météo spécial).
Le vent était modéré et de travers, bâbord amures (venant de la gauche du bateau).
La houle était significative, elle venait du nord ouest,
était courte et avait une amplitude de l'ordre de 1m.

Ces conditions étaient difficiles et pourtant le pilote a permis de maintenir le cap
du bateau pendant une heure.
"""
        )

##############################################################################
#                                                                            #
# Page Résultats avec graphiques.                                            #
#                                                                            #
##############################################################################

if page == pages[3] :
    st.header("Des résultats encourageants.")
    st.subheader("Un cap tenu pendant une heure dans une mer formée")
    st.write(
"""
le pilote automatique a tenu le cap pendant une heure sans défaillir
dans une mer formée.

"""
        )

    df, instantDebut, instantFin = read_df()

    # Curseur horizontal pour le début
    st.write("### Sélectionnez la plage de valeurs")
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
    axes[1].set_ylim(-25,25)
    axes[1].grid(True)

    # Tracer y3
    axes[2].plot(df_plage["instant"], df_plage["pitch_deg"], label="pitch (degrés)", color="green")
    axes[2].set_ylabel("tangage")
    axes[2].set_xlabel("temps (s)")
    axes[2].set_ylim(-10,15)
    axes[2].grid(True)

    # Titre global
    fig.suptitle("Cap, roulis et tangage au cours du temps")
    plt.tight_layout()
    st.pyplot(fig)

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
# Page Résultats avec graphiques.                                            #
#                                                                            #
##############################################################################

if page == pages[4] :
    st.header("Et Après ? ")
    st.write("Les essais sont encourageants, le pilote nécessite encore un travail de mise au point.")
    st.subheader("Développements immédiats")
    st.markdown(
"""
 - La commande du vérin 
 - Clavier dédié
"""
        )

    st.subheader("plus tard")
    st.markdown(
"""
 - Industrialisation pour un matériel adapté au milieu marin
 - Connectivité avec d'autres appareils

"""
        )
