
# Diretórios de arquivos
variaveis_csv_file = '../base/clientes_ficticios_1milhao.txt'
variaveis_dir = '../variaveis'
algoritmos_dir = '../algoritimos'
results_df = '../resultados/df_com_previsao.pickle'

#variaveis 
alvo = 'alvo.pickle'
previsores = 'previsores.pickle'
previsores_scalonados = 'previsores_scalonados.pickle'
previsores_scalonados_df = 'previsores_scalonados_df.pickle'
previsores_pca = 'previsores_pca.pickle'
df = 'df.pickle'
df_com_previsao = './algoritmos/df_com_previsao.pickle'
resultado_completo_df = 'resultado_completos_metrica_algoritimos.pickle'

#colunas previsores 
predicao = 'predicao'
score = 'score'
alvo = 'alvo'
faixa_score = 'Faixa_Score'

#modelos de treinos
rf =  "RandomForest"
lr = "LogisticRegression"
knn = "KNeighbors"
nb = "GaussianNB"
sgd = "SGDClassifier"
gb = "GradientBoosting"
ab =  "AdaBoost"
dt = "DecisionTree"
et = "ExtraTrees"
ct = "CatBoost"
bm = "BestModel"

#previsor_utilizado e modelo utilizado
previsor_utilizado = previsores
modelo_aplicado = algoritmos_dir + bm + ".pickle" 


