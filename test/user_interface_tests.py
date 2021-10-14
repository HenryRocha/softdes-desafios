import os
import unittest
from pathlib import Path
from tempfile import mkstemp

from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By


class InterfaceTest(unittest.TestCase):
    base_url: str = "localhost:3000"
    user: str = "admin"
    pwd: str = "admin"
    login_url: str = f"http://{user}:{pwd}@{base_url}"

    def setUp(self):
        executable_path: Path = Path(__file__).parent / "geckodriver"
        self.driver = webdriver.Firefox(executable_path=executable_path)
        super().setUp()

    def test_login_success(self):
        self.driver.get(self.login_url)
        navbar = self.driver.find_element(By.ID, "navbarsExampleDefault")
        navbar_user_hello = navbar.find_element(By.CLASS_NAME, "nav-link")
        self.assertIn(self.user, navbar_user_hello.text)

    def test_login_invalid(self):
        self.driver.get(f"http://{self.user}:x@{self.base_url}")

        # Dismiss the login alert.
        Alert(self.driver).dismiss()

        body = self.driver.find_element(By.TAG_NAME, "body")
        self.assertIn("Unauthorized Access", body.text)

    def test_send_quiz_with_correct_answer(self):
        self.driver.get(self.login_url)

        fd, path = mkstemp("sample", "py")
        with os.fdopen(fd, "w") as fp:
            fp.write("""def desafio1(number):\n\treturn 0""")

        self.driver.find_element(By.ID, "resposta").send_keys(path)
        self.driver.find_element(By.XPATH, '//button[text()="Enviar"]').click()
        os.unlink(path)

        assert self.driver.find_elements(By.TAG_NAME, "td")[2].text == "OK!"

    def test_send_quiz_with_incorrect_answer(self):
        self.driver.get(self.login_url)

        fd, path = mkstemp("sample", "py")
        with os.fdopen(fd, "w") as fp:
            fp.write("""def desafio1(number):\n\treturn 1""")

        self.driver.find_element(By.ID, "resposta").send_keys(path)
        self.driver.find_element(By.XPATH, '//button[text()="Enviar"]').click()
        os.unlink(path)

        assert self.driver.find_elements(By.TAG_NAME, "td")[2].text == "Erro"

    def tearDown(self):
        self.driver.close()
        super().tearDown()


if __name__ == "__main__":
    unittest.main()
