import pytest
import os
from main import Book, Library

@pytest.fixture
def library_fixture():
    """Her test için temiz bir Library nesnesi ve test dosyası oluşturur."""
    test_filename = "test_library.json"
    # Test öncesi varsa eski test dosyasını sil
    if os.path.exists(test_filename):
        os.remove(test_filename)
    
    library = Library(filename=test_filename)
    
    yield library  # Testin çalışacağı nokta
    
    # Test sonrası test dosyasını temizle
    if os.path.exists(test_filename):
        os.remove(test_filename)

def test_add_book(library_fixture: Library):
    book = Book("Test Title", "Test Author", "1234567890")
    library_fixture.add_book(book)
    assert len(library_fixture.books) == 1
    assert library_fixture.books[0].title == "Test Title"

def test_remove_book(library_fixture: Library):
    book = Book("Another Book", "Another Author", "0987654321")
    library_fixture.add_book(book)
    assert len(library_fixture.books) == 1

    library_fixture.remove_book("0987654321")
    assert len(library_fixture.books) == 0

def test_find_book(library_fixture: Library):
    book = Book("Find Me", "Finder", "1122334455")
    library_fixture.add_book(book)
    
    found_book = library_fixture.find_book("1122334455")
    assert found_book is not None
    assert found_book.title == "Find Me"
    
    not_found_book = library_fixture.find_book("0000000000")
    assert not_found_book is None

def test_persistence(library_fixture: Library):
    """Kitapların dosyaya kaydedilip tekrar yüklendiğini test eder."""
    book1 = Book("Persistent Book 1", "Author 1", "1010101010")
    book2 = Book("Persistent Book 2", "Author 2", "2020202020")
    library_fixture.add_book(book1)
    library_fixture.add_book(book2)

    # Yeni bir Library nesnesi oluşturarak verilerin yüklenip yüklenmediğini kontrol et
    new_library = Library(filename=library_fixture.filename)
    assert len(new_library.books) == 2
    found_book = new_library.find_book("1010101010")
    assert found_book is not None
    assert found_book.author == "Author 1"
