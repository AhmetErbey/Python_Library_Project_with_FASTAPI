# Aşama 2: Harici API ile Veri Zenginleştirme

Bu aşama, Aşama 1'deki uygulamayı Open Library API'sine bağlayarak kitap bilgilerini ISBN ile otomatik olarak çeker hale getirir.

## Teknik Gereksinimler

- `httpx` kütüphanesi

## Kurulum ve Çalıştırma

1. Bu dizine gidin:
   ```bash
   cd stage_2
   ```

2. Gerekli kütüphaneleri kurun:
   ```bash
   pip install -r requirements.txt
   ```

3. Uygulamayı çalıştırın:
   ```bash
   python main.py
   ```

## Testleri Çalıştırma

Proje bağımlılıkları kurulduktan sonra testleri doğrudan çalıştırabilirsiniz.

```bash
pip install -r requirements.txt # Zaten yapıldıysa bu adımı atlayabilirsiniz.
pytest
```
