import pytest
from pydantic import TypeAdapter
from typing import List
from models import Post

def test_get_all_posts(session, base_url):
    response = session.get(f"{base_url}/posts")
    assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
    all_posts = TypeAdapter(List[Post]).validate_python(response.json())
    assert len(all_posts) == 100, f"Ожидалось 100 постов, получено {len(all_posts)}"

@pytest.mark.parametrize("post_id, expected_title", [
    (1, "sunt aut facere repellat provident occaecati excepturi optio reprehenderit"),
    (50, "repellendus qui recusandae incidunt voluptates tenetur qui omnis exercitationem"),
    (100, "at nam consequatur ea labore ea harum")
])
def test_get_single_post(session, base_url, post_id, expected_title):
    response = session.get(f"{base_url}/posts/{post_id}")
    assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
    post = Post.model_validate(response.json())
    assert post.id == post_id, f"Ожидался {post_id}, получен {post.id}"
    assert post.title == expected_title, f"Ожидался: {expected_title}, получен: {post.title}"

@pytest.mark.parametrize("test_data, expected_id", [
    ({
         "userId": 123,
         "title": "My test title",
         "body": "This is test body"
     }, 101),
])
def test_create_post(session, base_url, test_data, expected_id):
    response = session.post(f"{base_url}/posts", json=test_data)
    assert response.status_code == 201, f"Ожидался 201, получен {response.status_code}"
    actual_post = Post.model_validate(response.json())
    expected_post = Post(userId=test_data['userId'],
                    id=expected_id,
                    title=test_data['title'],
                    body=test_data['body'])
    assert actual_post == expected_post, f"Ожидался: {expected_post}, получен: {actual_post}"
