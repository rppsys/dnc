from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

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
    pE_image_path = '/home/ronie/prog/dnc/lab/pE.PNG'
    pE_x = pE.x # Usei a Classe ClassePe pE passada no argumento
    pE_y = pE.y # Idem
    pE_z = 0

    # ---------------------------------------------------------
    # Pé Direito
    # ---------------------------------------------------------
    pD_image_path = '/home/ronie/prog/dnc/lab/pD.PNG'
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

def doStep(pA,strCmd, pE0,pD0):
    ''' Dado um pE e pD iniciais e um pA = pAlvo, executa strCmd modificando pA'''
    print('{}.{}'.format(pA.name,strCmd))
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





def main1():
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


def main():
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



main()


