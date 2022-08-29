# PlimFlow

Motor simples de execução de DAGs para orientação do fluxo de execução de funções genéricas definidas pelo usuário.

## Configuração

Esse projeto foi desenvolvido em Python, utilizando apenas bibliotecas nativas da linguagem de programação. A versão escolhida para o desenvolvimento foi a 3.9.12, cujo download pode ser realizado [aqui](https://www.python.org/downloads/release/python-3912/). Durante a instalação, garanta que o Python seja adicionado ao PATH de seu sistema operacional, selecionando a checkbox correspondente.

## Utilização

O PlimFlow permite executar funções genéricas seguindo um pipeline definido pelo usuário. Para isso, devem ser observados dois tipos de arquivos: o arquivo de definição do **workflow** e as próprias **funções** a serem executadas.

### Workflow

O arquivo de definição do workflow deve estar contido no diretório `/workflows`, em formato JSON. Um JSON nada mais é que um dicionário de dados, que para esse caso deve conter os seguintes campos:

- **Nome** (opcional): uma string contendo o nome do workflow (caso não seja definido, recebe o nome "Desconhecido");
- **Autor** (opcional): uma string contendo o nome do usuário (caso não seja definido, recebe o nome "Desconhecido");
- **Steps** (obrigatório): um novo dicionário contendo as steps ou funções a serem executadas.

Cada uma das steps deve ser definida pelos seguintes campos (obrigatórios):

- **NomeFuncao**: uma string contendo o nome da função a ser executada (sem a extensão .py);
- **Entradas**: uma lista com os valores que devem ser passados como entrada da função. Caso um desses valores seja correspondente ao output de uma função da qual a step é dependente, escreva o nome dessa função (sem a extensão .py);
- **Dependencias**: uma lista contendo as funções das quais a step é dependente (sem a extensão .py);

Esse repositório possui um exemplo de arquivo de definição de workflow, localizado em `/workspaces/SampleWorkflow.json`.

### Funções

Os arquivos fonte das funções devem estar contidos no diretório `/src`, em formato Python (.py). Cada um desses arquivos deve implementar uma única definição de função, cujo nome deve ser igual ao do arquivo (sem a extensão .py).

Esse repositório possui exemplos de funções, localizadas em `/src`: `Funcao_01.py`, `Funcao_01.py`, `Funcao_01.py` e `Funcao_04.py`.

## Execução

O único parâmetro necessário ao programa é o arquivo de definição do workflow. Para executá-lo, acesse o repositório do projeto através de uma interface de linha de comando e insira o seguinte:



```
python PlimFlow.py --workflow ./workflows/SampleWorkflow.json
```

No exemplo acima, o arquvo `SampleWorkflow.json` foi utilizado para a definição do workflow. 
