# Python_Library_Project_with_FASTAPI
# Python Kütüphane Projesi (Bootcamp Final Projesi)

Bu proje, Python 202 Bootcamp'i kapsamında geliştirilmiş olup, Nesne Yönelimli Programlama (OOP), harici API kullanımı ve FastAPI ile kendi web API'nizi oluşturma konularını bir araya getiren üç aşamalı bir uygulamadır.

## Proje Yapısı

Proje, her biri bir önceki aşamanın üzerine inşa edilen üç ayrı klasörden oluşur:

-   **/Opp_1:** OOP prensipleriyle geliştirilmiş, verileri `library.json` dosyasında saklayan temel bir komut satırı (CLI) kütüphane uygulaması.
-   **/API_2:** Aşama 1'deki uygulamayı, Open Library API'sini kullanarak ISBN ile kitap bilgilerini otomatik olarak getirecek şekilde zenginleştiren sürüm.
-   **/FastAPI_3:** Kütüphane mantığını bir web servisi olarak sunan, FastAPI ile geliştirilmiş bir REST API.

---

## Kurulum

Öncelikle projeyi bilgisayarınıza klonlayın:

```bash
git clone https://github.com/AhmetErbey/PythonLibraryProject_with_FASTAPI.git
cd PythonLibraryProject_with_FASTAPI
```

Her aşamanın kendi bağımlılıkları vardır ve ilgili klasörün içindeki `requirements.txt` dosyasından kurulmalıdır.

---

## Kullanım ve Çalıştırma

### Aşama 1: OOP Terminal Uygulaması

1.  Aşama 1 dizinine gidin:
    ```bash
    cd Opp_1
    ```
2.  Gerekli test kütüphanesini kurun:
    ```bash
    pip install -r requirements.txt
    ```
3.  Uygulamayı çalıştırın:
    ```bash
    python main.py
    ```

### Aşama 2: Harici API Entegrasyonlu Terminal Uygulaması

1.  Aşama 2 dizinine gidin:
    ```bash
    cd API_2
    ```
2.  Gerekli kütüphaneleri kurun:
    ```bash
    pip install -r requirements.txt
    ```
3.  Uygulamayı çalıştırın:
    ```bash
    python main.py
    ```

### Aşama 3: FastAPI Web Servisi

1.  Aşama 3 dizinine gidin:
    ```bash
    cd FastAPI_3
    ```
2.  Gerekli kütüphaneleri kurun:
    ```bash
    pip install -r requirements.txt
    ```
3.  API sunucusunu başlatın:
    ```bash
    uvicorn api:app --reload
    ```
4.  Tarayıcınızda [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) adresine giderek interaktif API dokümantasyonunu görüntüleyebilirsiniz.

---

## API Dokümantasyonu (Aşama 3)

API, aşağıdaki endpoint'leri sunmaktadır:

-   **`GET /books`**
    -   **Açıklama:** Kütüphanede kayıtlı olan tüm kitapları listeler.
    -   **Cevap:** `200 OK` - Kitap listesini içeren bir JSON dizisi.

-   **`POST /books`**
    -   **Açıklama:** Verilen ISBN numarasını kullanarak Open Library API'sinden kitap bilgilerini alır ve kütüphaneye ekler.
    -   **Request Body:**
        ```json
        {
          "isbn": "978-0321765723"
        }
        ```
    -   **Cevap:** `200 OK` - Eklenen kitabın bilgileri. `404 Not Found` - Kitap bulunamazsa.

-   **`DELETE /books/{isbn}`**
    -   **Açıklama:** Belirtilen ISBN'e sahip kitabı kütüphaneden siler.
    -   **Path Parametresi:** `isbn` (string)
    -   **Cevap:** `200 OK` - Başarılı silme mesajı. `404 Not Found` - Kitap bulunamazsa.

---

## Testleri Çalıştırma

Her aşamanın kendi testleri vardır. Testleri çalıştırmak için ilgili aşamanın dizinine gidin, bağımlılıkları kurun ve `pytest` komutunu çalıştırın.

**Örnek (Aşama 2 için):**

```bash
cd API_2
pip install -r requirements.txt
pytest
```
