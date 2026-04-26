# SIP-Ekspresi BK

**SIP-Ekspresi BK** adalah prototipe program komputer berbasis Streamlit untuk mengenali ekspresi wajah sebagai alat bantu observasi awal dalam kegiatan bimbingan dan konseling. Aplikasi menerima input gambar atau kamera, mendeteksi wajah, mengklasifikasikan ekspresi, menampilkan probabilitas, serta membuat log observasi sesi.

## Batas penggunaan

Aplikasi ini **bukan alat diagnosis psikologis**, bukan alat asesmen klinis, dan tidak boleh digunakan untuk mengambil keputusan otomatis terhadap siswa atau mahasiswa. Hasil prediksi hanya berfungsi sebagai pemantik observasi awal dan harus dikonfirmasi melalui wawancara/konseling.

## Fitur

1. Input gambar melalui upload atau kamera.
2. Deteksi wajah menggunakan OpenCV Haar Cascade.
3. Klasifikasi tujuh ekspresi: marah, jijik, takut/cemas, senang, netral, sedih, dan terkejut.
4. Tampilan confidence dan distribusi probabilitas.
5. Catatan interpretasi awal untuk konselor.
6. Log observasi sesi dan unduhan CSV.
7. Siap dijalankan secara lokal atau dideploy ke Streamlit Community Cloud.

## Struktur proyek

```text
sip_ekspresi_bk_streamlit/
├── 01_train_fer2013_streamlit_ready.ipynb
├── app.py
├── requirements.txt
├── README_DEPLOY.md
├── HKI_uraian_ciptaan.md
├── MODEL_CARD.md
├── .streamlit/
│   └── config.toml
├── data/
└── models/
```

## Dataset

Notebook menggunakan dataset publik FER2013 dari Kaggle. Dataset tidak disertakan dalam paket ini. Pengguna perlu mengunduh melalui Kaggle API atau mengunggah dataset secara manual sesuai petunjuk dalam notebook.

Dataset rujukan:
- Kaggle: `msambare/fer2013`
- Format umum: folder `train/` dan `test/` dengan subfolder per kelas ekspresi.

## Instalasi cepat

Untuk panduan instalasi sangat rinci, lihat file:

```text
INSTALL_DETAIL.md
```

Aplikasi ini juga mendukung **Mode Demo**, sehingga tetap dapat dijalankan meskipun model hasil training belum tersedia. Mode ini berguna untuk uji antarmuka, demonstrasi, screenshot, dan kelengkapan awal pendaftaran HKI. Untuk klaim prediksi ilmiah, jalankan notebook training terlebih dahulu.

## Cara menjalankan lokal

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
jupyter notebook 01_train_fer2013_streamlit_ready.ipynb
```

Jalankan seluruh notebook sampai menghasilkan:

```text
models/best_fer_model.keras
models/labels.json
```

Setelah model tersedia:

```bash
streamlit run app.py
```

## Deploy ke Streamlit Community Cloud

1. Buat repository GitHub baru.
2. Unggah `app.py`, `requirements.txt`, folder `.streamlit`, `README_DEPLOY.md`, dan folder `models/` yang sudah berisi model hasil pelatihan.
3. Buka Streamlit Community Cloud.
4. Pilih repository dan file utama `app.py`.
5. Klik Deploy.
6. Uji input gambar/kamera setelah aplikasi aktif.

## Catatan HKI

Yang didaftarkan sebagai ciptaan program komputer adalah source code, desain alur aplikasi, antarmuka Streamlit, modul inferensi, dan dokumentasi program. Dataset FER2013 adalah dataset pihak ketiga dan **tidak diklaim sebagai ciptaan**.