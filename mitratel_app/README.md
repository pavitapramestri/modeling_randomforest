# OM Dashboard – Mitratel (Flask)

Dashboard prediksi severity maintenance tower telekomunikasi berbasis Flask + ML.

## Struktur Folder

```
mitratel_app/
├── app.py                        # Flask backend
├── requirements.txt              # Dependencies
├── hasil_prediksi_severity.csv   # ← LETAKKAN FILE CSV DI SINI
├── templates/
│   ├── landing.html              # Landing page
│   └── dashboard.html            # Dashboard analitik
└── static/                       # (CSS/JS tambahan jika ada)
```

## Setup & Cara Menjalankan

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Letakkan File CSV
Salin file `hasil_prediksi_severity.csv` (output dari `model.ipynb`) ke dalam folder `mitratel_app/`.

Pastikan CSV memiliki kolom:
- `nama_site`
- `kota_kabupaten`
- `month`
- `scope_of_work`
- `actual_severity`
- `predicted_severity` (berisi "Minor" atau "Major")
- `confidence_score`
- `confidence_minor`
- `confidence_major`

### 3. Jalankan App
```bash
cd mitratel_app
python app.py
```

Buka browser: **http://localhost:5000**

## Halaman yang Tersedia

| URL | Keterangan |
|-----|------------|
| `/` | Landing page Mitratel |
| `/dashboard` | Dashboard analitik prediksi severity |
| `/api/sites?kota=...` | API: daftar site per kota |
| `/api/predict?kota=...&site=...` | API: hasil prediksi site |
| `/api/map-data` | API: data agregasi per kota untuk peta |

## Ringkasan Model Terbaru

- Algorithm: Random Forest + RUS
- Accuracy: 69.71%
- F1-Score: 72.94%
- CV Accuracy: 69.57% ± 0.82%
