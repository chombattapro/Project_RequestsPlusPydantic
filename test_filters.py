import pytest
from pydantic import TypeAdapter
from typing import List
from models import Post

def status_code_ok(response, expected=200):
    return response.status_code == expected

@pytest.mark.parametrize("user_id", (1, 3, 7))
def test_get_posts_by_userid_1(session, base_url, user_id):
    response1 = session.get(f"{base_url}/posts?userId={user_id}")
    assert status_code_ok(response1, 200), f"Ожидался 200, получен {response1.status_code}"
    all_posts1 = TypeAdapter(List[Post]).validate_python(response1.json())
    print(all_posts1)
    assert all(p.userId == user_id for p in all_posts1)

    response2 = session.get(f"{base_url}/users/{user_id}/posts")
    assert status_code_ok(response2, 200), f"Ожидался 200, получен {response2.status_code}"
    all_posts2 = TypeAdapter(List[Post]).validate_python(response2.json())
    print(all_posts2)
    assert all(p.userId == user_id for p in all_posts2)

    assert len(all_posts1) == len(all_posts2), f"Посты user {user_id}: v1{len(all_posts1)} и v2{len(all_posts2)}"

    set_ids_response1 = set(p.id for p in all_posts1)
    set_ids_response2 = set(p.id for p in all_posts2)
    assert set_ids_response1 == set_ids_response2, f"Различия: v1{set_ids_response1} и v2{set_ids_response2}"
