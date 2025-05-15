import streamlit as st
import os
import json
import random
import pandas as pd

# Fungsi untuk memuat data dari file JSON
def load_quiz_data():
    with open('assets/data.json', 'r') as f:
        return json.load(f)

# UI
st.title("📍 Quiz Ibu Kota Provinsi")

if "questions" not in st.session_state:
    st.session_state.questions = []
    st.session_state.current_answers = []
    st.session_state.user_name = ""

st.session_state.user_name = st.text_input("Masukkan nama kamu:")
num_questions = st.number_input("Jumlah soal:", min_value=1, max_value=10, step=1)

# Tombol mulai kuis
if st.button("Mulai Kuis"):
    if not st.session_state.user_name:
        st.warning("Silakan isi nama kamu dulu.")
    else:
        with st.spinner("Mengambil pertanyaan..."):
            quiz_data = load_quiz_data()
            st.session_state.questions = random.sample(quiz_data, num_questions)
            for q in st.session_state.questions:
                random.shuffle(q["options"])
            st.session_state.current_answers = []

# Tampilkan pertanyaan
if st.session_state.questions:
    st.subheader(f"Kuis untuk: {st.session_state.user_name}")

    for i, q in enumerate(st.session_state.questions):
        st.markdown(f"**{i+1}. {q['question']}**")
        st.radio(
            "Pilih jawaban kamu:",
            q["options"],
            key=f"answer_{i}"
        )

    # Tombol selesai
    if st.button("Selesai"):
        if not st.session_state.user_name:
            st.error("⚠️ Nama harus diisi sebelum menyelesaikan kuis.")
        else:
            benar = 0
            total = len(st.session_state.questions)

            st.subheader("📊 Review Jawaban")

            for i, q in enumerate(st.session_state.questions):
                user_answer = st.session_state.get(f"answer_{i}", None)
                is_correct = user_answer == q["answer"]
                if is_correct:
                    benar += 1

                col1, col2, col3 = st.columns([4, 3, 1])
                with col1:
                    st.markdown(f"**{i+1}. {q['question']}**")
                    st.markdown(f"Jawaban kamu: `{user_answer}`")
                with col2:
                    st.markdown(f"Jawaban benar: `{q['answer']}`")
                with col3:
                    st.markdown("✅" if is_correct else "❌")

            salah = total - benar

            # Tampilkan bar chart menggunakan st.bar_chart
            st.subheader("📈 Grafik Distribusi Jawaban")
            chart_data = pd.DataFrame({
                "Jumlah Soal": [benar, salah]
            }, index=["Benar", "Salah"])

            st.bar_chart(chart_data)

            # Hasil akhir
            nilai = round((benar / total) * 100)
            st.subheader("🎯 Hasil Kuis")
            st.write(f"**{st.session_state.user_name}**, skor kamu: **{nilai}**")

            if nilai == 100:
                st.success("Hebat sekali! Kamu berhasil mencapai nilai sempurna — pertahankan semangat belajarmu, karena ini baru awal dari prestasi-prestasi hebat berikutnya! 🌟")
                st.image("assets/a.jpg", caption="Grade SS")
                st.balloons()
            elif nilai >= 80:
                st.success("Luar biasa! Kamu hampir sempurna — pertahankan semangat belajarmu dan jadilah inspirasi bagi yang lain!")
                st.image("assets/a.jpg", caption="Grade A")
                st.balloons()
            elif nilai >= 60:
                st.warning("Kerja bagus! Tinggal sedikit lagi menuju kesempurnaan — lanjutkan semangat belajarmu dan buktikan bahwa kamu bisa lebih baik lagi!")
                st.image("assets/b.jpg", caption="Grade B")
                st.balloons()
            else:
                st.error("Jangan menyerah! Setiap langkah kecil adalah bagian dari perjalanan besar menuju pemahaman yang lebih baik — teruslah belajar, karena kamu pasti bisa lebih hebat lagi!")
                st.image("assets/c.jpg", caption="Grade C")
