import httpx
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Dict

# --- Pydantic Modelleri ---
class Book(BaseModel):
    """Kitap verisini modelleyen Pydantic modeli."""
    isbn: str = Field(..., description="Kitabın ISBN numarası")
    title: str = Field(..., description="Kitap başlığı")
    author: str = Field(..., description="Yazar(lar)")
    publication_year: int | None = Field(default=None, description="Yayınlanma Yılı")

class IsbnModel(BaseModel):
    """POST isteğinde alınacak ISBN verisi için model."""
    isbn: str

# --- Kütüphane Mantığı ---

# Veritabanı yerine geçecek basit bir in-memory sözlük
# Key: ISBN, Value: Book modeli
library_db: Dict[str, Book] = {}

class Library:
    """Kütüphane işlemlerini yöneten sınıf."""

    def get_all_books(self) -> List[Book]:
        """Kütüphanedeki tüm kitapları listeler."""
        return list(library_db.values())

    def remove_book(self, isbn: str) -> bool:
        """Verilen ISBN'e sahip kitabı kütüphaneden siler."""
        if isbn in library_db:
            del library_db[isbn]
            return True
        return False

    async def add_book_by_isbn(self, isbn: str) -> Book:
        """Open Library API'sini kullanarak ISBN ile kitap bulur ve kütüphaneye ekler."""
        if isbn in library_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Book with ISBN {isbn} already exists."
            )

        api_url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(api_url)
                response.raise_for_status()  # HTTP 4xx/5xx hatalarında exception fırlatır
                data = response.json()
            except httpx.RequestError as exc:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Error while requesting from Open Library: {exc}"
                )

        book_data = data.get(f"ISBN:{isbn}")
        if not book_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ISBN {isbn} not found in Open Library."
            )

        # Gelen veriden Book modelini oluştur
        new_book = Book(
            isbn=isbn,
            title=book_data.get("title", "N/A"),
            author=", ".join([author["name"] for author in book_data.get("authors", [])]),
            publication_year=int(book_data.get("publish_date", "0").split()[-1]) if book_data.get("publish_date") else None
        )

        # Kitabı veritabanına ekle
        library_db[new_book.isbn] = new_book
        return new_book

# --- FastAPI Uygulaması ---

app = FastAPI(
    title="Kütüphane API",
    description="FastAPI ile Open Library entegrasyonlu basit kütüphane servisi.",
    version="1.0.0",
)

library = Library()

@app.get("/books", response_model=List[Book])
async def get_books():
    """Kütüphanedeki tüm kitapların listesini döndürür."""
    return library.get_all_books()

@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(isbn_model: IsbnModel):
    """ISBN kullanarak Open Library'den bir kitabı kütüphaneye ekler."""
    return await library.add_book_by_isbn(isbn_model.isbn)

@app.delete("/books/{isbn}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(isbn: str):
    """Belirtilen ISBN'e sahip kitabı kütüphaneden siler."""
    success = library.remove_book(isbn)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ISBN {isbn} not found."
        )
    return
