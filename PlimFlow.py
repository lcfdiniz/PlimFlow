import argparse
import json
import sys
import importlib
import time
import datetime

# Definicao da versao
version = '0.0.1'

class DAG():
    def __init__(self, data):
        nome = data['DAG'] if 'DAG' in data.keys() else 'Desconhecido'
        autor = data['Autor'] if 'Autor' in data.keys() else 'Desconhecido'
        self.nome = nome
        self.autor = autor
        self.steps = data['Steps']
    
    # Ordena as steps de acordo com as dependencias
    def order_steps(self):
        self.layers = []
        top = []
        for step in self.steps:
            if step['Dependencias'] == []:
                top.append(step)
        self.layers.append(top)
        current = [step for layer in self.layers for step in layer]
        current_f = [step['NomeFuncao'] for step in current]
        remaining = [step for step in self.steps if step not in current]
        while len(remaining) > 0:
            layer = []
            for step in remaining:
                if all(item in current_f for item in step['Dependencias']):
                    layer.append(step)
            if layer == []:
                print('Erro. Verifique as dependências declaradas para as steps.')
                break
            else:
                self.layers.append(layer)
                current = [step for layer in self.layers for step in layer]
                current_f = [step['NomeFuncao'] for step in current]
                remaining = [step for step in self.steps if step not in current]
    
    # Armazena as funcoes especificadas
    def get_functions(self):
        for layer in self.layers:
            for step in layer:
                try:
                    module = importlib.import_module(step['NomeFuncao'])
                    method_to_call = getattr(module, step['NomeFuncao'])
                    step['Funcao'] = method_to_call
                except:
                    step['Funcao'] = 'ErrorCode'
    
    # Atualiza as entradas de uma funcao com as saidas de suas dependencias
    def update_state(self, param):
        step = [step for layer in self.layers for step in layer if step['NomeFuncao']==param][0]
        return step['Output']

    # Executa as funcoes de acordo com a ordem especificada
    def run_pipeline(self):
        for layer in self.layers:
            for step in layer:
                for i, param in enumerate(step['Entradas']):
                    if param in step['Dependencias']:
                        # Atualiza as entradas de uma funcao com as saidas de suas dependencias
                        param = self.update_state(param)
                        step['Entradas'][i] = param
                if ('ErrorCode' in step['Entradas']) or (step['Funcao'] == 'ErrorCode'):
                    step['Output'] = 'ErrorCode'
                else:
                    try:
                        step['Output'] = step['Funcao'](*step['Entradas'])
                    except:
                        step['Output'] = 'ErrorCode'

 # Verifica a consistencia dos dados
def assert_data(data):
    if 'Steps' not in data.keys():
        print('Erro. Parâmetro "Steps" não especificado.')
        return False
    else:
        steps_params = ['NomeFuncao', 'Entradas', 'Dependencias']
        for i, step in enumerate(data['Steps']):
            missing_params = list(set(steps_params) - set(step.keys()))
            for param in missing_params:
             print(f'Erro. Parâmetro "{param}" da step {i+1} não especificado.')
             return False
    return True

# Abre o arquivo com a definicao do workflow
def open_workflow(path):
    try:
        file = open(path)
        data = json.load(file)
        checked = assert_data(data)
        return checked, data
    except:
        print('Erro ao carregar o arquivo escolhido. ', end='')
        print('Verifique se o mesmo foi especificado corretamente ou se está no formato JSON.')
        return False, []

# Gera um log da execucao em JSON
def generate_log(dag, delta_t):
    log = dict()
    log['Nome'] = dag.nome
    log['Autor'] = dag.autor
    log['Duracao'] = round(delta_t*1000.0,2) # Tempo em ms
    for layer in dag.layers:
        for step in layer:
            step['Entradas'] = [str(type(entry)) for entry in step['Entradas']]
            if step['Funcao'] != 'ErrorCode': step['Funcao'] = 'OK'
            if step['Output'] != 'ErrorCode': step['Output'] = 'OK'
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
    checked, data = open_workflow(args.workflow)
    if checked:
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
    else:
        print('Erro na consistência dos dados, por favor verifique o arquivo de definição do workflow.')
