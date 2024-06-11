import pandas as pd
import streamlit as st


def get_data():
    data = pd.read_sql_table("flashcards", "sqlite:///flashcard_ai.db")
    return data


def add_sidebar():
    data = get_data()
    subjects = data["Subject"].unique().tolist()
    selectedSubjects = st.sidebar.selectbox("Select a Subject to revise", subjects)
    return selectedSubjects
