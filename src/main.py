import sqlite3
from pathlib import Path

from adduser import main as add_user_main
from softdes import main as softdes_main

if __name__ == "__main__":
    # Check if the file "quiz.db" exists in the current directory.
    # If it does not exist, create it.
    quiz_file = Path("quiz.db")
    if not quiz_file.is_file() or quiz_file.stat().st_size == 0:
        quiz_file.touch(exist_ok=True)

        # Run the sql script against the database.
        with sqlite3.connect("quiz.db") as conn:
            with open("quiz.sql", "r") as f:
                conn.executescript(f.read())

        # Check if the file "users.csv" exists in the current directory.
        # If it does not exist, throw an error.
        users_file = Path("users.csv")
        if not users_file.is_file():
            raise FileNotFoundError("users.csv")

        # Run the adduser script.
        add_user_main()

    # Run the app.
    softdes_main()
