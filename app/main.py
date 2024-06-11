import pandas as pd
from sqlalchemy import create_engine

pd.options.mode.chained_assignment = None  # default='warn'

import streamlit as st
from streamlit_extras.let_it_rain import rain

from database import *
from utils import *
from state_management import set_state, setIndex

from flashcards import flashcard
from fsrs import *
from datetime import datetime, timedelta, UTC


def getTimeDelta(datetime):
    now = datetime.now(UTC)
    timeDifference = datetime - now
    if timeDifference.days == 0:
        return f"< {timeDifference.seconds // 60} minutes"
    else:
        return f"{timeDifference.days} days"


def LetItRain():
    rain(
        emoji="🥳",
        font_size=54,
        falling_speed=10,
        animation_length="infinite",
    )


def main():
    # Initial page config
    st.set_page_config(
        page_title="Flashcard App",
        page_icon=":brain:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # load questions from database into dataframe
    questions_df = pd.read_sql_table("flashcards", "sqlite:///flashcard_ai.db")

    # Title section
    st.header("SmartCards AI :brain:", divider="rainbow")
    st.subheader("Intelligent Flashcards for National Quiz Champions!")

    # Sidebar
    st.sidebar.header("Select Filters")
    st.sidebar.write(
        ":orange[Please select a subject, year and round to start revision]"
    )

    ##  Filter questions by year, subject and round
    selectedYear = FilterByYear()
    selectedSubject = FilterBySubject()
    selectedRound = FilterByRound()

    # Main View
    # Setting initial state of the stage and index
    if "stage" not in st.session_state:
        st.session_state.stage = 0
    if "index" not in st.session_state:
        st.session_state.index = 0
    if st.session_state.stage == 0:
        setIndex(0)
        addSummary()
        startRevision = st.sidebar.button(
            "Start Revision", on_click=set_state, args=[1]
        )

    if st.session_state.stage == 1:
        restartRevision = st.sidebar.button(
            "Restart Revision", on_click=set_state, args=[0]
        )
        questionsToRevise = FilterQuestions(
            selectedSubject, selectedYear, selectedRound
        )
        if "cardsLeft" not in st.session_state:
            st.session_state.cardsLeft = len(questionsToRevise)
        # number of cards left
        st.write(f":red[Number of Cards Left: ] {st.session_state.cardsLeft}")
        st.write(f":green[Card Number: ] {st.session_state.index + 1}")

        indices = questionsToRevise.index.tolist()
        scheduler = FSRS()

        nextCard = st.button("Next Card", type="primary")
        if nextCard:
            st.session_state.index += 1
            st.session_state.cardsLeft -= 1

        with st.container(height=400):
            # get card and rating options
            card = getCard(questionsToRevise, indices, st.session_state.index)

            # initialise card for review
            schedulingCards = review_card(card, scheduler)

            # generate rating options
            cardEasy = card.rate_easy(schedulingCards)
            cardGood = card.rate_good(schedulingCards)
            cardHard = card.rate_hard(schedulingCards)
            cardAgain = card.rate_again(schedulingCards)

            # show card and answer
            showCard(card)
            showAnswer(card)

        # buttons
        col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1, 1, 2])

        with col2:
            nextReview = getTimeDelta(cardEasy.due)
            easyButton = st.button(f"Easy", type="primary")
            if easyButton:
                card = cardEasy
                rowid = indices[st.session_state.index]
                update_card(questionsToRevise, card, rowid)

                print(f"from getData {questionsToRevise.loc[rowid]}")
                st.write(f"Next review in: {nextReview}")

        with col3:
            nextReview = getTimeDelta(cardGood.due)
            goodButton = st.button("Good", type="primary")
            if goodButton:
                card = cardGood
                rowid = indices[st.session_state.index]
                update_card(questionsToRevise, card, rowid)

                print(f"from getData {questionsToRevise.loc[rowid]}")
                st.write(f"Next review in: {nextReview}")
        with col4:
            nextReview = getTimeDelta(cardHard.due)
            hardButton = st.button("Hard", type="primary")
            if hardButton:
                card = cardHard
                rowid = indices[st.session_state.index]
                update_card(questionsToRevise, card, rowid)

                print(f"from getData {questionsToRevise.loc[rowid]}")
                st.write(f"Next review in: {nextReview}")

        with col5:
            nextReview = getTimeDelta(cardAgain.due)
            againButton = st.button("Again", type="primary")
            if againButton:
                card = cardAgain
                rowid = indices[st.session_state.index]
                update_card(questionsToRevise, card, rowid)

                print(f"from getData {questionsToRevise.loc[rowid]}")
                st.write(f"Next review in: {nextReview}")

        # stop when cards are done
        if st.session_state.index == (len(questionsToRevise) - 1):
            set_state(3)
    if st.session_state.stage == 3:
        LetItRain()
        st.title(
            ":rainbow[You have completed this set. Select another set of questions to continue Learning]"
        )
        st.button("Start Over", on_click=set_state, args=[0])


if __name__ == "__main__":
    main()
