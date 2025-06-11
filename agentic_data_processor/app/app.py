# app.py

# # Example usage:
# # In bash
# streamlit run app.py
# # Then view at
# http://localhost:8501

import streamlit as st
import pandas as pd
from src.file_loader import load_file
from src.rag_loader import load_data_dictionary
from src.agent_manager import AgentManager
from src.dbt_mapper import parse_dbt_schema
from src.dw_loader import load_to_bigquery

st.set_page_config(page_title="🧹 Data Cleaning AI Agent", layout="wide")
st.title("🧹 Data Cleaning AI Agent (RAG + Tools Hybrid)")

# Global df
df = pd.DataFrame()

# Upload file
uploaded_file = st.file_uploader("Upload a CSV, Parquet, or JSON file", type=["csv", "parquet", "json"])

if uploaded_file is not None:
    with st.spinner("Loading file..."):
        df = load_file(uploaded_file)
        st.session_state.df = df  # Save to session state
        st.write("Preview of data:")
        st.dataframe(df.head())

    # Optional: Table name for dictionary + dbt schema
    table_name = st.text_input("Optional: Table name to load data dictionary and dbt schema")

    if table_name:
        data_dict = load_data_dictionary(table_name)
        st.write("Loaded data dictionary:")
        st.json(data_dict)

        cleaning_steps = parse_dbt_schema(f"data_dictionary/{table_name}_schema.yml")
        st.write("Suggested cleaning steps from dbt schema:")
        for step in cleaning_steps:
            st.write(f"- {step}")

    # Agent interaction
    user_command = st.text_area("Enter data cleaning instructions")
    rag_enabled = st.checkbox("Enable RAG (Retrieve cleaning rules)", value=True)

    if st.button("Run Agent"):
        agent_manager = AgentManager()
        result = agent_manager.run(user_command, rag_enabled=rag_enabled)
        st.success("Agent run complete!")
        st.write(result)
        st.dataframe(st.session_state.df.head())

    # DW loader (BigQuery)
    if st.button("Load cleaned data to BigQuery"):
        table_id = st.text_input("BigQuery Table ID (e.g. project.dataset.table)")
        load_to_bigquery(st.session_state.df, table_id)
        st.success("Data loaded to BigQuery!")

    # Download cleaned file
    if st.button("Download cleaned CSV"):
        st.download_button(
            label="Download",
            data=st.session_state.df.to_csv(index=False).encode('utf-8'),
            file_name='cleaned_data.csv',
            mime='text/csv'
        )
