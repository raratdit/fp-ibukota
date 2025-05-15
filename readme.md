# 🇮🇩 Kuis Ibu Kota Provinsi - Streamlit App

Aplikasi web kuis interaktif untuk menguji pengetahuan tentang **ibu kota provinsi di Indonesia**. Dibuat dengan Python dan Streamlit.

---

## 🚀 Fitur

- Input nama pengguna
- Pilih jumlah soal (1–10)
- Pertanyaan dan pilihan jawaban acak
- Penilaian otomatis
- Review jawaban (benar/salah)
- Grafik hasil jawaban (Bar chart)
- Motivasi berbasis skor
- Tampilan hasil berupa gambar dan emoji 🎯✅❌

---

## 📦 Struktur Proyek
```
├── app.py # File utama Streamlit
├── assets/
│ ├── data.json # Soal dan jawaban dalam format JSON
│ ├── a.jpg # Gambar untuk nilai A dan SS
│ ├── b.jpg # Gambar untuk nilai B
│ └── c.jpg # Gambar untuk nilai C
```
---

## 📝 Format `data.json`

```json
[
  {
    "question": "Apa ibu kota dari Provinsi Jawa Barat?",
    "options": ["Bandung", "Jakarta", "Semarang", "Surabaya"],
    "answer": "Bandung"
  },
  ...
]
```

▶️ Cara Menjalankan
Clone repositori ini atau salin file app.py dan folder assets/ ke direktori lokal.
Pastikan sudah menginstal Streamlit:
```
pip install streamlit
```

Jalankan aplikasi:
```
streamlit run app.py
```