import importlib
import sys

class DAG():
    def __init__(self, data):
        self.nome = data['DAG'] if 'DAG' in data.keys() else 'Desconhecido'
        self.autor = data['Autor'] if 'Autor' in data.keys() else 'Desconhecido'
        self.steps = data['Steps']
        self.error_codes = set([])
    
    # Ordena as steps de acordo com as dependencias
    def order_steps(self):
        self.layers = []
        # Completa a primeira camada, com as funcoes sem dependencias
        top = []
        for step in self.steps:
            if step['Dependencias'] == []: top.append(step)
        self.layers.append(top)
        current = [step for layer in self.layers for step in layer]
        remaining = [step for step in self.steps if step not in current]
        while len(remaining) > 0: # Enquanto existirem steps nao adicionadas as camadas do pipeline
            # Cria uma nova camada
            layer = []
            for step in remaining:
                # Verifica se as dependencias da funcao avaliada foram adicionadas as camadas anteriores
                if all(item in [step['NomeFuncao'] for step in current] for item in step['Dependencias']):
                    layer.append(step)
            # Se nenhuma step foi adicionada a camada, temos um deadlock na execucao da DAG
            assert len(layer)>0, "Erro! Ocorreu um Deadlock (steps bloqueadas). Verifique as dependências declaradas."
            self.layers.append(layer)
            current = [step for layer in self.layers for step in layer]
            remaining = [step for step in self.steps if step not in current]
    
    # Armazena as funcoes especificadas
    def get_functions(self):
        for layer in self.layers:
            for step in layer:
                try:
                    module = importlib.import_module(step['NomeFuncao'])
                    method = getattr(module, step['NomeFuncao'])
                    step['Funcao'] = method
                except ModuleNotFoundError:
                    print(f"Erro! O módulo {step['NomeFuncao']} não foi encontrado. Verifique o nome declarado na step ou se o módulo está no diretório /src")
                    sys.exit(1)
                except AttributeError:
                    print(f"Erro! A função {step['NomeFuncao']} não foi encontrada dentro do módulo de mesmo nome. Verifique o nome de função declarado no módulo.")
                    sys.exit(1)
    
    # Atualiza as entradas de uma funcao com as saidas de suas dependencias
    def update_state(self, param):
        step = [step for layer in self.layers for step in layer if step['NomeFuncao']==param][0]
        return step['Output']

    # Executa as funcoes de acordo com a ordem especificada
    def run_pipeline(self):
        for layer in self.layers:
            for step in layer:
                error = False
                for i, param in enumerate(step['Entradas']):
                    if param in step['Dependencias']:
                        # Atualiza as entradas de uma funcao com as saidas de suas dependencias
                        prev_output = self.update_state(param)
                        step['Entradas'][i] = prev_output
                        if prev_output in self.error_codes:
                            error = True
                            step['Output'] = "Erro Na Dependencia"
                            self.error_codes.add("Erro Na Dependencia")
                            break
                if not error:
                    try:
                        step['Output'] = step['Funcao'](*step['Entradas'])
                    except:
                        step['Output'] = str(sys.exc_info()[0])
                        self.error_codes.add(str(sys.exc_info()[0]))
