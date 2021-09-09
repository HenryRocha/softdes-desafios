# Guia do Professor

Através desta plataforma os professores poderão disponibilizar novos desafios para os alunos.

## Adicionar usuários
Para adicionar novos usuários é necessário criar um novo arquivo ```users.csv``` que armazenará os registros em cada linha do arquivo da seguinte forma:  
```nome,tipo```  
<br>
Sendo:  
> * Nome: nome do usuário  
> * Tipo: tipo do usuário (admin, professor ou aluno)  

Em seguida é necessário criar o banco de dados e atualizá-lo através do comando:  
```sh 
sqlite3 quiz.db < quiz.sql 
```  
Para efetuar a integração dos novos membros é necessário rodar o comando:  
```sh 
python adduser.py
```  
## Adicionar desafios
Para inserir um novo desafio é necessário realizar de forma manual através do comando SQL em exemplo:  
```sh 
Insert into QUIZ(numb, release, expire, problem, tests, results, diagnosis) values (1, '2018-08-01','2018-12-31 23:59:59','Exemplo de problema','[[1],[2],[3]]','[0, 0, 0]','["a","b","c"]');
```  
Sendo:  
> * numb: Número do quiz. 
> * release: Data de ínicio no formato YYYY-MM-DD. 
> * expire: Data limite para envio no formato YYYY-MM-DD HH:MM:SS.
> * problem: Descrição do desafio.
> * tests: Testes a serem utilizados no formato de lista.
> * results: Resultados esperados pelos testes no formato de lista.
> * diagnosis: Feedback dos testes no formato de lista.

