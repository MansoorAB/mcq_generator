import warnings
warnings.filterwarnings("ignore")

import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
import streamlit as st
from langchain_community.callbacks import get_openai_callback

from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging


# load the response .json file
with open('Response.json', 'r') as file:
    resp_format = json.load(file)

# creating a title
st.title('MCQ creation application with langchain.')

with st.form('user_inputs'):
    uploaded_file = st.file_uploader('Upload a .pdf or .txt file')
    print(type(uploaded_file))
    if uploaded_file: # not at page loading
        with open(uploaded_file.name, mode='wb') as w:
            w.write(uploaded_file.getvalue())
        print(f'local file written!')

    mcq_count = st.number_input('Mention the number of questions', min_value=1, max_value=7)
    subject = st.text_input('Mention the subject', max_chars=25)
    tone = st.text_input('Mention the complexity of the quiz', max_chars=25, placeholder='simple')

    button = st.form_submit_button('Create MCQs')

    # when all inputs are provided and button clicked
    if button and uploaded_file is not None and mcq_count and subject and tone:
        try:
            print(f'{uploaded_file=}')
            print(f'{uploaded_file.name=}')
            text = read_file(uploaded_file)
            
            # count the api call cost details
            with get_openai_callback() as cb:
                response=generate_evaluate_chain(
                    {
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        # json.dumps to convert dict --> string
                        "response_json": json.dumps(resp_format)
                    }
                )

            print(f"Total Tokens:{cb.total_tokens}")
            print(f"Prompt Tokens:{cb.prompt_tokens}")
            print(f"Completion Tokens:{cb.completion_tokens}")
            print(f"Total Cost:{cb.total_cost}")

            if isinstance(response, dict):
                quiz=response.get("quiz")
                if quiz is not None:
                    tabular_data = get_table_data(quiz)
                    if tabular_data is not None:
                        df = pd.DataFrame(tabular_data)
                        df.index += 1
                        st.table(df)
                        # display review also in a text box
                        st.text_area(label='Review', value=response['review'])
                    else:
                        st.error('Error in tabular data!')
            else:
                st.write(response)

        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            st.error('Error!')

