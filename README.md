# SonicCipher

<p align="center">
  <img src="https://github.com/user-attachments/assets/5a156943-9134-4653-add0-2c40aabf4116" alt="SonicCipher Logo" width="300"/>
</p>

<p align="center">
  <b>Transform Your Messages Into Sound — Where Cryptography Meets Audio Innovation</b>
</p>

---

## 🎧 Tentang SonicCipher

**SonicCipher** adalah aplikasi kriptografi modern yang mengubah teks menjadi audio terenkripsi menggunakan algoritma **Frequency-Shift Audio Encryption (FSAE)**. Tidak seperti metode konvensional yang hanya menghasilkan teks terenkripsi, SonicCipher menyembunyikan pesan Anda dalam bentuk suara — menggabungkan prinsip kriptografi dan steganografi audio.

<p align="center">
  <img src="https://github.com/user-attachments/assets/9a4c1de7-7a53-48f3-87af-3638d5ebe9af" alt="Tampilan Aplikasi" width="600"/>
</p>

---

## 🔧 Fitur Unggulan

* 🔊 **Enkripsi Teks ke Audio**
* 🔄 **Dekripsi Audio ke Teks**
* 🌐 **Dukungan Multi-Algoritma**: FSAE Standard, Enhanced, dan AES Hybrid
* 🎨 **Visualisasi Spektrogram & Waveform**
* ✅ **Pengujian Otomatis** untuk validasi proses enkripsi-dekripsi

---

## ⚙️ Cara Kerja

SonicCipher menggunakan alur enkripsi sebagai berikut:

1. Setiap karakter diubah menjadi kode ASCII
2. Diterapkan pergeseran berdasarkan kunci
3. Nilai dikonversi ke frekuensi audio tertentu
4. Nada disintesis menjadi file audio
5. Untuk varian Enhanced, durasi dan amplitudo juga bervariasi

<p align="center">
  <img src="https://github.com/user-attachments/assets/45b74a78-1198-4046-9f83-0e33e1bd93c4" alt="Diagram Proses" width="500"/>
</p>

---

## 💻 Instalasi

### Prasyarat

* Python >= 3.6
* Dependensi: `PyQt5`, `NumPy`, `SciPy`, `Matplotlib`, `Pygame`

### Langkah Instalasi

```bash
git clone git@github.com:SirHosen/SonicChipper.git
cd SonicCipher
pip install -r requirements.txt
python main.py
```

### Build ke Executable (Opsional)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "resources;resources" main.py
```

Output akan berada di folder `dist/`.

---

## ▶️ Panduan Penggunaan

### 🔊 Enkripsi Teks ke Audio

1. Buka tab **Enkripsi**
2. Masukkan pesan
3. Atur parameter: kunci, frekuensi dasar, durasi, algoritma
4. Klik **Enkripsi ke Suara**
5. Putar atau simpan audio hasil

### 🔒 Dekripsi Audio ke Teks

1. Buka tab **Dekripsi**
2. Pilih file audio
3. Atur parameter sesuai dengan yang digunakan saat enkripsi
4. Klik **Dekripsi Suara**

### 🎨 Visualisasi Audio

1. Buka tab **Visualisasi**
2. Pilih file audio
3. Pilih jenis visualisasi (Spektrogram, Waveform, dll.)
4. Klik **Analisis** untuk melihat grafik

<p align="center">
  <img src="https://github.com/user-attachments/assets/90ffd63b-6c90-42eb-8479-9ff4706a0d30" alt="Visualisasi Audio" width="600"/>
</p>

---

## 📁 Struktur Proyek

```
SonicCipher/
├── main.py                # Entry point aplikasi
├── ui_design.py           # UI dengan PyQt
├── audio_processor.py     # Algoritma FSAE & manipulasi audio
├── visualizer.py          # Modul visualisasi
├── utils.py               # Fungsi bantu
├── resources/             # Ikon dan aset lainnya
├── requirements.txt       # Dependensi Python
└── README.md              # Dokumentasi proyek
```

---

## 💡 Arsitektur Sistem

Aplikasi ini menggunakan pendekatan **modular 3-layer**:

1. **Presentasi**: UI dan interaksi pengguna
2. **Logika Bisnis**: Pemrosesan teks dan audio
3. **Data**: Penyimpanan file audio dan metadata

<p align="center">
  <img src="https://github.com/user-attachments/assets/fa36e5a9-2d62-4344-b348-2571cb8c7b6a" alt="Arsitektur Software" width="600"/>
</p>

---

## 🔠 Detail Algoritma FSAE

### Formula Enkripsi:

```
1. P = ASCII(char)
2. C = (P + K) % 256
3. F = F_base + (C / 256) × F_range
4. D = D_base + (i % 5) × 0.05  # (Enhanced only)
5. s(t) = A × sin(2πFt)
```

### Varian:

* **FSAE Standard**: Durasi tetap
* **FSAE Enhanced**: Durasi & amplitudo variatif
* **FSAE + AES**: Kombinasi dengan enkripsi AES untuk keamanan ganda

---

## ⚠️ Pemecahan Masalah

### "Metadata Tidak Ditemukan"

* Pastikan file `.metadata` ada di lokasi yang sama
* Gunakan mode "Analisis Audio" jika perlu

### "Dekripsi Tidak Akurat"

* Periksa kunci dan parameter frekuensi
* Sesuaikan toleransi (5-10%)

### "Audio Tidak Terdengar"

* Periksa koneksi speaker/headset
* Uji di media player eksternal

---

## ✨ Kontribusi

1. Fork repositori ini
2. Buat branch baru: `feature/NamaFitur`
3. Commit & push perubahan Anda
4. Ajukan Pull Request

---

## 🚀 Roadmap Pengembangan

* Peningkatan algoritma tanpa metadata
* Implementasi versi mobile (Android/iOS)
* Real-time audio transmission
* Optimasi ukuran file audio
* UI/UX yang lebih dinamis

---

## 🔒 Lisensi

Proyek ini didistribusikan di bawah Lisensi **MIT**. Lihat file `LICENSE` untuk detail.

---

## 📢 Kontak & Tautan

* **Developer**: SirHosen
* **Email**: [hoseaoktarivanes@gmail.com](mailto:hoseaoktarivanes@gmail.com)
* **Repo**: [github.com/SirHosen/SonicChipper](https://github.com/SirHosen/SonicChipper)
