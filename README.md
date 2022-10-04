# TimeSheet Project

## Tecnologias utilizadas

- Python 3.10.5
- Django + Django Rest Framework
- Postgres
- Nginx
- Docker + Docker Compose

## Fazendo deploy local do sistema

Após fazer o download do código fonte para sua máquina local, você deve entrar na pasta raiz do projeto e executar o seguinte código:

```shell
docker compose up -d
```

Caso a sua versão instalada do docker não tenha o `compose` mas você tem o `docker-compose` instalado, você pode utilizar o seguinte comando como alternativa:

```shell
docker-compose up -d
```

Este comando irá subir um container com a aplicação django, outro com um banco de dados postgres e o terceiro com o Nginx.

Em tempo de construção, ele também vai criar alguns registros para facilitar os testes.

Após subir o projeto e alguns segundos para o preenchimento e disponibilização da base de dados, você poderá acessar o sistema atraés da url `http://localhost`

Caso seja necessário subir em uma porta diferenta da porta `80` basta ir no arquivo `docker-compose.yml`, dentro da sessão `web` e alterar o seguinte trecho:

```
    ports:
      - "80:80"
```

Colocando na esquerda do sinal `:` a porta da sua máquina que você gostaria de usar.

### Acessando o sistema

#### Dados de acesso

Durante o build do sistema, são criados 11 usuários. E é possível acessar a aplicação com todos eles com seus respectivos usuário e senha, conforme tabela abaixo:


| Login  | Senha  | Admin |
|--------|--------|-------|
| admin  | admin  | Sim   |
| user02 | user02 | Não   |
| user03 | user03 | Não   |
| user04 | user04 | Não   |
| user05 | user05 | Não   |
| user06 | user06 | Não   |
| user07 | user07 | Não   |
| user08 | user08 | Não   |
| user09 | user09 | Não   |
| user10 | user10 | Não   |

#### Principais recursos visuais

O sistema conta com três interfaces para ajudar a administrar os dados.

- A primeira é acessada pela url inicial `http://localhost` e dá acesso a uma documentação no formato swagger onde você pode utilizar as apis, assim como ver também os dados de entrada e saída de cada uma delas.
- A segunda é acessada pela url `http://localhost/redoc` e você terá acesso a uma documentação estruturada e a possiblidade de fazer o download da documentação no formato `openAPI`
- A terceira é acessada pela url `http://localhost/admin` que é um painel administrativo onde você pode consultar e alterar dados de forma visual para facilitar a administração.

## Detalhes importantes do escopo

Informações de permissões não estavam presente no escopo e foram inferidas da seguinte forma:

- O administrador tem todos os acessos
- Usuário pode listar apenas o seu próprio usuário
- Usuário não podem criar, visualizar, editar ou excluir outros usuários que não o seu
- Usuário não pode criar, atualizar ou excluir um projeto
- Usuário tem acesso de visualizar projetos e membros apenas nos projetos dos quais faz parte
- Usuário tem acesso de inserir registro de hora apenas para projetos que faz parte
- Usuário pode listar, visualizar, alterar e excluir apenas os seus próprios registros de hora

## Manutenção do sistema

Conforme detalhado na sessão **Fazendo deploy local do sistema** você pode utilizar o docker em seu ambiente de desenvolvimento.

Porém, se preferir, é possível utilizar apenas os recursos locais. E para isso, basta seguir os passos:

- Fazer o checkout do código fonte em um local de sua preferência
- Copiar o arquivo `.env.sample` que está na raiz para a raiz, só que com o nome `.env`
  - Este arquivo tem as variáveis de ambiente utilizadas pelo sistema, caso queira alterar alguma, é necessário reiniciar o servidor local caso ele já tenha sido iniciado antes da alteração
- Dentro da pasta raiz, criar um virtua env com o seguinte comando `python -m venv .venv`
- Instalar as dependências do projeto com o comando `pip install -r requirements.txt`
- Ativar a virtual env. Caso esteja em um distro unix: `source ./venv/bin/activate` caso use windows: `.venv\Scripts\activate`
- Executar a migração do banco de dados com o comando `python manage.py migrate`
- Executar o comando customizado para pre popular a base de dados `python manage.py seed`
- Executar o servidor local do projeto com o comando `python manage.py runserver`
- Acessar o sistema através da url `http://localhost:8000`

### Qualidade de código

Para assegurar a qualidade durante a evolução do sistema, foram instalados e configurados as seguintes bibliotecas de qualidade de código:
- mypy
- flake8
- isort
- black

Você pode rodar cada uma deas isoladamente, conforma consta em suas respectivas documentações, como também pode executar um script que roda todas elas:

```
sh ./scripts/lint.sh
```

### Curiosidades

Para a implementação dos containers docker, foi utilizado uma estratégia de build chamada `multi-stage build`, que reduziu o tamanho da imagem da aplicação consideravelmente.