from tomato_stream.data import (
	get_netflix_catalog,
	get_ratings_for_catalog,
	save_to_gcloud,
)

if __name__ == "__main__":
	catalog = get_netflix_catalog()
	ratings_df = get_ratings_for_catalog(catalog)

	save_to_gcloud(ratings_df)
