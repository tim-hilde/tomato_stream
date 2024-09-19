def test_data_integrity():
	import pandas as pd
	from tomato_stream.data import load_ratings

	ratings_df = load_ratings()
	assert isinstance(ratings_df, pd.DataFrame)
	assert ratings_df.shape[0] > 0
	assert ratings_df.shape[1] == 11
	assert ratings_df.columns.tolist() == [
		"Titel",
		"Typ",
		"Jahr",
		"Link",
		"Genres",
		"Dauer",
		"Schauspieler",
		"Regisseur",
		"Handlung",
		"Tomatorscore",
		"Poster",
	]


def test_get_rating():
	from tomato_stream.data import get_rating

	imdb_id = "tt0111161"
	title, year, genres, runtime, actors, director, plot, rating, poster = get_rating(
		imdb_id
	)
	assert isinstance(title, str)
	assert isinstance(year, str)
	assert isinstance(genres, list)
	assert isinstance(runtime, str)
	assert isinstance(actors, str)
	assert isinstance(director, str)
	assert isinstance(plot, str)
	assert isinstance(rating, int)
	assert isinstance(poster, str)


def test_get_catalog():
	import pandas as pd
	from tomato_stream.data import get_netflix_catalog

	catalog = get_netflix_catalog()
	assert isinstance(catalog, pd.DataFrame)
	assert catalog.shape[0] > 0
	assert catalog.shape[1] == 4
	assert catalog.columns.tolist() == ["title", "title_type", "year", "link"]


def test_get_ratings_for_catalog():
	import pandas as pd
	from tomato_stream.data import get_ratings_for_catalog, get_netflix_catalog

	catalog = get_netflix_catalog().head(5)
	ratings_df = get_ratings_for_catalog(catalog)
	assert isinstance(ratings_df, pd.DataFrame)
	assert ratings_df.shape[0] > 0
	assert ratings_df.shape[1] == 11
	assert ratings_df.columns.tolist() == [
		"Titel",
		"Typ",
		"Jahr",
		"Link",
		"Genres",
		"Dauer",
		"Schauspieler",
		"Regisseur",
		"Handlung",
		"Tomatorscore",
		"Poster",
	]
