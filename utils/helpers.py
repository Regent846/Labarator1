import json
import allure
from datetime import datetime


def attach_response_to_allure(response):
    """Прикрепляет информацию о response к Allure отчету."""
    allure.attach(
        body=json.dumps(response.json(), indent=2, ensure_ascii=False),
        name=f"Response Body {datetime.now()}",
        attachment_type=allure.attachment_type.JSON
    )

    allure.attach(
        body=f"Status Code: {response.status_code}\nURL: {response.url}",
        name="Response Info",
        attachment_type=allure.attachment_type.TEXT
    )


def generate_curl_command(request):
    """Генерирует cURL команду из request объекта."""
    headers = ''.join([f"-H '{key}: {value}' " for key, value in request.headers.items()])
    body = f"-d '{request.body}' " if request.body else ""
    return f"curl -X {request.method} {headers}{body}'{request.url}'"