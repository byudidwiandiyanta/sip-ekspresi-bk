# Draf Uraian Ciptaan untuk Pencatatan Hak Cipta Program Komputer

## Judul Ciptaan

**SIP-Ekspresi BK: Sistem Pengenalan Ekspresi Wajah Berbasis Streamlit untuk Pendampingan Bimbingan dan Konseling**

## Jenis Ciptaan

Program komputer.

## Deskripsi Singkat Ciptaan

SIP-Ekspresi BK adalah program komputer berbasis web yang dikembangkan dengan Streamlit untuk membantu kegiatan bimbingan dan konseling melalui pengenalan ekspresi wajah dari gambar atau input kamera. Program ini memuat modul input citra, deteksi wajah, prapemrosesan citra, klasifikasi ekspresi wajah menggunakan model deep learning, visualisasi hasil prediksi, catatan interpretatif non-diagnostik, serta pencatatan log observasi sesi.

Program ini dirancang sebagai alat bantu observasi awal, bukan sebagai alat diagnosis psikologis. Hasil pengenalan ekspresi digunakan untuk membantu konselor membuka percakapan dan memahami kondisi awal peserta bimbingan secara lebih terstruktur.

## Fungsi Utama Program

1. Menerima input gambar melalui unggahan file atau kamera.
2. Mendeteksi area wajah pada gambar.
3. Melakukan prapemrosesan citra wajah menjadi format yang sesuai dengan model.
4. Mengklasifikasikan ekspresi wajah ke dalam tujuh kategori: marah, jijik, takut/cemas, senang, netral, sedih, dan terkejut.
5. Menampilkan probabilitas prediksi dan confidence model.
6. Menyediakan catatan interpretatif yang membantu konselor melakukan tindak lanjut non-diagnostik.
7. Menyediakan log observasi sesi dan ekspor ke format CSV.
8. Menampilkan batasan etika penggunaan agar aplikasi tidak disalahgunakan sebagai alat diagnosis otomatis.

## Keunikan Program

Keunikan program terletak pada integrasi model pengenalan ekspresi wajah dengan alur kerja bimbingan dan konseling. Aplikasi tidak hanya memberikan label ekspresi, tetapi juga menyajikan penjelasan interpretatif yang hati-hati, log observasi, dan batasan etika penggunaan. Program dikembangkan sebagai perangkat lunak siap pakai berbasis Streamlit sehingga dapat dijalankan secara lokal maupun dideploy pada layanan cloud.

## Komponen yang Diklaim sebagai Ciptaan

1. Source code aplikasi Streamlit.
2. Source code notebook pelatihan dan ekspor model.
3. Desain alur pemrosesan citra dan inferensi.
4. Desain antarmuka pengguna.
5. Modul interpretasi non-diagnostik untuk konteks bimbingan dan konseling.
6. Dokumentasi penggunaan dan deploy.

## Komponen yang Tidak Diklaim sebagai Ciptaan

Dataset publik FER2013 atau dataset pihak ketiga lain yang digunakan untuk pelatihan tidak diklaim sebagai ciptaan. Dataset hanya digunakan sebagai bahan pelatihan model sesuai ketentuan penyedia dataset.

## Bahasa Pemrograman dan Pustaka

Program dikembangkan menggunakan Python dengan pustaka utama Streamlit, TensorFlow/Keras, OpenCV, NumPy, Pandas, Pillow, scikit-learn, dan Matplotlib.

## Catatan Etika

Program tidak ditujukan untuk diagnosis klinis, asesmen psikologis formal, atau pengambilan keputusan otomatis terhadap peserta didik. Penggunaan program harus memperhatikan persetujuan subjek, privasi data, dan pendampingan profesional.