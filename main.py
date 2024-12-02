import utils
import streamlit as st

st.sidebar.title("Whatsapp Chat Analysis")
uploaded_file = st.sidebar.file_uploader("Upload chat text file", "txt")

if uploaded_file is not None:
    byte_data = uploaded_file.getvalue()
    data = byte_data.decode('utf-8')
    df = utils.process_data(data)

    st.dataframe(df)