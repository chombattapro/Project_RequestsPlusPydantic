import pytest
import requests_mock
from pydantic import ValidationError
from models import Post

@pytest.mark.parametrize("post_id", (1, 50, 100))
def test_validation_error_on_invalid_post(session, base_url, post_id):
    # Мок ответа сервера некорректными данными + эмуляция ответа для запроса GET /posts?userId=1
    with requests_mock.Mocker() as mock:
        mock.get(
            f"{base_url}/posts/{post_id}",
            json={
                "userId": "invalid",
                "id": 1,
                "title": "T",
                "body": "B"
            }
        )
        response = session.get(f"{base_url}/posts/{post_id}")
        with pytest.raises(ValidationError):
            Post.model_validate(response.json())
