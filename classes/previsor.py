import pandas as pd
import pickle
import constantes 

class Previsor:
    def __init__(self, modelo_path=None):
        self.modelo_path = modelo_path
        self.modelo = None

    def carregarModelo(self, novo_modelo_path=None):
        
        if novo_modelo_path is not None:
            self.modelo_path = novo_modelo_path
        if self.modelo_path is not None:
            with open(self.modelo_path, 'rb') as file:
                self.modelo = pickle.load(file)
            print("Modelo Carregado")
        else:
            raise ValueError("Nenhum caminho de modelo foi fornecido.")

    def prever(self, X):
       
        if self.modelo is None:
            raise ValueError("Nenhum modelo foi carregado.")
            print("Predict concluído")
        return self.modelo.predict(X)

    def preverProba(self, X):
        """Calcula os scores das predições e retorna os resultados."""
        if self.modelo is None:
            raise ValueError("Nenhum modelo foi carregado.")
        print("Criação do Score conc'luída")
        return self.modelo.predict_proba(X)[:, 1]

    def adicionarPredicoesAoDataFrame(self, df, X):
        """Adiciona colunas de predições e scores ao DataFrame fornecido."""
        df[constantes.predicao] = self.prever(X)
        df[constantes.score] = self.preverProba(X)
        print("Criação do Score concluída")
        
        return df
    
    def salvarDataFrame():
        with open(path, 'wb') as file:
            pickle.dump(df, file)
        print("DF salvo com score e predict")
        
        
