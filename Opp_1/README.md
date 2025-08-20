# Aşama 1: OOP ile Terminalde Çalışan Kütüphane

Bu aşama, Nesne Yönelimli Programlama (OOP) prensipleri kullanılarak geliştirilmiş bir komut satırı kütüphane uygulamasıdır.

## Özellikler

- Kitap ekleme, silme, listeleme ve arama.
- Verilerin `library.json` dosyasında kalıcı olarak saklanması.

## Kurulum ve Çalıştırma

1. Bu dizine gidin:
   ```bash
   cd stage_1
   ```

2. Gerekli test kütüphanesini kurun:
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
