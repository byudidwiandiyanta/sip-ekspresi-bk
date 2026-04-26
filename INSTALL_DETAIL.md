# Panduan Instalasi Detail SIP-Ekspresi BK

Dokumen ini dibuat agar aplikasi dapat dijalankan untuk kebutuhan demonstrasi, dokumentasi, dan pendaftaran HKI program komputer.

## A. Mode penggunaan yang disarankan

Ada dua mode:

1. **Mode Demo / HKI awal**
   - Aplikasi langsung dapat dibuka tanpa melatih model.
   - Cocok untuk menunjukkan alur software, antarmuka, input gambar/kamera, deteksi wajah, tampilan hasil, catatan konselor, dan log observasi.
   - Akurasi tidak dijadikan klaim utama.

2. **Mode Model Terlatih**
   - Jalankan notebook `01_train_fer2013_streamlit_ready.ipynb`.
   - Model disimpan sebagai `models/best_fer_model.keras`.
   - Aplikasi menggunakan model tersebut untuk prediksi ekspresi.

Untuk kebutuhan HKI awal, Mode Demo sudah cukup untuk membuktikan bentuk program komputer. Namun, untuk publikasi atau klaim ilmiah, gunakan Mode Model Terlatih.

---

## B. Instalasi lokal di Windows

### 1. Ekstrak file ZIP

Ekstrak paket:

```text
sip_ekspresi_bk_streamlit.zip
```

Misalnya menjadi:

```text
D:\HKI\sip_ekspresi_bk_streamlit\
```

Masuk ke folder tersebut melalui Command Prompt atau Terminal:

```bash
cd D:\HKI\sip_ekspresi_bk_streamlit
```

### 2. Buat virtual environment

```bash
python -m venv .venv
```

Aktifkan environment:

```bash
.venv\Scripts\activate
```

Jika berhasil, di awal baris terminal akan muncul:

```text
(.venv)
```

### 3. Upgrade pip

```bash
python -m pip install --upgrade pip
```

### 4. Instal dependensi

```bash
pip install -r requirements.txt
```

Proses ini dapat memakan waktu karena TensorFlow cukup besar.

### 5. Jalankan aplikasi

```bash
streamlit run app.py
```

Browser akan terbuka pada alamat lokal, biasanya:

```text
http://localhost:8501
```

Jika file model belum ada, centang pilihan:

```text
Izinkan mode demo jika model belum tersedia
```

Aplikasi tetap dapat dijalankan untuk demonstrasi.

---

## C. Instalasi lokal di macOS/Linux

Masuk ke folder proyek:

```bash
cd sip_ekspresi_bk_streamlit
```

Buat virtual environment:

```bash
python3 -m venv .venv
```

Aktifkan environment:

```bash
source .venv/bin/activate
```

Upgrade pip dan instal paket:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Jalankan aplikasi:

```bash
streamlit run app.py
```

---

## D. Training model dari Kaggle

Bagian ini hanya diperlukan jika ingin menggunakan model sungguhan.

### 1. Buat akun Kaggle

Buka Kaggle, login, lalu buat API token melalui:

```text
Account > Create New API Token
```

File `kaggle.json` akan terunduh.

### 2. Siapkan kredensial Kaggle

Di Windows, letakkan file `kaggle.json` di:

```text
C:\Users\NAMA_USER\.kaggle\kaggle.json
```

Di macOS/Linux:

```text
~/.kaggle/kaggle.json
```

Untuk macOS/Linux, jalankan:

```bash
chmod 600 ~/.kaggle/kaggle.json
```

### 3. Jalankan notebook

Masih dalam virtual environment:

```bash
jupyter notebook 01_train_fer2013_streamlit_ready.ipynb
```

Jalankan cell dari atas sampai bawah. Notebook akan mengunduh dataset FER2013 dan melatih model.

Target output:

```text
models/best_fer_model.keras
models/labels.json
```

Setelah dua file itu ada, aplikasi Streamlit akan otomatis menggunakan model terlatih.

---

## E. Deploy ke Streamlit Community Cloud

### 1. Buat repository GitHub

Nama contoh:

```text
sip-ekspresi-bk
```

Upload file berikut:

```text
app.py
requirements.txt
README_DEPLOY.md
INSTALL_DETAIL.md
MODEL_CARD.md
HKI_uraian_ciptaan.md
.streamlit/config.toml
models/
```

Untuk Mode Demo, folder `models/` boleh kosong. Untuk Mode Model Terlatih, folder `models/` harus berisi:

```text
best_fer_model.keras
labels.json
```

### 2. Masuk ke Streamlit Community Cloud

Pilih:

```text
New app
```

Lalu atur:

```text
Repository: sip-ekspresi-bk
Branch: main
Main file path: app.py
```

Klik:

```text
Deploy
```

### 3. Uji aplikasi

Setelah aplikasi aktif:

- unggah gambar wajah;
- pastikan wajah terdeteksi;
- lihat ekspresi dominan;
- cek tabel probabilitas;
- cek catatan konselor;
- unduh log CSV.

---

## F. Troubleshooting

### 1. `streamlit` tidak dikenali

Pastikan virtual environment sudah aktif:

```bash
.venv\Scripts\activate
```

Lalu ulangi:

```bash
pip install -r requirements.txt
```

### 2. TensorFlow gagal terinstal

Gunakan Python versi stabil, disarankan Python 3.10 atau 3.11. Hindari Python yang terlalu baru jika TensorFlow belum mendukung penuh.

### 3. Kamera tidak muncul di browser

Periksa izin kamera pada browser. Pada beberapa browser, kamera hanya aktif pada `localhost` atau koneksi HTTPS.

### 4. Wajah tidak terdeteksi

Gunakan gambar:
- wajah frontal;
- pencahayaan cukup;
- tidak terlalu jauh;
- tidak terlalu banyak wajah dalam satu gambar.

### 5. Aplikasi berjalan, tetapi hasil prediksi terasa aneh

Jika Mode Demo aktif, hasil memang hanya untuk demonstrasi. Untuk prediksi model terlatih, jalankan notebook training terlebih dahulu.

---

## G. Catatan penting untuk HKI

Untuk pendaftaran HKI program komputer, yang disiapkan adalah:

1. source code aplikasi;
2. uraian program;
3. screenshot antarmuka;
4. manual penggunaan;
5. identitas pencipta/pemegang hak cipta;
6. pernyataan bahwa dataset pihak ketiga tidak diklaim sebagai ciptaan.

Judul ciptaan yang disarankan:

```text
SIP-Ekspresi BK: Sistem Pengenalan Ekspresi Wajah Berbasis Streamlit untuk Pendampingan Bimbingan dan Konseling
```

Hindari klaim bahwa aplikasi melakukan diagnosis psikologis. Gunakan frasa:

```text
alat bantu observasi awal
```

atau

```text
sistem pendukung pendampingan konseling
```
