# Prediksi Tingkat Keparahan Site

Project ini membangun model Random Forest untuk memprediksi severity maintenance site: minor (0) atau major (1).

## Data
- Sumber: MySQL database datawarehouse_om
- Fitur: scope_of_work, city, month, site_major_rate
- Target: severity (mapping eksplisit minor=0, major=1)

## Alur Singkat
1. Ambil data dari MySQL (SQL join tabel fakta + dimensi)
2. Preprocessing (drop kolom id, drop null)
3. Encoding fitur kategorikal
4. Split data train/test 80:20 (stratify)
5. Train RandomForestClassifier
6. Evaluasi: Accuracy, Precision, Recall, F1, Classification Report, Confusion Matrix
7. Analisis feature importance

## Dependency
pandas, numpy, scikit-learn, matplotlib, seaborn, sqlalchemy, pymysql

## Menjalankan
1. Pastikan MySQL aktif dan database datawarehouse_om tersedia
2. Atur kredensial DB lewat environment variable (lihat .env.example)
3. Jalankan [model.ipynb](model.ipynb) dari Cell 1 sampai terakhir

Environment variable yang dipakai:
- DB_HOST
- DB_PORT
- DB_USER
- DB_PASSWORD
- DB_NAME

## Catatan
- Untuk target severity, gunakan mapping manual agar tidak tertukar: minor=0 dan major=1
- Simpan model (misal joblib) jika akan dipakai untuk inferensi di luar notebook
