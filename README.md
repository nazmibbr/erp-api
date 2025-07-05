# Mini ERP API (Python + FastAPI)

Bu proje, özgeçmişinizde veya GitHub profilinizde gösterebileceğiniz basit bir ERP API sistemidir. Python ile FastAPI kullanılarak yazılmıştır.

## Özellikler (Endpointler)

- ✅ Ürün ekleme → `POST /urun/ekle`
- ✅ Ürün listeleme → `GET /urunler`
- ✅ Stok güncelleme → `PUT /urun/stok-guncelle/{urun_kodu}`
- ✅ Fatura kesme → `POST /fatura/olustur` (stoktan otomatik düşer)

## Kullanılan Teknolojiler

- Python
- FastAPI
- Pydantic

## Uygulama Nasıl Çalıştırılır?

1. Gerekli paketleri yükleyin:
   ```
   pip install -r requirements.txt
   ```

2. Sunucuyu başlatın:
   ```
   uvicorn main:app --reload
   ```

3. API'yı test edin:
   - `http://127.0.0.1:8000/docs` üzerinden Swagger arayüzünü kullanabilirsiniz.

## Not

Veriler sadece geçici olarak bellekte (listede) tutulur. Gerçek bir veritabanı entegrasyonu yapılmamıştır.
