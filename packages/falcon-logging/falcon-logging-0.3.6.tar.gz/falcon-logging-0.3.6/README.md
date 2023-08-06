# Wrapper para trabalhar com a API do Cloud Logging

## Procedimento para upload no PYPI

### Pré requisitos
Instalar pacotes python
`python3 -m pip install --upgrade setuptools build wheel twine`

### Build e enviar ao PYPI

`python3 -m build`

`python3 -m twine upload dist/*`


### Instalar o pacote no projeto

`pip install falcon-logging`


## Utilização da biblioteca

Essa biblioteca espera que você passe o schema dos dados da tabela.

É aconselhado criar um arquivo de schema.py ou model.py onde seja definido a estrutura de dados da tabela.

### Instanciar o Middleware

Com o schema definido, você deve instanciar um classe

```python
from falcon_logging.logging import LogMiddleware

import falcon

class HealthCheckResource(object):

    def on_get(self, _, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200
        resp.body = 'OK'


def create():

    middlewares=[LogMiddleware()]

    _app = falcon.API(middleware=middlewares)
    _app.add_route('/', HealthCheckResource())

    return _app


app = create()
```

### Principais operações

Usando a classe `logging`, você pode executar algumas operações para auxiliar no desenvolvimento.

##### Logging

```python
from falcon_logging.logging import logging
logging.info({"key": "value"})
```
