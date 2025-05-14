# 📍 Mini Quiz App - Tebak Ibu Kota Provinsi

Aplikasi kuis sederhana berbasis **Streamlit** untuk menguji pengetahuan pengguna tentang **ibu kota provinsi di Indonesia**. Setelah menjawab semua pertanyaan, pengguna akan mendapatkan **skor** dan **motivasi personal** berdasarkan performa kuis mereka yang dihasilkan oleh **model AI (LLM)**.

## 🚀 Fitur Utama

- ✅ Input nama pengguna dan jumlah soal kuis
- ✅ Pertanyaan pilihan ganda acak dari file JSON
- ✅ Skoring otomatis berdasarkan jawaban
- ✅ Motivasi personal berbasis AI (LLM via Groq API)
- ✅ Tampilan hasil dengan gambar & animasi 🎉
- ✅ UI sederhana dan intuitif

## 🖼️ Preview

| Tampilan Kuis | Tampilan Hasil |
|---------------|----------------|
| ![Preview Soal](assets/preview_soal.jpg) | ![Preview Hasil](assets/preview_hasil.jpg) |

## 🧱 Struktur Folder
```
fun_project_1_REAID/
│
├── app.py
├── assets/
│ ├── data.json # Data pertanyaan kuis
│ ├── a.jpg # Gambar untuk nilai A (>=80)
│ ├── b.jpg # Gambar untuk nilai B (60–79)
│ ├── c.jpg # Gambar untuk nilai C (<60)
│ ├── preview_soal.jpg # Screenshot soal (opsional)
│ └── preview_hasil.jpg# Screenshot hasil (opsional)
└── README.md
```

## 🛠️ Cara Menjalankan

1. **Clone atau download repositori ini:**

```bash
git clone https://github.com/username/fun_project_1_REAID.git
cd fun_project_1_REAID

pip install streamlit python-dotenv langchain
```
## Install dependensi:

```bash
pip install streamlit python-dotenv langchain
Atur environment variable untuk LLM:
```

Buat file .env dan isi seperti ini:
```bash
GROQ_API=your_groq_api_key
GROQ_URL=https://api.groq.com/openai/v1
```

Jalankan aplikasi:
```bash
streamlit run app.py
```