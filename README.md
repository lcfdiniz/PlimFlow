# :globe_with_meridians: PlimFlow

Motor simples de execução de DAGs para orientação do fluxo de execução de funções genéricas definidas pelo usuário.

## :wrench: Configuração

Esse projeto foi desenvolvido em Python, utilizando apenas bibliotecas nativas da linguagem de programação. A versão escolhida para o desenvolvimento foi a 3.9.12, cujo download pode ser realizado [aqui](https://www.python.org/downloads/release/python-3912/). Durante a instalação, garanta que o Python seja adicionado ao PATH de seu sistema operacional, selecionando a checkbox correspondente.

## :book: Utilização

O PlimFlow permite executar funções genéricas seguindo um pipeline definido pelo usuário. Para isso, devem ser observados dois tipos de arquivos: o arquivo de definição do **workflow** e as próprias **funções** a serem executadas.

### Workflow

O arquivo de definição do workflow deve estar contido no diretório `/workflows`, em formato JSON. Um JSON nada mais é que um dicionário de dados, que para esse caso deve conter os seguintes campos:

- **DAG** (opcional): uma string contendo o nome do workflow (caso não seja definido, recebe o nome "Desconhecido");
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

## :rocket: Execução

O único parâmetro necessário ao programa é o arquivo de definição do workflow. Para executá-lo, acesse o repositório do projeto através de uma interface de linha de comando e insira o seguinte:



```
python PlimFlow.py --workflow ./workflows/SampleWorkflow.json
```

No exemplo acima, o arquvo `SampleWorkflow.json` foi utilizado para a definição do workflow.

## :scroll: Logs

No diretório `/logs` podem ser vistos os históricos de execução do programa, caso essa tenha sido bem sucedida. O arquivo de log contém as seguintes informações:

- **Nome**: nome da DAG, conforme apresentado no arquivo de definição do workflow (caso não seja definido, recebe o nome "Desconhecido");
- **Autor**: nome do autor, conforme apresentado no arquivo de definição do workflow (caso não seja definido, recebe o nome "Desconhecido");
- **Duracao**: tempo de execução do workflow, em milissegundos (ms);
- **Pipeline**: uma lista contendo as camadas de execução e suas respectivas steps.

Para cada uma das steps, as seguintes informações são disponibilizadas:

- **NomeFuncao**: nome da função executada;
- **Entradas**: tipo dos dados de entrada utilizados;
- **Dependencias**: dependências da função;
- **Funcao**: "OK" caso a função tenha sido carregada corretamente (único caso, senão não é gerado log);
- **Output**: "OK" caso a função não retorne uma exceção ou erro, senão, a exceção ou erro apresentado é exibido.

## :mag: Testes

No diretório `/tests` está localizado o arquivo `test.py`, que implementa uma série de testes das funções do programa, divididos por classe (função alvo). Para executar os testes em seu ambiente local, acesse o repositório do projeto através de uma interface de linha de comando e insira o seguinte:

```
python -m unittest tests/test.py
```

## :question: Dúvidas ou Sugestões?

Entre em contato comigo! :smile:

- [<img align="left" alt="Lucas F. Diniz | LinkedIn" width="22px" src="https://github.com/lcfdiniz/lcfdiniz/blob/main/images/linkedin.png" />](https://www.linkedin.com/in/lcfdiniz/) [LinkedIn](https://www.linkedin.com/in/lcfdiniz/)
- [<img align="left" alt="Lucas F. Diniz | Medium" width="22px" src="https://github.com/lcfdiniz/lcfdiniz/blob/main/images/medium.png" />](https://medium.com/@lcfdiniz) [Medium](https://medium.com/@lcfdiniz)
- <img align="left" alt="Lucas F. Diniz | Outlook" width="22px" src="https://github.com/lcfdiniz/lcfdiniz/blob/main/images/outlook.png" /> lcfdiniz@outlook.com
