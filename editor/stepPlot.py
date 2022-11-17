from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

import os

# Imagens
import cv2
import imutils

strPathDir = '/home/ronie/prog/dnc/editor'
strSep = os.path.sep

# Leio daqui
strImgPE_original = strPathDir  + strSep +  "IMG" + strSep +  "ORIGINAL" + strSep + "pE-original.png"
strImgPD_original = strPathDir  + strSep +  "IMG" + strSep +  "ORIGINAL" + strSep + "pD-original.png"

# Salvo aqui
strImgPE = strPathDir  + strSep +  "IMG" + strSep + "pE-atual.png"
strImgPD = strPathDir  + strSep +  "IMG" + strSep + "pD-atual.png"


# --------------
#    ClassePe
# --------------

# Lê imagem, rotaciona e escreve
def imgReadRotWrite(strFileImage,numAngle,strFileOut):
    image = cv2.imread(strFileImage)
    rotated_image = imutils.rotate(image, angle=numAngle)
    booRet = cv2.imwrite(strFileOut, rotated_image)
    return booRet

class ClassePe:
    def __new__(cls, *args, **kwargs):
        # print("1. Create a new instance of Point.")
        return super().__new__(cls)

    def __init__(self,name, b, x, y):
        # print("2. Initialize the new instance of Point.")
        self.name = name #Nome do Pé
        self.b = b # Qual pé? 0 = Falso = Pé Esquerdo / 1 = True = Pé Direito / Por isso b de booleano
        self.x = x # Posição x do pé no plano cartesiano
        self.y = y # Posição y do pé no plano cartesiano

        # Parâmetros Pré-Definidos
        self.DJ = 2.0 # Distância Entre Pés Juntos = 2
        self.DP = 4.0 # Distância de Passo = 4 tanto em x quanto em y

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={self.name}, b={self.b}, x={self.x}, y={self.y})"

    def retPeMirror(self):
        '''Retorna a Classe ClasePe que é o espelhamento (mirror) do Objeto Pe atual - Espelho Regular'''
        strNovoNome = '/{}'.format(self.name) # O nome vai ser um / nome significa que o Pe foi espelhado
        if (self.b): # Se Verdadeiro = 1 = Pé Direito
            booNovoB = False
            floatNovoX = self.x - self.DJ
            floatNovoY = self.y
        else: # Se Falso = 0 = Pé Esquerdo
            booNovoB = True
            floatNovoX = self.x + self.DJ
            floatNovoY = self.y
        retPe = ClassePe(strNovoNome,booNovoB,floatNovoX,floatNovoY)
        return retPe

    def retPeCruzado(self):
        '''Retorna a Classe ClasePe que é o espelhamento (mirror) do Objeto Pe atual - Espelho Inverso'''
        strNovoNome = '\{}'.format(self.name) # O nome vai ser um / nome significa que o Pe foi espelhado
        if (self.b): # Se Verdadeiro = 1 = Pé Direito
            booNovoB = False
            floatNovoX = self.x + self.DJ
            floatNovoY = self.y
        else: # Se Falso = 0 = Pé Esquerdo
            booNovoB = True
            floatNovoX = self.x - self.DJ
            floatNovoY = self.y
        retPe = ClassePe(strNovoNome,booNovoB,floatNovoX,floatNovoY)
        return retPe

def doStep(pA,strCmd, pE0,pD0):
    ''' Dado um pE e pD iniciais e um pA = pAlvo, executa strCmd modificando pA'''
    # print('{}.{}'.format(pA.name,strCmd))
    # O referencial é a projeção do outro pé
    if (pA.b): #Se o Alvo é o Pé Direito
        pJ = pE0.retPeMirror() # Pega a Projeção Espelhada do Pé Esquerdo = É o referencial
        pI = pE0.retPeCruzado()
    else: #Se o Alvo é o Pé Esquerdo
        pJ = pD0.retPeMirror() # Pega a Projeção Espelhada do Pé Direito = É o referencial
        pI = pD0.retPeCruzado()

    if strCmd == 'ABR': # Abrir
        if (pA.b): # Se Verdadeiro -> Alvo é Pé Direito -> Direção X Positiva
            pA.x = pJ.x + pA.DP - pA.DJ
        else: # Se Falso -> Alvo é Pé Esquerdo -> Direção X Negativa
            pA.x = pJ.x - pA.DP + pA.DJ
        pA.y = pJ.y
    elif strCmd == 'JUN': # Juntar é ir para a posição da projeção do outro pré
        pA.x = pJ.x
        pA.y = pJ.y
    elif strCmd == 'LUG': # Lugar não muda o lugar
        pass
    elif strCmd == 'FRT': # Frente
        pA.x = pA.x
        pA.y = pJ.y + pA.DP
    elif strCmd == 'TRS': # Trás
        pA.x = pA.x
        pA.y = pJ.y - pA.DP
    elif strCmd == 'ABF': # Abrir indo à Frente
        if (pA.b): # Se Verdadeiro -> Alvo é Pé Direito -> Direção X Positiva
            pA.x = pJ.x + pA.DP - pA.DJ
        else: # Se Falso -> Alvo é Pé Esquerdo -> Direção X Negativa
            pA.x = pJ.x - pA.DP + pA.DJ
        pA.y = pJ.y + pA.DP
    elif strCmd == 'ABT': # Abrir indo à Atras
        if (pA.b): # Se Verdadeiro -> Alvo é Pé Direito -> Direção X Positiva
            pA.x = pJ.x + pA.DP - pA.DJ
        else: # Se Falso -> Alvo é Pé Esquerdo -> Direção X Negativa
            pA.x = pJ.x - pA.DP + pA.DJ
        pA.y = pJ.y - pA.DP
    elif strCmd == 'JCF': # Junta Cruzado pela Frente
        pA.x = pI.x
        pA.y = pI.y
    elif strCmd == 'JCT': # Juntar Cruzado por Tras - Mesma coisa - Muda a forma como as pernas se cruzam
        pA.x = pI.x
        pA.y = pI.y
    elif strCmd == 'FCF': # Frente Cruzando pela Frente = Gancho do Samba
        pA.x = pI.x
        pA.y = pJ.y + pA.DP
    elif strCmd == 'TCT': # Tras Cruzando por Tras = Gancho Invertido
        pA.x = pI.x
        pA.y = pJ.y - pA.DP

def plotaPes(pE,pD,strFilename):
    fig = plt.figure(figsize=[0.7*12.8,0.7*4.8])
    ax = fig.add_subplot(1, 2, 1, projection='3d')
    bx = fig.add_subplot(1, 2, 2)

    # -------------------
    # Propriedades de ax
    # -------------------
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_zlim(0, 10)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.view_init(elev=30., azim=-70, roll=0)

    # -------------------
    # Propriedades de bx
    # -------------------
    bx.set_xlim(-10, 10)
    bx.set_ylim(-10, 10)
    bx.set_xlabel('X')
    bx.set_ylabel('Y')
    bx.grid()

    def getImage(path, zoom=0.2):
        return OffsetImage(plt.imread(path), zoom=zoom)

    def pt3d(strCap,xx,yy,zz,strCor):
        x,y,z = xx,yy,zz
        ax.scatter(x, y, z, label='{} ({},{},{})'.format(strCap,x,y,z),color=strCor)

    # ---------------------------------------------------------
    # Linhas e Pontos de Referência para me situar no Espaço 3D
    # ---------------------------------------------------------

    # Pontos no Espaço 3D
    pt3d('O',0,0,0,'black')
    pt3d('X',10,0,0,'red')
    pt3d('Y',0,10,0,'green')
    pt3d('Z',0,0,10,'blue')

    # Eixo X
    x = np.linspace(0, 10, 100)
    y = x*0
    ax.plot(x, y, zs=0, zdir='z', label='X', color='red')

    # Eixo Y
    y = np.linspace(0, 10, 100)
    x = y*0
    ax.plot(x, y, zs=0, zdir='z', label='Y', color='green')

    # Eixo Z
    z = np.linspace(0, 10, 100)
    x = z*0
    y = z*0
    ax.plot(x, y, z, zdir='z', label='Z', color='blue')

    # ---------------------------------------------------------
    # Pé Esquerdo
    # ---------------------------------------------------------
    pE_image_path = strImgPE
    pE_x = pE.x # Usei a Classe ClassePe pE passada no argumento
    pE_y = pE.y # Idem
    pE_z = 0

    # ---------------------------------------------------------
    # Pé Direito
    # ---------------------------------------------------------
    pD_image_path = strImgPD
    pD_x = pD.x # Usei a Classe ClassePe pD passada no argumento
    pD_y = pD.y # Idem
    pD_z = 0

    ############################################################
    # Plotagem 3D dos Pontos dos Pés - Plot ax
    ############################################################
    pt3d('pE',pE_x,pE_y,pE_z,'magenta')
    pt3d('pD',pD_x,pD_y,pD_z,'orange')

    ############################################################
    # Plotagem 2D das Imagens dos Pés - Plot bx
    ############################################################

    # Insere Pé Esquerdo
    abPE = AnnotationBbox(getImage(pE_image_path), (pE_x, pE_y), frameon=False)
    bx.add_artist(abPE)

    # Insere Pé Direito
    abPD = AnnotationBbox(getImage(pD_image_path), (pD_x, pD_y), frameon=False)
    bx.add_artist(abPD)

    ############################################################
    # Salva Figura
    ############################################################
    plt.savefig(strFilename)
    plt.close()


def teste1():
    # Defino a posição inicial no Plano Cartesiano para pE e pD
    pE = ClassePe('pE',False,-1,+0)
    pD = ClassePe('pD',True,+1,+0)
    plotaPes(pE,pD,'a1-inicio.png')

    print(pE)
    doStep(pE,'ABR', pE,pD)
    print(pE)
    doStep(pE,'ABR', pE,pD)
    print(pE)

    plotaPes(pE,pD,'a2-ABR.png')

    doStep(pD,'ABR', pE,pD)
    plotaPes(pE,pD,'a3-ABR.png')

    doStep(pD,'JUN', pE,pD)
    plotaPes(pE,pD,'a4-JUN.png')

    doStep(pD,'FRT', pE,pD)
    doStep(pD,'FRT', pE,pD)
    doStep(pD,'FRT', pE,pD)
    plotaPes(pE,pD,'a5-FRT.png')

    doStep(pE,'FRT', pE,pD)
    plotaPes(pE,pD,'a6-FRT.png')


    doStep(pE,'JUN', pE,pD)
    plotaPes(pE,pD,'a7.png')

    doStep(pE,'TRS', pE,pD)
    plotaPes(pE,pD,'a8.png')

    doStep(pD,'TRS', pE,pD)
    plotaPes(pE,pD,'a9.png')

    doStep(pE,'JUN', pE,pD)
    plotaPes(pE,pD,'a10.png')


    doStep(pD,'ABF', pE,pD)
    plotaPes(pE,pD,'a11.png')

    doStep(pE,'ABF', pE,pD)
    plotaPes(pE,pD,'a12.png')

    doStep(pE,'ABT', pE,pD)
    plotaPes(pE,pD,'a13.png')

    doStep(pD,'ABT', pE,pD)
    plotaPes(pE,pD,'a14.png')

    doStep(pD,'ABF', pE,pD)
    plotaPes(pE,pD,'a15.png')

    doStep(pE,'JUN', pE,pD)
    plotaPes(pE,pD,'a16.png')

    doStep(pD,'JCF', pE,pD)
    doStep(pD,'JCF', pE,pD)
    doStep(pE,'JCT', pE,pD)
    plotaPes(pE,pD,'a17-pD-JCF.png')

    doStep(pE,'JUN', pE,pD)
    plotaPes(pE,pD,'a18-pE-JUN.png')


    doStep(pD,'FCF', pE,pD)
    plotaPes(pE,pD,'a19-Gancho.png')

    doStep(pD,'JUN', pE,pD)
    plotaPes(pE,pD,'a20.png')

    doStep(pD,'TCT', pE,pD)
    plotaPes(pE,pD,'a21-GanchoInvertido.png')

def teste2():
    # Defino a posição inicial no Plano Cartesiano para pE e pD
    pE = ClassePe('pE',False,-1,+0)
    pD = ClassePe('pD',True,+1,+0)
    plotaPes(pE,pD,'a1-inicio.png')


    doStep(pD,'JCF', pE,pD)
    doStep(pD,'JCF', pE,pD)
    doStep(pE,'JCT', pE,pD)
    plotaPes(pE,pD,'a2-pD-JCF.png')

    doStep(pE,'JUN', pE,pD)
    plotaPes(pE,pD,'a3-pE-JUN.png')


    doStep(pD,'FCF', pE,pD)
    plotaPes(pE,pD,'a4-Gancho.png')

    doStep(pD,'JUN', pE,pD)
    plotaPes(pE,pD,'a5.png')

    doStep(pD,'TCT', pE,pD)
    plotaPes(pE,pD,'a6-GanchoInvertido.png')

    doStep(pE,'JCF', pE,pD)
    plotaPes(pE,pD,'a7.png')

    doStep(pD,'JUN', pE,pD)
    plotaPes(pE,pD,'a8.png')

# Passos Fundamentais
# ABR - OK
# JUN - OK
# FRT - OK
# TRS - OK
# LUG - OK

# ACT - Abre Cruzando Atrás - Nao faz sentido - Mudar para FCT - Que é o mesmo que JCT - errado(FCT) -> JCT - Ok
# ACF - Mudar para FCF - Fecha Cruzando à Frente - Que é o mesmo que JCF - errado(FCF) - JCF - Ok
# JCF - foi feito
# JCT - foi feito

# E vou precisar de:

# ABF = Abre Indo a Frente - OK
# ABT = Abre Indo a Atras - OK

# FCF = Frente Cruzando à Frente
# TCT = Tras Cruzando à Trás


# Tudo bem, Nao pode ser FCF pq F é Frente e nao pode ser Fechar
# Entao FCF fica mesmo JCF = Junta Cruzando à Frente e JCT

################################################################################
# Classe Dançarino, Condutor, Conduzido
# Nomeei como Agente mesmo ou seja é aquele que age
################################################################################

class ClasseAgente:
    def __new__(cls, *args, **kwargs):
        # print("1. Create a new instance of Point.")
        return super().__new__(cls)

    def __init__(self,name, b, x, y, h, t):
        # print("2. Initialize the new instance of Point.")
        self.name = name # Condutor ou Conduzido
        self.b = b # Tipo de Agente? 0 = Falso = Conduzido / 1 = True = Condutor
        self.x = x # Posição x do Core em relação à pista de dança
        self.y = y # Posição y do Core em relação à pista de dança
        self.h = h # Altura do Core do Agente
        self.t = t # Angulo Theta de Referencia em relação a y positivo sentido anti-horario

        # Parâmetros Pré-Definidos
        self.DJ = 2.0 # Distância Entre Pés Juntos = 2
        self.DP = 4.0 # Distância de Passo = 4 tanto em x quanto em y

        # Pés
        # Importante aqui as coordenadas dos pés é no referencial que fica no core
        # Para Plotar na Pista de Dança preciso transformar as coordenadas
        self.pE = ClassePe('pE',False,-1,0)
        self.pD = ClassePe('pD',True,+1,0)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={self.name}, b={self.b}, x={self.x}, y={self.y}, h={self.h}, t={self.t})"

    def retCorePoint(self):
        ''' Retorna Posições X e Y do Core do Agente no Referencial Absoluto '''
        return self.x,self.y

    def retCorePoint3D(self):
        ''' Retorna Posições X e Y do Core do Agente no Referencial Absoluto '''
        return self.x,self.y, self.h

    def retPeDireitoPoint(self):
        ''' Retorna Posições X e Y do Pe Direito no Referencial Absoluto '''
        return self.x + self.pD.x,self.y + self.pD.y

    def retPeEsquerdoPoint(self):
        ''' Retorna Posições X e Y do Pe Esquerdo no Referencial Absoluto '''
        return self.x + self.pE.x,self.y + self.pE.y

    def plotaAgente(self,tamanhoPista):
        ''' Plota o Agente no Espaço 3D X,Y,Z '''
        fig = plt.figure(figsize=[0.7*12.8,2*0.7*5])
        ax = fig.add_subplot(2, 2, 1, projection='3d')
        bx = fig.add_subplot(2, 2, 2)
        cx = fig.add_subplot(2, 2, 3)
        dx = fig.add_subplot(2, 2, 4)

        ax.set_title('Pista 3D')
        bx.set_title('Pista 2D')
        cx.set_title('Nao Sei')
        dx.set_title('Agente')

        fig.tight_layout()
        plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)

        # -------------------
        # Propriedades de ax - Pista 3D
        # -------------------
        ax.set_xlim(0, tamanhoPista)
        ax.set_ylim(0, tamanhoPista)
        ax.set_zlim(0, tamanhoPista)
        ax.set_xlabel('X - Pista')
        ax.set_ylabel('Y - Pista')
        ax.set_zlabel('Z - Pista')
        ax.view_init(elev=30., azim=-70, roll=0)

        # -------------------
        # Propriedades de bx - Pista 2D
        # -------------------
        bx.set_xlim(0, tamanhoPista)
        bx.set_ylim(0, tamanhoPista)
        # bx.set_xlabel('X - Pista')
        bx.set_ylabel('Y - Pista')
        bx.grid()


        # -------------------
        # Propriedades de cx - Não Sei
        # -------------------
        cx.set_xlim(0, tamanhoPista)
        cx.set_ylim(0, tamanhoPista)
        cx.grid()

        # -------------------
        # Propriedades de dx - Agente
        # -------------------
        dx.set_xlim(-10, 10)
        dx.set_ylim(-10, 10)
        dx.set_xlabel('X - Agente')
        dx.set_ylabel('Y - Agente')
        dx.grid()

        # Vou colocar duas linhas infinitas na origem
        dx.axhline(y=0, color="black", linestyle=":")
        dx.axvline(x=0, color="black", linestyle=":")


        def getImage(path, zoom=0.2):
            return OffsetImage(plt.imread(path), zoom=zoom)

        def pt3d(strCap,xx,yy,zz,strCor):
            x,y,z = xx,yy,zz
            ax.scatter(x, y, z, label='{} ({},{},{})'.format(strCap,x,y,z),color=strCor)

        # ---------------------------------------------------------
        # Linhas e Pontos de Referência para me situar no Espaço 3D
        # ---------------------------------------------------------

        # Pontos no Espaço 3D
        pt3d('O',0,0,0,'black')
        pt3d('X',tamanhoPista,0,0,'red')
        pt3d('Y',0,tamanhoPista,0,'green')
        pt3d('Z',0,0,tamanhoPista,'blue')

        # Eixo X
        x = np.linspace(0, tamanhoPista, 100)
        y = x*0
        ax.plot(x, y, zs=0, zdir='z', label='X', color='red')

        # Eixo Y
        y = np.linspace(0, tamanhoPista, 100)
        x = y*0
        ax.plot(x, y, zs=0, zdir='z', label='Y', color='green')

        # Eixo Z
        z = np.linspace(0, tamanhoPista, 100)
        x = z*0
        y = z*0
        ax.plot(x, y, z, zdir='z', label='Z', color='blue')



        # ---------------------------------------------------------
        # Core
        # ---------------------------------------------------------
        Core_x, Core_y, Core_z = self.retCorePoint3D()

        # ---------------------------------------------------------
        # Pé Esquerdo
        # ---------------------------------------------------------
        pE_image_path = strImgPE
        pE_x, pE_y = self.retPeEsquerdoPoint()
        pE_z = 0

        # ---------------------------------------------------------
        # Pé Direito
        # ---------------------------------------------------------
        pD_image_path = strImgPD
        pD_x, pD_y = self.retPeDireitoPoint()
        pD_z = 0

        ############################################################
        # Plotagem 3D dos Pontos dos Pés - Plot ax - Pista de Dança
        ############################################################
        pt3d('pE',pE_x,pE_y,pE_z,'magenta')
        pt3d('pD',pD_x,pD_y,pD_z,'orange')
        pt3d('Core',Core_x,Core_y,Core_z,'red')

        ############################################################
        # Plotagem 2D das Imagens dos Pés - Plot bx - Pista de Dança
        ############################################################

        # Insere Pé Esquerdo
        abPE = AnnotationBbox(getImage(pE_image_path), (pE_x, pE_y), frameon=False)
        bx.add_artist(abPE)

        # Insere Pé Direito
        abPD = AnnotationBbox(getImage(pD_image_path), (pD_x, pD_y), frameon=False)
        bx.add_artist(abPD)

        ############################################################
        # Plotagem 2D das Imagens dos Pés - Plot dx - Ref: Core do Agente
        ############################################################

        # Insere Pé Esquerdo
        abPE2 = AnnotationBbox(getImage(pE_image_path), (self.pE.x, self.pE.y), frameon=False)
        dx.add_artist(abPE2)

        # Insere Pé Direito
        abPD2 = AnnotationBbox(getImage(pD_image_path), (self.pD.x, self.pD.y), frameon=False)
        dx.add_artist(abPD2)

        ############################################################
        # Salva Figuras
        ############################################################
        # plt.show()

        # https://stackoverflow.com/questions/4325733/save-a-subplot-in-matplotlib
        eax = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        ebx = bx.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        ecx = cx.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        edx = dx.get_window_extent().transformed(fig.dpi_scale_trans.inverted())

        fig.savefig('IMG/ax-atual.png', bbox_inches=eax.expanded(1.1, 1.2))
        fig.savefig('IMG/bx-atual.png', bbox_inches=ebx.expanded(1.1, 1.2))
        fig.savefig('IMG/cx-atual.png', bbox_inches=ecx.expanded(1.1, 1.2))
        fig.savefig('IMG/dx-atual.png', bbox_inches=edx.expanded(1.1, 1.2))

        # Fecha!
        plt.close()

    def moveCore(self):
        ''' Quando pés se movimentam o core deve ir junto '''
        # Só que o core é referente ao sistema absoluto
        Core_x,Core_y = self.retCorePoint()
        pE_x,pE_y = self.retPeEsquerdoPoint()
        pD_x,pD_y = self.retPeDireitoPoint()

        self.x = (pE_x + pD_x) / 2
        self.y = (pE_y + pD_y) / 2

        # --------------------------------------------------------------------
        # Mexeu no Core então preciso recalcular as Posicoes Relativas dos Pes
        # --------------------------------------------------------------------

        if pE_x < pD_x: # Pé Esquerdo à esquerda do Pé Direito
            self.pE.x = - abs(self.x - pE_x)
            self.pD.x = + abs(self.x - pD_x)
        else: # Pé Esquerdo à direita do Pé Direito (posição cruzada)
            self.pD.x = - abs(self.x - pD_x)
            self.pE.x = + abs(self.x - pE_x)

        if pD_y > pE_y: # Pé Direito na Frente
            self.pD.y = + abs(self.y - pD_y)
            self.pE.y = - abs(self.y - pE_y)
        else: # Pé Esquerdo na Frente
            self.pE.y = + abs(self.y - pE_y)
            self.pD.y = - abs(self.y - pD_y)

    # Esse está dentro da Classe Agente
    def agenteDoStep(self,strPeAlvo,strCmd,strMod):
        ''' Executa strCmd modificando o pe alvo'''
        pE0 = self.pE
        pD0 = self.pD
        if strPeAlvo == 'pE':
            pA = self.pE
        else:
            pA = self.pD

        if strMod != '':
            print('{} - {}.{}({})'.format(self.name,pA.name,strCmd,strMod))
        else:
            print('{} - {}.{}'.format(self.name,pA.name,strCmd))


        # Vou rodar aqui
        if strMod != '':
            if strPeAlvo == 'pE':
                if strMod == 'q': #90
                    imgReadRotWrite(strImgPE_original, 90, strImgPE)
                elif strMod == 'v': #180
                    imgReadRotWrite(strImgPE_original, 180, strImgPE)
                elif strMod == 't': #45
                    imgReadRotWrite(strImgPE_original, 45, strImgPE)
            else:
                if strMod == 'q': #90
                    imgReadRotWrite(strImgPD_original, 90, strImgPD)
                elif strMod == 'v': #180
                    imgReadRotWrite(strImgPD_original, 180, strImgPD)
                elif strMod == 't': #45
                    imgReadRotWrite(strImgPD_original, 45, strImgPD)

        doStep(pA, strCmd, pE0, pD0)
        self.moveCore()  
