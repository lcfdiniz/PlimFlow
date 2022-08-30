import argparse
import json
import sys
import time
import datetime
from dag import DAG

# Definicao da versao
version = '0.0.1'

# Verifica a consistencia dos dados
def check_data(data):
    assert 'Steps' in data.keys(), "Erro. Parâmetro 'Steps' não especificado."
    assert type(data['Steps']) == list, "Erro. Suas steps devem estar contidas em uma lista."
    assert len(data['Steps'])>0, "Erro. Suas steps devem ser uma lista não vazia."
    for i, step in enumerate(data['Steps']):
        assert type(step) == dict, f"Erro na step {i+1}. Cada uma de suas steps deve estar no formato de um dicionário de dados."
        assert 'NomeFuncao' in step.keys(), f"Erro na step {i+1}. Parâmetro 'NomeFuncao' não especificado."
        assert type(step['NomeFuncao']) == str, f"Erro na step {i+1}. Defina o nome da função como uma string, sem a extensão (.py)."
        assert 'Entradas' in step.keys(), f"Erro na step {i+1}. Parâmetro 'Entradas' não especificado."
        assert type(step['Entradas']) == list, f"Erro na step {i+1}. Defina as entradas da função em formato de lista."
        assert 'Dependencias' in step.keys(), f"Erro na step {i+1}. Parâmetro 'Dependencias' não especificado."
        assert type(step['Dependencias']) == list, f"Erro na step {i+1}. Defina as dependências da função em formato de lista."

# Abre o arquivo com a definicao do workflow
def open_workflow(path):
    try:
        file = open(path)
        data = json.load(file)
    except FileNotFoundError:
        print("Erro! Arquivo não encontrado.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Erro! Verifique se o arquivo está em um formato válido (JSON).")
        sys.exit(1)
    # Verifica a consistencia dos dados
    check_data(data)
    return data

# Gera um log da execucao em JSON
def generate_log(dag, delta_t):
    log = dict()
    log['Nome'] = dag.nome
    log['Autor'] = dag.autor
    log['Duracao'] = round(delta_t*1000.0,2) # Tempo em ms
    for layer in dag.layers:
        for step in layer:
            for i, entry in enumerate(step['Entradas']):
                if entry not in dag.error_codes: step['Entradas'][i] = str(type(entry))
            step['Funcao'] = 'OK'
            if step['Output'] not in dag.error_codes: step['Output'] = 'OK'
    log['Pipeline'] = dag.layers
    data = datetime.datetime.now()
    filename = f'{data.day}_{data.month}_{data.year}__{data.hour}_{data.minute}_{data.second}'
    # Salva o dicionario em formato JSON
    with open('./logs/' + filename, "w") as outfile:
        json.dump(log, outfile, indent=4)

if __name__ == '__main__':
    # Inicializando o parser
    parser = argparse.ArgumentParser()
    # Adicionando um argumento obrigatorio
    parser.add_argument("--workflow",
                        help="Arquivo contendo as definicoes do workflow a ser executado", required=True)
    # Le argumentos da linha de comando
    args = parser.parse_args()
    # Abre o arquivo com a definicao do workflow e verifica a consistencia dos dados
    data = open_workflow(args.workflow)
    # Inicia o contador de tempo de execucao
    t = time.time()
    # Cria um objeto do tipo DAG
    dag = DAG(data)
    # Ordena as steps de acordo com suas dependencias de execucao
    dag.order_steps()
    # Permite acessar o path ./src
    sys.path.insert(0, './src')
    # Armazena as funcoes especificadas
    dag.get_functions()
    # Executa as funcoes de acordo com a ordem especificada
    dag.run_pipeline()
    # Registra o intervalo de tempo decorrido na execucao da DAG
    delta_t = time.time() - t
    # Gera um log da execucao em JSON
    generate_log(dag, delta_t)
