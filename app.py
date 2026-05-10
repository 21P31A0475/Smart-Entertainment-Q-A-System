import streamlit as st
import google.generativeai as genai
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
import base64

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(
    page_title="Smart Entertainment Q&A System",
    page_icon="🎬",
    layout="centered"
)

def get_base64(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg = get_base64("Entertainment Image.png")

st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/png;base64,{bg}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
[data-testid="stHeader"] {{
    background: transparent;
}}
.main {{
    background: rgba(0,0,0,0.75);
    padding: 25px;
    border-radius: 15px;
}}
h1, h2, h3, h4, p, label {{
    color: white;
}}
.stTextInput > div > div > input {{
    background-color: rgba(255,255,255,0.9);
    color: black;
    border-radius: 10px;
}}
.stButton>button {{
    width: 100%;
    background: red;
    color: white;
    border-radius: 10px;
    height: 45px;
    font-size: 18px;
    border: none;
}}
.stButton>button:hover {{
    background: darkred;
}}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center'>
<img src='https://innomatics.in/wp-content/uploads/2023/01/innomatics-footer-logo.png' width='500'>
</div>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 style='text-align:center;'>🎬 Smart Entertainment Q&A System</h1>",
    unsafe_allow_html=True
)
with open("template.txt") as f:
    template = f.read()

query = st.text_input(
    "Enter your entertainment mood or preference"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", "{query}")
])

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.5
)

parser = JsonOutputParser()

chain = prompt | model | parser

if st.button("🎬 Recommend"):
    if query.strip() == "":
        st.warning("Please enter your preference.")
    else:
        try:          
            response = chain.invoke({"query": query})
            st.markdown("<div class='main'>", unsafe_allow_html=True)
            st.markdown("## 🔑 Keywords")
            keywords = ", ".join(word.title() for word in response["Keywords"])
            st.write(keywords)
            st.markdown("## 🎥 Recommendations")
            for rec in response["Recommendations"]:
                st.markdown(f"""
                ### 🎬 {rec['Title']}
                **🎭 Genre:** {rec['Genre']}
                **📺 Platform:** {rec['Platform']}
                **⭐ Rating:** {rec['Rating']}
                **📖 Overview:**  
                {rec['Overview']}
                **🔥 Why Watch:**  
                {rec['Why_Watch']}
                ---
                """)
            st.markdown("## 🌐 Suggested Links")

            for link in response["Suggested_Links"]:
                st.markdown(f"- {link}")
                
            st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {str(e)}")
