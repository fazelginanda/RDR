# Ripple Down Rules

## Tugas Besar 1 IF4070 Representasi Pengetahuan dan Penalaran

## Deskripsi Program
Ripple Down Rules (RDR) adalah suatu metode dalam sistem berbasis pengetahuan yang mengadopsi pendekatan penalaran dengan pengecualian atau penalaran berbasis aturan. Dalam RDR, pohon pengetahuan dibangun secara iteratif, dimulai dari kesimpulan default dan dikembangkan berdasarkan input data yang diberikan oleh pakar. Setiap kali pakar tidak setuju dengan kesimpulan yang diberikan oleh RDR terhadap suatu data baru, maka aturan baru ditambahkan ke dalam pohon untuk menangani kasus tersebut. Metode ini sangat berguna dalam mengelola sistem berbasis pengetahuan yang dinamis, terutama dalam sistem inferensi atau sistem diagnosis berbasis aturan.

## Fitur
1. Membuat pohon basis pengetahuan yang memiliki struktur pohon biner dengan cabang TRUE ke kanan dan FALSE ke kiri
2. Membuat pohon pengetahuan dari awal basis pengetahuan yang kosong atau memuat pohon yang sudah ada dalam bentuk file pickle (.pkl)
3. Menyimpan pohon basis pengetahuan yang telah dimodifikasi dengan penambahan aturan baru dalam format file pickle (.pkl)
4. Menghasilkan dan menyimpan visualisasi pohon pengetahuan dalam format gambar dengan ekstensi .png
5. Memungkinkan pakar untuk menambahkan data baru, memberikan kesimpulan berdasarkan data yang ditambahkan, dan memperbarui pohon pengetahuan dengan aturan baru jika kesimpulan tidak sesuai dengan pendapat pakar

## Cara Penggunaan Program
1. Buka terminal dan clone repository ini
2. Pastikan python telah terinstal pada komputer
3. Instal semua library yang diperlukan dengan command ``pip install -r requirements.txt``
4. Ketik ``python rdr.py`` di terminal dan tekan Enter

## Identitas Kelompok
| NIM  | Nama |
| ------------- | ------------- |
| 13521098 | Fazel Ginanda |
| 13521164 | Akhmad Setiawan |
| 13521168 | Satria Octavianus Nababan |