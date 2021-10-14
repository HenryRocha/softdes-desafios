from typing import Dict

import softdes


def test_lambda_handler_invalid_function_name():
    test_code: str = """def desafio1(test_input):\n\tpass"""

    event: Dict = {"ndes": "0", "code": test_code, "args": ["0"], "resp": "0", "diag": "0"}

    errors: str = softdes.lambda_handler(event, "")
    assert errors == "Nome da função inválido. Usar 'def desafio0(...)'"


def test_lambda_handler_correct_function_correct_answer():
    test_code: str = """def desafio1(test_input):\n\treturn 5 + int(test_input)"""

    event: Dict = {"ndes": "1", "code": test_code, "args": ["5"], "resp": [10], "diag": ["3"]}

    errors: str = softdes.lambda_handler(event, "")
    assert errors == ""


def test_lambda_handler_correct_function_wrong_answer():
    test_code: str = """def desafio1(test_input):\n\treturn 5 + int(test_input)"""

    event: Dict = {
        "ndes": "1",
        "code": test_code,
        "args": ["5"],
        "resp": [11],
        "diag": ["Answer should be 11."],
    }

    errors: str = softdes.lambda_handler(event, "")
    assert errors == "Answer should be 11."
