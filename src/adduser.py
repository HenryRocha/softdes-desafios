"""
Esse modulo é usado para criar todos os usuários, a partir do arquivo .csv,
e inserio-los no banco de dados.
"""


import sqlite3
import hashlib


def add_user(user, pwd, user_type):
    """
    Insire um usuário no banco de dados.
    """

    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()
    cursor.execute(
        'Insert into USER(user,pass,type) values("{0}","{1}","{2}");'.format(user, pwd, user_type)
    )
    conn.commit()
    conn.close()


def main():
    """
    Função principal do script.
    Lê o arquivo .csv e insire os usuários no banco de dados.
    """

    with open("users.csv", "r", encoding="utf-8") as file:
        lines = file.read().splitlines()

    for users in lines:
        (user, user_type) = users.split(",")
        print(user)
        print(user_type)
        add_user(user, hashlib.md5(user.encode()).hexdigest(), user_type)


if __name__ == "__main__":
    main()
