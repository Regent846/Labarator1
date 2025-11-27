import pytest
import random

@pytest.fixture
def random_user_data():
    """Генерирует случайные данные пользователя."""
    return {
        "name": f"Test User {random.randint(1000, 9999)}",
        "username": f"user_{random.randint(1000, 9999)}",
        "email": f"test{random.randint(1000, 9999)}@example.com"
    }

@pytest.fixture
def random_post_data():
    """Генерирует случайные данные поста."""
    return {
        "title": f"Test Post Title {random.randint(1000, 9999)}",
        "body": f"This is test post body content {random.randint(1000, 9999)}",
        "userId": random.randint(1, 10)
    }

@pytest.fixture
def random_comment_data():
    """Генерирует случайные данные комментария."""
    return {
        "postId": random.randint(1, 10),
        "name": f"Test Comment {random.randint(1000, 9999)}",
        "email": f"comment{random.randint(1000, 9999)}@example.com",
        "body": f"This is test comment body {random.randint(1000, 9999)}"
    }