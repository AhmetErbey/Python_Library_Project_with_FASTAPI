import json
import os

class Book:
    """Her bir kitabı temsil eden sınıf."""
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn

    def __str__(self) -> str:
        return f'"{self.title}" by {self.author} (ISBN: {self.isbn})'

    def to_dict(self) -> dict:
        """Book nesnesini sözlük formatına çevirir."""
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn
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

    def add_book(self, book: Book):
        """Yeni bir kitabı kütüphaneye ekler."""
        if self.find_book(book.isbn):
            print(f"Hata: {book.isbn} ISBN numaralı kitap zaten mevcut.")
            return
        self.books.append(book)
        self.save_books()
        print(f"'{book.title}' kütüphaneye eklendi.")

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
        print("\n--- Kütüphane Menüsü ---")
        print("1. Kitap Ekle")
        print("2. Kitap Sil")
        print("3. Kitapları Listele")
        print("4. Kitap Ara")
        print("5. Çıkış")

        choice = input("Seçiminiz (1-5): ")

        if choice == '1':
            title = input("Kitap Başlığı: ")
            author = input("Yazar: ")
            isbn = input("ISBN: ")
            if title and author and isbn:
                library.add_book(Book(title, author, isbn))
            else:
                print("Hata: Tüm alanlar doldurulmalıdır.")
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
