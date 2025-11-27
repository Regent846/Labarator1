import pytest
import jsonschema
from ..schemas.post_schema import post_schema


@pytest.mark.functional
class TestPosts:
    """Тесты для работы с постами."""

    def test_get_all_posts(self, api_client):
        """Получение всех постов."""
        response = api_client.get("/posts")
        assert response.status_code == 200
        posts = response.json()
        assert isinstance(posts, list)
        assert len(posts) > 0

        # Проверка структуры первого поста
        if posts:
            jsonschema.validate(instance=posts[0], schema=post_schema)

    def test_get_post_by_id(self, api_client):
        """Получение конкретного поста по ID."""
        response = api_client.get("/posts/1")
        assert response.status_code == 200
        post_data = response.json()

        # Валидация схемы
        jsonschema.validate(instance=post_data, schema=post_schema)

        # Проверка обязательных полей
        assert post_data["id"] == 1
        assert "title" in post_data
        assert "body" in post_data
        assert "userId" in post_data

    def test_create_post(self, api_client):
        """Создание нового поста."""
        new_post = {
            "title": "Test Post Title",
            "body": "This is a test post body content",
            "userId": 1
        }
        response = api_client.post("/posts", json=new_post)
        assert response.status_code == 201
        created_post = response.json()

        # Проверка, что пост создан с правильными данными
        assert created_post["title"] == new_post["title"]
        assert created_post["body"] == new_post["body"]
        assert created_post["userId"] == new_post["userId"]
        assert "id" in created_post

    def test_update_post(self, api_client):
        """Обновление существующего поста."""
        updated_data = {
            "title": "Updated Title",
            "body": "Updated body content",
            "userId": 1
        }
        response = api_client.put("/posts/1", json=updated_data)
        assert response.status_code == 200
        updated_post = response.json()
        assert updated_post["title"] == updated_data["title"]

    def test_delete_post(self, api_client):
        """Удаление поста."""
        response = api_client.delete("/posts/1")
        assert response.status_code == 200  # JSONPlaceholder возвращает 200 для DELETE

    @pytest.mark.negative
    @pytest.mark.parametrize("invalid_post_id, expected_status", [
        (0, 404),  # Невалидный ID
        (99999, 404),  # Несуществующий ID
        ("abc", 404),  # Строковый ID
    ])
    def test_get_invalid_post(self, api_client, invalid_post_id, expected_status):
        """Негативные тесты получения поста."""
        response = api_client.get(f"/posts/{invalid_post_id}")
        assert response.status_code == expected_status