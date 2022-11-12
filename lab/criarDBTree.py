#Cria a estrutura de banco de dados e insere os dados HARD CODED

import sqlite3
import datetime
import numpy as np
import pandas as pd

strDbTree = "dbDanceTree.db"

listTypeNo = {'root','cls','obj','stp'}
listTypeAD = {'cls-obj','cls-stp'}

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

def DataSearch(tbTable,dtData):
    conn=sqlite3.connect(strDbFilename)
    cur=conn.cursor()
    codigoSQL = "SELECT * FROM " + tbTable + " WHERE dtData = " + sqlite3_DateTimeForSQL(dtData)
    cur.execute(codigoSQL)
    rows=cur.fetchall()
    conn.close()
    return rows



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
########## tbSTP
####################

def dbCria_tbSTP():
    conn=sqlite3.connect(strDbTree)
    cur=conn.cursor()
    textSQL = '''
    CREATE TABLE IF NOT EXISTS tbSTP
    (
    cod INTEGER PRIMARY KEY,
    strNAME TEXT UNIQUE,
    strDESC TEXT,
    codNO INTEGER
    )
    '''
    cur.execute(textSQL)
    conn.commit()

def tbSTP_insert(p_cod,p_strNAME,p_strDESC,p_codNO):
    conn=sqlite3.connect(strDbTree)
    cur=conn.cursor()
    textSQL = 'INSERT INTO tbSTP VALUES (?,?,?,?)'
    cur.execute(textSQL,(p_cod,p_strNAME,p_strDESC,p_codNO))
    conn.commit()

def tbSTP_append(p_strNAME,p_strDESC,p_codNO):
    nCod = nC('tbSTP')
    tbSTP_insert(nCod,p_strNAME,p_strDESC,p_codNO)
    return nCod

####################
########## tbCLS
####################

def dbCria_tbCLS():
    conn=sqlite3.connect(strDbTree)
    cur=conn.cursor()
    textSQL = '''
    CREATE TABLE IF NOT EXISTS tbCLS
    (
    cod INTEGER PRIMARY KEY,
    strNAME TEXT UNIQUE,
    codNO INTEGER
    )
    '''
    cur.execute(textSQL)
    conn.commit()

def tbCLS_insert(p_cod,p_strNAME,p_codNO):
    conn=sqlite3.connect(strDbTree)
    cur=conn.cursor()
    textSQL = 'INSERT INTO tbCLS VALUES (?,?,?)'
    cur.execute(textSQL,(p_cod,p_strNAME,p_codNO))
    conn.commit()

def tbCLS_append(p_strNAME,p_codNO):
    nCod = nC('tbCLS')
    tbCLS_insert(nCod,p_strNAME,p_codNO)
    return nCod

####################
########## tbOBJ
####################

def dbCria_tbOBJ():
    conn=sqlite3.connect(strDbTree)
    cur=conn.cursor()
    textSQL = '''
    CREATE TABLE IF NOT EXISTS tbOBJ
    (
    cod INTEGER PRIMARY KEY,
    strNAME TEXT UNIQUE,
    codNO INTEGER
    )
    '''
    cur.execute(textSQL)
    conn.commit()

def tbOBJ_insert(p_cod,p_strNAME,p_codNO):
    conn=sqlite3.connect(strDbTree)
    cur=conn.cursor()
    textSQL = 'INSERT INTO tbOBJ VALUES (?,?,?)'
    cur.execute(textSQL,(p_cod,p_strNAME,p_codNO))
    conn.commit()

def tbOBJ_append(p_strNAME,p_codNO):
    nCod = nC('tbOBJ')
    tbOBJ_insert(nCod,p_strNAME,p_codNO)
    return nCod

###############################################################################
#       Criar Banco de Dados Vazio
###############################################################################
def criarDBTree_Vazio():
    dbCria_tbNO()
    dbCria_tbAD()
    dbCria_tbCLS()
    dbCria_tbOBJ()
    dbCria_tbSTP()

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
    strNAME = 'ABR'
    txtDESC = 'Abrir normal: Afastar um pé do outro na direção horizontal (para o lado).'
    tbCod = tbSTP_append(strNAME,txtDESC,-1)
    noCod = tbNO_append('stp',tbCod,-1,-1,-1,-1,-1,'',True)
    updateTbCodNO('tbSTP',tbCod,noCod)
    tbAD_append('cls-stp',paiCod,noCod)
    # Cruzar à Frente
    strNAME = 'ACF'
    txtDESC = 'Cruzar a frente: Abertura, mas o pé que se movimenta cruza à frente do pé que fica parado. Você se desloca em sentido oposto ao de ABR.'
    tbCod = tbSTP_append(strNAME,txtDESC,-1)
    noCod = tbNO_append('stp',tbCod,-1,-1,-1,-1,-1,'',True)
    updateTbCodNO('tbSTP',tbCod,noCod)
    tbAD_append('cls-stp',paiCod,noCod)
    # Cruzar à Frente
    strNAME = 'ACT'
    txtDESC = 'Cruzar a traz: Abertura, mas o pé que se movimenta cruza por traz do pé que fica parado. Você se desloca em sentido oposto ao de ABR.'
    tbCod = tbSTP_append(strNAME,txtDESC,-1)
    noCod = tbNO_append('stp',tbCod,-1,-1,-1,-1,-1,'',True)
    updateTbCodNO('tbSTP',tbCod,noCod)
    tbAD_append('cls-stp',paiCod,noCod)
    # 2 - Movimentos de aproximação de um pé do outro
    # Juntar normal
    strNAME = 'JUN'
    txtDESC = 'Juntar normal: Deslocar o pé para a posição normal ao lado do outro. O pé se desloca para o mesmo local da projeção do outro pé.'
    tbCod = tbSTP_append(strNAME,txtDESC,-1)
    noCod = tbNO_append('stp',tbCod,-1,-1,-1,-1,-1,'',True)
    updateTbCodNO('tbSTP',tbCod,noCod)
    tbAD_append('cls-stp',paiCod,noCod)
    # Juntar Cruzado à Frente
    strNAME = 'JCF'
    txtDESC = 'Juntar cruzado à frente: Ao juntar o pé passa pela frente do imóvel permanecendo ao seu lado de forma cruzada.'
    tbCod = tbSTP_append(strNAME,txtDESC,-1)
    noCod = tbNO_append('stp',tbCod,-1,-1,-1,-1,-1,'',True)
    updateTbCodNO('tbSTP',tbCod,noCod)
    tbAD_append('cls-stp',paiCod,noCod)
    # Juntar Cruzado à Traz
    strNAME = 'JCT'
    txtDESC = 'Juntar cruzado à traz: Ao juntar o pé passa por de traz do imóvel permanecendo ao seu lado de forma cruzada.'
    tbCod = tbSTP_append(strNAME,txtDESC,-1)
    noCod = tbNO_append('stp',tbCod,-1,-1,-1,-1,-1,'',True)
    updateTbCodNO('tbSTP',tbCod,noCod)
    tbAD_append('cls-stp',paiCod,noCod)
    # 3 - Movimentos de distanciamento longo um pé do outro para frente/traz - direção vertical
    # Juntar Cruzado à Traz
    strNAME = 'FRT'
    txtDESC = 'Frente: Passo à frente'
    tbCod = tbSTP_append(strNAME,txtDESC,-1)
    noCod = tbNO_append('stp',tbCod,-1,-1,-1,-1,-1,'',True)
    updateTbCodNO('tbSTP',tbCod,noCod)
    tbAD_append('cls-stp',paiCod,noCod)
    # Juntar Cruzado à Traz
    strNAME = 'TRS'
    txtDESC = 'Tras: Passo a tras'
    tbCod = tbSTP_append(strNAME,txtDESC,-1)
    noCod = tbNO_append('stp',tbCod,-1,-1,-1,-1,-1,'',True)
    updateTbCodNO('tbSTP',tbCod,noCod)
    tbAD_append('cls-stp',paiCod,noCod)

    # 4 - Movimentaçõa no lugar
    strNAME = 'LUG'
    txtDESC = 'Lugar: O pé levanta e desce permanecendo no mesmo lugar.'
    tbCod = tbSTP_append(strNAME,txtDESC,-1)
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

def criar():
    # Apague o banco de dados e rode essa função para fazer tudo
    criarDBTree_Vazio()
    popularDBTree()
    mostrar()
