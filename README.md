# Dataset de Repositórios OSS (Open Source Software)

Este repositório contém scripts Python para montagem de um dataset de repositórios OSS utilizando para tanto a [API do GitHub](https://docs.github.com/en/rest).

Foi feito utilizando as seguintes tecnologias:

- [Python 3.8](https://www.python.org/)
- [SQLite3](https://www.sqlite.org/index.html)
- [Perceval](https://github.com/chaoss/grimoirelab-perceval)
- [Requests](https://docs.python-requests.org/en/master/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

## Configuração

Será necessário instalar alguns pacotes e realizar alguns procedimentos na sua máquina local para a configuração, como abordado a seguir.

### SQLite3

Verifique se você tem o SQLite3 instalado utilizando o comando a seguir:
```sh
$ sqlite3 -version
>>> 3.31.1 2020-01-27 [...]
```
Note que para executar tal comando, o SQLite3 deve estar no PATH do sistema. Caso o comando não retorne uma resposta com  a versão do SQLite3, siga o passo a passo para instalação [aqui](https://www.servermania.com/kb/articles/install-sqlite/).

### Python 3.8

Verifique se você tem a versão 3.8 do Python instalada utilizando o comando a seguir:
```sh
$ python3 --version
>>> Python 3.8.10
```

Caso o comando não possua uma saída semelhante, é provavel que seja necessária a instalação do Python seguindo este [tutorial](https://tutorial.djangogirls.org/en/installation/#python).

### pip

Verifique se você tem o pip instalado executando o comando:
```sh
$ pip --version
>>> pip 20.0.2 from /usr/lib/python3/dist-packages/pip (python 3.8)
```
Caso não tenha instalado, siga os passos descritos [aqui](https://pip.pypa.io/en/stable/installation/#installation).

## Virtualenv
Crie uma Virtualenv na pasta raiz do projeto executando o comando:
```sh
$ python3 -m venv env
```
Onde `env` é o nome dado para a Virtualenv. Escolha o nome `env` ou `venv`.

Em seguida, ative a Virtualenv criada.

#### Linux e MacOS

Execute
```sh
$ source env/bin/activate
```
ou
```sh
$ . env/bin/activate
```

#### Windows
Execute

```sh
> env\Scripts\activate
```

Lembre-se que `env` é o nome escolhido anteriormente para sua Virtualenv.

### Instalando requisitos
Com a Virtualenv ativada, execute o seguinte comando:

```sh
$ pip install -r requirements.txt -r requirements_dev.txt
```

Logo todas as dependencias para o projeto serão instaladas

### Variáveis de ambiente do projeto

Para finalizar, copie o `.env.sample` e cole com o nome `.env` na pasta raiz do projeto e preencha a variável `GITHUB_OAUTH_TOKEN`. Você pode colocar um ou mais tokens do GitHub separados por vírgula. Para obter este token, siga estes [passos](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token).


## Atualizando dependências

Com a Virtualenv ativada, primeiro altere ou adicione a dependência e a versão que deseja instalar/atualizar no arquivo `requirments.in`. Após isso, rode o comando `pip-compile --output-file=requirements.txt requirements.in` no diretório raiz.

## Arquivos do projeto

Uma simples explicação de cada arquivo contido no diretório `scripts`:

- `clone_repo.py`: Nele fazemos o clone dos repositórios com ajuda do Perceval
- `db.py`: Este arquivo contém funções úteis para comunicação com o banco de dados
- `enrich_repo.py`: Este arquivo envia para o ElasticSearch dados enriquecidos
- `files.py`: Arquivo com funções para I/O com arquivos JSON
- `github_api.py`: Script para comunicação com a API do Github
- `models.py`: Arquivo que contém as tabelas do banco de dados
- `projects.py`: Gera o arquivo `projects.json` para o GrimoireLab
- `query_repo.py`: Script que inicia a busca dos repositórios

## Utilizando o projeto

Se a instalação foi feita com sucesso, você poderá executar os scripts do projeto.

### `query_repo.py`

Script ara buscar e salvar repositórios dado uma query de busca. Para utilizar, execute o  comando `python scripts/query_repo.py`. Irá aparecer um prompt com um texto de apoio de como deve ser a query de busca.

Para mais informações sobre as querys de busca de repositórios, siga a [documentação](https://docs.github.com/en/rest/reference/search) da API do GitHub.

Os dados obtidos pelo script são salvos em um banco de dados SQLite3, chamado `db.sqlite3`.
