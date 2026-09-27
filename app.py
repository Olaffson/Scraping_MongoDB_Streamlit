import streamlit as st
# la connexion à MongoDB est ouverte dans fonctions_streamlit
from fonctions_streamlit import film_le_plus_long, cinq_films_mieux_notes, get_acteurs, nb_films_acteur
from fonctions_streamlit import trois_meilleurs_films_genre, get_genres

# Affichage film_le_plus_long avec Streamlit
st.title("La Palme du film le plus long est décerné à :")
st.write(film_le_plus_long())

# Affichage cinq_films_mieux_notes avec Streamlit
st.title("Les 5 films les mieux notés sont :")
list_film = cinq_films_mieux_notes()
for i, film in enumerate(list_film):
    st.write(f"{i+1}. {film}")

# Affichage pour trouver le nombre de films dans lesquels un acteur a joué
st.title("Trouver le nombre de films dans lequel un acteur à jouer :")
acteurs = get_acteurs()
acteur_selectionne = st.selectbox('Sélectionnez un acteur', acteurs)

if acteur_selectionne:
    nb_films = nb_films_acteur(acteur_selectionne)
    st.write(acteur_selectionne, 'a joué dans', nb_films, 'films')


# Affichage pour trouver les 3 meilleurs films par genre
st.title("Trouver les 3 meilleurs films par genre :")
genre = get_genres()
selected_genre = st.selectbox("Sélectionnez un genre", genre)
if selected_genre:
    films = trois_meilleurs_films_genre(selected_genre)
    st.write(f"Les trois meilleurs films du genre {selected_genre} sont :")
    for i, film in enumerate(films):
        st.write(f"{i+1}. {film}")
else:
    st.write("Sélectionnez un genre dans la liste.")
