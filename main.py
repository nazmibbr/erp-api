from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# ----- MODELLER -----

class Urun(BaseModel):
    urun_kodu: str
    urun_adi: str
    stok: int
    fiyat: float

class Fatura(BaseModel):
    musteri_adi: str
    urun_adi: str
    miktar: int
    birim_fiyat: float

# ----- SAHTE VERİTABANI -----

urun_listesi = []

# ----- ENDPOINTLER -----

# Ürün Ekleme Endpointi
@app.post("/urun/ekle")
def urun_ekle(urun: Urun):
    urun_listesi.append(urun)
    return {
        "mesaj": f"{urun.urun_adi} başarıyla eklendi.",
        "toplam_urun_sayisi": len(urun_listesi)
    }

# Ürün Listeleme Endpointi
@app.get("/urunler")
def urunleri_getir():
    return urun_listesi

# Stok Güncelleme Endpointi
@app.put("/urun/stok-guncelle/{urun_kodu}")
def stok_guncelle(urun_kodu: str, yeni_stok: int):
    for urun in urun_listesi:
        if urun.urun_kodu == urun_kodu:
            urun.stok = yeni_stok
            return {
                "mesaj": f"{urun.urun_adi} ürününün stoğu {yeni_stok} olarak güncellendi."
            }
    raise HTTPException(status_code=404, detail="Ürün bulunamadı.")

# Fatura Oluşturma ve Stok Düşme Endpointi
@app.post("/fatura/olustur")
def fatura_olustur(fatura: Fatura):
    for urun in urun_listesi:
        if urun.urun_adi.lower() == fatura.urun_adi.lower():
            if urun.stok >= fatura.miktar:
                urun.stok -= fatura.miktar
                toplam_tutar = fatura.miktar * fatura.birim_fiyat
                return {
                    "fatura_no": "FT2025001",
                    "musteri": fatura.musteri_adi,
                    "urun": fatura.urun_adi,
                    "miktar": fatura.miktar,
                    "birim_fiyat": fatura.birim_fiyat,
                    "toplam": toplam_tutar,
                    "kalan_stok": urun.stok,
                    "tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Stok yetersiz! Mevcut stok: {urun.stok}"
                )
    raise HTTPException(status_code=404, detail="Ürün bulunamadı.")
