import pygame
import random
from recursos.funcoes import inicializarBancoDeDados, limpar_tela, escreverDados, maior_pontuador

#Preparação inicial
limpar_tela()
inicializarBancoDeDados()
nome_maior, maior_pontos, dataJogada = maior_pontuador()
pygame.init()

#Pedir nome do jogador
while True:
    nome = input("Nickname: ")
    if len(nome) > 0: 
        break
    else:
        print("Nome Inválido!")
        

        # Configuração da tela
tamanho = (1000,700)
pygame.display.set_caption("Void Knight")
icone  = pygame.image.load("Bases/Icone.png")
pygame.display.set_icon(icone)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho ) 
branco = (255, 255, 255)
preto = (0, 0, 0)

#Carregar imagens
fundo = pygame.image.load("Bases/FUNDO.png")
fundoDead = pygame.image.load("Bases/Tela de morte.png")
fundoStart = pygame.image.load("Bases/TELA DE INICIO.png")
void = pygame.image.load("Bases/VOID.png")
void = pygame.transform.scale(void, (220,250))
Inimigo_do_void = pygame.image.load("Bases/inimigo.png")
Inimigo_do_void = pygame.transform.scale(Inimigo_do_void, (280,250))

#Carregar sons e fonte
som_inimgo = pygame.mixer.Sound("Bases/Som inimigo.wav")
musica_de_morte = pygame.mixer.Sound("Bases/Musica de morte.mp3")
#pygame.mixer.music.load("Bases/combate.wav")
fonteMenu = pygame.font.SysFont("comicsans",18)


#Variáveis iniciais do jogo
def jogar():
    fundoMov1 = 0
    fundoMov2 = 1129
    posicaoXPersona = 0
    posicaoYPersona = 60
    movimentoXPersona  = 0
    movimentoYPersona  = 0
    velocidadeMovPersona = 5
    posicaoXMissel = 800
    posicaoYMissel = 100
    velocidadeMissel = 2
    pontos = 0
    pygame.mixer.Sound.play(som_inimgo)
    pygame.mixer.music.play(-1)
    dificuldade = 20

  
    while True:   # jogo rodando sem parar.
        #movimentação
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: #Fechar janela
                quit()
                movimentoXPersona = 0
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_UP or evento.type == pygame.KEYDOWN and evento.key == pygame.K_w:
                movimentoYPersona = -velocidadeMovPersona
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_DOWN or evento.type == pygame.KEYDOWN and evento.key == pygame.K_s:
                movimentoYPersona = velocidadeMovPersona
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_UP or evento.type == pygame.KEYUP and evento.key == pygame.K_w:
                movimentoYPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_DOWN or evento.type == pygame.KEYUP and evento.key == pygame.K_s:
                movimentoYPersona = 0
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT or  evento.type == pygame.KEYDOWN and evento.key == pygame.K_d:
                movimentoXPersona = velocidadeMovPersona
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT or  evento.type == pygame.KEYDOWN and evento.key == pygame.K_a:
                movimentoXPersona = -velocidadeMovPersona
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT or evento.type == pygame.KEYUP and evento.key == pygame.K_d:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT or evento.type == pygame.KEYUP and evento.key == pygame.K_a:
                movimentoXPersona = 0
                
        #Atualizar posição do personagem
        posicaoXPersona = posicaoXPersona + movimentoXPersona          
        posicaoYPersona = posicaoYPersona + movimentoYPersona    

        #Limitar personagem dentro da tela        
        if posicaoXPersona < 0 :
            posicaoXPersona = 0
        elif posicaoXPersona > 880:
            posicaoXPersona = 880
        if posicaoYPersona < 0 :
            posicaoYPersona = 0
        elif posicaoYPersona > 650:
            posicaoYPersona = 650
            
            #Movimento do míssil (sempre para a esquerda)
        posicaoXMissel = posicaoXMissel - velocidadeMissel

        #Quando o míssil sai da tela
        if posicaoXMissel < -125:
            pygame.mixer.Sound.play(som_inimgo)
            posicaoXMissel = 800
            pontos = pontos + 1
            velocidadeMissel = velocidadeMissel + 1
            posicaoYMissel = random.randint(0,200)
                            
        #Desenhar fundo                            
        tela.fill(branco)
        tela.blit(fundo, (0,0) )
        
        
        #Desenhar personagem, inimigo e pontos
        tela.blit(void, (posicaoXPersona,posicaoYPersona))
        tela.blit( Inimigo_do_void, (posicaoXMissel, posicaoYMissel) )
        texto = fonteMenu.render("Pontos: "+str(pontos), True, branco)
        tela.blit(texto, (700,15))
            
            #Colisão
        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona+116))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona+51))
        pixelsMisselX = list(range(posicaoXMissel, posicaoXMissel + 125))
        pixelsMisselY = list(range(posicaoYMissel, posicaoYMissel + 25))
        if  len( list( set(pixelsMisselY).intersection(set(pixelsPersonaY))) ) > dificuldade:
            if len( list( set(pixelsMisselX).intersection(set(pixelsPersonaX))   ) )  > dificuldade:
                escreverDados(nome, pontos)
                dead()
                return
                
            else:
                print("Ainda Vivo, mas por pouco!")
        else:
            print("Ainda Vivo")
        
        #Atualizar tela e FPS
        pygame.display.update()
        relogio.tick(60)

#Função dead()
def dead():

    #Parar música e tocar explosão
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(musica_de_morte)
    som_inimgo.stop()

    #Botões da tela de morte
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN: #usar botao do mouse

                #Clique nos botões
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonStart = 150
                    alturaButtonStart  = 40

                    musica_de_morte.stop()
                    som_inimgo.stop()
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("Bases/combate.wav")
                    pygame.mixer.music.play(-1)

                    jogar()
                    return

                    jogar()
                if quitButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
            
        #Desenhar tela de morte
        tela.fill(branco)
        tela.blit(fundoDead, (0,0))
        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))


        pygame.display.update()
        relogio.tick(60)


#Função start()
def start():
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                #Botões da tela inicial
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("Bases/combate.wav")
                    pygame.mixer.music.play(-1)
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
            
        tela.fill(branco)
        tela.blit(fundoStart, (0,0))
        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))
        #Mostrar maior pontuador
        texto = fonteMenu.render(f"The Best - {nome_maior} - {maior_pontos} - { dataJogada} ", True, branco)
        tela.blit(texto, (480,15))
        

        pygame.display.update()
        relogio.tick(60)
          #Começar o jogo 
pygame.mixer.music.load("Bases/Som inicio do jogo.mp3")
pygame.mixer.music.play(-1)
start()