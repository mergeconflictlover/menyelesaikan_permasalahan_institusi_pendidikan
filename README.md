# Proyek Akhir: Menyelesaikan Permasalahan Institusi Pendidikan

## Business Understanding
Jaya Jaya Institut merupakan institusi pendidikan tinggi yang menghadapi masalah tingkat `dropout` siswa yang masih tinggi. Kondisi ini berisiko menurunkan angka kelulusan, mengganggu efektivitas program akademik, dan membuat intervensi dari pihak kampus sering terlambat dilakukan. Karena itu, proyek ini difokuskan untuk membantu institusi mendeteksi status siswa sedini mungkin berdasarkan data pendaftaran, kondisi administratif, dan performa akademik semester awal.

### Permasalahan Bisnis
- Bagaimana karakteristik umum siswa yang berisiko `dropout`?
- Faktor apa yang paling berpengaruh terhadap status akhir siswa: `Dropout`, `Enrolled`, atau `Graduate`?
- Bagaimana pihak institusi dapat memonitor indikator penting siswa secara cepat melalui dashboard?
- Bagaimana menyediakan prototype machine learning yang siap digunakan untuk memprediksi status siswa baru atau siswa aktif?

### Cakupan Proyek
- Melakukan analisis data siswa dari tahap business understanding sampai evaluation.
- Membangun model machine learning multiclass untuk memprediksi status siswa.
- Menyimpan model terbaik agar siap dipakai ulang pada prototype Streamlit.
- Menyusun dokumentasi proyek, kesimpulan, dan action items yang relevan untuk institusi pendidikan.
- Menyiapkan aplikasi `Streamlit` lokal yang dapat digunakan untuk melakukan prediksi status siswa.

### Persiapan
Sumber data:
- Dataset utama yang digunakan dalam submission: `data/data.csv`
- Sumber asli dataset dari repository Dicoding: `https://github.com/dicodingacademy/dicoding_dataset/tree/main/students_performance`
- File dataset asli dari repository Dicoding: `https://github.com/dicodingacademy/dicoding_dataset/blob/main/students_performance/data.csv`
- Dokumentasi dataset lokal hasil salinan referensi: `students_performance/README.md`

Setup environment:

Instalasi package via `requirements.txt`
```bash
pip install -r requirements.txt
```

### Setup Environment - Anaconda
```bash
conda create --name main-ds python=3.12
conda activate main-ds
pip install -r requirements.txt
```

### Setup Environment - Shell/Terminal
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
Dashboard bisnis utama untuk submission ini menggunakan `Metabase`, mengikuti pendekatan yang sama seperti submission sebelumnya. Dashboard ini difokuskan untuk membantu institusi memonitor indikator yang paling berkaitan dengan risiko dropout, seperti status pembayaran biaya kuliah, jumlah mata kuliah yang lulus pada semester pertama dan kedua, distribusi status siswa, serta perbedaan performa antar program studi.

Metrik yang paling penting untuk dimonitor adalah:
- proporsi siswa `Dropout`, `Enrolled`, dan `Graduate`;
- jumlah mata kuliah semester kedua yang berhasil diselesaikan;
- status `Tuition_fees_up_to_date`;
- jumlah mata kuliah semester pertama yang disetujui;
- distribusi risiko berdasarkan program studi dan kelompok usia.

Dashboard Metabase dirancang sebagai dashboard monitoring ringkas yang langsung menampilkan indikator utama terkait risiko dropout, performa akademik, status pembayaran biaya kuliah, kelompok usia, dan program studi yang perlu diprioritaskan untuk intervensi.

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

Dashboard alternatif juga dibuat menggunakan Looker Studio dan dapat diakses melalui:

- `https://lookerstudio.google.com/reporting/5927d08e-c3b1-4f24-a10e-fe8f5b0b7b5f`

Dokumentasi visual Looker Studio yang disertakan pada folder submission:

- Screenshot dashboard Looker Studio: `lookerstudio.google.com.png`

## Menjalankan Sistem Machine Learning
Aplikasi prototype dimuat dari model terlatih pada folder `model/student_status_pipeline.joblib`. Prototype menerima input profil siswa dan performa akademik awal, lalu menampilkan:
- prediksi status siswa;
- probabilitas untuk setiap kelas;
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
Proyek ini menunjukkan bahwa masalah dropout di Jaya Jaya Institut paling kuat berkaitan dengan kombinasi performa akademik awal dan kedisiplinan administrasi siswa.

Beberapa temuan utama dari analisis dan model:
- Dataset berisi `4.424` siswa tanpa missing value dan tanpa data duplikat.
- Distribusi target didominasi oleh `Graduate` sebanyak `2.209` siswa, disusul `Dropout` sebanyak `1.421` siswa, dan `Enrolled` sebanyak `794` siswa.
- Model terbaik adalah `Gradient Boosting` dengan `accuracy 0,7661` dan `weighted f1-score 0,7547`.
- Faktor paling berpengaruh terhadap prediksi status siswa adalah `Curricular_units_2nd_sem_approved`, `Tuition_fees_up_to_date`, `Curricular_units_1st_sem_approved`, `Course`, dan `Age_at_enrollment`.
- Siswa dengan jumlah mata kuliah semester kedua yang sedikit disetujui, pembayaran biaya kuliah yang tidak lancar, dan capaian semester pertama yang rendah cenderung lebih dekat ke status `Dropout`.
- Kelas `Enrolled` masih menjadi kelas yang paling sulit diprediksi dengan baik, sehingga intervensi lanjutan perlu difokuskan pada kelompok transisi ini.
- Evaluasi tidak hanya menggunakan accuracy, tetapi juga `precision`, `recall`, `f1-score`, `confusion matrix`, dan `feature importance`.
- Analisis lanjutan pada notebook juga menyiapkan evaluasi kelompok, sehingga model tidak hanya dilihat dari performa umum tetapi juga dari perilaku prediksi pada subset tertentu seperti gender dan kelompok usia.

### Rekomendasi Action Items
- Bangun sistem peringatan dini yang menandai siswa dengan `Curricular_units_2nd_sem_approved <= 2` sebagai prioritas intervensi akademik level satu. Rata-rata siswa `Dropout` hanya menyelesaikan `1,94` mata kuliah pada semester kedua, jauh di bawah kelompok `Graduate` yang berada di `6,18`.
- Prioritaskan intervensi gabungan akademik dan finansial untuk siswa dengan `Tuition_fees_up_to_date = 0`. Berdasarkan dashboard, kelompok dengan pembayaran tidak mutakhir memiliki `457` kasus dropout dari `528` siswa atau sekitar `86,6%`, sehingga kelompok ini harus masuk daftar monitoring harian bagian akademik dan keuangan.
- Fokuskan program retensi untuk siswa usia masuk `25 tahun ke atas`. Analisis dashboard menunjukkan dropout rate kelompok usia `25-29` mencapai `57,6%` dan kelompok `30+` mencapai `54,1%`, sehingga format intervensi yang lebih fleksibel seperti mentoring singkat, kelas malam, atau konsultasi daring perlu diprioritaskan pada segmen ini.
- Susun daftar prioritas program studi berdasarkan `dropout count` dan `dropout rate`, lalu lakukan evaluasi kurikulum dan beban studi pada program dengan beban dropout tertinggi. Intervensi ini lebih terarah dibanding pendekatan umum karena berbasis segmentasi risiko per program studi.
- Perlakukan status `Enrolled` sebagai kelompok transisi yang perlu evaluasi berkala, bukan sebagai kelompok aman. Model menunjukkan kelas ini paling sulit diprediksi, sehingga siswa yang masih `Enrolled` tetapi memiliki performa semester awal rendah perlu ditinjau ulang setiap akhir semester menggunakan dashboard dan prototype machine learning.
