# Proyek Akhir: Menyelesaikan Permasalahan Institusi Pendidikan

## Business Understanding
Jaya Jaya Institut merupakan institusi pendidikan tinggi yang menghadapi masalah tingkat `dropout` siswa yang masih tinggi. Kondisi ini berisiko menurunkan angka kelulusan, mengganggu efektivitas program akademik, dan membuat intervensi dari pihak kampus sering terlambat dilakukan. Karena itu, proyek ini difokuskan untuk membantu institusi mendeteksi status siswa sedini mungkin berdasarkan data pendaftaran, kondisi administratif, dan performa akademik semester awal.

### Permasalahan Bisnis
- Jaya Jaya Institut belum memiliki mekanisme yang terstruktur untuk mengidentifikasi siswa yang cenderung berakhir `Dropout` dibanding `Graduate` berdasarkan data akademik dan administratif semester awal.
- Institusi belum memiliki dashboard monitoring yang secara spesifik menyoroti faktor-faktor yang membedakan kelompok `Dropout` dan `Graduate`, sehingga prioritas intervensi sering terlambat atau terlalu umum.
- Institusi belum memiliki prototype machine learning yang siap digunakan untuk membantu staf akademik memperkirakan apakah profil seorang siswa lebih dekat ke pola `Dropout` atau `Graduate`.

### Cakupan Proyek
- Melakukan analisis data siswa dari tahap business understanding sampai evaluation.
- Memfokuskan analisis pada siswa dengan status akhir `Dropout` dan `Graduate`, sedangkan siswa `Enrolled` dikeluarkan dari dashboard dan pemodelan agar sesuai dengan tujuan deteksi dini risiko dropout.
- Membangun model machine learning biner untuk memprediksi status akhir siswa: `Dropout` atau `Graduate`.
- Menyimpan model terbaik agar siap dipakai ulang pada prototype Streamlit.
- Menyusun dokumentasi proyek, kesimpulan, dan action items yang relevan untuk institusi pendidikan.
- Menyiapkan aplikasi `Streamlit` lokal yang dapat digunakan untuk melakukan prediksi status siswa.

### Persiapan
Sumber data:
- Dataset utama yang digunakan dalam submission: `data/data.csv`
- Sumber asli dataset dari repository Dicoding: `https://github.com/dicodingacademy/dicoding_dataset/tree/main/students_performance`
- File dataset asli dari repository Dicoding: `https://github.com/dicodingacademy/dicoding_dataset/blob/main/students_performance/data.csv`
- Dokumentasi dataset lokal hasil salinan referensi: `students_performance/README.md`

### Setup Environment

Instalasi package via `requirements.txt`
```bash
pip install -r requirements.txt
```

#### Anaconda
```bash
conda create --name main-ds python=3.12
conda activate main-ds
pip install -r requirements.txt
```

#### Shell/Terminal
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Menjalankan Notebook
```bash
jupyter notebook notebook.ipynb
```

### Menjalankan Prototype Sistem Machine Learning
```bash
streamlit run app.py
```

Jika aplikasi berhasil berjalan, buka URL lokal yang ditampilkan Streamlit, biasanya:
```text
http://localhost:8501
```

## Business Dashboard
Dashboard bisnis utama untuk submission ini menggunakan `Metabase`, dengan sumber data yang telah difilter agar hanya mencakup siswa berstatus `Dropout` dan `Graduate`. Dashboard ini difokuskan untuk membantu institusi memonitor indikator yang paling berkaitan dengan risiko dropout, seperti status pembayaran biaya kuliah, jumlah mata kuliah yang lulus pada semester pertama dan kedua, serta perbedaan performa antar program studi.

Metrik yang paling penting untuk dimonitor adalah:
- proporsi siswa `Dropout` dan `Graduate`;
- jumlah mata kuliah semester kedua yang berhasil diselesaikan;
- status `Tuition_fees_up_to_date`;
- jumlah mata kuliah semester pertama yang disetujui;
- distribusi risiko berdasarkan program studi dan kelompok usia.

Dashboard Metabase dirancang sebagai dashboard monitoring ringkas yang langsung menampilkan indikator utama terkait risiko dropout, performa akademik, status pembayaran biaya kuliah, kelompok usia, dan program studi yang perlu diprioritaskan untuk intervensi. Setiap visualisasi pada dashboard digunakan untuk tujuan berikut:
- `Student Status Distribution` menampilkan proporsi akhir siswa antara `Dropout` dan `Graduate` sebagai gambaran umum hasil akhir populasi yang dianalisis.
- `Tuition Status by Student Outcome` menunjukkan hubungan antara kelancaran pembayaran biaya kuliah dan status akhir siswa untuk membantu tim akademik dan keuangan memprioritaskan intervensi gabungan.
- `Dropout Rate by Gender` memperlihatkan apakah ada perbedaan tingkat dropout antar gender pada data biner yang digunakan.
- `Top Courses by Dropout Count` menunjukkan program studi dengan jumlah kasus dropout tertinggi agar evaluasi kurikulum dan dukungan akademik dapat diprioritaskan.
- `Average Approved Units by Status` membandingkan capaian approved units semester pertama dan kedua antara kelompok `Dropout` dan `Graduate`.
- `Dropout Rate by Age Band` membantu memantau kelompok usia masuk yang paling berisiko.
- `Dropout Rate by Attendance` digunakan untuk melihat apakah pola kehadiran siang atau malam berkaitan dengan risiko dropout.
- `Course Risk Table` memberikan ringkasan operasional per program studi agar tim kampus dapat langsung menentukan urutan intervensi.

Untuk menjalankan dashboard Metabase secara lokal, gunakan tahapan berikut:
```bash
docker pull metabase/metabase:v0.59.4
docker run -d -p 3000:3000 --name metabase-review -v "$(pwd)":/submission -e MB_DB_FILE=/submission/metabase.db metabase/metabase:v0.59.4
```

Setelah container aktif, akses Metabase melalui:
```text
http://localhost:3000
```

Dashboard utama dapat dibuka melalui:
```text
http://localhost:3000/dashboard/2
```

Kredensial Metabase yang digunakan:
```text
email: root@mail.com
password: root123
```

Catatan penting:
- file `metabase.db.mv.db` dan `students_performance.db` harus tetap berada pada root folder submission dalam direktori yang sama dengan `README.md`;
- dashboard yang disiapkan pada file Metabase ini bernama `Student Retention & Performance Dashboard` dan berada di collection `Jaya Jaya Institut Submission`;
- variabel `MB_DB_FILE=/submission/metabase.db` membuat Metabase membaca file `metabase.db.mv.db` yang ada di root folder submission;
- sebelum melakukan zip submission, matikan container Metabase agar file database tidak sedang terkunci;
- aplikasi `Streamlit` pada submission ini tetap dipakai sebagai prototype machine learning, sedangkan business dashboard utamanya menggunakan Metabase.

Dokumentasi visual dashboard yang disertakan pada folder submission:

- Screenshot dashboard Metabase: `himbarbuana-dashboard.png`

## Menjalankan Sistem Machine Learning
Aplikasi prototype dimuat dari model terlatih pada folder `model/student_status_pipeline.joblib`. Prototype menerima input profil siswa dan performa akademik awal, lalu menampilkan:
- prediksi status siswa;
- probabilitas untuk dua kelas akhir siswa: `Dropout` dan `Graduate`;
- highlight faktor yang paling sering berkaitan dengan risiko dropout berdasarkan hasil analisis proyek;
- simulasi `what-if` sederhana untuk melihat dampak perubahan jumlah mata kuliah semester kedua yang disetujui.

Langkah menjalankan aplikasi:
```bash
streamlit run app.py
```

Prototype juga telah di-deploy ke Streamlit Community Cloud dan dapat diakses melalui:

- `https://studentstatuspredictor.streamlit.app/`

Repository GitHub untuk deployment:

- `https://github.com/mergeconflictlover/menyelesaikan_permasalahan_institusi_pendidikan`

Struktur artefak utama yang digunakan aplikasi:
- `app.py`
- `model_utils.py`
- `model/student_status_pipeline.joblib`
- `model/metrics_summary.json`

Dokumentasi visual prototype yang disertakan pada folder submission:

- Screenshot Streamlit lokal: `localhost:8501.png`
- Screenshot Streamlit Community Cloud: `studentstatuspredictor.streamlit.app.png`

Dokumentasi video submission yang disertakan pada folder submission:

- Video penjelasan proyek: `himbarbuana-video.mp4`

## Conclusion
Proyek ini menunjukkan bahwa masalah dropout di Jaya Jaya Institut paling kuat berkaitan dengan kombinasi performa akademik awal dan kedisiplinan administrasi siswa. Fokus proyek diarahkan untuk membedakan siswa yang berakhir `Dropout` dan `Graduate`, sehingga hasil analisis dan model dapat langsung dipakai sebagai dasar intervensi retensi yang lebih praktis.

Beberapa temuan utama dari analisis dan model:
- Dataset awal berisi `4.424` siswa tanpa missing value dan tanpa data duplikat, lalu difilter menjadi `3.630` siswa dengan status akhir `Dropout` dan `Graduate` agar analisis sesuai dengan tujuan proyek.
- Distribusi target pada data final terdiri dari `Graduate` sebanyak `2.209` siswa dan `Dropout` sebanyak `1.421` siswa.
- Model terbaik adalah `Logistic Regression` dengan `accuracy 0,9160` dan `weighted f1-score 0,9150`.
- Faktor paling berpengaruh terhadap prediksi status siswa adalah `Curricular_units_2nd_sem_approved`, `Curricular_units_1st_sem_approved`, `Curricular_units_2nd_sem_enrolled`, `Tuition_fees_up_to_date`, dan `Curricular_units_1st_sem_enrolled`.
- Siswa dengan jumlah mata kuliah semester kedua yang sangat rendah, pembayaran biaya kuliah yang tidak lancar, dan capaian semester pertama yang rendah cenderung lebih dekat ke status `Dropout`, sedangkan profil yang mulai mendekati rata-rata `Graduate` umumnya memiliki capaian semester kedua sekitar `6` mata kuliah approved atau lebih.
- Evaluasi tidak hanya menggunakan accuracy, tetapi juga `precision`, `recall`, `f1-score`, `confusion matrix`, dan `feature importance`.
- Analisis lanjutan pada notebook juga menyiapkan evaluasi kelompok, sehingga model tidak hanya dilihat dari performa umum tetapi juga dari perilaku risiko pada subset tertentu seperti gender dan kelompok usia.

### Rekomendasi Action Items
- Prioritas 1: Bangun sistem peringatan dini yang menandai siswa dengan `Curricular_units_2nd_sem_approved <= 2` sebagai kandidat intervensi akademik paling mendesak. Rata-rata siswa `Dropout` hanya menyelesaikan `1,94` mata kuliah pada semester kedua, jauh di bawah kelompok `Graduate` yang berada di `6,18`, sehingga ambang ini dapat dipakai sebagai trigger awal untuk mentoring wajib, kelas remedial, dan review rencana studi dalam `1-2` minggu setelah nilai semester keluar.
- Prioritas 2: Gabungkan intervensi akademik dan finansial untuk siswa dengan `Tuition_fees_up_to_date = 0`. Pada data final, kelompok dengan pembayaran tidak mutakhir memiliki `457` kasus dropout dari `486` siswa atau sekitar `94,0%`, sehingga institusi dapat membuat daftar pantauan harian lintas akademik-keuangan, menawarkan skema cicilan atau bantuan darurat, lalu memeriksa kembali progres akademik mereka pada bulan yang sama.
- Prioritas 3: Fokuskan program retensi pada siswa usia masuk `25 tahun ke atas`, terutama kelompok `25-29` dengan dropout rate `70,2%` dan kelompok `30+` dengan dropout rate `61,4%`. Implementasi praktisnya dapat berupa mentoring singkat, jadwal konsultasi di luar jam kerja, kelas malam, atau kanal dukungan daring yang lebih fleksibel untuk segmen nontradisional ini.
- Prioritas 4: Susun daftar intervensi per program studi berdasarkan kombinasi `dropout count` dan `dropout rate`, lalu mulai evaluasi dari program dengan beban dropout tertinggi. Pendekatan ini lebih aplikatif daripada intervensi umum karena memungkinkan institusi menyesuaikan beban studi, dukungan akademik, dan kapasitas wali studi sesuai risiko masing-masing program.
- Prioritas 5: Gunakan prototipe machine learning sebagai alat triase untuk membedakan siswa yang pola akademik-awalnya lebih dekat ke `Dropout` atau `Graduate`. Siswa yang memperoleh probabilitas `Dropout` tinggi dan juga berada pada ambang approved units semester dua yang rendah harus diprioritaskan untuk intervensi paling awal.
