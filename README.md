# Analisis Kualitas Air Sungai dan Danau Provinsi Aceh Tahun 2020

Program Python berbasis terminal untuk mengolah data kualitas air sungai dan danau di Provinsi Aceh tahun 2020. Program menghitung rata-rata parameter **pH, DO, BOD, dan COD** per lokasi pengamatan, mencari nilai tertinggi/terendah/rentang, dan mengurutkan lokasi berdasarkan **Nilai Indeks Pencemaran (IP)** untuk menentukan prioritas pemantauan.

> **Mini Project Pemrograman Komputer** — Kelompok 9A
> Laboratorium Sistem Informasi dan Keputusan, Departemen Teknik Industri, Fakultas Teknik, Universitas Andalas, 2026.

## Anggota Kelompok

| Nama | NIM |
| --- | --- |
| Gisella Zashika Zifi | 2610931001 |
| Muhammad Rauf | 2610932020 |
| Miftahul Irsyad Hali | 2610932040 |

**Asisten Pembimbing:** Intan Permata Mustika
**Dosen Pengampu:** Wisnel, S.T., M.Sc.

## Latar Belakang Singkat

Pengolahan dan perbandingan data kualitas air dari banyak lokasi secara manual memakan waktu dan rawan salah hitung. Program ini mengotomatiskan pengolahan data sekunder agar perbandingan antarlokasi dan penentuan prioritas pemantauan bisa dilakukan lebih cepat dan konsisten.

## Fitur

- **Register & Login** — akun dibuat dengan password yang disimpan dalam bentuk hash; login diberi 3 kali kesempatan.
- **Rata-rata per lokasi** — rata-rata pH, DO, BOD, dan COD dikelompokkan berdasarkan sungai dan lokasi sampling, dengan filter kata kunci (kabupaten/kota, sungai, atau lokasi).
- **Cari data** — cari nilai tertinggi, terendah, atau dalam rentang tertentu untuk pH, DO, BOD, COD, atau Nilai IP.
- **Prioritas pemantauan** — lokasi diurutkan dari Nilai IP terbesar (paling tercemar) beserta ringkasan jumlah titik per status mutu air.
- **Validasi data** — baris yang tidak lengkap, bukan tahun 2020, atau bernilai tidak valid otomatis dilewati dan dilaporkan jumlahnya.

## Dataset

| Aspek | Keterangan |
| --- | --- |
| Nama dataset | Data Kualitas Air Sungai dan Danau Tahun 2020 |
| Sumber | [Open Data Aceh](https://data.acehprov.go.id/id/dataset/parameter-kualitas-air-sungai-dan-danau/resource/0ee08406-9f75-426d-82fb-5e7370e12bb7) |
| Jenis data | Data sekunder |
| Format | CSV (pemisah `;`, encoding `cp1252`) |
| Jumlah baris / kolom | 150 / 34 |
| Parameter | pH, DO, BOD, COD (+ Nilai IP dan Status Mutu Air) |

Metode status mutu air: Indeks Pencemaran (IP) sesuai Kepmen LH No. 115 Tahun 2003, dengan baku mutu PP No. 22 Tahun 2021.

## Struktur Repository

```
.
├── main.py                        # kode program (sesuaikan dengan nama file Anda)
├── data-kualitas-air-sungai.csv   # dataset
├── images/                        # flowchart dan screenshot output (opsional)
└── README.md
```

## Cara Menjalankan

**Prasyarat:** Python 3.8 atau lebih baru. Tidak perlu menginstal library tambahan (hanya memakai modul bawaan `csv` dan `os`).

1. Clone repository:
   ```bash
   git clone https://github.com/<username>/<nama-repository>.git
   cd <nama-repository>
   ```
2. Pastikan file `data-kualitas-air-sungai.csv` berada **satu folder** dengan file program.
3. Jalankan program:
   ```bash
   python main.py
   ```
4. Pilih **Register** untuk membuat akun, lalu **Login**, kemudian gunakan menu utama.

> **Catatan:** akun disimpan di memori, sehingga hilang saat program ditutup. Register ulang setiap kali program dijalankan.

## Alur Penggunaan

```
=== KUALITAS AIR SUNGAI & DANAU ACEH 2020 ===
 1. Register
 2. Login
 3. Keluar

=== MENU UTAMA ===
 1. Rata-rata pH, DO, BOD, COD per lokasi
 2. Cari data (tertinggi / terendah / rentang)
 3. Prioritas pemantauan (Nilai IP & status)
 4. Logout
```

## Input, Proses, dan Output

| Tahap | Ringkasan |
| --- | --- |
| **Input** | Username, password, pilihan menu, parameter dan kriteria pencarian, rentang nilai, jumlah data yang ditampilkan, filter kata kunci (opsional). |
| **Proses** | Baca CSV, validasi dan bersihkan data, saring tahun 2020, kelompokkan per sungai dan lokasi, hitung rata-rata, urutkan dan cari data, urutkan berdasarkan Nilai IP. |
| **Output** | Pesan autentikasi, tabel rata-rata per lokasi, hasil pencarian, peringkat prioritas pemantauan, dan ringkasan status mutu air. |

## Daftar Fungsi

| Fungsi | Deskripsi |
| --- | --- |
| `ke_angka(teks)` | Mengubah teks menjadi desimal (menghapus `<`, koma menjadi titik); `None` jika gagal. |
| `input_password(password)` | Mengubah kata sandi menjadi kode hash. |
| `saring(data, kata)` | Menyaring data berdasarkan kabupaten, sungai, atau lokasi (tidak peka huruf besar/kecil). |
| `urutkan(data, kunci, besar_dulu)` | Mengurutkan data (bubble sort) naik atau turun. |
| `pilih_jumlah(total, satuan)` | Menampilkan pilihan 5, 10, atau semua data. |
| `register(akun)` | Membuat akun baru dengan validasi username dan panjang password minimal 4 karakter. |
| `login(akun)` | Memverifikasi login dengan 3 kali percobaan. |
| `muat_data()` | Membaca CSV, mengambil data 2020, dan melewati baris tidak valid. |
| `cetak_tabel(hasil, kunci, label)` | Menampilkan hasil dalam bentuk tabel. |
| `menu_rata_rata(data)` | Menghitung rata-rata pH, DO, BOD, COD per sungai dan lokasi. |
| `menu_cari(data)` | Mencari data tertinggi, terendah, atau rentang nilai. |
| `menu_prioritas(data)` | Mengurutkan lokasi berdasarkan Nilai IP dan merangkum status mutu air. |
| `main()` | Mengatur alur program dari awal sampai selesai. |

## Flowchart

**Flowchart utama**

![Flowchart Utama](images/flowchart-utama.png)

| Fungsi `muat_data()` | Fungsi Registrasi | Fungsi Login |
| :---: | :---: | :---: |
| <img src="images/flowchart-muat-data.png" width="260"> | <img src="images/flowchart-registrasi.png" width="260"> | <img src="images/flowchart-login.png" width="260"> |

| Menu Rata-rata | Menu Cari | Menu Prioritas |
| :---: | :---: | :---: |
| <img src="images/flowchart-menu-rata-rata.png" width="260"> | <img src="images/flowchart-menu-cari.png" width="260"> | <img src="images/flowchart-menu-prioritas.png" width="260"> |

## Tampilan Output

**1. Menu Register, Login, dan Menu Utama**

![Output Register Login](images/output-1-register-login-menu.png)

**2. Rata-rata per lokasi**

![Output Rata-rata](images/output-2-rata-rata.png)

**3. Menu cari data (tertinggi, terendah, rentang)**

![Output Menu Cari](images/output-3-menu-cari.png)

**4. Semua data tertinggi**

![Output Semua Data Tertinggi](images/output-4-semua-data-tertinggi.png)

**5. Cari data tertinggi**

![Output Cari Data Tertinggi](images/output-5-cari-data-tertinggi.png)

**6. Prioritas pemantauan**

![Output Prioritas A](images/output-6-prioritas-a.png)
![Output Prioritas B](images/output-7-prioritas-b.png)
![Output Prioritas C](images/output-8-prioritas-c.png)

## Batasan

- Data yang digunakan hanya data kualitas air sungai dan danau Provinsi Aceh tahun 2020.
- Parameter yang dianalisis: pH, DO, BOD, dan COD.
- Penelitian mengolah data sekunder; tidak ada pengambilan sampel di lapangan.

## Referensi Utama

- Effendi, H. (2003). *Telaah Kualitas Air.*
- Kamila dkk. (2024), kualitas air Sungai Citarum, Karawang.
- Salmin. (2005). Oksigen terlarut (DO) dan kebutuhan oksigen biologi (BOD) sebagai salah satu indikator untuk menentukan kualitas perairan. *Oseana, 30*(3), 21–26.

Daftar
