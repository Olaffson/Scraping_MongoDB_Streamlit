import streamlit as st
import requests
import pandas as pd
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import os


# Fonction pour trouver le film le plus long
def film_le_plus_long():
    result = collection.find().sort('duree', pymongo.DESCENDING).limit(1)
    for r in result:
        return r['titre']


# Fonction pour trouver les 5 films les mieux notés
def cinq_films_mieux_notes():
    result = collection.find().sort('score', pymongo.DESCENDING).limit(5)
    films = []
    for r in result:
        films.append(r['titre'])
    return films


# Fonction pour trouver le nombre de films dans lesquels un acteur a joué
def nb_films_acteur(acteur):
    result = collection.find({'acteurs': {'$regex': acteur, '$options': 'i'}})
    count = collection.count_documents({'acteurs': {'$regex': acteur, '$options': 'i'}})
    return count

# Fonction pour extraire les noms uniques des acteurs de la collection
def get_acteurs():
    result = collection.distinct('acteurs')
    return result


# Fonction pour trouver les trois meilleurs films d'un genre donné
def trois_meilleurs_films_genre(genre):
    result = collection.find({'genres': {'$regex': genre, '$options': 'i'}}).sort('score', pymongo.DESCENDING).limit(3)
    films = []
    for r in result:
        films.append(r['titre'])
    return films

def get_genres():
    genre = collection.distinct('genre')
    return genre


# # Fonction pour trouver la durée moyenne d'un film pour un genre donné
# def duree_moyenne_genre(genre):
#     result = collection.aggregate([
#         {'$match': {'genres': {'$regex': genre, '$options': 'i'}}},
#         {'$group': {'_id': '$genres', 'duree_moyenne': {'$avg': '$duree'}}}
#     ])
#     for r in result:
#         return r['duree_moyenne']

# Fonction pour trouver la durée moyenne d'un film pour un genre donné
def duree_moyenne_genre(genre):
    result = collection.aggregate([
        {'$match': {'genre': {'$in': [genre]}}},
        {'$group': {'_id': '$genre', 'duree_moyenne': {'$avg': '$duree'}}}
    ])
    for r in result:
        return r['duree_moyenne']




load_dotenv()
ATLAS_KEY=os.getenv('ATLAS_KEY')
client = MongoClient(ATLAS_KEY)
db_film = client['myfilms']
collection = db_film["film_table"]

