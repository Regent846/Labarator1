import pytest
import jsonschema
from tests.schemas.user_schema import user_schema

@pytest.mark.functional
class TestUsers:
    def test_get_all_users(self, api_client):
        response = api_client.get("/users")
        assert response.status_code == 200
        # Проверка, что ответ - это список пользователей
        assert isinstance(response.json(), list)

    def test_get_user_by_id(self, api_client):
        response = api_client.get("/users/1")
        assert response.status_code == 200
        user_data = response.json()

        # Валидация JSON-схемы (Контрактное тестирование)
        jsonschema.validate(instance=user_data, schema=user_schema)

        # Проверка конкретных полей
        assert user_data["id"] == 1
        assert "name" in user_data

    @pytest.mark.parametrize("user_id, expected_status", [
        (1, 200),
        (9999, 404),  # Негативный кейс: несуществующий пользователь
    ])
    def test_get_user_status_code(self, api_client, user_id, expected_status):
        """Data-driven тест для проверки кодов ответа."""
        response = api_client.get(f"/users/{user_id}")
        assert response.status_code == expected_status

    def test_create_user(self, api_client):
        new_user = {
            "name": "Leanne Graham",
            "username": "Bret",
            "email": "Sincere@april.biz"
        }
        response = api_client.post("/users", json=new_user)
        assert response.status_code == 201
        created_user = response.json()
        assert created_user["name"] == new_user["name"]
        assert "id" in created_user