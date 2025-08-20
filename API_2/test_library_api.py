import pytest
import os
from unittest.mock import patch, Mock
from main import Library

@pytest.fixture
def library_fixture():
    """Her test için temiz bir Library nesnesi ve test dosyası oluşturur."""
    test_filename = "test_library_stage2.json"
    if os.path.exists(test_filename):
        os.remove(test_filename)
    
    library = Library(filename=test_filename)
    
    yield library
    
    if os.path.exists(test_filename):
        os.remove(test_filename)

@patch('main.httpx.get')
def test_add_book_by_isbn_success(mock_get, library_fixture: Library):
    """API'den başarılı bir yanıt geldiğinde kitabın eklenmesini test eder."""
    isbn = "978-0321765723" # The C++ Programming Language
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        f"ISBN:{isbn}": {
            "title": "The C++ Programming Language",
            "authors": [{"name": "Bjarne Stroustrup"}],
            "publish_date": "May 2013"
        }
    }
    mock_get.return_value = mock_response

    library_fixture.add_book_by_isbn(isbn)

    assert len(library_fixture.books) == 1
    added_book = library_fixture.find_book(isbn)
    assert added_book is not None
    assert added_book.title == "The C++ Programming Language"
    assert added_book.author == "Bjarne Stroustrup"
    assert added_book.publication_year == 2013

@patch('main.httpx.get')
def test_add_book_by_isbn_not_found(mock_get, library_fixture: Library):
    """API'de kitap bulunamadığında (404) ne olduğunu test eder."""
    isbn = "0000000000000"
    mock_response = Mock()
    mock_response.status_code = 200 # API 404 dönmüyor, boş data dönüyor
    mock_response.json.return_value = {}
    mock_get.return_value = mock_response

    library_fixture.add_book_by_isbn(isbn)

    assert len(library_fixture.books) == 0 # Kitap eklenmemeli

@patch('main.httpx.get')
def test_add_book_api_error(mock_get, library_fixture: Library):
    """API isteği başarısız olduğunda ne olduğunu test eder."""
    isbn = "1111111111111"
    # httpx.RequestError fırlatmasını simüle et
    mock_get.side_effect = pytest.importorskip("httpx").RequestError("Network error")

    library_fixture.add_book_by_isbn(isbn)

    assert len(library_fixture.books) == 0 # Kitap eklenmemeli
