# Dataset de Repositórios OSS (Open Source Software)

Este repositório contém scripts python para montagem de um dataset de repositórios OSS utilizando para tanto a [API do Github](https://docs.github.com/en/rest)

Foi feito utilizando as seguintes tecnologias:

- [Python 3.8](https://www.python.org/)
- [SQLite3](https://www.sqlite.org/index.html)
- [Perceval](https://github.com/chaoss/grimoirelab-perceval)
- [Requests](https://docs.python-requests.org/en/master/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

## Configuração

Verifique se você tem o SQLite3 instalado na sua máquina local. Caso contrário, siga o passo a passo para instalação [aqui](https://www.servermania.com/kb/articles/install-sqlite/)

Verifique se você tem a versão 3.8 instalada do Python na sua máquina local. Caso não tenha, siga este [tutorial](https://tutorial.djangogirls.org/en/installation/#python)

Se tudo estiver ok, teste estes dois comandos em seu terminal e veja se tem um output parecido:

```sh
$ python --version
>>> Python 3.8.0

$ pip --version
>>> pip 21.0.1 from ~/.asdf/installs/python/3.8.0/lib/python3.8/site-packages/pip (python 3.8)
```

Após as checagens, crie uma virtualenv na pasta raiz do projeto seguindo este [tutorial](https://tutorial.djangogirls.org/en/django_installation/#virtual-environment). Crie com o nome `env` ou `venv` e após a conclusão, ative a virtualenv.

Com a virtualenv ativada, execute o seguinte comando:

```sh
pip install -r requirements.txt -r requirments_dev.txt
```

Logo todas as dependencias para o projeto serão instaladas

Para finalizar, copie o `.env.sample` e cole com o nome `.env` na pasta raiz do projeto e preencha com a informação que está faltando

Para a `GITHUB_OAUTH_TOKEN` siga estes [passos](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token)

Se for utilizar mais de um token, preencha separado por virgulas como no exemplo do arquivo `.env.sample`. Caso contrário, apenas coloque o token.

## Atualizando dependências

Com a virtualenv ativada, primeiro altere ou adicione a dependência e a versão que deseja instalar/atualizar no arquivo `requirments.in`

Após isso, rode o comando no diretório raiz: `pip-compile --output-file=requirements.txt requirements.in`

## Arquivos

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

Se tudo estiver ok com a sua instalação você poderá utilizar os seguintes scripts:

- Para buscar e salvar repositórios dado uma query de busca, rode este comando:
`python scripts/query_repo.py`
Irá aparecer um prompt com um texto de apoio de como deve ser a query de busca
Para mais informações sobre as querys de busca de repositórios, siga a [documentação](https://docs.github.com/en/rest/reference/search)
