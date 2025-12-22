import pytest
import requests
from pydantic import BaseModel, TypeAdapter
from typing import List

class Post(BaseModel):
    userId: int
    id: int
    title: str
    body: str

BASE_URL = "https://jsonplaceholder.typicode.com"

@pytest.fixture
def session():
    return requests.Session()

def test_get_all_posts(session):
    response = session.get(f"{BASE_URL}/posts")
    assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
    all_posts = TypeAdapter(List[Post]).validate_python(response.json())
    assert len(all_posts) == 100, f"Ожидалось 100 постов, получено {len(all_posts)}"

@pytest.mark.parametrize("post_id, expected_title", [
    (1, "sunt aut facere repellat provident occaecati excepturi optio reprehenderit"),
    (50, "repellendus qui recusandae incidunt voluptates tenetur qui omnis exercitationem"),
    (100, "at nam consequatur ea labore ea harum")
])
def test_get_single_post(session, post_id, expected_title):
    response = session.get(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
    post = Post.model_validate(response.json())
    assert len([post]) == 1, f"Ожидался 1, получен {len([post])}"
    assert post.title == expected_title, f"Ожидался: {expected_title}, получен: {post.title}"

@pytest.mark.parametrize("test_data, expected_id", [
    ({
         "userId": 123,
         "title": "My test title",
         "body": "This is test body"
     }, 101),
])
def test_create_post(session, test_data, expected_id):
    response = session.post(f"{BASE_URL}/posts", json=test_data)
    assert response.status_code == 201, f"Ожидался 201, получен {response.status_code}"
    created_post = Post.model_validate(response.json())
    assert created_post.userId == test_data["userId"], f"Ожидался: {test_data["userId"]}, получен: {created_post.userId}"
    assert created_post.title == test_data["title"], f"Ожидался: {test_data["title"]}, получен: {created_post.title}"
    assert created_post.body == test_data["body"], f"Ожидался: {test_data["body"]}, получен: {created_post.body}"
    assert created_post.id == expected_id, f"Ожидался: {expected_id}, получен: {created_post.id}"
