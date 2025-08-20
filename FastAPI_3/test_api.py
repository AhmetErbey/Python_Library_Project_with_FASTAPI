import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock

# Testleri çalıştırmadan önce api.py'nin import edilebilir olduğundan emin olun.
# Bu dosyanın api.py ile aynı dizinde olduğunu varsayıyoruz.
from api import app, library_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_db_before_each_test():
    """Her testten önce veritabanını temizler."""
    library_db.clear()
    yield # test çalışır


def test_get_books_empty():
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == []

@patch('api.httpx.AsyncClient.get')
async def test_create_book_success(mock_get):
    isbn = "978-0134494166" # Effective C++
    
    # Mock API yanıtı
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        f"ISBN:{isbn}": {
            "title": "Effective C++",
            "authors": [{"name": "Scott Meyers"}],
            "publish_date": "2005"
        }
    }
    
    # asenkron context manager'ı mock'lamak için
    async def async_magic_mock(*args, **kwargs):
        return mock_response

    mock_get.return_value = await async_magic_mock()

    # POST isteği
    response = client.post("/books", json={"isbn": isbn})
    
    # Yanıtı kontrol et
    assert response.status_code == 201
    data = response.json()
    assert data["isbn"] == isbn
    assert data["title"] == "Effective C++"
    assert data["author"] == "Scott Meyers"
    assert data["publication_year"] == 2005
    
    # Veritabanını kontrol et
    assert len(library_db) == 1
    assert library_db[isbn].title == "Effective C++"

def test_create_book_already_exists():
    # Önce bir kitap ekleyelim
    isbn = "12345"
    library_db[isbn] = Mock(isbn=isbn, title="Existing Book")

    response = client.post("/books", json={"isbn": isbn})
    assert response.status_code == 409 # Conflict

@patch('api.httpx.AsyncClient.get')
async def test_delete_book(mock_get):
    isbn = "978-0134494166"
    
    # Kitabı eklemek için create_book testindeki mock'u kullanalım
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        f"ISBN:{isbn}": {
            "title": "Effective C++",
            "authors": [{"name": "Scott Meyers"}],
            "publish_date": "2005"
        }
    }
    async def async_magic_mock(*args, **kwargs):
        return mock_response
    mock_get.return_value = await async_magic_mock()
    client.post("/books", json={"isbn": isbn})
    
    # Kitabın eklendiğini doğrula
    assert len(library_db) == 1

    # Silme isteği
    delete_response = client.delete(f"/books/{isbn}")
    assert delete_response.status_code == 204
    
    # Veritabanının boş olduğunu doğrula
    assert len(library_db) == 0

def test_delete_book_not_found():
    response = client.delete("/books/non-existent-isbn")
    assert response.status_code == 404
