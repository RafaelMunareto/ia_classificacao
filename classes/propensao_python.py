from tratamento_variaveis import TratamentoVariaveis
from looping_algoritimos import LoopingAlgoritmos
from maquina_comites import MaquinaDeComites
from previsor import Previsor
import constantes 


#processar a base
data_processor = TratamentoVariaveis(constantes.variaveis_csv_file)
data_processor.capturaDados()  
data_processor.salvarVariaveis(constantes.variaveis_dir)

# ## rodar modelos
# loop = LoopingAlgoritmos(constantes.variaveis_dir, constantes.algoritmos_dir)
# loop.carregarDados()
# loop.treinarModelos()
# resultados = loop.obterResultados()

#escolher os 2 melhores e juntar
# comites = MaquinaDeComites(constantes.algoritimos_dir)
# best_model = comites.criarComite()

# #Aplicador modelo e fazer a previsão
# preditor = Preditor(constantes.modelo_aplicado)
# preditor.carregarModelo()
# preditor.salvarDataFrameComPrevisao(constantes.df_com_predicoes, constantes.results_df)


# #analise
# # Exemplo de uso
# analise = Analise(constantes.df_com_previsao)
# analise.carregarDados()
# analise.compararAcertos()
# analise.analisarFaixasDeScore()


    