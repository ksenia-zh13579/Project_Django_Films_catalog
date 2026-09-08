film_name = "Spirited Away"
film_director = "Hayao Miyazaki"
film_genres = ["fantasy", "adventure", "thriller"]
film_ratings = [9, 10, 7, 5, 8]

def get_film_rating(film_ratings):
    avg_rating = 0
    for i in range(len(film_ratings)):
        avg_rating += film_ratings[i]
    avg_rating /= len(film_ratings)
    return avg_rating

print(f"Название фильма: {film_name}")
print(f"Режиссер фильма: {film_director}")
print(f"Жанры: {film_genres}")
print(f"Средняя оценка: {get_film_rating(film_ratings)}")