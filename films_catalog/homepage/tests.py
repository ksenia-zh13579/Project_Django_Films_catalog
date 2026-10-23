from django.test import TestCase


class HomepagePagesTests(TestCase):
    def test_home_page_contains_navigation_and_catalogue(self) -> None:
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Открыть каталог")
        self.assertContains(response, "Пользователи")

    def test_users_page_displays_statuses(self) -> None:
        response = self.client.get("/users/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Анна")
        self.assertContains(response, "Просмотрено")

    def test_about_page_is_available(self) -> None:
        response = self.client.get("/about/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "О проекте")
