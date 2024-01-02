import pandas as pd
import numpy as np
import pickle
from datetime import datetime
import constantes

class InterativoTratamentoVariaveis:
    def __init__(self, df):
        self.df = df
        self.alvo = None
        self.previsores = None
        self.respostas = {}

    def solicitarEntradaValida(self, pergunta, funcao_validacao):
        while True:
            resposta = input(pergunta).strip().lower()
            if funcao_validacao(resposta):
                return resposta
            else:
                print("Resposta inválida, tente novamente.")

    def processarColunas(self):
        for coluna in list(self.df.columns):
            print(f"Amostra da coluna '{coluna}':\n{self.df[coluna].head(3)}")

            # Solicitando a entrada e convertendo para minúscula para padronização
            resposta = self.solicitarEntradaValida(
                f"Essa coluna '{coluna}' é alvo, previsor ou descartar? (A/P/D): ",
                lambda x: x.lower() in ['a', 'p', 'd']
            ).lower()

            if resposta == 'd':
                self.df.drop(coluna, axis=1, inplace=True)
            elif resposta == 'a':
                self.definirAlvo(coluna)
            elif resposta == 'p':
                novo_nome = input(f"Deseja renomear a coluna '{coluna}'? Deixe em branco para manter ou digite o novo nome: ")
                if novo_nome:
                    self.df.rename(columns={coluna: novo_nome}, inplace=True)
                    coluna = novo_nome

                self.tratarPrevisor(coluna)

                nan_count = self.df[coluna].isna().sum()
                print(f"Coluna {coluna} - NAN: {nan_count}")



    def definirAlvo(self, coluna):
        self.alvo = self.df[coluna]
        if self.alvo.dtype == 'object' and len(self.alvo.unique()) == 2:
            self.alvo = pd.Categorical(self.alvo).codes
        elif self.alvo.dtype in ['int64', 'float64'] and not set(self.alvo.unique()).issubset({0, 1}):
            print("Aviso: A coluna alvo não é binária e não foi convertida.")
        self.df['alvo'] = self.alvo
        self.df.drop(columns=coluna, inplace=True)
        self.respostas['alvo'] = {'coluna_original': coluna}
        
    def tratarQuantitativo(self, coluna):
        escolha = self.solicitarEntradaValida(
            f"Para NaN/Null na coluna '{coluna}', escolha (media/mediana/moda/0/1/descartar): ",
            lambda x: x in ['media', 'mediana', 'moda', '0', '1', 'descartar']
        )
        self.aplicarTratamentoNaN(coluna, escolha)
        
    def tratarPrevisor(self, coluna):
        tipo_dados = self.solicitarEntradaValida(
            f"Qual o tipo de dados da coluna '{coluna}'? (QT/QL/DT/CEP): ",
            lambda x: x in ['qt', 'ql', 'dt', 'cep']
        ).lower()

        if tipo_dados == 'qt':
            self.tratarQuantitativo(coluna)
        elif tipo_dados == 'ql':
            self.tratarQualitativo(coluna)
        elif tipo_dados == 'dt':
            self.tratarData(coluna)
        elif tipo_dados == 'cep':
            self.tratarCEP(coluna)

    def tratarQualitativo(self, coluna):
        escolha = self.solicitarEntradaValida(
            f"Para NaN/Null na coluna '{coluna}', escolha (descartar/preencher): ",
            ['descartar', 'preencher']
        )
        self.aplicarTratamentoNaN(coluna, escolha)
        self.df[coluna] = pd.Categorical(self.df[coluna]).codes

    def tratarCEP(self, coluna):
        digitos = int(self.solicitarEntradaValida(
            "Quantos dígitos do CEP deseja usar para representar a região? ",
            lambda x: x.isdigit() and int(x) > 0
        ))
    
        escolha_preenchimento = self.solicitarEntradaValida(
            f"Para NaN/Null na coluna '{coluna}', escolha entre descartar os registros com NaN ou preencher com um valor padrão (descartar/preencher): ",
            lambda x: x in ['descartar', 'preencher']
        )
    
        if escolha_preenchimento == 'preencher':
            while True:
                valor_preenchimento = input(f"Digite o valor numérico (com exatamente {digitos} dígitos) para preencher NaN/Null na coluna '{coluna}': ")
                if valor_preenchimento.isdigit() and len(valor_preenchimento) == digitos:
                    self.df[coluna].fillna(valor_preenchimento, inplace=True)
                    break
                print(f"Por favor, digite um número com exatamente {digitos} dígitos.")
        elif escolha_preenchimento == 'descartar':
            self.df.dropna(subset=[coluna], inplace=True)
    
        self.df[coluna] = self.df[coluna].astype(str).str[:digitos]


    def tratarQualitativo(self, coluna):
        escolha = self.solicitarEntradaValida(
            f"Para NaN/Null na coluna '{coluna}', escolha (descartar/preencher): ",
            lambda x: x in ['descartar', 'preencher']
        )
        self.aplicarTratamentoNaN(coluna, escolha)
        self.df[coluna] = pd.Categorical(self.df[coluna]).codes
       

    def tratarData(self, coluna):
        escolha_data = self.solicitarEntradaValida(
            f"Como deseja tratar a coluna de data '{coluna}'? (dias/meses/anos): ",
            lambda x: x in ['dias', 'meses', 'anos']
        )
        coluna_data = pd.to_datetime(self.df[coluna], errors='coerce')
        if escolha_data == 'dias':
            data_referencia = pd.Timestamp('1900-01-01')
            self.df[coluna] = (coluna_data - data_referencia).dt.days
        elif escolha_data == 'meses':
            self.df[coluna] = coluna_data.dt.year * 12 + coluna_data.dt.month - 190001
        elif escolha_data == 'anos':
            self.df[coluna] = coluna_data.dt.year

        escolha = self.solicitarEntradaValida(
            f"Para NaN/Null na coluna '{coluna}', escolha (media/mediana/moda/0/1/descartar): ",
            lambda x: x in ['media', 'mediana', 'moda', '0', '1', 'descartar']
        )
        self.aplicarTratamentoNaN(coluna, escolha)

    def aplicarTratamentoNaN(self, coluna, escolha):
        if escolha in ['media', 'mediana', 'moda', '0', '1']:
            # Tratamentos que dependem do tipo de dados da coluna
            if escolha == 'media':
                self.df[coluna].fillna(self.df[coluna].mean(), inplace=True)
            elif escolha == 'mediana':
                self.df[coluna].fillna(self.df[coluna].median(), inplace=True)
            elif escolha == 'moda':
                moda = self.df[coluna].mode()
                if len(moda) > 0:
                    self.df[coluna].fillna(moda[0], inplace=True)
            elif escolha == '0':
                self.df[coluna].fillna(0, inplace=True)
            elif escolha == '1':
                self.df[coluna].fillna(1, inplace=True)
        elif escolha == 'preencher':
            preenchimento = input(f"Escolha o valor para preencher NaN/Null na coluna '{coluna}' (qualitativo): ")
            self.df[coluna].fillna(preenchimento, inplace=True)
            self.df[coluna] = pd.Categorical(self.df[coluna]).codes
        elif escolha == 'descartar':
            self.df.dropna(subset=[coluna], inplace=True)

    def salvarRespostas(self):
        data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.respostas['data'] = data_atual
        with open(constantes.respostas_tratamento_base, 'wb') as file:
            pickle.dump(self.respostas, file)
        print(f"Respostas salvas em {constantes.respostas_tratamento_base} em {data_atual}.")

    def processar(self):
        self.processarColunas()
        if self.alvo is not None:
            self.previsores = self.df.drop(columns=['alvo'])
        else:
            self.previsores = self.df
        if self.alvo is not None:
            print(f'alvo:\n{self.alvo}')
            print(f'previsores:\n{self.previsores}')
        else:
            print("Alvo não definido")
        return self.previsores, self.alvo
