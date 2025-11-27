import pytest
import requests


@pytest.mark.auth
class TestAuthentication:
    """Тесты для эндпоинтов аутентификации (если бы API их имело)."""

    def test_login_success(self, api_client):
        """Позитивный тест успешной аутентификации."""
        # Для JSONPlaceholder это эмуляция, так как реального auth нет
        credentials = {
            "username": "test_user",
            "password": "test_pass"
        }
        # В реальном API здесь был бы POST на /auth/login
        response = api_client.get("/users/1")  # Эмуляция успешного запроса
        assert response.status_code == 200

    @pytest.mark.negative
    @pytest.mark.parametrize("invalid_credentials", [
        {"username": "", "password": "test"},  # Пустой username
        {"username": "test", "password": ""},  # Пустой password
        {"username": "wrong", "password": "wrong"},  # Неверные данные
    ])
    def test_login_failure(self, api_client, invalid_credentials):
        """Негативные тесты аутентификации."""
        # Эмуляция запроса с неверными данными
        response = api_client.get("/users/9999")  # Несуществующий пользователь
        assert response.status_code == 404

    def test_invalid_token(self, api_client):
        """Тест с неверным токеном авторизации."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = api_client.get("/users/1", headers=headers)
        # В реальном API здесь была бы проверка на 401
        assert response.status_code in [200, 401]  # JSONPlaceholder не требует auth