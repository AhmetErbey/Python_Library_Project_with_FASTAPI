# Aşama 3: FastAPI ile Kendi API'nizi Oluşturma

Bu aşama, kütüphane mantığını bir web servisi (API) haline getirir. Bu sayede verilere HTTP istekleri ile erişilebilir.

## Teknik Gereksinimler

- `fastapi`
- `uvicorn`
- `httpx`

## Kurulum ve Çalıştırma

1. Bu dizine gidin:
   ```bash
   cd stage_3
   ```

2. Gerekli kütüphaneleri kurun:
   ```bash
   pip install -r requirements.txt
   ```

3. API sunucusunu başlatın:
   ```bash
   uvicorn api:app --reload
   ```

4. Tarayıcınızda [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) adresine giderek interaktif API dokümantasyonunu görüntüleyebilir ve endpoint'leri test edebilirsiniz.

## Testleri Çalıştırma

Proje bağımlılıkları kurulduktan sonra testleri doğrudan çalıştırabilirsiniz.

```bash
pip install -r requirements.txt # Zaten yapıldıysa bu adımı atlayabilirsiniz.
pytest
```
