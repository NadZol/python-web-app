# Nadezda Zolotareva 6282871

import requests
import main_functions
import nltk
from nltk import word_tokenize
# nltk.download("stopwords")
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(
        page_title="Project 1",
        page_icon="📰",
        layout="centered",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://docs.streamlit.io/library/api-reference',
            'Report a bug': "https://docs.streamlit.io/library/api-reference",
            'About': "# This is Project 1 for COP 4813 - Prof. Gregory Reis"
        })

st.title("Project 1 - News App")

st.sidebar.markdown("## Select an API")
add_selectbox = st.sidebar.selectbox(
    "",
    ("", "Top Stories", "Most Popular Articles")
)

if add_selectbox == "":
    st.header("Please select an API")
elif add_selectbox == "Top Stories":

    st.header("The Stories API")
    st.subheader("I - WordCloud")

    nyt_api = main_functions.read_from_file("JSON_Files/api_key.json")
    nyt_key = nyt_api["my_key"]

    topic = st.selectbox("Select a topic of your interest",
                         options=["", "arts", "automobiles", "books", "business", "fashion", "food", "health", "home", "insider", "magazine",
                                 "movies", "nyregion", "opinion", "politics", "realestate", "science", "sports", "sundayreview",
                                "technology", "theater", "t-magazine", "travel", "upshot", "us", "world"])

    if topic:
        url = "https://api.nytimes.com/svc/topstories/v2/{0}.json?api-key={1}".format(topic, nyt_key)
        response = requests.get(url).json()
        main_functions.save_to_file(response, "JSON_Files/articlesChosenByTheUser.json")
        articlesChosenByTheUser = main_functions.read_from_file("JSON_Files/articlesChosenByTheUser.json")

        abstracts = ""
        for i in articlesChosenByTheUser["results"]:
            abstracts = abstracts + i["abstract"]

        words = word_tokenize(abstracts)

        no_punkt = []
        for w in words:
            if w.isalpha():
                no_punkt.append(w)

        stop_words = set(stopwords.words("english"))

        filtered_list = []
        for w in no_punkt:
            if w not in stop_words:
                filtered_list.append(w)

        col1, col2 = st.columns(2)
        with col1:
            max = st.slider("Choose a maximum amount of words to be displayed", 1, 200)
            colors = st.selectbox("Choose a colormap",
                                 options=["prism", "viridis", "plasma", "magma", "cividis", "cool", "spring"])
            back = st.color_picker('Choose a background color', '#FFFFFF')

        with col2:
            user_wordcloud = WordCloud(width=1000,
                                       height=1000,
                                       stopwords=stop_words,
                                       max_words=max,
                                       colormap=colors,
                                       background_color=back).generate(abstracts)

            fig, ax = plt.subplots()
            plt.imshow(user_wordcloud, interpolation='bilinear')
            plt.axis('off')
            st.pyplot(fig)

        st.subheader("II - Frequency Distribution")

        freq = st.checkbox('Click here to display the frequency distribution plot')
        if freq:
            num = st.slider("Choose the number of words", 1, 20)

            freq_distribution = FreqDist(filtered_list)

            most_common_words = pd.DataFrame(freq_distribution.most_common(num))

            most_common = pd.DataFrame(
                {
                    "words": most_common_words[0],
                    "count": most_common_words[1]
                }
            )
            fig = px.histogram(most_common, x="words", y="count", title="", color="count")
            st.plotly_chart(fig)

elif add_selectbox == "Most Popular Articles":
    st.header("Most Popular Articles")
    st.subheader("I - Comparing Most Shared, Viewed and Emailed Articles")

    nyt_api = main_functions.read_from_file("JSON_Files/api_key.json")
    nyt_key = nyt_api["my_key"]

    articles_set = st.selectbox("Select your preferred set of articles",
                         options=["", "shared", "emailed", "viewed"])

    time = st.selectbox("Select the age of your article in days",
                       options=["", "1", "7", "30"])

    if articles_set and time:
        url = "https://api.nytimes.com/svc/mostpopular/v2/{0}/{1}.json?api-key={2}".format(articles_set, time, nyt_key)
        response = requests.get(url).json()
        main_functions.save_to_file(response, "JSON_Files/articlesChosenByTheUser.json")
        articlesChosenByTheUser = main_functions.read_from_file("JSON_Files/articlesChosenByTheUser.json")

        abstracts = ""
        for i in articlesChosenByTheUser["results"]:
            abstracts = abstracts + i["abstract"]

        words = word_tokenize(abstracts)

        no_punkt = []
        for w in words:
            if w.isalpha():
                no_punkt.append(w)

        stop_words = set(stopwords.words("english"))

        filtered_list = []
        for w in no_punkt:
            if w not in stop_words:
                filtered_list.append(w)

        col1, col2 = st.columns(2)
        with col1:
            max = st.slider("Choose a maximum amount of words to be displayed", 1, 200)
            colors = st.selectbox("Choose a colormap",
                                  options=["prism", "viridis", "plasma", "magma", "cividis", "cool", "spring"])
            back = st.color_picker('Choose a background color', '#FFFFFF')

        with col2:
            user_wordcloud = WordCloud(width=1000,
                                       height=1000,
                                       stopwords=stop_words,
                                       max_words=max,
                                       colormap=colors,
                                       background_color=back).generate(abstracts)

            fig, ax = plt.subplots()
            plt.imshow(user_wordcloud, interpolation='bilinear')
            plt.axis('off')
            st.pyplot(fig)

        st.subheader("II - Frequency Distribution")

        freq = st.checkbox('Click here to display the frequency distribution plot')
        if freq:
            num = st.slider("Choose the number of words", 1, 20)

            freq_distribution = FreqDist(filtered_list)

            most_common_words = pd.DataFrame(freq_distribution.most_common(num))

            most_common = pd.DataFrame(
                {
                    "words": most_common_words[0],
                    "count": most_common_words[1]
                }
            )
            fig = px.histogram(most_common, x="words", y="count", title="", color="count")
            st.plotly_chart(fig)

