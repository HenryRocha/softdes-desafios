# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 09:00:39 2017

@author: rauli
"""

import hashlib
import numbers
import sqlite3
from datetime import datetime

from flask import Flask, render_template, request
from flask_httpauth import HTTPBasicAuth

DBNAME = "./quiz.db"


def lambda_handler(event, _context):
    """
    Lambda handler.
    Executa o que foi passado como evento.
    """

    def not_equals(first, second):
        if isinstance(first, numbers.Number) and isinstance(second, numbers.Number):
            return abs(first - second) > 1e-3
        return first != second

    ndes = int(event["ndes"])
    code = event["code"]
    args = event["args"]
    resp = event["resp"]
    diag = event["diag"]

    try:
        exec(code, locals())  # pylint: disable=exec-used

        test = []
        for index, _arg in enumerate(args):
            if not "desafio{0}".format(ndes) in locals():
                return "Nome da função inválido. Usar 'def desafio{0}(...)'".format(ndes)

            if not_equals(
                eval("desafio{0}(*_arg)".format(ndes)), resp[index]  # pylint: disable=eval-used
            ):
                test.append(diag[index])
    except Exception:  # pylint: disable=broad-except
        return "Função inválida."

    return " ".join(test)


def converte_data(orig):
    """
    Converte orig para uma string em formato de data padrão,
    utilizada para representar a data de expiração de um quiz.
    """

    return (
        orig[8:10]
        + "/"
        + orig[5:7]
        + "/"
        + orig[0:4]
        + " "
        + orig[11:13]
        + ":"
        + orig[14:16]
        + ":"
        + orig[17:]
    )


def get_quizes(user):
    """Mostrar todos quizes (admin) ou apenas aqueles antes da release"""

    conn = sqlite3.connect(DBNAME)
    cursor = conn.cursor()
    if user in ("admin", "fabioja"):
        cursor.execute("SELECT id, numb from QUIZ")
    else:
        cursor.execute(
            "SELECT id, numb from QUIZ where release < '{0}'".format(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )
    info = list(cursor.fetchall())
    conn.close()
    return info


def get_user_quiz(userid, quizid):
    """Mostrar quiz do usuario"""

    conn = sqlite3.connect(DBNAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT sent, answer, result FROM USERQUIZ "
        + "WHERE userid = ? AND quizid = ? ORDER BY sent DESC",
        (userid, quizid),
    )
    info = list(cursor.fetchall())
    conn.close()
    return info


def set_user_quiz(userid, quizid, sent, answer, result):
    """Quiz para um usuario"""

    conn = sqlite3.connect(DBNAME)
    cursor = conn.cursor()
    cursor.execute(
        "insert into USERQUIZ(userid, quizid, sent, answer, result) values (?, ?, ?, ?, ?);",
        (userid, quizid, sent, answer, result),
    )
    conn.commit()
    conn.close()


def get_quiz(id_, user):
    """Mostrar quiz específico"""

    conn = sqlite3.connect(DBNAME)
    cursor = conn.cursor()
    if user in ("admin", "fabioja"):
        cursor.execute(
            "SELECT id, release, expire, problem, tests, results, diagnosis, numb "
            + "FROM QUIZ where id = ?",
            (id_,),
        )
    else:
        cursor.execute(
            "SELECT id, release, expire, problem, tests, results, diagnosis, numb "
            + "FROM QUIZ where id = ? and release < ?",
            (id_, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
    info = list(cursor.fetchall())
    conn.close()
    return info


def set_info(pwd, user):
    """Definir senha para usuário"""

    conn = sqlite3.connect(DBNAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE USER set pass = ? where user = ?", (pwd, user))
    conn.commit()
    conn.close()


def get_info(user):
    """Pegar informações do usuário"""

    conn = sqlite3.connect(DBNAME)
    cursor = conn.cursor()
    cursor.execute("SELECT pass, type from USER where user = ?;", (user,))
    info = [reg[0] for reg in cursor.fetchall()]
    conn.close()
    if len(info) == 0:
        return None

    return info[0]


auth = HTTPBasicAuth()

app = Flask(__name__, static_url_path="")
app.secret_key = "A0Zr98j/3yX R~XHH!jmN]LWX/,?TX"


@app.route("/", methods=["GET", "POST"])
@auth.login_required
def main():
    """Página principal"""

    msg = ""
    page = 1
    challenges = get_quizes(auth.username())
    sent = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if request.method == "POST" and "ID" in request.args:
        id_ = request.args.get("ID")
        quiz = get_quiz(id_, auth.username())
        if len(quiz) == 0:
            msg = "Boa tentativa, mas não vai dar certo!"
            page = 2
            return render_template(
                "index.html",
                username=auth.username(),
                challenges=challenges,
                p=page,
                msg=msg,
            )

        quiz = quiz[0]
        if sent > quiz[2]:
            msg = "Sorry... Prazo expirado!"

        files = request.files["code"]
        filename = "./upload/{0}-{1}.py".format(auth.username(), sent)
        files.save(filename)
        with open(filename, "r", encoding="utf-8") as file_p:
            answer = file_p.read()

        # lamb = boto3.client('lambda')
        args = {
            "ndes": id_,
            "code": answer,
            "args": eval(quiz[4]),  # pylint: disable=eval-used
            "resp": eval(quiz[5]),  # pylint: disable=eval-used
            "diag": eval(quiz[6]),  # pylint: disable=eval-used
        }

        feedback = lambda_handler(args, "")

        result = "Erro"
        if len(feedback) == 0:
            feedback = "Sem erros."
            result = "OK!"

        set_user_quiz(auth.username(), id_, sent, feedback, result)

    if request.method == "GET":
        if "ID" in request.args:
            id_ = request.args.get("ID")
        else:
            id_ = 1

    if len(challenges) == 0:
        msg = "Ainda não há desafios! Volte mais tarde."
        page = 2
        return render_template(
            "index.html",
            username=auth.username(),
            challenges=challenges,
            p=page,
            msg=msg,
        )

    quiz = get_quiz(id_, auth.username())

    if len(quiz) == 0:
        msg = "Oops... Desafio invalido!"
        page = 2
        return render_template(
            "index.html",
            username=auth.username(),
            challenges=challenges,
            p=page,
            msg=msg,
        )

    answers = get_user_quiz(auth.username(), id_)

    return render_template(
        "index.html",
        username=auth.username(),
        challenges=challenges,
        quiz=quiz[0],
        e=(sent > quiz[0][2]),
        answers=answers,
        p=page,
        msg=msg,
        expi=converte_data(quiz[0][2]),
    )


@app.route("/pass", methods=["GET", "POST"])
@auth.login_required
def change():
    """Página para alterar senha"""

    if request.method == "POST":
        velha = request.form["old"]
        nova = request.form["new"]
        repet = request.form["again"]

        page = 1
        msg = ""
        if nova != repet:
            msg = "As novas senhas nao batem"
            page = 3
        elif get_info(auth.username()) != hashlib.md5(velha.encode()).hexdigest():
            msg = "A senha antiga nao confere"
            page = 3
        else:
            set_info(hashlib.md5(nova.encode()).hexdigest(), auth.username())
            msg = "Senha alterada com sucesso"
            page = 3
    else:
        msg = ""
        page = 3

    return render_template(
        "index.html",
        username=auth.username(),
        challenges=get_quizes(auth.username()),
        p=page,
        msg=msg,
    )


@app.route("/logout")
def logout():
    """Logout"""

    return render_template("index.html", p=2, msg="Logout com sucesso"), 401


@auth.get_password
def get_password(username):
    """Pegar senha do usuário"""

    return get_info(username)


@auth.hash_password
def hash_pw(password):
    """Hash senha do usuário"""

    return hashlib.md5(password.encode()).hexdigest()


def main():
    """Iniciar servidor"""

    app.run(debug=True, host="0.0.0.0", port=80)


if __name__ == "__main__":
    main()
