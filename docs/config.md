# Guia do Desenvolvimento

Através desta plataforma os professores poderão disponibilizar novos desafios para os alunos.

## Ambiente de desenvolvimento

Primeiro é necessário instalar as dependências:  
```sh 
pip3 install black pylint flask flask-httpauth
```  

Em seguida é necessário criar o banco de dados:  
```sh 
sqlite3 quiz.db < quiz.sql
```  

Então criamos os usuários da aplicação através de um arquivo CSV:  
```sh
# Criar o usuário admin e o usuário username
printf "admin,0\nusername,0\n" > users.csv && python3 adduser.py
```

Para rodar a aplicação:  
```sh
python3 softdes.py
```


Existem dois endpoints nesta aplicação, `/` e `/pass`. Ambos os endpoints requerem autenticação. É necessário que o usuário esteja logado para ele possa ver qualquer conteúdo. 

A função responsável por receber e tratar todas as requisições em `/` é a função `main`. Ela aceita tanto requisições `GET` quanto `POST`. Quando a requisição de trata de um `GET`, ela retorna uma página HTML contendo os desafios e os envios feitos pelo usuário e também possibilita que o usuário faça um novo envio. A interface de usuário para essa página pode ser encontrada em `templates/index.html`.

Já quando a requisição feita em `/` é do tipo `POST`, ela significa o envio de uma solução para um desafio. O desafio é identificado pelo número do desafio, que vem junto da requisição, no parâmetro `ID`. O código enviado deve ser um arquivo `.py`. O código é verificado e o resultado é enviado para o usuário.

