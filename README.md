# SonicCipher

![logo (1)](https://github.com/user-attachments/assets/52a1559f-1369-4199-98e8-7412dc336124)

## Aplikasi Kriptografi Teks ke Suara dengan Algoritma FSAE

SonicCipher adalah aplikasi kriptografi inovatif yang mengubah teks menjadi pola suara menggunakan algoritma Frequency-Shift Audio Encryption (FSAE). Berbeda dengan metode kriptografi konvensional yang menghasilkan teks terenkripsi, SonicCipher menghasilkan file audio yang berisi pesan rahasia, menggabungkan konsep kriptografi dan steganografi.

![Screenshot 2025-06-13 010547](https://github.com/user-attachments/assets/9a4c1de7-7a53-48f3-87af-3638d5ebe9af)

## Fitur Utama

- **Enkripsi Teks ke Suara**: Ubah pesan teks menjadi pola suara dengan parameter yang dapat disesuaikan
- **Dekripsi Suara ke Teks**: Kembalikan file audio terenkripsi menjadi pesan teks asli
- **Visualisasi Audio**: Analisis spektrogram, bentuk gelombang, dan distribusi frekuensi
- **Multiple Algoritma**: Pilih antara FSAE Standard, FSAE Enhanced, atau FSAE + AES
- **Tema Gelap/Terang**: Antarmuka yang nyaman untuk berbagai kondisi pencahayaan
- **Pengujian Otomatis**: Verifikasi enkripsi/dekripsi dengan satu klik

## Cara Kerja

SonicCipher mengimplementasikan algoritma Frequency-Shift Audio Encryption (FSAE) yang bekerja dengan prinsip dasar:

1. Setiap karakter dalam teks diubah menjadi nilai ASCII
2. Nilai ASCII dimodifikasi menggunakan kunci enkripsi (shift)
3. Nilai yang dimodifikasi dipetakan ke frekuensi audio tertentu
4. Frekuensi-frekuensi ini dikombinasikan untuk membuat pola suara unik
5. Durasi setiap nada bervariasi berdasarkan posisi karakter dalam pesan

![FSAE Algorithm](https://placeholder-for-algorithm-diagram.png)

## Instalasi

### Prasyarat

- Python 3.6 atau lebih baru
- Pustaka-pustaka Python: PyQt5, NumPy, SciPy, Matplotlib, Pygame

### Langkah Instalasi

1. Clone repositori ini:
   ```bash
   git clone https://github.com/yourusername/SonicCipher.git
   cd SonicCipher
   ```

2. Instal dependensi yang diperlukan:
   ```bash
   pip install -r requirements.txt
   ```

3. Jalankan aplikasi:
   ```bash
   python main.py
   ```

### Membuat File Executable (Opsional)

Untuk membuat file .exe yang dapat dijalankan di Windows tanpa instalasi Python:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "resources;resources" main.py
```

File .exe akan tersedia di folder `dist`.

## Penggunaan

### Enkripsi Teks ke Suara

1. Buka tab "Enkripsi"
2. Masukkan pesan yang ingin dienkripsi
3. Atur parameter enkripsi:
   - Kunci Enkripsi (1-25)
   - Frekuensi Dasar (200-500 Hz)
   - Durasi Dasar (50-500 ms)
   - Algoritma (Standard, Enhanced, AES)
4. Klik "Enkripsi ke Suara"
5. Gunakan tombol "Putar Suara" untuk mendengarkan hasil
6. Simpan file audio dengan tombol "Simpan Suara"

![Encryption Tab](https://placeholder-for-encryption-tab.png)

### Dekripsi Suara ke Teks

1. Buka tab "Dekripsi"
2. Pilih file audio terenkripsi
3. Atur parameter dekripsi:
   - Kunci Dekripsi (harus sama dengan kunci enkripsi)
   - Toleransi Frekuensi (1-20%)
   - Metode Dekripsi (Otomatis, Gunakan Metadata, Analisis Audio)
4. Klik "Dekripsi Suara"
5. Lihat hasil dekripsi di area teks

![Decryption Tab](https://placeholder-for-decryption-tab.png)

### Visualisasi Audio

1. Buka tab "Visualisasi"
2. Pilih file audio untuk dianalisis
3. Pilih jenis visualisasi (Spektrogram, Waveform, dll.)
4. Atur parameter visualisasi
5. Klik "Analisis"
6. Ekspor gambar jika diperlukan

![Visualization Tab](https://placeholder-for-visualization-tab.png)

## Struktur Proyek

```
SonicCipher/
│
├── main.py                # File utama untuk menjalankan aplikasi
├── ui_design.py           # Desain antarmuka pengguna
├── audio_processor.py     # Pemrosesan audio dan algoritma FSAE
├── visualizer.py          # Visualisasi audio
├── utils.py               # Fungsi-fungsi utilitas
│
├── resources/             # Folder untuk ikon dan resource lainnya
│   ├── icon.png
│   ├── logo.png
│   └── ...
│
├── requirements.txt       # Daftar dependensi
└── README.md              # Dokumentasi proyek
```

## Arsitektur Software

SonicCipher dibangun dengan arsitektur modular yang terdiri dari tiga lapisan utama:

1. **Lapisan Presentasi**: Menangani antarmuka pengguna dan visualisasi
2. **Lapisan Logika Bisnis**: Menangani algoritma FSAE dan pemrosesan audio
3. **Lapisan Data**: Menangani penyimpanan dan pembacaan file audio dan metadata

![Software Architecture](https://placeholder-for-architecture-diagram.png)

## Algoritma FSAE

Algoritma FSAE tersedia dalam tiga varian:

1. **FSAE Standard**: Implementasi dasar dengan durasi tetap untuk semua karakter
2. **FSAE Enhanced**: Menambahkan variasi durasi dan amplitudo berdasarkan karakter dan posisinya
3. **FSAE + AES**: Kombinasi FSAE dengan enkripsi AES untuk keamanan tambahan

Proses enkripsi FSAE secara matematis dapat dirumuskan sebagai berikut:

1. Konversi karakter ke ASCII:
   ```
   P = ASCII(char)
   ```

2. Penerapan shift menggunakan kunci:
   ```
   C = (P + K) % 256
   ```

3. Pemetaan ke frekuensi audio:
   ```
   F = F_base + (C / 256) × F_range
   ```

4. Variasi durasi berdasarkan posisi (untuk FSAE Enhanced):
   ```
   D = D_base + (i % 5) × 0.05
   ```

5. Sintesis audio menggunakan gelombang sinus:
   ```
   s(t) = A × sin(2πFt)
   ```

## Pemecahan Masalah

### Metadata Tidak Ditemukan

**Masalah**: Saat dekripsi, muncul pesan "File metadata tidak ditemukan. Dekripsi mungkin kurang akurat."

**Solusi**:
- Pastikan file metadata (.wav.metadata) berada di lokasi yang sama dengan file audio
- Coba simpan ulang file audio terenkripsi
- Gunakan metode dekripsi "Analisis Audio" jika metadata tidak tersedia
- Sesuaikan parameter dekripsi manual (frekuensi dasar, toleransi)

### Dekripsi Tidak Akurat

**Masalah**: Hasil dekripsi tidak sesuai dengan pesan asli

**Solusi**:
- Pastikan menggunakan kunci dekripsi yang sama dengan kunci enkripsi
- Sesuaikan toleransi frekuensi (coba nilai antara 5-10%)
- Jika tidak menggunakan metadata, pastikan frekuensi dasar yang dimasukkan sama dengan yang digunakan saat enkripsi
- Coba berbagai kombinasi parameter hingga mendapatkan hasil yang benar

### Audio Tidak Terdengar

**Masalah**: Audio tidak terdengar atau terputus-putus

**Solusi**:
- Pastikan perangkat audio (speaker/headphone) terhubung dan berfungsi
- Periksa volume sistem dan aplikasi
- Coba simpan audio dan putar dengan aplikasi lain
- Restart aplikasi jika masalah berlanjut

## Kontribusi

Kontribusi untuk pengembangan SonicCipher sangat diterima. Untuk berkontribusi:

1. Fork repositori
2. Buat branch untuk fitur baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan Anda (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buka Pull Request

## Pengembangan Lanjutan

Beberapa arah pengembangan lanjutan untuk SonicCipher:

- Peningkatan keamanan kunci
- Optimasi ukuran file audio
- Peningkatan algoritma dekripsi tanpa metadata
- Ekspansi ke platform mobile
- Penerapan dalam komunikasi real-time

## Lisensi

Didistribusikan di bawah Lisensi MIT. Lihat `LICENSE` untuk informasi lebih lanjut.

## Kontak

[Nama Anda] - [Email Anda]

Link Proyek: [https://github.com/yourusername/SonicCipher](https://github.com/yourusername/SonicCipher)

## Pengakuan

- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/)
- [NumPy](https://numpy.org/)
- [SciPy](https://scipy.org/)
- [Matplotlib](https://matplotlib.org/)
- [Pygame](https://www.pygame.org/)

---

**Catatan**: Ganti placeholder gambar dengan path aktual ke gambar Anda. Tambahkan screenshot aplikasi, diagram arsitektur, dan ilustrasi algoritma untuk README yang lebih informatif dan menarik.
