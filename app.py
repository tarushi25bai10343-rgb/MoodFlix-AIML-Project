from flask import Flask, render_template, request
from pyswip import Prolog
import random

app = Flask(__name__)

prolog = Prolog()
prolog.consult("logic.pl")

def get_genres(mood):
    results = list(prolog.query(f"genre({mood}, Genre)"))
    return [r['Genre'] for r in results]

def get_recommendation(genre):
    movie_results = list(prolog.query(f"movie({genre}, Movie)"))
    song_results = list(prolog.query(f"song({genre}, Song)"))
    aesthetic_result = list(prolog.query(f"aesthetic({genre}, Aesthetic)"))

    movie = random.choice(movie_results)['Movie']
    
    if isinstance(movie, bytes):
        movie = movie.decode('utf-8')

    print("Movie:", movie)

    song = random.choice(song_results)['Song']

    if isinstance(song, bytes):
        song = song.decode('utf-8')

    aesthetic = aesthetic_result[0]['Aesthetic']

    if isinstance(aesthetic, bytes):
        aesthetic = aesthetic.decode('utf-8')

    poster_map = {
        "Home Alone": "homealone.jpg",
        "Murder Mystery": "murdermystery.jpg",
        "Mr. Bean": "mrbean.jpg",
        "3 Idiots": "3idiots.jpg",
        "Taare Zameen Par": "taarezameenpar.jpg",
        "The Pursuit of Happyness": "thepursuitofhappyness.jpg",
        "10 Things I Hate About You": "10thingsihateaboutyou.jpg",
        "Beauty And The Beast": "beautyandthebeast.jpg",
        "How To Lose A Guy In 10 Days": "howtoloseaguyin10days.jpg",
        "Fast And Furious": "fastandfurious.jpg",
        "Avengers": "avengers.jpg",
        "Baby Driver": "babydriver.jpg",
        "Now You See Me 2": "nowyouseeme2.jpg",
        "The Call": "thecall.jpg",
        "Midnight": "midnight.jpg",
        "Jumanji": "jumanji.jpg",
        "Journey 2:The Mysterious Island": "journeytothemysteriousisland.jpg",
        "The Good Dinosaur": "thegooddinosaur.jpg"
    }

    poster = movie.lower().replace(" ", "").replace(".", "") + ".jpg"

    return movie, song, aesthetic, poster

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        mood = request.form.get("mood")
        genres = get_genres(mood)

        genre = request.form.get("genre")

        if not genre and genres:
            return render_template("index.html", mood=mood, genres=genres)

        if genre:
            movie, song, aesthetic, poster = get_recommendation(genre)

            return render_template("index.html", mood=mood, genre=genre,
                                   movie=movie, song=song,
                                   aesthetic=aesthetic, poster=poster)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)