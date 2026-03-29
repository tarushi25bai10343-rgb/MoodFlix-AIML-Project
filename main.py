from pyswip import Prolog
import random 

prolog = Prolog()
prolog.consult("logic.pl")

def get_genres(mood):
    results = list(prolog.query(f"genre({mood}, Genre)"))
    return [r['Genre'] for r in results]

def get_recommendation(genre):
    movie_results = list(prolog.query(f"movie({genre}, Movie)"))
    song_results = list(prolog.query(f"song({genre}, Song)"))

    if not movie_results or not song_results:
        return "No recommendations found"

    movie = random.choice(movie_results)['Movie']
    song = random.choice(song_results)['Song']

    aesthetic_result = list(prolog.query(f"aesthetic({genre}, Aesthetic)"))

    if not aesthetic_result:
        aesthetic = "No aesthetic found"
    else:
        aesthetic = aesthetic_result[0]['Aesthetic']

    return movie, song, aesthetic

mood = input("Enter your mood(happy/sad/bored/stressed): ").lower()

genres = get_genres(mood)

if not genres:
    print("Mood not found")
else:
    print("\nAvailable genres for your mood:")

    for i, g in enumerate(genres, start=1):
        print(f"{i}. {g.capitalize()}")

    try:
        choice = int(input("Choose a genre (enter number): "))
    except:
        print("Please enter a valid number")
        exit()

    if choice < 1 or choice > len(genres):
        print("Invalid choice")
    else:
        selected_genre = genres[choice - 1]

        result = get_recommendation(selected_genre)

        if isinstance(result, str):
            print(result)
        else:
            movie, song, aesthetic = result

            print("\n Selected Genre:", selected_genre.capitalize())
            print("Movie Recommendation:", movie)
            print("Song Suggestion:", song)
            print("Aesthetic:", aesthetic)