import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import streamlit as st

from packages.search_song import search_song
from packages.run_recommender import get_feature_vector, show_similar_songs

# Load data
dat = pd.read_csv('data/processed/dat_for_recommender.csv')

# Extract unique song names from dataset
unique_songs = dat['name'].unique().tolist()

# Add placeholder to the list of songs
unique_songs.insert(0, "Select a song from the dropdown")

# Features to select for recommendation
song_features_normalized = ['valence', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness']
song_features_not_normalized = ['duration_ms', 'key', 'loudness', 'mode', 'tempo']
all_features = song_features_normalized + song_features_not_normalized + ['decade', 'popularity']

# Set app layout
st.markdown(
    """
    <style>
    .big-font {
        font-size:20px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def main():
    st.markdown("# Customized Music Recommender")
    st.markdown("Welcome to this music recommender! \
                \n You can search for a song and get recommendations based on the song you searched for. \
                \n You can also customize the recommendations by selecting the features you care about. Enjoy!")

    # Sidebar - select features
    st.sidebar.markdown("### Select Features")
    features = st.sidebar.multiselect('Select the features you care about', all_features, default=all_features)
    
    # Sidebar - select number of recommendations
    st.sidebar.markdown("### Number of Recommendations")
    num_recommendations = st.sidebar.slider('Select the number of recommendations', 10, 50)

    # Dropdown for dynamically generated song list with a placeholder
    st.markdown("### Ready to get recommendations based on my song?")
    song_name = st.selectbox('Choose a song from the dropdown', options=unique_songs)

    # Input for year
    year = st.text_input('Enter the year of the song (e.g. 2009). \
                         \nIf you are not sure if the song is in the database or not sure about the year, \
                         please leave the year blank and click the button below to search for the song.')
    if year:
        year = int(year)

    # Button for searching song
    if st.button('Search for my song'):
        if song_name == "Select a song from the dropdown":
            st.markdown("Please select a song from the dropdown!")
        else:
            found_flag, found_song = search_song(song_name, dat)
            if found_flag:
                st.markdown("Perfect, this song is in the dataset:")
                st.markdown(found_song)
            else:
                st.markdown("Sorry, this song is not in the dataset. Please try another song!")

    # Button for getting recommendations
    if st.button('Get Recommendations'):
        if song_name == "Select a song from the dropdown":
            st.markdown("Please select a valid song from the dropdown!")
        elif not year:
            st.markdown("Please enter the year of the song!")
        else:
            # Show similar songs in wordcloud
            fig_cloud = show_similar_songs(song_name, year, dat, features, num_recommendations, plot_type='wordcloud')
            st.markdown(f"### Great! Here are your recommendations for \
                        \n#### {song_name} ({year})!")
            st.pyplot(fig_cloud)

            # Show the most similar songs in bar chart
            fig_bar = show_similar_songs(song_name, year, dat, features, top_n=10, plot_type='bar')
            st.markdown("### Get a closer look at the top 10 recommendations for you!")
            st.pyplot(fig_bar)

if __name__ == "__main__":
    main()
