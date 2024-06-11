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


# def update_card(card, id, flashcard):
#     """
#     Updates a card in the database with the given ID.

#     Parameters:
#         id_ (int): The ID of the card to update.
#         *args: Variable length argument list.
#         **kwargs: Arbitrary keyword arguments.

#     Returns:
#         str: A message indicating that the card has been updated.

#     Raises:
#         Error: If there is an error executing the SQL query.

#     This function updates a card in the database with the given ID. It first checks if the ID is provided and assigns it to the `id_` attribute of the class. Then, it gets a database connection and executes an SQL query to update the card in the `flashcards` table. The query updates the `due`, `stability`, `difficulty`, `elapsed_days`, `scheduled_days`, `reps`, `lapses`, and `state` columns of the card with the corresponding values from the class attributes. The card is identified by its ID. If the update is successful, the function commits the changes and returns a message indicating that the card has been updated. If there is an error executing the SQL query, it raises an `Error` exception.
#     """
#     self.id_ = id_
#     # get database connection
#     with get_db() as conn:
#         cur = conn.cursor()
#         try:
#             cur.execute(
#                 "UPDATE flashcards SET due = ?, stability = ?, difficulty = ?, elapsed_days = ?, scheduled_days = ?, reps = ?, lapses = ?, state = ? WHERE rowid = ?",
#                 (
#                     self.due,
#                     self.stability,
#                     self.difficulty,
#                     self.elapsed_days,
#                     self.scheduled_days,
#                     self.reps,
#                     self.lapses,
#                     self.state,
#                     self.id_,
#                 ),
#             )
#             conn.commit()
#             print("updated card")
#             return "Updated card"
#         except Error as e:
#             raise
