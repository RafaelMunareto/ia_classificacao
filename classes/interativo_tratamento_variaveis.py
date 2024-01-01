import pandas as pd
import numpy as np

class InterativoTratamentoVariaveis:
    def __init__(self, df):
        self.df = df
        self.alvo = None
        self.previsores = None
        self.respostas = {} 

    def processarColunas(self):
        for coluna in list(self.df.columns):
            resposta = input(f"Essa coluna '{coluna}' é alvo, previsor ou descartar? (A/P/D): ").upper()
            if resposta == 'A':
                self.definirAlvo(coluna)
            elif resposta == 'P':
                self.tratarPrevisor(coluna)
            elif resposta == 'D':
                self.df.drop(coluna, axis=1, inplace=True)

    def definirAlvo(self, coluna):
        # Transformar para valores binários se necessário ou realizar outro tratamento específico
        self.alvo = self.df[coluna]
        self.df.drop(coluna, axis=1, inplace=True)

    def tratarPrevisor(self, coluna):
        tipo = input(f"Qual o tipo de dados da coluna '{coluna}'? (QT/QL/DT/CEP): ").lower()
        if tipo == 'qt':
            self.tratarQuantitativo(coluna)
        elif tipo == 'ql':
            self.tratarQualitativo(coluna)
        elif tipo == 'dt':
            self.tratarData(coluna)
        elif tipo == 'cep':
            self.tratarCEP(coluna)

    def tratarQuantitativo(self, coluna):
        escolha = input(f"Para NaN/Null na coluna '{coluna}', escolha (media/mediana/moda/0/descartar): ").lower()
        if escolha == 'media':
            self.df[coluna].fillna(self.df[coluna].mean(), inplace=True)
        elif escolha == 'mediana':
            self.df[coluna].fillna(self.df[coluna].median(), inplace=True)
        elif escolha == 'moda':
            self.df[coluna].fillna(self.df[coluna].mode()[0], inplace=True)
        elif escolha == '0':
            self.df[coluna].fillna(0, inplace=True)
        elif escolha == 'descartar':
            self.df.dropna(subset=[coluna], inplace=True)
            
    def tratarCEP(self, coluna):
        digitos = int(input("Quantos dígitos do CEP deseja usar para representar a região? "))
        self.tratarNaN(coluna, "cep")
        self.df[coluna] = self.df[coluna].astype(str).str[:digitos]

    def tratarQualitativo(self, coluna):
        self.tratarNaN(coluna, "qualitativo")
        # Transformação de categorias em números
        self.df[coluna] = self.df[coluna].astype('category').cat.codes
        
    def tratarNaN(self, coluna, tipo_dado):
        escolha = input(f"Para NaN/Null na coluna '{coluna}' (tipo {tipo_dado}), escolha (descartar/preencher): ").lower()
        if escolha == 'preencher':
            if tipo_dado == "qualitativo":
                preenchimento = input(f"Escolha o valor para preencher NaN/Null na coluna '{coluna}': ")
                self.df[coluna].fillna(preenchimento, inplace=True)
            elif tipo_dado in ["data", "cep"]:
                preenchimento = input(f"Escolha o valor numérico para preencher NaN/Null na coluna '{coluna}': ")
                self.df[coluna].fillna(preenchimento, inplace=True)
        elif escolha == 'descartar':
            self.df.dropna(subset=[coluna], inplace=True)

    def tratarData(self, coluna):
        escolha = input(f"Como deseja tratar a coluna de data '{coluna}'? (dias/meses/anos): ").lower()
        coluna_data = pd.to_datetime(self.df[coluna])
        if escolha == 'dias':
            self.df[coluna] = (coluna_data - coluna_data.min()).dt.days
        elif escolha == 'meses':
            self.df[coluna] = (coluna_data.dt.year - coluna_data.min().year) * 12 + coluna_data.dt.month
        elif escolha == 'anos':
            self.df[coluna] = coluna_data.dt.year - coluna_data.min().year
        
    def salvarRespostas(self):
        data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.respostas['data'] = data_atual
        with open(constantes.respostas_tratamento_base, 'wb') as file:
            pickle.dump(self.respostas, file)
        print(f"Respostas salvas em {nome_arquivo} em {data_atual}.")
        
    def processar(self):
        self.processarColunas()
        self.previsores = self.df.drop(columns=[self.alvo.name])
        print(f'isna dos previsores: {self.previsores.isna().sum()}')
        print(f'isna do alvo: {self.alvo.isna().sum()}')
        
        return self.previsores, self.alvo

# Exemplo de uso
# df = pd.read_csv('seu_arquivo.csv')
# tratamento = InterativoTratamentoVariaveis(df)
# previsores, alvo = tratamento.processar()
