# ERP API (Python + FastAPI)

ERP için fatura kesme ve satın alma endpoint, 

## Özellikler şunlar (Endpointler)

-  Ürün ekleme → `POST /urun/ekle`
-  Ürün listeleme → `GET /urunler`
-  Stok güncelleme → `PUT /urun/stok-guncelle/{urun_kodu}`
-  Fatura kesme → `POST /fatura/olustur` (stoktan otomatik düşer)
-  Satın alma → `POST /satin-al`

## Kullanılan Teknolojiler

- Python
- FastAPI
- Pydantic

## Uygulama Nasıl Çalıştırılır?

1. Gerekli paketler:
   ```
   pip install -r requirements.txt
   ```

2. Sunucuyu başlat:
   ```
   uvicorn main:app --reload
   ```

3. API'yı test et:
   - `http://127.0.0.1:8000/docs` üzerinden Swagger arayüzünü kullanabilirsiniz.

## Not

## Veritabanı Kullanımı

Bu projede SQLite veritabanı (`erp_mock_database_extended.db`) kullandım. Veritabanı bağlantısı doğrudan `main.py` içerisinde kuruludur.

Veri yapısı: 30 ürün ve 30 örnek fatura kaydı içerir.

