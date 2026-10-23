from django.test import TestCase


class FilmPagesTests(TestCase):
    def test_film_list_page_displays_loaded_film(self) -> None:
        response = self.client.get("/films/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Унесенные призраками")

    def test_film_detail_page_displays_ratings(self) -> None:
        response = self.client.get("/films/0/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "средняя оценка")
        self.assertContains(response, "10/10")

    def test_unknown_film_returns_not_found(self) -> None:
        response = self.client.get("/films/99/")

        self.assertEqual(response.status_code, 404)
