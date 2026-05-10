import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
import base64

load_dotenv()

st.set_page_config(
    page_title="Smart Entertainment Q&A System",
    page_icon="🎬",
    layout="centered"
)

def get_base64(img):
    with open(img, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg = get_base64("Entertainment Image.png")

st.markdown(f"""
<style>

[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/png;base64,{bg}");
    background-size: cover;
    background-position: center;
}}

[data-testid="stHeader"] {{
    background: transparent;
}}

.main {{
    background: rgba(0,0,0,0.7);
    padding: 20px;
    border-radius: 15px;
}}

h1,h2,h3,p {{
    color: white;
}}

.stButton>button {{
    width: 100%;
    background: red;
    color: white;
    border-radius: 10px;
}}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center'>
<img src='https://innomatics.in/wp-content/uploads/2023/01/innomatics-footer-logo.png' width='650'>
</div>
""", unsafe_allow_html=True)

st.markdown(
    "<h2 style='text-align:center;'>🎬 Smart Entertainment Q&A System</h2>",
    unsafe_allow_html=True
)

with open("template.txt") as f:
    template = f.read()

query = st.text_input("Enter your entertainment mood or preference")

prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", "{query}")
])

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)

chain = prompt | model | JsonOutputParser()

if st.button("Recommend"):

    if query.strip() == "":
        st.warning("Please enter something")

    else:

        response = chain.invoke({"query": query})

        st.markdown("<div class='main'>", unsafe_allow_html=True)

        st.markdown(
            f"### 🔑 {', '.join(word.title() for word in response['Keywords'])}"
        )

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

        st.markdown("### 🌐 Suggested Links")

        for link in response["Suggested_Links"]:
            st.markdown(f"- {link}")

        st.markdown("</div>", unsafe_allow_html=True)