import pandas as pd
import html
import os
import requests
import streamlit as st
from tomato_stream import utils

pd.set_option("mode.copy_on_write", True)

API_KEY = os.environ.get("API_KEY", "58977120")
RAPID_API_KEY = os.environ.get("RAPID_API_KEY")


def get_netflix_catalog() -> pd.DataFrame:
	url = "https://unogs-unogs-v1.p.rapidapi.com/search/titles"

	params = {
		"limit": 200000,
		"country_list": 39,
	}

	headers = {
		"x-rapidapi-key": RAPID_API_KEY,
		"x-rapidapi-host": "unogs-unogs-v1.p.rapidapi.com",
	}

	response = requests.get(url, headers=headers, params=params)

	results = response.json()["results"]

	catalog = (
		pd.DataFrame(results)
		.loc[lambda _df: _df["imdb_id"] != ""]
		.assign(
			title=lambda _df: _df["title"].apply(html.unescape),
		)
		.loc[:, ["title", "title_type", "imdb_id", "netflix_id"]]
	)

	return catalog


def get_rating(imdb_id):
	params = {"apikey": API_KEY, "i": imdb_id}
	url = "http://www.omdbapi.com/"
	response = requests.get(url, params=params)
	if response.status_code == 200:
		response_json = response.json()

		title = response_json.get("Title", "")
		year = response_json.get("Year", "")
		genres = response_json.get("Genre", "")
		runtime = response_json.get("Runtime", "")
		actors = response_json.get("Actors", "")
		director = response_json.get("Director", "")
		plot = response_json.get("Plot", "")
		poster = response_json.get("Poster", "")

		rotten_tomatoes_rating = ""

		if "Ratings" in response_json:
			for rating in response_json["Ratings"]:
				if rating["Source"] == "Rotten Tomatoes":
					rotten_tomatoes_rating = int(rating["Value"].strip("%"))
					break

		return (
			title,
			rotten_tomatoes_rating,
			year,
			genres,
			runtime,
			actors,
			director,
			plot,
			poster,
		)
	else:
		raise Exception(f"Error: {response.status_code}")


def get_ratings_for_catalog(catalog: pd.DataFrame) -> pd.DataFrame:
	catalog[
		[
			"title_2",
			"rating",
			"year",
			"genres",
			"runtime",
			"actors",
			"director",
			"plot",
			"poster",
		]
	] = catalog["imdb_id"].apply(get_rating).apply(pd.Series)

	ratings_df = (
		catalog.loc[(catalog.title == catalog.title_2) & (catalog.rating != "")]
		.assign(
			link=lambda _df: _df["netflix_id"].apply(
				lambda x: f"https://www.netflix.com/title/{x}"
			),
		)
		.drop(columns=["title_2", "imdb_id", "netflix_id"])
		.reset_index(drop=True)
		.rename(
			columns={
				"title": "Titel",
				"title_type": "Typ",
				"rating": "Tomatoscore",
				"year": "Jahr",
				"genres": "Genres",
				"runtime": "Dauer",
				"actors": "Schauspieler",
				"director": "Regisseur",
				"plot": "Handlung",
				"poster": "Poster",
				"link": "Link",
			}
		)
	)

	return ratings_df


def get_new_ratings() -> pd.DataFrame:
	catalog = get_netflix_catalog()
	ratings_df = get_ratings_for_catalog(catalog)

	ratings_df.to_pickle(utils.get_output_path("ratings.pkl"))
	return ratings_df


@st.cache_data
def load_ratings() -> pd.DataFrame:
	ratings_df = pd.read_pickle(utils.get_output_path("ratings.pkl"))
	return ratings_df
