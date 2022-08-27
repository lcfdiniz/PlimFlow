import argparse
import json
import sys
import importlib

# Definicao da versao
version = '0.0.1'

class DAG():
    def __init__(self, data):
        nome = data['DAG'] if 'DAG' in data.keys() else 'Desconhecido'
        autor = data['Autor'] if 'Autor' in data.keys() else 'Desconhecido'
        self.nome = nome
        self.autor = autor
        self.steps = data['Steps']
    
    def order_steps(self):
        self.layers = []
        top = []
        for step in self.steps:
            if step['Dependencias'] == []:
                top.append(step)
        self.layers.append(top)
        current = [step for layer in self.layers for step in layer]
        current_f = [step['Funcao'] for step in current]
        remaining = [step for step in self.steps if step not in current]
        while len(remaining) > 0:
            layer = []
            for step in remaining:
                if all(item in current_f for item in step['Dependencias']):
                    layer.append(step)
            self.layers.append(layer)
            current = [step for layer in self.layers for step in layer]
            current_f = [step['Funcao'] for step in current]
            remaining = [step for step in self.steps if step not in current]
    
    def get_functions(self):
        functions = [step['Funcao'] for layer in self.layers for step in layer]
        self.pipeline = []
        for function in functions:
            module = importlib.import_module(function)
            method_to_call = getattr(module, function)
            self.pipeline.append(method_to_call)

 # Verifica a consistencia dos dados
def assert_data(data):
    if 'Steps' not in data.keys():
        print('Erro. Parâmetro "Steps" não especificado.')
        return False
    else:
        steps_params = ['Funcao', 'Entradas', 'Dependencias']
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
        dag = DAG(data)
        # Ordena as steps de acordo com suas dependencias de execucao
        dag.order_steps()
        # Permite acessar o path ./src
        sys.path.insert(0, './src')
        # Armazena as funcoes especificadas
        dag.get_functions()
        for step in dag.pipeline:
            print(step.__code__.co_varnames)
            step(5,3)
    else:
        print('Erro na consistência dos dados, por favor verifique o arquivo de definição do workflow.')
