-- 1. Список всех произведений.
SELECT id, name, director
FROM films
ORDER BY name;

-- 2. Список пользователей.
SELECT id, name
FROM users
ORDER BY name;

-- 3. Поиск произведений по режиссёру.
SELECT id, name, director
FROM films
WHERE director LIKE ?;

-- 4. Поиск произведений по жанру.
SELECT f.id, f.name, f.director
FROM films AS f
JOIN film_genres AS fg ON fg.film_id = f.id
JOIN genres AS g ON g.id = fg.genre_id
WHERE g.name = ?;

-- 5. Произведения и их жанры (JOIN).
SELECT f.name AS film_name, GROUP_CONCAT(g.name, ', ') AS genres
FROM films AS f
JOIN film_genres AS fg ON fg.film_id = f.id
JOIN genres AS g ON g.id = fg.genre_id
GROUP BY f.id, f.name
ORDER BY f.name;

-- 6. Оценки с именами пользователей и произведений (JOIN).
SELECT u.name AS user_name, f.name AS film_name, r.value
FROM ratings AS r
JOIN users AS u ON u.id = r.user_id
JOIN films AS f ON f.id = r.film_id
ORDER BY f.name, u.name;

-- 7. Количество произведений.
SELECT COUNT(*) AS film_count
FROM films;

-- 8. Средняя оценка каждого произведения.
SELECT f.name, ROUND(AVG(r.value), 2) AS average_rating
FROM films AS f
LEFT JOIN ratings AS r ON r.film_id = f.id
GROUP BY f.id, f.name;

-- 9. Количество оценок по пользователям.
SELECT u.name, COUNT(r.id) AS rating_count
FROM users AS u
LEFT JOIN ratings AS r ON r.user_id = u.id
GROUP BY u.id, u.name;

-- 10. Произведения с двумя и более оценками (HAVING).
SELECT f.name, COUNT(r.id) AS rating_count
FROM films AS f
JOIN ratings AS r ON r.film_id = f.id
GROUP BY f.id, f.name
HAVING COUNT(r.id) >= 2;

-- 11. Статусы пользователей по произведениям (JOIN).
SELECT u.name AS user_name, f.name AS film_name, s.status
FROM statuses AS s
JOIN users AS u ON u.id = s.user_id
JOIN films AS f ON f.id = s.film_id
ORDER BY u.name, f.name;

-- 12. Средняя оценка произведений выше заданного порога (HAVING).
SELECT f.name, ROUND(AVG(r.value), 2) AS average_rating
FROM films AS f
JOIN ratings AS r ON r.film_id = f.id
GROUP BY f.id, f.name
HAVING AVG(r.value) >= ?;
