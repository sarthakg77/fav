import pandas as pd
import openai
import streamlit as st
#from classes import get_primer, format_question, run_request
import warnings

warnings.filterwarnings("ignore")
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(page_icon="deloitte.png", layout="wide", page_title="Consult AI")

st.markdown("<h1 style='text-align: center; font-weight:bold; font-family:Times New Roman; padding-top: 0rem;'>Consult AI</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;padding-top: 0rem;'>Creating Visualisations using GPT</h2>", unsafe_allow_html=True)

available_models = {"ChatGPT-3.5": "gpt-3.5-turbo", "GPT-3": "text-davinci-003"}

# List to hold datasets
if "datasets" not in st.session_state:
    datasets = {}
    st.session_state["datasets"] = datasets
else:
    # use the list already loaded
    datasets = st.session_state["datasets"]

my_key = st.text_input(label=":key: OpenAI Key:", help="Please ensure you have an OpenAI API account with credit. ChatGPT Plus subscription does not include API access.", type="password")

with st.sidebar:
    # First we want to choose the dataset, but we will fill it with choices once we've loaded one
    dataset_container = st.empty()

    # Add facility to upload a dataset
    uploaded_file = st.file_uploader(":computer: Load a CSV file:", type="csv")
    index_no = 0
    if uploaded_file is not None:
        # Read in the data, add it to the list of available datasets
        file_name = uploaded_file.name[:-4].capitalize()
        datasets[file_name] = pd.read_csv(uploaded_file)
        # Default for the radio buttons
        index_no = len(datasets) - 1

    # Radio buttons for dataset choice
    if datasets:  # Only show if there are datasets available
        chosen_dataset = dataset_container.radio(":bar_chart: Choose your data:", list(datasets.keys()), index=index_no)

    st.write(":brain: Choose your model(s):")
    use_model = {}
    for model_desc, model_name in available_models.items():
        label = f"{model_desc} ({model_name})"
        key = f"key_{model_desc}"
        use_model[model_desc] = st.checkbox(label, value=True, key=key)

# Text area for query
question = st.text_area(":eyes: What would you like to visualise?", height=10)
go_btn = st.button("Go...")

model_list = [model_name for model_name, choose_model in use_model.items() if choose_model]
model_count = len(model_list)

# Execute chatbot query
if go_btn and model_count > 0:
    plots = st.columns(model_count)
    if 'chosen_dataset' in locals():  # Ensure chosen_dataset is defined
        primer1, primer2 = get_primer(datasets[chosen_dataset], 'datasets["' + chosen_dataset + '"]')
        question_to_ask = format_question(primer1, primer2, question)

        for plot_num, model_type in enumerate(model_list):
            with plots[plot_num]:
                st.subheader(model_type)
                try:
                    answer = ""
                    answer = run_request(question_to_ask, available_models[model_type], key=my_key)
                    answer = primer2 + answer
                    plot_area = st.empty()
                    plot_area.pyplot(exec(answer))
                except Exception as e:
                    # ... Your error handling code ...

# Display the datasets in a list of tabs if they exist
if datasets:
    tab_list = st.tabs(list(datasets.keys()))

    for dataset_num, tab in enumerate(tab_list):
        with tab:
            dataset_name = list(datasets.keys())[dataset_num]
            st.subheader(dataset_name)
            st.dataframe(datasets[dataset_name], hide_index=True)

footer = """<style>.footer {position: fixed;left: 0;bottom: 0;width: 100%;text-align: center;}</style><div class="footer">
<p> <a style='display: block; text-align: center;'> Team 1 : Sarthak ,Antoine ,Jeff, Adriana </a></p></div>"""
st.caption(" Team 1 : Sarthak ,Antoine ,Jeff, Adriana")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
