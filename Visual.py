import pandas as pd
import openai
import streamlit as st
import warnings
from classes import get_primer, format_question, run_request

warnings.filterwarnings("ignore")
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(page_icon="deloitte.png", layout="wide", page_title="Consult AI")

st.markdown("<h1 style='text-align: center; font-weight:bold; font-family:Times New Roman; padding-top: 0rem;'> \
            Consult AI</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;padding-top: 0rem;'>Creating Visualisations using GPT-3 \
            </h2>", unsafe_allow_html=True)

# Sidebar for OpenAI Key and CSV Import
with st.sidebar:
    # Input for OpenAI Key
    my_key = st.text_input(label=":key: OpenAI Key:", help="Please ensure you have an OpenAI API account with credit. ChatGPT Plus subscription does not include API access.", type="password")

    # CSV file upload
    uploaded_file = st.file_uploader(":computer: Load a CSV file:", type="csv")
    if uploaded_file is not None:
        # Read in the data
        dataset = pd.read_csv(uploaded_file)

# Text area for query
question = st.text_area(":eyes: What would you like to visualise?", height=10)
go_btn = st.button("Go...")

# Execute chatbot query
if go_btn:
    # Get the primer for this dataset
    primer1, primer2 = get_primer(dataset, 'dataset')
    # Format the question
    question_to_ask = format_question(primer1, primer2, question)

    try:
        # Run the question
        answer = run_request(question_to_ask, "text-davinci-003", key=my_key)
        # The answer is the completed Python script, so add the primer to it
        answer = primer2 + answer
        st.pyplot(exec(answer))
    except Exception as e:
        # Handle various OpenAI errors
        # ... (keep your error handling code here)

# Hide menu and footer
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
