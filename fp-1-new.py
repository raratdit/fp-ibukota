import streamlit as st
import os
import json
from dotenv import load_dotenv
import random
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# Load variabel lingkungan
load_dotenv()
GROQ_API = os.getenv("GROQ_API")
GROQ_URL = os.getenv("GROQ_URL")

# Konfigurasi LLM
llm = ChatOpenAI(
    model="llama3-8b-8192",
    openai_api_key=GROQ_API,
    base_url=GROQ_URL,
    temperature=0,
)

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

# Menambahkan button untuk mulai kuis
if st.button("Mulai Kuis"):
    if not st.session_state.user_name:
        st.warning("Silakan isi nama kamu dulu.")
    else:
        with st.spinner("Mengambil pertanyaan..."):
            # Memuat data kuis dari file JSON
            quiz_data = load_quiz_data()
            # Menyimpan pertanyaan acak ke dalam session state
            st.session_state.questions = random.sample(quiz_data, num_questions)
            # Acak pilihan jawaban untuk setiap pertanyaan
            for q in st.session_state.questions:
                random.shuffle(q["options"])
            # Inisialisasi jawaban yang sudah dipilih
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
       
    
    if st.button("Selesai"):
        if not st.session_state.user_name:
            st.error("⚠️ Nama harus diisi sebelum menyelesaikan kuis.")
        else:
            benar = 0
            total = len(st.session_state.questions)
            for i, q in enumerate(st.session_state.questions):
                user_answer = st.session_state.get(f"answer_{i}", None)
                if user_answer == q["answer"]:
                    benar += 1

            nilai = round((benar / total) * 100)

            # Generate motivasi berdasarkan nilai
            prompt_motivasi = f"""
            Saya mendapatkan skor {nilai} dari kuis tentang ibu kota provinsi di Indonesia.
            Buatkan kalimat motivasi dalam 1-2 kalimat yang mendorong saya untuk terus belajar.
            Gunakan bahasa yang positif dan membangkitkan semangat. gunakan bahasa indonesia.
            """

            motivasi_response = llm([HumanMessage(content=prompt_motivasi)])
            motivasi_text = motivasi_response.content.strip()

            # Tampilkan hasil kuis dan motivasi
            st.subheader("🎯 Hasil Kuis")
            st.write(f"**{st.session_state.user_name}**, skor kamu: **{nilai}**")

            mess= f"💡 Motivasi untukmu:\n\n{motivasi_text}"
            if nilai >= 80:
                st.success(mess)
                st.image("assets/a.jpg", caption="Grade A")
                st.balloons()
            elif nilai >= 60:
                st.warning(mess)
                st.image("assets/b.jpg", caption="Grade B")
                st.balloons()
            else:
                st.error(mess)
                st.image("assets/c.jpg", caption="Grade C")
