import os
import pytest
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def base_url():
    return "https://jsonplaceholder.typicode.com"


@pytest.fixture
def api_client(base_url):
    """Фикстура с retry логикой и увеличенным таймаутом."""
    session = requests.Session()

    # Настройка retry стратегии
    retry_strategy = Retry(
        total=3,  # Максимум 3 попытки
        backoff_factor=1,  # Задержка между попытками
        status_forcelist=[429, 500, 502, 503, 504],  # Коды для retry
    )

    # Создаем адаптер с retry
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    def make_request(method, endpoint, **kwargs):
        if not endpoint.startswith('http'):
            if not endpoint.startswith('/'):
                endpoint = '/' + endpoint
            url = base_url + endpoint
        else:
            url = endpoint

        # Увеличиваем таймаут для больших запросов
        if endpoint in ['/comments', '/posts', '/users']:
            kwargs.setdefault('timeout', 30)  # 30 секунд для больших эндпоинтов
        else:
            kwargs.setdefault('timeout', 10)  # 10 секунд для остальных

        return session.request(method, url, **kwargs)

    session.get = lambda endpoint, **kwargs: make_request('GET', endpoint, **kwargs)
    session.post = lambda endpoint, **kwargs: make_request('POST', endpoint, **kwargs)
    session.put = lambda endpoint, **kwargs: make_request('PUT', endpoint, **kwargs)
    session.delete = lambda endpoint, **kwargs: make_request('DELETE', endpoint, **kwargs)

    session.headers.update({
        "Content-Type": "application/json",
        "User-Agent": "ApiAutomation/1.0"
    })

    yield session
    session.close()