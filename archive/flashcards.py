from fsrs import *
from datetime import datetime, UTC

import sqlite3
from sqlite3 import Error
from contextlib import contextmanager
from database import get_db
from fsrs import *


class flashcard(Card):
    def __init__(self, has_preamble, preamble_text, question, answer, *args, **kwargs):
        super().__init__()
        if has_preamble == "Yes":
            self.has_preamble = True
        else:
            self.has_preamble = False
        self.preamble_text = preamble_text
        self.question = question
        self.answer = answer

    def __repr__(self):
        if self.has_preamble:
            return f"""Card: 
                preamble: {self.preamble_text} 
                question: {self.question} 
                answer: {self.answer} 
                due: {self.due} 
                stability: {self.stability}
                difficulty: {self.difficulty}
                elapsed_days:{self.elapsed_days}
                scheduled_days: {self.scheduled_days}
                reps: {self.reps}
                laspes: {self.lapses}
                state: {self.state}
            """
        else:
            return f"""Card: 
                    question: {self.question} 
                    answer: {self.answer} 
                    due: {self.due} 
                    stability: {self.stability}
                    difficulty: {self.difficulty}
                    elapsed_days:{self.elapsed_days}
                    scheduled_days: {self.scheduled_days}
                    reps: {self.reps}
                    laspes: {self.lapses}
                    state: {self.state}
                """

    def update_card(self, id_, *args, **kwargs):
        """
        Updates a card in the database with the given ID.

        Parameters:
            id_ (int): The ID of the card to update.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            str: A message indicating that the card has been updated.

        Raises:
            Error: If there is an error executing the SQL query.

        This function updates a card in the database with the given ID. It first checks if the ID is provided and assigns it to the `id_` attribute of the class. Then, it gets a database connection and executes an SQL query to update the card in the `flashcards` table. The query updates the `due`, `stability`, `difficulty`, `elapsed_days`, `scheduled_days`, `reps`, `lapses`, and `state` columns of the card with the corresponding values from the class attributes. The card is identified by its ID. If the update is successful, the function commits the changes and returns a message indicating that the card has been updated. If there is an error executing the SQL query, it raises an `Error` exception.
        """
        self.id_ = id_
        # get database connection
        with get_db() as conn:
            cur = conn.cursor()
            try:
                cur.execute(
                    "UPDATE flashcards SET due = ?, stability = ?, difficulty = ?, elapsed_days = ?, scheduled_days = ?, reps = ?, lapses = ?, state = ? WHERE rowid = ?",
                    (
                        self.due,
                        self.stability,
                        self.difficulty,
                        self.elapsed_days,
                        self.scheduled_days,
                        self.reps,
                        self.lapses,
                        self.state,
                        self.id_,
                    ),
                )
                conn.commit()
                print("updated card")
                return "Updated card"
            except Error as e:
                raise

    def review_card(self, scheduler, *args, **kwargs):
        time = datetime.now(UTC)
        scheduling_cards = scheduler.repeat(self, time)
        return scheduling_cards

    def rate_easy(self, scheduling_cards):
        card_easy = scheduling_cards[Rating.Easy].card
        return card_easy

    def rate_good(self, scheduling_cards):
        card_good = scheduling_cards[Rating.Good].card
        return card_good

    def rate_hard(self, scheduling_cards):
        card_hard = scheduling_cards[Rating.Hard].card
        return card_hard

    def rate_again(self, scheduling_cards):
        card_again = scheduling_cards[Rating.Again].card
        return card_again
