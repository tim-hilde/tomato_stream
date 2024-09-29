import streamlit as st
import pandas as pd
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

ratings_df = (
	ratings_df.sort_values(by="Tomatoscore", ascending=False)
	.assign(
		Dauer=lambda _df: _df["Dauer"].str.replace(" min", "").astype(float),
	)
	.rename(columns={"Dauer": "Dauer (min)"})
)

genres = []

for genre in ratings_df.loc[:, "Genres"]:
	for single_genre in genre.split(", "):
		genres.append(single_genre)

genres = list(set(genres))
genres.sort()

genre_selection = st.multiselect(
	"Wähle Sie ein oder mehrere Genre aus", genres, default=None
)

for genre in genre_selection:
	ratings_df = ratings_df.loc[ratings_df["Genres"].str.contains(genre), :]

genre_anti_selection = st.multiselect(
	"Wähle Sie ein oder mehrere Genre aus, die **nicht** enthalten sein sollen",
	genres,
	default=None,
)

for genre in genre_anti_selection:
	ratings_df = ratings_df.loc[~ratings_df["Genres"].str.contains(genre), :]

duration_range = range(0, int(ratings_df["Dauer (min)"].max()) + 10, 10)

dauer = st.select_slider(
	"Dauer (Minuten)",
	options=duration_range,
	value=[min(duration_range), max(duration_range)],
)
st.write(dauer)
ratings_df = ratings_df.loc[
	(ratings_df["Dauer (min)"] >= dauer[0]) & (ratings_df["Dauer (min)"] <= dauer[1]), :
]

st.data_editor(
	ratings_df,
	height=800,
	disabled=True,
	column_config={
		"Poster": st.column_config.ImageColumn(
			"Poster", help="Streamlit app preview screenshots"
		),
		"Link": st.column_config.LinkColumn(),
	},
	column_order=[
		"Poster",
		"Titel",
		"Typ",
		"Tomatoscore",
		"Jahr",
		"Genres",
		"Dauer (min)",
		"Handlung",
		"Schauspieler",
		"Regisseur",
		"Link",
	],
	hide_index=True,
)
