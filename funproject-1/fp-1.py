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

import re
import json

# Fungsi untuk ekstrak JSON dari response
def extract_json(text):
    
    match = re.search(r"\[\s*{.*?}\s*\]", text)
    st.markdown(f"**JSON yang diekstrak:** \n\n {text}\n\n{match}")
    if match:
        try:
            return json.loads(match)
        except json.JSONDecodeError:

            print("Gagal parse JSON.")
            return []
    return []

# Fungsi untuk generate pertanyaan
def generate_questions(n: int):
    prompt = f"""
Buatkan {n} pertanyaan kuis pilihan ganda tentang ibu kota provinsi di Indonesia.

- Pertanyaan harus dalam bahasa Indonesia.
- Setiap pertanyaan memiliki 4 pilihan jawaban (A, B, C, D).
- Jawaban yang benar harus ditempatkan secara acak dalam daftar pilihan.
- Jangan selalu tampilkan provinsi Papua.
- Tampilkan output hanya dalam format JSON seperti berikut, tanpa tambahan penjelasan apa pun:

[
  {{
    "question": "Ibu kota provinsi Papua adalah?",
    "options": ["Makassar", "Jayapura", "Manokwari", "Sorong"],
    "answer": "Jayapura"
  }},
  ...
]
"""


    response = llm([HumanMessage(content=prompt)])
    # print(response.content)
    st.markdown(f"**Response dari LLM:** \n\n {response.content}")
    questions = json.loads(response.content)
    if not questions:
        st.error("Gagal mendapatkan pertanyaan. Silakan coba lagi.")
        return []
    return questions

# UI
st.title("📍 Quiz Ibu Kota Provinsi")

if "questions" not in st.session_state:
    st.session_state.questions = []
    st.session_state.current_answers = []
    st.session_state.user_name = ""

st.session_state.user_name = st.text_input("Masukkan nama kamu:")
num_questions = st.number_input("Jumlah soal:", min_value=1, max_value=10, step=1)

if st.button("Mulai Kuis"):
    if not st.session_state.user_name:
        st.warning("Silakan isi nama kamu dulu.")
    else:
        with st.spinner("Mengambil pertanyaan..."):
            st.session_state.questions = generate_questions(int(num_questions))
            for q in st.session_state.questions:
                random.shuffle(q["options"])
            st.session_state.current_answers = []

# Tampilkan pertanyaan
if st.session_state.questions:
    st.subheader(f"Kuis untuk: {st.session_state.user_name}")
    # for i, q in enumerate(st.session_state.questions):
    #     random.shuffle(q['options'])

    for i, q in enumerate(st.session_state.questions):
        st.markdown(f"**{i+1}. {q['question']}**")
        st.radio(
            "Pilih jawaban kamu:",
            q["options"],
            key=f"answer_{i}"
        )
        # options_with_placeholder = ["-- Pilih jawaban --"] + q["options"]
        # st.radio(
        #     f"**{i+1}. {q['question']}**",
        #     options_with_placeholder,
        #     key=f"answer_{i}"
        # )
    
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

            st.info(f"💡 Motivasi untukmu:\n\n{motivasi_text}")
            if nilai >= 80:
                # st.success("🎉 Selamat, kamu lulus dengan nilai tinggi!")
                st.image("assets/a.jpg", caption="Grade A")
                st.balloons()
            elif nilai >= 60:
                # st.warning("🙂 Nilai kamu cukup. Masih ada ruang untuk berkembang.")
                st.image("assets/b.jpg", caption="Grade B")
                st.balloons()
            else:
                # st.error("😢 Kamu belum lulus. Tapi jangan patah semangat.")
                st.image("assets/c.jpg", caption="Grade C")

            # Tampilkan motivasi dari LLM
            
            # st.bomb()
