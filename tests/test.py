import unittest
from PlimFlow import open_workflow
from PlimFlow import check_data
from dag import DAG

class TestOpenWorkflow(unittest.TestCase):
    def test_file_not_found(self):
        """
        Testa o tratamento de exceção para o caso de arquivo não encontrado
        """
        path = './workflows/ArquivoNaoExistente.json'
        with self.assertRaises(SystemExit):
            result = open_workflow(path)
    
    def test_invalid_file(self):
        """
        Testa o tratamento de exceção para o caso de um arquivo inválido
        """
        path = './workflows/ArquivoInvalido.txt'
        with self.assertRaises(SystemExit):
            result = open_workflow(path)

class TestCheckData(unittest.TestCase):
    def test_steps_not_found(self):
        """
        Testa o tratamento de exceção para o caso de um workflow sem parâmetro Steps
        """
        data = {"DAG": "DagParaTeste", "Autor": "Fulano"}
        with self.assertRaises(AssertionError):
            check_data(data)

    def test_steps_not_list(self):
        """
        Testa o tratamento de exceção para o caso em que Steps não é uma lista
        """
        data = {"DAG": "DagParaTeste", "Autor": "Fulano", 'Steps': 'Um texto'}
        with self.assertRaises(AssertionError):
            check_data(data)
    
    def test_steps_empty_list(self):
        """
        Testa o tratamento de exceção para o caso em que Steps é uma lista vazia
        """
        data = {"DAG": "DagParaTeste", "Autor": "Fulano", 'Steps': []}
        with self.assertRaises(AssertionError):
            check_data(data)
    
    def test_steps_not_dict(self):
        """
        Testa o tratamento de exceção para o caso em que uma step não é definida por um dicionário
        """
        data = {"DAG": "DagParaTeste", "Autor": "Fulano", 'Steps': ["Um texto"]}
        with self.assertRaises(AssertionError):
            check_data(data)

    def test_nomefuncao_not_found(self):
        """
        Testa o tratamento de exceção para o caso de uma step sem o parâmetro NomeFuncao
        """
        data = {"DAG": "DagParaTeste", "Autor": "Fulano", 'Steps': [{"Entradas": [1,2], "Dependencias": []}]}
        with self.assertRaises(AssertionError):
            check_data(data)
    
    def test_nomefuncao_not_string(self):
        """
        Testa o tratamento de exceção para o caso de uma step com parâmetro NomeFuncao diferente de string
        """
        data = {"DAG": "DagParaTeste", "Autor": "Fulano", 'Steps': [{"NomeFuncao": 1, "Entradas": [1,2], "Dependencias": []}]}
        with self.assertRaises(AssertionError):
            check_data(data)

    def test_entradas_not_found(self):
        """
        Testa o tratamento de exceção para o caso de uma step sem o parâmetro Entradas
        """
        data = {"DAG": "DagParaTeste", "Autor": "Fulano", 'Steps': [{"NomeFuncao": "Funcao_01", "Dependencias": []}]}
        with self.assertRaises(AssertionError):
            check_data(data)

    def test_entradas_not_list(self):
        """
        Testa o tratamento de exceção para o caso de uma step com parâmetro Entradas diferente de lista
        """
        data = {"DAG": "DagParaTeste", "Autor": "Fulano", 'Steps': [{"NomeFuncao": "Funcao_01", "Entradas": (1,2), "Dependencias": []}]}
        with self.assertRaises(AssertionError):
            check_data(data)

    def test_dependencias_not_found(self):
        """
        Testa o tratamento de exceção para o caso de uma step sem o parâmetro Dependencias
        """
        data = {"DAG": "DagParaTeste", "Autor": "Fulano", 'Steps': [{"NomeFuncao": "Funcao_01", "Entradas": [1,2]}]}
        with self.assertRaises(AssertionError):
            check_data(data)
    
    def test_dependencias_not_list(self):
        """
        Testa o tratamento de exceção para o caso de uma step com parâmetro Dependencias diferente de lista
        """
        data = {"DAG": "DagParaTeste", "Autor": "Fulano", 'Steps': [{"NomeFuncao": "Funcao_01", "Entradas": [1,2], "Dependencias": "Funcao_01"}]}
        with self.assertRaises(AssertionError):
            check_data(data)

class TestOrderSteps(unittest.TestCase):
    def test_deadlock(self):
        """
        Testa o tratamento de exceção para o caso de uma sequência de execução inatingível
        """
        dag = DAG({"Steps": [{"NomeFuncao": "Funcao_05", "Entradas": [1,2], "Dependencias": ["Funcao_06"]}]})
        with self.assertRaises(AssertionError):
            dag.order_steps()

class TestGetFunctions(unittest.TestCase):
    def test_module_not_found(self):
        """
        Testa o tratamento de exceção para o caso de módulo não encontrado
        """
        dag = DAG({"Steps": [{"NomeFuncao": "Funcao_05", "Entradas": [1,2], "Dependencias": []}]})
        dag.order_steps()
        with self.assertRaises(SystemExit):
            dag.get_functions()
        
    def test_method_not_found(self):
        """
        Testa o tratamento de exceção para o caso de método não encontrado
        """
        dag = DAG({"Steps": [{"NomeFuncao": "Funcao_Teste", "Entradas": [1,2], "Dependencias": []}]})
        dag.order_steps()
        with self.assertRaises(SystemExit):
            dag.get_functions()

if __name__ == '__main__':
    unittest.main()
