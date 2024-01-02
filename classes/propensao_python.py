from tratamento_variaveis import TratamentoVariaveis
from looping_algoritimos import LoopingAlgoritmos
from maquina_comites import MaquinaDeComites
from previsor import Previsor
import constantes 

def processarBase():
    data_processor = TratamentoVariaveis(constantes.variaveis_csv_file)
    data_processor.capturaDados()  
    data_processor.salvarVariaveis(constantes.variaveis_dir)
    data_processor.salvarVariaveis(constantes.variaveis_dir)
    
    
def rodarModelos():
    loop = LoopingAlgoritmos(constantes.variaveis_dir, constantes.algoritimos_dir)
    loop.carregarDados()
    loop.treinarModelos()
    resultados = loop.obterResultados()

def maquinaComites():
    comites = MaquinaDeComites(constantes.algoritimos_dir)
    best_model = comites.criarComite()


def previsao():
    preditor = Preditor(constantes.modelo_aplicado)
    preditor.carregarModelo()
    preditor.salvarDataFrameComPrevisao(constantes.df_com_predicoes, constantes.results_df)

def analise():     
    analise = Analise(constantes.df_com_previsao)
    analise.carregarDados()
    analise.compararAcertos()
    analise.analisarFaixasDeScore()

def menu_principal():
    while True:
        print("\nEscolha uma opção:")
        print("P - Processar a base")
        print("M - Rodar modelos")
        print("C - Máquina de comitês")
        print("PR - Propensão")
        print("A - Análise")
        print("T - Tudo")
        print("S - Sair")
    
        escolha = input("Digite sua escolha (P/M/C/PR/A/T/S): ").upper()
    
        if escolha == "P":
            processarBase()
            pass
        elif escolha == "M":
            rodarModelos()
            pass
        elif escolha == "C":
            maquinaComites()
            pass
        elif escolha == "PR":
            previsao()
            pass
        elif escolha == "A":
            analise()
            pass
        elif escolha == "T":
            processarBase()
            rodarModelos()
            maquinaComites()
            previsao()
            analise()
            pass
        elif escolha == "S":
            print("Saindo do programa.")
            break
        else:
            print("Escolha inválida. Tente novamente.")

menu_principal()