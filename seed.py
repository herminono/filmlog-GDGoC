import json
from pathlib import Path
from main import app, db, Movie

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "movies.json"


def seed_movies():
    with DATA_PATH.open("r", encoding="utf-8") as file:
        movies = json.load(file)

    with app.app_context():
        db.create_all()

        added = 0

        for movie in movies:
            existing = db.session.get(Movie, movie["id"])

            if existing:
                continue

            new_movie = Movie(
                id=movie["id"],
                title=movie["title"],
                year=movie["year"],
                director=movie["director"],
                genres=movie["genres"],
                rating=movie["rating"],
                duration=movie["duration"],
                synopsis=movie["synopsis"],
                poster_url=movie["poster_url"],
                cast=movie["cast"]
            )

            db.session.add(new_movie)
            added += 1

        db.session.commit()

        print(f"Successfully seeded {added} movies!")
        print(f"Total movies: {db.session.query(Movie).count()}")


if __name__ == "__main__":
    seed_movies()
