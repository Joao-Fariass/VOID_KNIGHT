import os, time
import json
import random
from datetime import datetime





def verificar_vida_extra(pontos, vidas, ultimo_bonus):
    if pontos % 10 == 0 and pontos > 0 and pontos != ultimo_bonus:
        vidas += 1
        ultimo_bonus = pontos

    return vidas, ultimo_bonus

def gerar_inimigo_lado_aleatorio(largura_tela, altura_tela):
    lado = random.choice(["esquerda", "direita", "cima", "baixo"])

    if lado == "esquerda":
        x = -50
        y = random.randint(0, altura_tela)

    elif lado == "direita":
        x = largura_tela + 50
        y = random.randint(0, altura_tela)

    elif lado == "cima":
        x = random.randint(0, largura_tela)
        y = -50

    else:  # baixo
        x = random.randint(0, largura_tela)
        y = altura_tela + 50

    return x, y






def limpar_tela():
    os.system("cls")
    
def aguarde(segundos):
    time.sleep(segundos)
    
def inicializarBancoDeDados():
    # r - read, w - write, a - append
    try:
        banco = open("base.atitus","r")
    except:
        print("Banco de Dados Inexistente. Criando...")
        banco = open("base.atitus","w")
    
def escreverDados(nome, pontos):
    # INI - inserindo no arquivo
    banco = open("base.atitus","r")
    dados = banco.read()
    banco.close()
    if dados != "":
        dadosDict = json.loads(dados)
    else:
        dadosDict = {}
        
    data_br = datetime.now().strftime("%d/%m/%Y")
    dadosDict[nome] = (pontos, data_br)
    
    banco = open("base.atitus","w")
    banco.write(json.dumps(dadosDict))
    banco.close()
    
    # END - inserindo no arquivo
    
def maior_pontuador():
    banco = open("base.atitus","r")
    dados = banco.read()
    banco.close()
    if dados != "":
        dadosDict = json.loads(dados)
    else:
        dadosDict = {}

    nome_maior = None
    dataJogada =  None
    maior_pontos = -1

    for nome, info in dadosDict.items():

        pontos = info[0]
        
        if pontos > maior_pontos:
            maior_pontos = pontos
            nome_maior = nome
            dataJogada = info[1]            

    return nome_maior, maior_pontos, dataJogada