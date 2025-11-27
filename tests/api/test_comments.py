import pytest
import jsonschema
from tests.schemas.comment_schema import comment_schema


@pytest.mark.functional
class TestComments:

    def test_get_comments_for_post(self, api_client):
        """Получение комментариев для конкретного поста."""
        # Ограничиваем количество комментариев
        response = api_client.get("/posts/1/comments")
        assert response.status_code == 200
        comments = response.json()
        assert isinstance(comments, list)
        if comments:
            jsonschema.validate(instance=comments[0], schema=comment_schema)

    def test_get_all_comments(self, api_client):
        """Получение всех комментариев с лимитом."""
        # ИСПРАВЛЕНИЕ: Добавляем лимит чтобы не грузить все 500 комментариев
        response = api_client.get("/comments?_limit=5")  # Только 5 комментариев
        assert response.status_code == 200
        comments = response.json()
        assert isinstance(comments, list)
        assert len(comments) <= 5  # Проверяем что не больше лимита

    @pytest.mark.parametrize("post_id", [1, 2])
    def test_comments_belong_to_post(self, api_client, post_id):
        """Data-driven тест с ограничением."""
        response = api_client.get(f"/posts/{post_id}/comments?_limit=3")
        assert response.status_code == 200
        comments = response.json()

        for comment in comments[:2]:  # Проверяем только первые 2
            assert comment["postId"] == post_id
            jsonschema.validate(instance=comment, schema=comment_schema)

    def test_create_comment(self, api_client):
        """Создание нового комментария."""
        new_comment = {
            "postId": 1,
            "name": "Test Comment",
            "email": "test@example.com",
            "body": "This is a test comment body"
        }
        response = api_client.post("/comments", json=new_comment)
        assert response.status_code == 201
        created_comment = response.json()
        assert created_comment["postId"] == new_comment["postId"]