# Servidor de Desafios

## Descrição

Esse projeto consiste em uma dashboard em que é possível registrar novos usuários e novos desafios (Quizzes) atrelados aos membros. Para o desenvolvimento dele foram utilizadas, principalmente, as bibliotecas Flask para produção de páginas web, SQLite como banco de dados SQL.

## Testes

### Unidade

Para executar os testes de unidade basta executar o seguinte comando:

```bash
pytest src/unit_tests.py
```

### Interface de usuário

Como usamos o Selenium para executar os testes, em conjunto com o WebDriver do Firefox, é necessário fazer o download do Geckodriver e coloca-lo dentro da pasta `src`. O driver pode ser encontrado nesse [link](https://github.com/mozilla/geckodriver/releases).

Para executar os testes de interface de usuário é necessário deixar o servidor rodando:

```
cd src && python3 main.py
```

e depois executar o seguinte comando:

```
python3 src/user_interface_tests.py
```
