import pickle
from sklearn.ensemble import VotingClassifier
import constantes 

class MaquinaDeComites:
    def __init__(self, algoritmos_dir):
        self.algoritmos_dir = algoritmos_dir
        self.resultados = None
        self.previsores = None
        self.alvo = None
        self.modelos = {}

    def carregarResultados(self):
        with open(f'{self.algoritmos_dir}/{constantes.resultado_completo_df}', 'rb') as file:
            self.resultados = pickle.load(file)
        print("Resultado dos algoritimos carregados")

    def carregarModelos(self):
        for nome in self.resultados['resultados']:
            with open(f'{self.algoritmos_dir}/{nome}_modelo.pickle', 'rb') as file:
                self.modelos[nome] = pickle.load(file)
        print("Todos os dados de treinos carregados")
        
    def selecionarMelhores(self):
        # Ordena os modelos com base na acurácia e pega os dois melhores
        melhores_nomes = sorted(
            self.resultados['resultados'], 
            key=lambda x: self.resultados['resultados'][x]['accuracy'], 
            reverse=True
        )[:2]
        print("Os 2 melhores algoritimos escolhidos")
        return [self.modelos[melhores_nomes[0]], self.modelos[melhores_nomes[1]]]

    def criarComite(self):
        with open(f'{constantes.variaveis_dir}/{constantes.previsor_utilizado}', 'rb') as file:
            self.alvo = pickle.load(file)
        with open(f'{constantes.variaveis_dir}/{constantes.alvo}', 'rb') as file:
            self.alvo = pickle.load(file)
        self.carregarResultados()
        self.carregarModelos()
        melhores_modelos = self.selecionarMelhores()
        
        # Cria um modelo de Voting com os dois melhores modelos
        voting = VotingClassifier(estimators=[
            ('best1', melhores_modelos[0]),
            ('best2', melhores_modelos[1])
        ], voting='soft')

        # Assume-se que self.alvo e self.previsores são carregados de outra parte do código
        voting.fit(self.previsores, self.alvo)
        print("Criação do melhor algoritimo pela máquina de comitês")
        # Salva o melhor modelo híbrido
        with open(f'{self.algoritmos_dir}/{constantes.bm}.pickle', 'wb') as file:
            pickle.dump(voting, file)

        return voting


