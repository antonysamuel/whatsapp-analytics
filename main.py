import utils
import streamlit as st
from matplotlib import pyplot as plt

st.sidebar.title("Whatsapp Chat Analysis")
uploaded_file = st.sidebar.file_uploader("Upload chat text file", "txt")

if uploaded_file is not None:
    byte_data = uploaded_file.getvalue()
    data = byte_data.decode('utf-8')
    df = utils.process_data(data)

    st.dataframe(df)

    users = df['users'].unique().tolist()
    if 'group_notification' in users:
        users.remove('group_notification')
    if 'Whatsapp' in users:
        users.remove('Whatsapp')
    users.sort()
    users.insert(0,"Overall")

    current_user = st.sidebar.selectbox("Select User for Analysis", users)

    st.sidebar.button("Show analysis")


    num_messages, num_words, num_media_shared, num_urls = utils.fetch_stats(df, current_user)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.header("Total Messages")
        st.title(num_messages)

    with col2:
        st.header("Total Words")
        st.title(num_words)

    with col3:
        st.header("Total Media Shared")
        st.title(num_media_shared)

    with col4:
        st.header("Links Shared")
        st.title(num_urls)

    if current_user == 'Overall':
        st.title("Most Busy Users")
        busy_users, busy_percent = utils.get_busy_users(df)
        fig, ax = plt.subplots()

        col1, col2 = st.columns(2)

        with col1:
            ax.bar(busy_users.index, busy_users.values)
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(busy_percent)

    st.title("Word Cloud")
    wordcloud = utils.create_wordcloud(current_user, df)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud)
    st.pyplot(fig)

