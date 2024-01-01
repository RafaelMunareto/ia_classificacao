import pickle
import pandas as pd
import matplotlib.pyplot as plt
import constantes 

class Analise:
    def __init__(self, arquivo_previsao):
        self.arquivo_previsao = arquivo_previsao
        self.df = None

    def carregarDados(self):
        with open(self.arquivo_previsao, 'rb') as file:
            self.df = pickle.load(file)
        print("Carregado DF para análise.")

    def compararAcertos(self):
        # Comparando as previsões com os valores reais
        acertos = self.df[self.df[constantes.predicao] == self.df[constantes.alvo]]
        erros = self.df[self.df[constantes.predicao] != self.df[constantes.alvo]]
        
        # Criando o gráfico
        plt.bar(['Acertos', 'Erros'], [len(acertos), len(erros)])
        plt.title('Comparação de Acertos e Erros')
        plt.ylabel('Quantidade')
        print("Criação do gráfico de predict")
        plt.show()

    def analisarFaixasDeScore(self):
        # Definindo as faixas de score
        faixas = [0, 99.99, 199.99, 299.99, 399.99, 500]
        self.df['Faixa_Score'] = pd.cut(self.df['Score'], faixas)

        # Agrupando os dados por faixa e calculando os totais
        agrupado = self.df.groupby([constantes.faixa_score, constantes.alvo]).size().unstack()

        # Criando o gráfico
        agrupado.plot(kind='bar', stacked=True)
        plt.title('Análise de Pagamentos por Faixa de Score')
        plt.xlabel('Faixa de Score')
        plt.ylabel('Quantidade')
        print("Criação do gráfico de score")
        plt.show()


