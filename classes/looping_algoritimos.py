import pickle
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier, ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from catboost import CatBoostClassifier
from datetime import datetime
import constantes 

class LoopingAlgoritmos:
    def __init__(self, variaveis_dir, algoritmos_dir):
        self.variaveis_dir = variaveis_dir
        self.algoritmos_dir = algoritmos_dir
        self.alvo = None
        self.previsores = None
        self.modelos = {}
        self.resultados = {}

        

    def carregarDados(self):
        
        with open(f'{self.variaveis_dir}/{constantes.alvo}', 'rb') as file:
            self.alvo = pickle.load(file)
        with open(f'{self.variaveis_dir}/{constantes.previsor_utilizado}', 'rb') as file:
            self.previsores = pickle.load(file)
        
    def treinarModelos(self):
        print(f'Previsor utilizado {constantes.previsor_utilizado}')
        inicio_treinamento = datetime.now()
        X_train, X_test, y_train, y_test = train_test_split(
            self.previsores, self.alvo, test_size=0.3, random_state=42
        )
        print("Terminou a divisão treino e teste")

        algoritmos = {
            # constantes.rf: RandomForestClassifier(),
            # constantes.lg: LogisticRegression(max_iter=1000),
            # constantes.knn: KNeighborsClassifier(),
            constantes.nb: GaussianNB(),
            # constantes.sgd: SGDClassifier(),
            # constantes.gb: GradientBoostingClassifier(),
            # constantes.ab: AdaBoostClassifier(),
            # constantes.dt: DecisionTreeClassifier(),
            constantes.et: ExtraTreesClassifier(),
            constantes.ct: CatBoostClassifier(verbose=0)
        }

        resultados = {}

        for nome, modelo in algoritmos.items():
            cv_scores = cross_val_score(modelo, X_train, y_train, cv=10)
            cv_accuracy = np.mean(cv_scores)
            cv_std = np.std(cv_scores)
            modelo.fit(X_train, y_train)
            y_pred = modelo.predict(X_test)
            acc = accuracy_score(y_test, y_pred)
            print(f'Fazendo o algoritimo {nome}...')
            self.modelos[nome] = modelo
            resultados[nome] = {
                "accuracy": acc,
                "cv_accuracy": cv_accuracy,
                "cv_std": cv_std
            }
            

            with open(f'{self.algoritmos_dir}/{nome}_modelo.pickle', 'wb') as file:
                pickle.dump(modelo, file)
                
     
        fim_treinamento = datetime.now()
        
        resultados_completos = {
            "resultados": resultados,
            "inicio": inicio_treinamento.strftime('%Y-%m-%d %H:%M:%S'),
            "fim": fim_treinamento.strftime('%Y-%m-%d %H:%M:%S')
        }
        print(f'Fazendo o algoritimo {resultados_completos}')
        print("Finalizdos todos os algoritimos")
        with open(f'{self.algoritmos_dir}/{constantes.resultado_completo_df}', 'wb') as file:
            pickle.dump(resultados_completos, file)

        self.resultados = resultados_completos


    def obterResultados(self):
        return self.resultados