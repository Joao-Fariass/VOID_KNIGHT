import pygame
import random
from recursos.Trabalho import inicializarBancoDeDados, limpar_tela, escreverDados, maior_pontuador
from recursos.Trabalho import verificar_vida_extra
from recursos.Trabalho import dano_inimigo

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
void_esquerda = pygame.transform.flip(void, True, False)
Inimigo_do_void = pygame.image.load("Bases/inimigo.png")
Inimigo_do_void = pygame.transform.scale(Inimigo_do_void, (280,250))
ataque = pygame.image.load("Bases/Ataque.png")
ataque = pygame.transform.scale(ataque, (180, 120))
ataque_esquerda =  pygame.transform.flip(ataque, True, False)
#Carregar sons e fonte
som_inimgo = pygame.mixer.Sound("Bases/Som inimigo.wav")
musica_de_morte = pygame.mixer.Sound("Bases/Musica de morte.mp3")
som_ataque = pygame.mixer.Sound("Bases/som ataque.mp3")
#pygame.mixer.music.load("Bases/combate.wav")
fonteMenu = pygame.font.SysFont("comicsans",18)


#Variáveis iniciais do jogo
def jogar():
    posicaoXPersona = 390
    posicaoYPersona = 385
    movimentoXPersona  = 0
    velocidadeMovPersona = 6
    posicaoXinimigo = 860
    posicaoYinimigo = 385
    velocidadeinimigo = 2

    lado_inimigo = random.choice(["direita", "esquerda"])
    if lado_inimigo == "direita":
        posicaoXinimigo = 860
    else:
        posicaoXinimigo = -120

    pontos = 0
    vidas = 3 
    vidas_inimigo = 3
    UltimoBonus= 0
    ultimo_ataque = 0
    cooldown_ataque = 500
    mostrar_ataque = False
    tempo_ataque = 0
    duracao_ataque = 150
    direcao = "direita"
    direcao_ataque = direcao
    posicaoXataque = 0
    posicaoYataque = 0
    som_inimgo.play(-1)
    pygame.mixer.music.load("Bases/combate.wav")
    pygame.mixer.music.play(-1)
    dificuldade = 20
    pausado = False
    fontePause = pygame.font.SysFont("comicsans", 60)

  
    while True:   # jogo rodando sem parar.
        #movimentação
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: #Fechar janela
                    quit()

            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                pausado = not pausado

                if pausado:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("Bases/Som inicio do jogo.mp3")
                    pygame.mixer.music.play(-1)

                    som_inimgo.stop()

                else:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("Bases/combate.wav")
                    pygame.mixer.music.play(-1)

                    som_inimgo.play(-1)

            elif not pausado and (
                evento.type == pygame.MOUSEBUTTONDOWN
                or 
                (evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN)
            ):
                tempo_atual = pygame.time.get_ticks()
                if tempo_atual - ultimo_ataque >= cooldown_ataque:
                    ultimo_ataque = tempo_atual

                    mostrar_ataque = True
                    tempo_ataque = tempo_atual
                    posicaoXataque = posicaoXPersona
                    direcao_ataque = direcao
                    pygame.mixer.Sound.play(som_ataque)

                    if direcao_ataque == "direita":
                         acertou = posicaoXinimigo > posicaoXPersona and posicaoXinimigo < posicaoXPersona + 300
                    else:
                        acertou = posicaoXinimigo < posicaoXPersona and posicaoXinimigo - posicaoXPersona - 300

                    if acertou:
                        vidas_inimigo = dano_inimigo(vidas_inimigo)

                        
                        if vidas_inimigo <= 0:
                            pontos += 1
                            velocidadeinimigo = 2 + (pontos // 5)
                            cooldown_ataque = max(300, 500 - (pontos * 10))
                            velocidadeMovPersona = min(8, 5 + (pontos // 10))

                            vidas, UltimoBonus = verificar_vida_extra(pontos,vidas,UltimoBonus)

                            vidas_inimigo = 3

                            lado_inimigo = random.choice(["direita", "esquerda"])

                            if lado_inimigo == "direita":
                                 posicaoXinimigo = 860
                            else:
                                posicaoXinimigo = -120

                            posicaoYinimigo = 385


            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT or  evento.type == pygame.KEYDOWN and evento.key == pygame.K_d:
                movimentoXPersona = velocidadeMovPersona
                direcao = "direita"
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT or  evento.type == pygame.KEYDOWN and evento.key == pygame.K_a:
                movimentoXPersona = -velocidadeMovPersona
                direcao = "esquerda"
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT or evento.type == pygame.KEYUP and evento.key == pygame.K_d:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT or evento.type == pygame.KEYUP and evento.key == pygame.K_a:
                movimentoXPersona = 0
                

        if pausado:
            tela.blit(fundo, (0,0))

            textoPause = fontePause.render("PAUSE", True, branco)
            tela.blit(textoPause, (400, 300))

            textoAjuda = fonteMenu.render("Press Space to Continue", True, branco)
            tela.blit(textoAjuda, (400, 380))

            pygame.display.update()
            relogio.tick(60)
            continue

        #Atualizar posição do personagem
        posicaoXPersona = posicaoXPersona + movimentoXPersona          
       
        #Limitar personagem dentro da tela        
        if posicaoXPersona < -70:
            posicaoXPersona = -70
        elif posicaoXPersona > 860:
            posicaoXPersona = 860
     
    
            #Movimento do inimigo (sempre para a esquerda)
        if lado_inimigo == "direita":
            posicaoXinimigo = posicaoXinimigo - velocidadeinimigo
        else:
            posicaoXinimigo = posicaoXinimigo + velocidadeinimigo

        #Quando o inimigo sai da tela
        if posicaoXinimigo < -125:
            pygame.mixer.Sound.play(som_inimgo)
            posicaoXinimigo = 800
            pontos = pontos + 1
            vidas, UltimoBonus = verificar_vida_extra (
                pontos,
                vidas,
                UltimoBonus
            )

            velocidadeinimigo = velocidadeinimigo + 1
            posicaoYinimigo = random.randint(0,200)
                            
        #Desenhar fundo                            
        tela.fill(branco)
        tela.blit(fundo, (0,0) )
        
        
        #Desenhar personagem, inimigo e pontos
        if direcao == "direita":
            tela.blit(void, (posicaoXPersona,posicaoYPersona))
        else: 
            tela.blit(void_esquerda, (posicaoXPersona, posicaoYPersona))
        if mostrar_ataque:
            if direcao_ataque == "direita":
                tela.blit(ataque,(posicaoXataque +120, 430))
            else: 
                tela.blit(ataque_esquerda, (posicaoXataque - 80, 430))

            if pygame.time.get_ticks() - tempo_ataque > duracao_ataque:
                mostrar_ataque = False
                
        tela.blit( Inimigo_do_void, (posicaoXinimigo, posicaoYinimigo) )
        texto = fonteMenu.render("Pontos: "+str(pontos), True, branco)
        textoVidas= fonteMenu.render("Vidas:" + str(vidas), True, branco)
        textoVidaInimigo = fonteMenu.render("vidas_inimigo: " + str(vidas_inimigo),True,branco)

        tela.blit(textoVidaInimigo, (700,65))
        tela.blit(textoVidas,(700,40))
        tela.blit(texto, (700,15))

        textoPauseGame = fonteMenu.render("Press Space to Pause Game",True,branco)
        tela.blit(textoPauseGame, (730, 650))
            #Colisão
        pixelsPersonaX = list(range(posicaoXPersona+100, posicaoXPersona+140))
        pixelsPersonaY = list(range(posicaoYPersona+40, posicaoYPersona+220))
        pixels_inimigoX = list(range(posicaoXinimigo+130, posicaoXinimigo + 170))
        pixels_inimigoY = list(range(posicaoYinimigo+50, posicaoYinimigo + 200))
        if  len( list( set(pixels_inimigoY).intersection(set(pixelsPersonaY))) ) > dificuldade:
            if len( list( set(pixels_inimigoX).intersection(set(pixelsPersonaX))   ) )  > dificuldade:
                vidas = vidas - 1
                vidas_inimigo = 3 


                lado_inimigo = random.choice(["direita", "esquerda"])

                if lado_inimigo == "direita":
                    posicaoXinimigo = 860
                else:
                    posicaoXinimigo = -120

                posicaoYinimigo = 385


                if vidas <= 0:
                    escreverDados(nome,pontos)
                
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

    #Parar música e tocar musica de morte
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(musica_de_morte)
    som_inimgo.stop()

    #Botões da tela de morte
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    startButton = pygame.Rect(10, 10, larguraButtonStart, alturaButtonStart)
    quitButton = pygame.Rect(10, 60, larguraButtonQuit, alturaButtonQuit)
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

def boas_vindas():
    larguraButtonStart = 220
    alturaButtonStart = 45

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    pygame.mixer.music.stop()
                    jogar()
                    return

        tela.blit(fundoStart, (0,0))

        titulo = fonteMenu.render("Bem-vindo ao Void Knight, " + nome + "!", True, branco)
        explicacao1 = fonteMenu.render("Use A e D ou as setas para se mover.", True, branco)
        explicacao2 = fonteMenu.render("Clique com o mouse ou com o ENTER para atacar os inimigos.", True, branco)
        explicacao3 = fonteMenu.render("Sobreviva, ganhe pontos e bata o recorde!", True, branco)

        recorde = fonteMenu.render(
            f"Maior pontuador: {nome_maior} - {maior_pontos} pontos - {dataJogada}",
            True,
            branco
        )

        tela.blit(titulo, (300,270 ))
        tela.blit(explicacao1, (260, 330))
        tela.blit(explicacao2, (260, 360))
        tela.blit(explicacao3, (260, 390))
        tela.blit(recorde, (220, 450))

        startButton = pygame.draw.rect(
            tela,
            branco,
            (390, 600, larguraButtonStart, alturaButtonStart),
            border_radius=15
        )

        textoBotao = fonteMenu.render("Iniciar partida", True, preto)
        tela.blit(textoBotao, (430, 612))

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
boas_vindas()