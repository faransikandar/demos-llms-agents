# ##############################
# # Example usage
# from src.rag_loader import load_data_dictionary

# data_dict = load_data_dictionary("customer_data")

# print(data_dict)

# # Later, replace this with LangChain Retriever
# from langchain.vectorstores import FAISS
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.text_splitter import RecursiveCharacterTextSplitter

# # Index YAML files as text → FAISS → Retriever → used in agent context
# ##############################

import yaml
import glob
import os

# Simple mapping of table name → YAML dict
def load_data_dictionary(table_name: str, dict_folder='data_dictionary/') -> dict:
    yaml_files = glob.glob(os.path.join(dict_folder, '*.yaml'))
    for path in yaml_files:
        if table_name in path:
            with open(path, 'r') as f:
                return yaml.safe_load(f)
    return {}
