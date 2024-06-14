import pandas as pd

from sqlalchemy import create_engine
import sqlite3
from sqlite3 import Error
from contextlib import contextmanager

DB_NAME = "flashcard_ai.db"


def add_questions_to_table(df):
    engine = create_engine("sqlite:///flashcard_ai.db")
    table_name = "flashcards"
    df.to_sql(table_name, engine, if_exists="append", index=False)
    return "Added questions to table"


@contextmanager
def get_db():
    # create db connection
    try:
        conn = sqlite3.connect(DB_NAME)
        yield conn
    except Error as e:
        raise
    finally:
        if conn:
            conn.close()


def select_flashcard_by_id(id):
    with get_db() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM flashcards WHERE rowid = ?", (id,))
            for row in cur:
                return dict(
                    (column[0], row[index])
                    for index, column in enumerate(cur.description)
                )
        except Error as e:
            raise


def select_all_flashcards():
    with get_db() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM flashcards")
            return cur.fetchall()
        except Error as e:
            raise


def update_card(df, card, rowid):
    # update values in dataframe
    df.loc[rowid, "due"] = card.due
    df.loc[rowid, "stability"] = card.stability
    df.loc[rowid, "difficulty"] = card.difficulty
    df.loc[rowid, "elapsed_days"] = card.elapsed_days
    df.loc[rowid, "scheduled_days"] = card.scheduled_days
    df.loc[rowid, "reps"] = card.reps
    df.loc[rowid, "lapses"] = card.lapses
    df.loc[rowid, "state"] = card.state

    # persist in sql database
    engine = create_engine("sqlite:///flashcard_ai.db")
    table_name = "flashcards"
    df.to_sql(table_name, engine, if_exists="append", index=False)
    return "Success"
