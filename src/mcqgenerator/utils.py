import os
import json
from langchain_community.document_loaders import PyPDFLoader
import traceback

def read_file(file):
    if file.name.endswith('.pdf'):
        try:
            loader = PyPDFLoader(file.name)
            pages = loader.load_and_split()
            print('pdf read successfully!')
            string_list = [pages[i].page_content for i in range(len(pages))]
            text = ' '.join(string_list)
            # # print(pages[0])
            # # pdf_reader = PyPDF2.PdfReader(file)
            # text = ''
            # for page in pages:
            #     text += page
            return text
        except Exception as exp:
            raise Exception('error reading the .pdf file')
    elif file.endswith('.txt'):
        return file.read().decode('utf-8')
    else:
        raise Exception('Unsupported file format - only .pdf and .txt are currently supported!')
    
def get_table_data(quiz_str):
    try:
        # convert quiz from str to dict
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []

        for key, value in quiz_dict.items():
            mcq = value["mcq"]
            options = " || ".join(
                    [
                    f"{option}: {option_value}"
                    for option, option_value in value["options"].items()
                    ]
                )
            correct = value["correct"]
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})
        
        return quiz_table_data
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False