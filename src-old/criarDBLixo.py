#Cria a estrutura de banco de dados e insere os dados HARD CODED

# Esse eu mantive por causa das funcoes genericas para criar tabelas,
#mas nao vou usar.

import sqlite3
import datetime
import numpy as np
import pandas as pd

strDbS = "dbDance"
strDbN = "Zouk"
strDbE = ".db"
strDbTree = strDbS + strDbN + strDbE

listTypeNo = ['root']
listTypeAD = []

###############################################################################
#   Funções Auxiliares
###############################################################################
def nC(tbTable):
    conn=sqlite3.connect(strDbTree)
    cur=conn.cursor()
    cur.execute("SELECT MAX(cod) FROM " + tbTable)
    row = cur.fetchone()
    conn.close()
    if row[0] == None:
        return 1
    else:
        return row[0] + 1

def updateTbCodNO(tbTable,codTable,codNO):
    conn=sqlite3.connect(strDbTree)
    cur=conn.cursor()
    cur.execute("UPDATE " + tbTable + " SET codNO=? WHERE cod=?",(codNO,codTable))
    conn.commit()
    conn.close()

def retPandasDfFromSQL(textSQL):
    conn=sqlite3.connect(strDbTree)
    cur=conn.cursor()
    cur.execute(textSQL)
    colnames = [description[0] for description in cur.description]
    rows=cur.fetchall()
    retDF = pd.DataFrame.from_records(rows,columns=colnames)
    retDF.index = retDF['cod']
    retDF.drop('cod',axis=1,inplace=True)
    return retDF

def findTbFieldByValue(tbTable,findField,findValue,retField):
    conn=sqlite3.connect(strDbTree)
    cur=conn.cursor()
    codigoSQL = "SELECT " + findField + ", " + retField + " FROM " + tbTable + " WHERE " + findField + " = " + findValue
    #print(codigoSQL)
    cur.execute(codigoSQL)
    row=cur.fetchone()
    conn.close()
    return row[1]

###############################################################################
#                                  ÁRVORE
###############################################################################

####################
########## tbNO
####################

def dbCria_tbNO():
    conn=sqlite3.connect(strDbTree)
    cur=conn.cursor()
    textSQL = '''
    CREATE TABLE IF NOT EXISTS tbNO
    (
    cod INTEGER PRIMARY KEY,
    typeNO TEXT,
    codPointer INTEGER,
    drwGX INTEGER,
    drwGY INTEGER,
    drwLev INTEGER,
    drwHei INTEGER,
    drwPos INTEGER,
    drwRel TEXT,
    booActive BOOLEAN
    )
    '''
    cur.execute(textSQL)
    conn.commit()

def tbNO_insert(p_cod,p_typeNO,p_codPointer,p_drwGX,p_drwGY,p_drwLev,p_drwHei,p_drwPos,p_drwRel,p_booActive):
    conn=sqlite3.connect(strDbTree)
    cur=conn.cursor()
    textSQL = 'INSERT INTO tbNO VALUES (?,?,?,?,?,?,?,?,?,?)'
    cur.execute(textSQL,(p_cod,p_typeNO,p_codPointer,p_drwGX,p_drwGY,p_drwLev,p_drwHei,p_drwPos,p_drwRel,p_booActive))
    conn.commit()

def tbNO_append(p_typeNO,p_codPointer,p_drwGX,p_drwGY,p_drwLev,p_drwHei,p_drwPos,p_drwRel,p_booActive):
    nCod = nC('tbNO')
    tbNO_insert(nCod,p_typeNO,p_codPointer,p_drwGX,p_drwGY,p_drwLev,p_drwHei,p_drwPos,p_drwRel,p_booActive)
    return nCod

####################
########## tbAD
####################

def dbCria_tbAD():
    conn=sqlite3.connect(strDbTree)
    cur=conn.cursor()
    textSQL = '''
    CREATE TABLE IF NOT EXISTS tbAD
    (
    cod INTEGER PRIMARY KEY,
    typeAD TEXT,
    codFrom INTEGER,
    codTo INTEGER
    )
    '''
    cur.execute(textSQL)
    conn.commit()

def tbAD_insert(p_cod,p_typeAD,codFrom,codTo):
    conn=sqlite3.connect(strDbTree)
    cur=conn.cursor()
    textSQL = 'INSERT INTO tbAD VALUES (?,?,?,?)'
    cur.execute(textSQL,(p_cod,p_typeAD,codFrom,codTo))
    conn.commit()

def tbAD_append(p_typeAD,codFrom,codTo):
    nCod = nC('tbAD')
    tbAD_insert(nCod,p_typeAD,codFrom,codTo)
    return nCod

###############################################################################
#                                  Tipos de Nos
###############################################################################

####################
########## tbTable
####################

listTbTable = []
def tbTable_create(tbTable):
    listTbTable.append(tbTable)
    conn=sqlite3.connect(strDbTree)
    cur=conn.cursor()
    textSQL = 'CREATE TABLE IF NOT EXISTS ' + tbTable + '''
    (
    cod INTEGER PRIMARY KEY,
    strNAME TEXT UNIQUE,
    strTYPE TEXT,
    codNO INTEGER
    )
    '''
    cur.execute(textSQL)
    conn.commit()

def tbTable_insert(tbTable,p_cod,p_strNAME,p_strTYPE,p_codNO):
    conn=sqlite3.connect(strDbTree)
    cur=conn.cursor()
    textSQL = 'INSERT INTO ' + tbTable + ' VALUES (?,?,?,?)'
    cur.execute(textSQL,(p_cod,p_strNAME,p_strTYPE,p_codNO))
    conn.commit()

def tbTable_append(tbTable,p_cod,p_strNAME,p_strTYPE,p_codNO):
    nCod = nC(tbTable)
    tbTable_insert(tbTable,nCod,p_strNAME,p_strTYPE,p_codNO)
    return nCod

###############################################################################
#       Criar Banco de Dados Vazio
###############################################################################
def criarDBTree_Vazio():
    dbCria_tbNO()
    dbCria_tbAD()
    tbTable_create('tbHEAD')
    tbTable_create('tbTAG')


def noAd():
    pass


###############################################################################
#   Popular dbDanceTree com os passos básicos universais, classes e objetos
###############################################################################

def popularDBTree():
    # Cria o tbNO root
    rootCod = tbNO_append('root',0,-1,-1,-1,-1,-1,'',True)

    ####################
     #Agora as Classes
    ####################
    # Classe PÉ
    tbCod = tbCLS_append('PE',-1)
    noCod = tbNO_append('cls',tbCod,-1,-1,-1,-1,-1,'',True)
    updateTbCodNO('tbCLS',tbCod,noCod)
    tbAD_append('root-cls',rootCod,noCod)
    # Classe Pegada
    tbCod = tbCLS_append('PEGADA',-1)
    noCod = tbNO_append('cls',tbCod,-1,-1,-1,-1,-1,'',True)
    updateTbCodNO('tbCLS',tbCod,noCod)
    tbAD_append('root-cls',rootCod,noCod)
    # Classe Pospar
    tbCod = tbCLS_append('POSPAR',-1)
    noCod = tbNO_append('cls',tbCod,-1,-1,-1,-1,-1,'',True)
    updateTbCodNO('tbCLS',tbCod,noCod)
    tbAD_append('root-cls',rootCod,noCod)
    ####################
    ##### CLASSE PÉ
    ####################
    paiCod = findTbFieldByValue('tbCLS','strNAME','"PE"','codNO')
    ##########
    # Objetos da Classe Pé
    ##########
    # Pé Direito
    tbCod = tbOBJ_append('pD',-1)
    noCod = tbNO_append('obj',tbCod,-1,-1,-1,-1,-1,'',True)
    updateTbCodNO('tbOBJ',tbCod,noCod)
    tbAD_append('cls-obj',paiCod,noCod)
    # Pé Esquerdo
    tbCod = tbOBJ_append('pE',-1)
    noCod = tbNO_append('obj',tbCod,-1,-1,-1,-1,-1,'',True)
    updateTbCodNO('tbOBJ',tbCod,noCod)
    tbAD_append('cls-obj',paiCod,noCod)
    ##########
    # Métodos da Classe Pé ou STEPS
    ##########
    # 1 - Movimentos de distanciamento longo um pé do outro para o lado - direção horizontal
    # Abrir normal
    strTAG = 'ABR'
    txtDESC = 'Abrir normal: Afastar um pé do outro na direção horizontal (para o lado).'
    tbCod = tbSTP_append(strTAG,txtDESC,-1)
    noCod = tbNO_append('stp',tbCod,-1,-1,-1,-1,-1,'',True)
    updateTbCodNO('tbSTP',tbCod,noCod)
    tbAD_append('cls-stp',paiCod,noCod)
    # Cruzar à Frente
    strTAG = 'ACF'
    txtDESC = 'Cruzar a frente: Abertura, mas o pé que se movimenta cruza à frente do pé que fica parado. Você se desloca em sentido oposto ao de ABR.'
    tbCod = tbSTP_append(strTAG,txtDESC,-1)
    noCod = tbNO_append('stp',tbCod,-1,-1,-1,-1,-1,'',True)
    updateTbCodNO('tbSTP',tbCod,noCod)
    tbAD_append('cls-stp',paiCod,noCod)
    # Cruzar à Frente
    strTAG = 'ACT'
    txtDESC = 'Cruzar a traz: Abertura, mas o pé que se movimenta cruza por traz do pé que fica parado. Você se desloca em sentido oposto ao de ABR.'
    tbCod = tbSTP_append(strTAG,txtDESC,-1)
    noCod = tbNO_append('stp',tbCod,-1,-1,-1,-1,-1,'',True)
    updateTbCodNO('tbSTP',tbCod,noCod)
    tbAD_append('cls-stp',paiCod,noCod)
    # 2 - Movimentos de aproximação de um pé do outro
    # Juntar normal
    strTAG = 'JUN'
    txtDESC = 'Juntar normal: Deslocar o pé para a posição normal ao lado do outro. O pé se desloca para o mesmo local da projeção do outro pé.'
    tbCod = tbSTP_append(strTAG,txtDESC,-1)
    noCod = tbNO_append('stp',tbCod,-1,-1,-1,-1,-1,'',True)
    updateTbCodNO('tbSTP',tbCod,noCod)
    tbAD_append('cls-stp',paiCod,noCod)
    # Juntar Cruzado à Frente
    strTAG = 'JCF'
    txtDESC = 'Juntar cruzado à frente: Ao juntar o pé passa pela frente do imóvel permanecendo ao seu lado de forma cruzada.'
    tbCod = tbSTP_append(strTAG,txtDESC,-1)
    noCod = tbNO_append('stp',tbCod,-1,-1,-1,-1,-1,'',True)
    updateTbCodNO('tbSTP',tbCod,noCod)
    tbAD_append('cls-stp',paiCod,noCod)
    # Juntar Cruzado à Traz
    strTAG = 'JCT'
    txtDESC = 'Juntar cruzado à traz: Ao juntar o pé passa por de traz do imóvel permanecendo ao seu lado de forma cruzada.'
    tbCod = tbSTP_append(strTAG,txtDESC,-1)
    noCod = tbNO_append('stp',tbCod,-1,-1,-1,-1,-1,'',True)
    updateTbCodNO('tbSTP',tbCod,noCod)
    tbAD_append('cls-stp',paiCod,noCod)
    # 3 - Movimentos de distanciamento longo um pé do outro para frente/traz - direção vertical
    # Juntar Cruzado à Traz
    strTAG = 'FRT'
    txtDESC = 'Frente: Passo à frente'
    tbCod = tbSTP_append(strTAG,txtDESC,-1)
    noCod = tbNO_append('stp',tbCod,-1,-1,-1,-1,-1,'',True)
    updateTbCodNO('tbSTP',tbCod,noCod)
    tbAD_append('cls-stp',paiCod,noCod)
    # Juntar Cruzado à Traz
    strTAG = 'TRS'
    txtDESC = 'Tras: Passo a tras'
    tbCod = tbSTP_append(strTAG,txtDESC,-1)
    noCod = tbNO_append('stp',tbCod,-1,-1,-1,-1,-1,'',True)
    updateTbCodNO('tbSTP',tbCod,noCod)
    tbAD_append('cls-stp',paiCod,noCod)

    # 3 - Movimentos no Lugar
    # Lugar
    strTAG = 'LUG'
    txtDESC = 'Lugar: O pé levanta e pisa no mesmo lugar onde está'
    tbCod = tbSTP_append(strTAG,txtDESC,-1)
    noCod = tbNO_append('stp',tbCod,-1,-1,-1,-1,-1,'',True)
    updateTbCodNO('tbSTP',tbCod,noCod)
    tbAD_append('cls-stp',paiCod,noCod)



def mostrar():
    df_tbNO = retPandasDfFromSQL('Select * From tbNO')
    df_tbAD = retPandasDfFromSQL('Select * From tbAD')
    df_tbCLS = retPandasDfFromSQL('Select * From tbCLS')
    df_tbOBJ = retPandasDfFromSQL('Select * From tbOBJ')
    df_tbSTP = retPandasDfFromSQL('Select * From tbSTP')
    print('tbNO:')
    print(df_tbNO)
    print('tbAD:')
    print(df_tbAD)
    print('tbCLS:')
    print(df_tbCLS)
    print('tbOBJ:')
    print(df_tbOBJ)
    print('tbSTP:')
    print(df_tbSTP)

def teste():
    # Apague o banco de dados e rode essa função para fazer tudo
    criarDBTree_Vazio()
    popularDBTree()
    mostrar()



# Só funciona com STPs diferentes
def tagMake(strN,strT):
    row = []
    conn=sqlite3.connect(strDbTree)
    cur=conn.cursor()
    codigoSQL = "SELECT * FROM tbSTP WHERE strNAME = {0} AND strTYPE = {1}"
    cur.execute(codigoSQL.format("'" + strN + "'","'" + strT + "'"))
    row=cur.fetchone()
    conn.close()
    if row == None:
        # Não existe, então cria e retorna seu codNO
        tbCod = tbSTP_append(strN,strT,'',-1)
        noCod = tbNO_append('tag',tbCod,-1,-1,-1,-1,-1,'',True)
        updateTbCodNO('tbSTP',tbCod,noCod)
        return noCod
    else:
        # Existe, então retorna seu codNO
        return row[4]



# O Código abaixo só funcionaria caso todas as tags fossem diferentes
def tagJoin(strN1,strT1,strN2,strT2):
    # Se não existir strN1 de tipo strT1 cria, caso contrario pega codNO
    codNo1 = tagMake(strN1,strT1)
    # Se não existir strN2 de tipo strT2 cria, caso contrari pega codNO
    codNo2 = tagMake(strN2,strT2)
    # Faz o AD entre eles com typeAD = strT1-strT2
    tbAD_append(strT1 + '-' + strT2,codNo1,codNo2)
    # Retorna codNo1 para poder fazer AD entre ele e seu pai
    return codNo1
