import json
import os
import httpx

class Book:
    """Her bir kitabı temsil eden sınıf."""
    def __init__(self, title: str, author: str, isbn: str, publication_year: int | None = None):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publication_year = publication_year

    def __str__(self) -> str:
        year_str = f", {self.publication_year}" if self.publication_year else ""
        return f'"{self.title}" by {self.author} (ISBN: {self.isbn}{year_str})'

    def to_dict(self) -> dict:
        """Book nesnesini sözlük formatına çevirir."""
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "publication_year": self.publication_year
        }

class Library:
    """Kütüphane operasyonlarını yöneten sınıf."""
    def __init__(self, filename: str = "library.json"):
        self.filename = filename
        self.books = []
        self.load_books()

    def load_books(self):
        """JSON dosyasından kitapları yükler."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    books_data = json.load(f)
                    self.books = [Book(**data) for data in books_data]
                    print(f"{len(self.books)} kitap {self.filename} dosyasından yüklendi.")
            except (json.JSONDecodeError, TypeError):
                print(f"Uyarı: {self.filename} dosyası okunamadı veya formatı bozuk.")
                self.books = []
        else:
            print(f"Bilgi: {self.filename} bulunamadı. Yeni bir kütüphane oluşturuluyor.")

    def save_books(self):
        """Kütüphanedeki kitapları JSON dosyasına kaydeder."""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([book.to_dict() for book in self.books], f, indent=4, ensure_ascii=False)

    def add_book_by_isbn(self, isbn: str):
        """Open Library API'sini kullanarak ISBN ile kitap bulur ve kütüphaneye ekler."""
        if self.find_book(isbn):
            print(f"Hata: {isbn} ISBN numaralı kitap zaten kütüphanede mevcut.")
            return

        api_url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
        print(f"{isbn} için Open Library'den bilgi alınıyor...")

        try:
            response = httpx.get(api_url)
            response.raise_for_status() # HTTP 4xx/5xx hatalarında exception fırlatır
            data = response.json()
        except httpx.RequestError as exc:
            print(f"API isteği sırasında bir hata oluştu: {exc}")
            return
        except json.JSONDecodeError:
            print("API'den gelen yanıt JSON formatında değil.")
            return

        book_data = data.get(f"ISBN:{isbn}")
        if not book_data:
            print(f"Hata: {isbn} ISBN numarası ile Open Library'de kitap bulunamadı.")
            return

        title = book_data.get("title", "N/A")
        authors = [author["name"] for author in book_data.get("authors", [])]
        author_str = ", ".join(authors) if authors else "N/A"
        
        # Yayınlanma yılını al ve sadece yıl kısmını sakla
        publish_date = book_data.get("publish_date")
        publication_year = None
        if publish_date:
            try:
                # Genellikle 'July 2006' gibi formatlarda gelir, son kelimeyi alırız
                publication_year = int(publish_date.split()[-1])
            except (ValueError, IndexError):
                publication_year = None # Sayıya çevrilemezse None bırak

        new_book = Book(title, author_str, isbn, publication_year)
        self.books.append(new_book)
        self.save_books()
        print(f"Başarıyla eklendi: {new_book}")

    def remove_book(self, isbn: str):
        """ISBN'e göre bir kitabı siler."""
        book_to_remove = self.find_book(isbn)
        if book_to_remove:
            self.books.remove(book_to_remove)
            self.save_books()
            print(f"{isbn} ISBN numaralı kitap silindi.")
        else:
            print(f"Hata: {isbn} ISBN numaralı kitap bulunamadı.")

    def list_books(self):
        """Kütüphanedeki tüm kitapları listeler."""
        if not self.books:
            print("Kütüphanede hiç kitap yok.")
            return
        print("--- Kütüphanedeki Kitaplar ---")
        for book in self.books:
            print(book)
        print("---------------------------")

    def find_book(self, isbn: str) -> Book | None:
        """ISBN'e göre bir kitabı bulur."""
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

def main_menu(library: Library):
    """Kullanıcıya ana menüyü sunar ve işlemleri yönetir."""
    while True:
        print("\n--- Kütüphane Menüsü (API Destekli) ---")
        print("1. Kitap Ekle (ISBN ile)")
        print("2. Kitap Sil")
        print("3. Kitapları Listele")
        print("4. Kitap Ara")
        print("5. Çıkış")

        choice = input("Seçiminiz (1-5): ")

        if choice == '1':
            isbn = input("Eklenecek kitabın ISBN'i: ")
            if isbn:
                library.add_book_by_isbn(isbn)
            else:
                print("Hata: ISBN boş olamaz.")
        elif choice == '2':
            isbn = input("Silinecek kitabın ISBN'i: ")
            library.remove_book(isbn)
        elif choice == '3':
            library.list_books()
        elif choice == '4':
            isbn = input("Aranacak kitabın ISBN'i: ")
            book = library.find_book(isbn)
            if book:
                print("Kitap bulundu:")
                print(book)
            else:
                print("Bu ISBN ile bir kitap bulunamadı.")
        elif choice == '5':
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim. Lütfen 1-5 arasında bir numara girin.")

if __name__ == "__main__":
    my_library = Library()
    main_menu(my_library)
