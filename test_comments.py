import pytest
from pydantic import ValidationError, TypeAdapter
from models import Comment
from typing import List

@pytest.mark.parametrize("post_id", (1, 50, 100))
def test_comments_to_documents(session, base_url, post_id, tmp_path):
    # 1) Забираем все комментарии для поста
    response = session.get(f"{base_url}/comments", params={"postId": post_id})
    assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
    comments_json = response.json()

    # Валидация через TypeAdapter
    comments_adapter = TypeAdapter(List[Comment])
    try:
        valid_comments = comments_adapter.validate_python(comments_json)
    except ValidationError as e:
        pytest.fail(f"Некорректный формат комментариев: {comments_json}. Ошибка: {e}")

    # 2) Создание документов по количеству комментариев
    created_files = []
    for idx, c in enumerate(valid_comments, start=1):
        line = f"{c.name} ({c.email}) сказал `{c.body}`"
        print(line)
        filename = tmp_path / f"comment_{post_id}_{idx}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(line)
        created_files.append(str(filename))

    # 3) Проверка, что файлы созданы и содержат корректный текст
    for idx, c in enumerate(valid_comments, start=1):
        filename = tmp_path / f"comment_{post_id}_{idx}.txt"
        assert filename.exists(), f"Файл не создан: {filename}"
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        expected_line = f"{c.name} ({c.email}) сказал `{c.body}`"
        assert content == expected_line, (
            f"Контент файла некорректен в {filename}. "
            f"Ожидалось: {expected_line!r}, Получено: {content!r}"
        )
