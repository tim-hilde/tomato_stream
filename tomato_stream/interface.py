import streamlit as st
import pandas as pd
from tomato_stream.data import load_from_gcloud
from st_files_connection import FilesConnection

st.set_page_config(
	page_title="Tomato Stream",
	page_icon="🍅",
	layout="wide",
	initial_sidebar_state="collapsed",
)

conn = st.connection("gcs", type=FilesConnection)

ratings_df = conn.read("tomato-stream-database/ratings.csv", input_format="csv")

# Add a title and description
st.title("🍅 Tomato Stream")
st.markdown("""
    Willkommen bei Tomato Stream! Hier können Sie Bewertungen von Filmen und Serien durchsuchen.
    Wählen Sie eine Kategorie aus, um die entsprechenden Bewertungen anzuzeigen.
""")

selection = st.radio(
	"Wählen Sie eine Kategorie:",
	("Filme", "Serien", "Beides"),
	index=2,
	horizontal=True,
)
if selection == "Filme":
	ratings_df = ratings_df.loc[lambda _df: _df["Typ"] == "movie"].drop(columns=["Typ"])
elif selection == "Serien":
	ratings_df = ratings_df.loc[lambda _df: _df["Typ"] == "series"].drop(
		columns=["Typ"]
	)

ratings_df = ratings_df.sort_values(by="Tomatoscore", ascending=False)

genres = []

for genre in ratings_df.loc[:, "Genres"]:
	for single_genre in genre.split(", "):
		genres.append(single_genre)

genre_selection = st.multiselect(
	"Wähle Sie ein oder mehrere Genre aus", set(genres), default=None
)

for genre in genre_selection:
	ratings_df = ratings_df.loc[ratings_df["Genres"].str.contains(genre), :]

st.data_editor(
	ratings_df,
	height=800,
	disabled=True,
	column_config={
		"Poster": st.column_config.ImageColumn(
			"Poster", help="Streamlit app preview screenshots"
		),
	},
	column_order=[
		"Poster",
		"Titel",
		"Typ",
		"Tomatoscore",
		"Jahr",
		"Genres",
		"Dauer",
		"Handlung",
		"Schauspieler",
		"Regisseur",
		"Link",
	],
	hide_index=True,
)
