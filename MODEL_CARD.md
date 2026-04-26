# Model Card: SIP-Ekspresi BK FER Model

## Tujuan model

Model digunakan untuk mengenali ekspresi wajah dasar dari gambar wajah tunggal sebagai alat bantu observasi awal dalam konteks bimbingan dan konseling.

## Kelas keluaran

1. angry / marah
2. disgust / jijik
3. fear / takut atau cemas
4. happy / senang
5. neutral / netral
6. sad / sedih
7. surprise / terkejut

## Data pelatihan

Model dilatih menggunakan dataset FER2013 dari Kaggle. Dataset terdiri atas gambar wajah grayscale berukuran kecil dan label ekspresi dasar. Dataset tidak disertakan di dalam paket program.

## Keterbatasan

1. Ekspresi wajah tidak selalu sama dengan keadaan emosi internal.
2. Model dapat bias terhadap pencahayaan, sudut wajah, usia, warna kulit, aksesori, dan kualitas kamera.
3. Model tidak boleh digunakan untuk diagnosis psikologis.
4. Untuk anak atau peserta didik di bawah umur, penggunaan aplikasi memerlukan persetujuan dan pendampingan etis.
5. Hasil satu gambar tidak boleh dianggap sebagai kesimpulan kondisi emosional seseorang.

## Rekomendasi penggunaan

Gunakan prediksi sebagai bahan refleksi awal dalam sesi konseling. Konselor tetap harus melakukan wawancara, observasi, serta mempertimbangkan konteks akademik, sosial, dan keluarga.