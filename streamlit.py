import requests
import pandas as pd
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import streamlit as st
from fonctions_streamlit import film_le_plus_long, cinq_films_mieux_notes, get_acteurs, nb_films_acteur
from fonctions_streamlit import trois_meilleurs_films_genre, get_genres, duree_moyenne_genre

######################################################################################################################################
# se connecter à la base de données MongoDB
######################################################################################################################################

load_dotenv()
ATLAS_KEY=os.getenv('ATLAS_KEY')
client = MongoClient(ATLAS_KEY)
db_film = client['myfilms']
collection = db_film["film_table"]


######################################################################################################################################
# Affichage film_le_plus_long avec Streamlit
######################################################################################################################################

st.title("La Palme du film le plus long est décerné à :")
st.write(film_le_plus_long())


######################################################################################################################################
# Affichage cinq_films_mieux_notes avec Streamlit
######################################################################################################################################

st.title("Les 5 films les mieux notés sont :")
list_film = cinq_films_mieux_notes()
for i, film in enumerate(list_film):
    st.write(f"{i+1}. {film}")


######################################################################################################################################
# Affichage pour trouver le nombre de films dans lesquels un acteur a joué
######################################################################################################################################

st.title("Trouver le nombre de films dans lequel un acteur à jouer :")
acteurs = get_acteurs()
acteurs.insert(0, "")  # Ajouter une option vide en première position
acteur_selectionne = st.selectbox('Sélectionnez un acteur', acteurs)

if acteur_selectionne:
    nb_films = nb_films_acteur(acteur_selectionne)
    st.write(acteur_selectionne, 'a joué dans', nb_films, 'films')


######################################################################################################################################
# Affichage pour trouver les 3 meilleurs films par genre
######################################################################################################################################

st.title("Trouver les 3 meilleurs films par genre :")
genres = get_genres()
genres.insert(0, "")  # Ajouter une option vide en première position
selected_genre = st.selectbox("Sélectionnez un genre", genres)
if selected_genre:
    films = trois_meilleurs_films_genre(selected_genre)
    st.write(f"Les trois meilleurs films du genre {selected_genre} sont :")
    for i, film in enumerate(films):
        st.write(f"{i+1}. {film['titre']} ({film['annee']})")
else:
    st.write("Sélectionnez un genre dans la liste.")


######################################################################################################################################
# affichage du pourcentage de films par pays parmis les 100 films avec le plus haut score
######################################################################################################################################

# Récupérer les 100 films avec le plus haut score
top_films = collection.find().sort("score", pymongo.DESCENDING).limit(100)

# Extraire les IDs des 100 films avec le plus haut score
top_ids = [f["_id"] for f in top_films]

# Compter le nombre de films pour chaque pays parmi les 100 films avec le plus haut score
result = collection.aggregate([
    {"$match": {"_id": {"$in": top_ids}}},
    {"$group": {"_id": "$pays", "nombre_de_films": {"$sum": 1}}},
    {"$sort": {"nombre_de_films": -1}}
])

# Calculer le pourcentage pour chaque pays
total_films = len(top_ids)
st.title("Pourcentage de films par pays parmi les 100 films avec le plus haut score")
for r in result:
    percentage = (r["nombre_de_films"] / total_films) * 100
    st.write(f"{r['_id']} : {percentage:.2f} %")


######################################################################################################################################
# Affichage de la durée moyenne des films par genre
######################################################################################################################################

st.title("Durée moyenne des films par genre")
genres = collection.distinct('genre') # Liste des genres à afficher
for genre in genres:
    moyenne = duree_moyenne_genre(genre)
    st.write(f"Pour le genre {genre}, la durée moyenne est de {moyenne} minutes.")


######################################################################################################################################
# Affichage des infos d un film par selection du titre
######################################################################################################################################

# Liste de tous les titres de films
titres = [film["titre"] for film in collection.find()]

# Fonction pour récupérer les informations d'un film par son titre
def infos_film(titre):
    film = collection.find_one({"titre": titre})
    if film:
        # st.write(f"Titre : {film['titre']}")
        st.write(f"Genre : {film['genre']}")
        st.write(f"Durée : {film['duree']} minutes")
        st.write(f"Acteurs : {', '.join(film['acteurs'])}")
        st.write(f"Année de sortie : {film['annee']}")
        st.write(f"Score : {film['score']}")
        st.write(f"Pays d'origine : {film['pays']}")
        st.write(f"Public : {film['public']}")
        st.write(f"Synopsis : {film['description']}")
    else:
        st.write("Film introuvable")

# Affichage de la liste déroulante et des informations du film sélectionné
st.title("Sélection des infos d'un film")
titres.insert(0, "")  # Ajouter une option vide en première position
titre_selectionne = st.selectbox("Sélectionnez un titre de film", titres)
if titre_selectionne:
    infos_film(titre_selectionne)
