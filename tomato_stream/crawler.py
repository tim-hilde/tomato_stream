from tomato_stream.data import (
	get_netflix_catalog,
	get_ratings_for_catalog,
	load_from_gcloud,
	save_to_gcloud,
)
from tomato_stream import utils
from datetime import date

if __name__ == "__main__":
	with open(utils.get_project_path("last_run.txt"), "r") as file:
		last_run = file.read().strip()

	new_catalog = get_netflix_catalog(last_run)
	new_ratings_df = get_ratings_for_catalog(new_catalog)
	try:
		old_ratings = load_from_gcloud()

		all_ratings = old_ratings.append(new_ratings_df)
	except Exception:
		all_ratings = new_ratings_df

	with open(utils.get_project_path("last_run.txt"), "w") as file:
		file.write(date.today.isoformat())

	save_to_gcloud(all_ratings)
