import os
import pytest
from pydantic import ValidationError
from models import Comment

@pytest.fixture(scope="session")
def post_id():
    """
    Определяем номер поста для проверки
    """
    return 1

@pytest.fixture
def output_dir(tmp_path):
    """
    Используем временную директорию pytest для файлов
    """
    return tmp_path

def test_comments_to_documents(session, base_url, post_id, output_dir):
    """
    1) Забираем все комментарии для поста
    """
    response = session.get(f"{base_url}/comments", params={"postId": post_id})
    assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
    comments_json = response.json()
    """
    Валидация каждого комментария через Pydantic
    """
    valid_comments = []
    for item in comments_json:
        try:
            c = Comment.model_validate(item)
            valid_comments.append(c)
        except ValidationError as e:
            pytest.fail(f"Некорректный формат комментария: {item}. Ошибка: {e}")
    """
    2) Создание документов по количеству комментариев
    """
    created_files = []
    try:
        for idx, c in enumerate(valid_comments, start=1):
            line = f"{c.name} ({c.email}) сказал `{c.body}`"
            print(line)
            filename = os.path.join(output_dir, f"comment_{post_id}_{idx}.txt")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(line)
            created_files.append(filename)
        """
        3) Проверка, что файлы созданы и содержат корректный текст
        """
        for idx, c in enumerate(valid_comments, start=1):
            filename = os.path.join(output_dir, f"comment_{post_id}_{idx}.txt")
            assert os.path.exists(filename), f"Файл не создан: {filename}"
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
            expected_line = f"{c.name} ({c.email}) сказал `{c.body}`"
            assert content == expected_line, (
                f"Контент файла некорректен в {filename}. "
                f"Ожидалось: {expected_line!r}, Получено: {content!r}"
            )
        """
        4) Сообщение об успехе и удаление файлов
        """
        for fpath in created_files:
            os.remove(fpath)
        """
        Валидация удаления
        """
        for fpath in created_files:
            assert not os.path.exists(fpath), f"Файл не удалён: {fpath}"
        print(f"Test passed: все файлы созданы и удалены: {created_files}")

    except Exception as exc:
        """
        5) В любом случае очищаем созданные файлы и сообщаем об ошибке
        """
        for fpath in created_files:
            if os.path.exists(fpath):
                os.remove(fpath)
        pytest.fail(f"Неудача в тесте: {exc}")
