import numpy as np
import pandas as pd
from interativo_tratamento_variaveis import InterativoTratamentoVariaveis
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import IncrementalPCA
import pickle
import constantes 

class TratamentoVariaveis:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.alvo = None
        self.previsores = None
        self.previsores_scalonados = None
        self.previsores_scalonados_df = None
        self.pca_model = None
        self.variance_explained = None

    def capturaDados(self): 
        self.df = pd.read_csv(self.file_path, sep=';')
        # self.df = self.df.sample(frac=0.1, random_state=42)
        print("Dados caputurados")
        self.tratamentoVariaveis()

    def tratamentoVariaveis(self): 
        tratamento = InterativoTratamentoVariaveis(self.df)
        self.previsores, self.alvo = tratamento.processar()
        self.pca()
        self.escalonarPrevisores()

    def escalonarPrevisores(self):
        scaler = StandardScaler()
        self.previsores_scalonados = scaler.fit_transform(self.previsores)
        self.previsores_scalonados_df = scaler.inverse_transform(self.previsores_scalonados)
        print("Variáveis escalonadas")

    def pca(self, variance_threshold=0.90, batch_size=None):
        n_components = 0
        variance_explained = 0

        while variance_explained < variance_threshold and n_components < self.previsores.shape[1]:
            n_components += 1
            ipca = IncrementalPCA(n_components=n_components, batch_size=batch_size)
            transformed_data = ipca.fit_transform(self.previsores)
            variance_explained = np.sum(ipca.explained_variance_ratio_)

        self.pca_model = ipca
        self.variance_explained = variance_explained
        self.previsores = transformed_data
        print("Redução de dimensionalidade concluída")
        print(f'Fazendo o algoritimo {n_components} de {self.previsores.shape}')
        print(f'Variância de {variance_explained}')


    def salvarVariaveis(self, dir_path):
        pickle_files = {
            constantes.alvo: self.alvo,
            constantes.previsores: self.previsores,
            constantes.previsores_scalonados: self.previsores_scalonados,
            constantes.previsores_scalonados_df: self.previsores_scalonados_df,
            constantes.previsores_pca: self.pca_model,
            constantes.df: self.df
        }
       
        print(f'Previsores {self.previsores}')
        print(f'alvo scalonados {self.alvo}')
        totalizador_alvo = pd.DataFrame(self.alvo)
        totalizador_previsores= pd.DataFrame(self.previsores)
        print(f'isna previsores:  {totalizador_previsores.isna().sum()}')
        print(f'isna alvo {totalizador_alvo.isna().sum()}')
        for filename, data in pickle_files.items():
            with open(f'{dir_path}/{filename}', 'wb') as file:
                pickle.dump(data, file)
        print("Variáveis salvas.")
