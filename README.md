# Prediksi Maintenance: Apakah Perbaikan Ringan atau Berat?

**Tujuan Proyek:** Membuat model data mining yang bisa memprediksi apakah sebuah pekerjaan maintenance akan ringan (minor) atau berat (major).

## Masalah & Solusi

**Masalah:** 
Dalam data maintenance, kasus ringan lebih banyak dari kasus berat. Jadi model AI cenderung "malas" memprediksi kasus berat karena jarang bertemu. Seperti dokter yang lebih familiar dengan pasien flu daripada pasien kanker.

**Solusi:** 
Kami mengurangi jumlah data kasus ringan (supaya seimbang dengan kasus berat), tapi tidak terlalu banyak dikurangi. Strategi ini membuat model bisa "belajar" dengan seimbang tanpa kehilangan banyak informasi.

## Hasil (Akurasi)

Model ini bisa memprediksi dengan benar **77% dari waktu**.

Ini artinya: Dari 100 kasus maintenance, model akan memprediksi dengan tepat sekitar 77 kasus.

## Cara Kerja (3 Langkah Utama)

### 1️⃣ Data Preparation (Persiapan)
- Ambil data dari database
- Bersihkan data yang tidak valid
- Pisahkan data untuk training (80%) dan testing (20%)
- Seimbangkan antara kasus ringan dan berat

### 2️⃣ Modeling (Membangun Model)
- Ajarkan model dengan data training
- Coba berbagai pengaturan untuk mendapatkan model terbaik
- Simpan model yang paling akurat

### 3️⃣ Evaluation (Evaluasi)
- Uji model dengan data testing
- Lihat akurasi dan performa

## Cara Menjalankan

### 1. Setup
Buka terminal dan jalankan:
```bash
pip install pandas numpy scikit-learn imbalanced-learn matplotlib seaborn sqlalchemy pymysql
```

Lalu buat file `.env` dengan isi:
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=password_anda
DB_NAME=datawarehouse_om
```

### 2. Jalankan Model
Buka Jupyter Notebook:
```bash
jupyter notebook model.ipynb
```

Tekan "Run All" atau jalankan cell demi cell dari atas ke bawah.

## Data yang Dipakai

- **Sumber:** Database MySQL (datawarehouse_om)
- **Informasi yang dipakai:** Bulan, jenis pekerjaan, kota, lokasi
- **Yang diprediksi:** Apakah perbaikan ringan atau berat

## Mengapa Strategi Ini Dipilih?

Model kami menggunakan strategi khusus (sampling_strategy=0.6) karena:
1. **Tidak kehilangan banyak data** - Hanya mengurangi 20% data ringan
2. **Tetap realistis** - Dalam dunia nyata, maintenance ringan memang lebih sering
3. **Hasil akurat** - Strategi ini memberikan akurasi 77%, lebih baik dari strategi lain

## File Penting

- `model.ipynb` - File utama (model)
- `README.md` - Dokumentasi ini
- `.env` - Konfigurasi database
