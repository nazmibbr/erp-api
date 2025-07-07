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

class SatinAlma(BaseModel):
    musteri_adi: str
    urun_kodu: str
    miktar: int

# ----- SAHTE VERİTABANI -----

urun_listesi = []
satin_alma_listesi = []

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

# Satın Alma Endpointi
@app.post("/satin-al")
def satin_al(satin_alma: SatinAlma):
    for urun in urun_listesi:
        if urun.urun_kodu == satin_alma.urun_kodu:
            if urun.stok >= satin_alma.miktar:
                urun.stok -= satin_alma.miktar
                satin_alma_listesi.append({
                    "musteri": satin_alma.musteri_adi,
                    "urun": urun.urun_adi,
                    "miktar": satin_alma.miktar,
                    "tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                return {
                    "mesaj": f"{urun.urun_adi} satın alındı. Yeni stok: {urun.stok}"
                }
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Stok yetersiz! Mevcut stok: {urun.stok}"
                )
    raise HTTPException(status_code=404, detail="Ürün bulunamadı.")

# Satın Alma Geçmişi Listeleme
@app.get("/satin-alar")
def satin_alma_gecmisi():
    return satin_alma_listesi

#  BURASINI VERİ TABANI İLE BİRLİKTE DEĞİŞTİRDİM

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import sqlite3

app = FastAPI()

# ----- VERITABANI BAĞLANTISI -----
DB_PATH = "erp_mock_database_extended.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

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

class SatinAlma(BaseModel):
    musteri_adi: str
    urun_kodu: str
    miktar: int

# ----- ENDPOINTLER -----

# Ürün Listeleme Endpointi
@app.get("/urunler")
def urunleri_getir():
    conn = get_db_connection()
    urunler = conn.execute("SELECT * FROM urunler").fetchall()
    conn.close()
    return [dict(u) for u in urunler]

# Fatura Listeleme Endpointi
@app.get("/faturalar")
def faturalar_getir():
    conn = get_db_connection()
    faturalar = conn.execute("SELECT * FROM faturalar").fetchall()
    conn.close()
    return [dict(f) for f in faturalar]

# Fatura Oluşturma ve Veritabanına Ekleme
@app.post("/fatura/olustur")
def fatura_olustur(fatura: Fatura):
    conn = get_db_connection()
    urun = conn.execute("SELECT * FROM urunler WHERE urun_adi = ?", (fatura.urun_adi,)).fetchone()
    if not urun:
        conn.close()
        raise HTTPException(status_code=404, detail="Ürün bulunamadı.")
    if urun["stok"] < fatura.miktar:
        conn.close()
        raise HTTPException(status_code=400, detail=f"Stok yetersiz! Mevcut stok: {urun['stok']}")

    yeni_stok = urun["stok"] - fatura.miktar
    toplam = round(fatura.miktar * fatura.birim_fiyat, 2)
    tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fatura_no = f"FT{datetime.now().strftime('%Y%m%d%H%M%S')}"

    conn.execute("UPDATE urunler SET stok = ? WHERE id = ?", (yeni_stok, urun["id"]))
    conn.execute("""
        INSERT INTO faturalar (fatura_no, musteri_adi, urun_adi, miktar, birim_fiyat, toplam, tarih)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (fatura_no, fatura.musteri_adi, fatura.urun_adi, fatura.miktar, fatura.birim_fiyat, toplam, tarih))
    conn.commit()
    conn.close()

    return {
        "fatura_no": fatura_no,
        "musteri": fatura.musteri_adi,
        "urun": fatura.urun_adi,
        "miktar": fatura.miktar,
        "birim_fiyat": fatura.birim_fiyat,
        "toplam": toplam,
        "kalan_stok": yeni_stok,
        "tarih": tarih
    }
