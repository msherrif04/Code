import pandas as pd
import streamlit as st
from datetime import datetime, UTC
from flashcards import flashcard
from fsrs import *
from state_management import set_state

import os
from langchain_groq import ChatGroq

# from dotenv import load_dotenv, find_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from chatexplain import get_explanation, api_key

flaschardParams = [
    "Has Preamble",
    "Preamble Text",
    "Question",
    "Answer",
    "due",
    "stability",
    "difficulty",
    "elapsed_days",
    "scheduled_days",
    "reps",
    "lapses",
    "state",
]

# setting up environment variables
# load_dotenv(".env")
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# model = ChatGroq(model="llama3-8b-8192", api_key=GROQ_API_KEY)


def GetData():
    data = pd.read_sql_table("flashcards", "sqlite:///flashcard_ai.db")
    return data


def _NormaliseSubjectList(subjects):
    unique_subjects = set()

    for entry in subjects:
        # Split the entry by commas and normalize each subject
        for subject in entry.split(","):
            normalized_subject = subject.strip().capitalize()
            unique_subjects.add(normalized_subject)

    # Convert the set back to a list
    return sorted(list(unique_subjects))


def FilterBySubject():
    data = GetData()
    subjects = data["Subject"].unique().tolist()
    subjects = _NormaliseSubjectList(subjects)
    selectedSubjects = st.sidebar.radio("Select a Subject to revise", subjects)
    return selectedSubjects


def FilterByYear():
    data = GetData()
    years = data["year"].sort_values(ascending=True).unique().tolist()
    selectedYear = st.sidebar.selectbox("Select a Year to revise", years)
    return selectedYear


def FilterByRound():
    data = GetData()
    rounds = sorted(data["round"].unique().tolist())
    selectedRound = st.sidebar.selectbox("Select a Round to revise", rounds)
    return selectedRound


def FilterQuestions(subject, year, round):
    data = GetData()
    # Filter by subject, round and year
    filteredData = data[
        (data["Subject"].str.contains(subject, case=False))
        & (data["year"] == year)
        & (data["round"] == round)
        # & ((data["due"] <= datetime.now(UTC)) | (data["due"].isnull()))
    ]
    filteredData["due"] = pd.to_datetime(filteredData["due"], utc=UTC)
    dueQuestionsDf = filteredData[
        (filteredData["due"] <= datetime.now(UTC)) | (filteredData["due"].isnull())
    ]
    return dueQuestionsDf


def getCard(filteredQuestions, indices, index):
    currentQuestion = filteredQuestions.loc[indices[index]].to_dict()
    paramsList = [currentQuestion[param] for param in flaschardParams]
    card = flashcard(*paramsList)
    return card


def showCard(card):
    # set review period of card to now
    if card.has_preamble:
        st.write(card.preamble_text)
    st.write(card.question)


def showAnswer(card):
    # show answer button
    showAnswer = st.button("Show Answer")
    # if answer button is click, show answer
    if showAnswer:
        st.write(card.answer)
        # set_state(2)
    explanation = get_explanation(
        card.question,
        card.answer,
        api_key,
    )
    return explanation


def review_card(card, scheduler):
    schedulingCards = card.review_card(scheduler)
    return schedulingCards


def addSummary():
    st.markdown(
        """
            ### Addressing Inequitable Distribution of Preparation Materials for the National Science and Maths Quiz

The National Science and Maths Quiz (NSMQ) is a prestigious competition that tests the knowledge and skills of students across various subjects. However, a significant problem undermines the fairness of this competition: the inequitable distribution of preparation materials. While well-funded, prestigious schools have access to high-quality study resources, students from less privileged schools often struggle with inadequate materials. This disparity creates an uneven playing field, where only students from more privileged backgrounds can fully prepare and excel.

### The Power of Spaced Repetition in Learning

To address this issue, we need to focus on the most effective methods of learning and information retention. Spaced repetition is widely recognized as one of the best techniques for mastering new information. This method involves reviewing information at increasing intervals over time, which helps to reinforce memory and understanding. By spacing out the repetition of study materials, students can significantly enhance their retention and recall abilities, leading to better long-term mastery of the content.

### Flashcards: The Ideal Tool for Spaced Repetition

Flashcards have proven to be an excellent tool for implementing spaced repetition. They allow students to break down complex information into manageable chunks, making it easier to review and memorize key concepts. With flashcards, students can systematically revisit information, reinforcing their learning in a structured and effective manner.

By leveraging the power of flashcards and spaced repetition, we can help level the playing field for all students preparing for the NSMQ. Providing equitable access to high-quality flashcard sets and incorporating spaced repetition into study routines can ensure that every student, regardless of their school's resources, has the opportunity to excel in the competition. This approach not only promotes fairness but also enhances the overall quality of education and learning outcomes for students across the board.
        """
    )
