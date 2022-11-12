#Cria a estrutura de banco de dados e insere os dados HARD CODED

import sqlite3
import datetime
import numpy as np
import pandas as pd
import csv
import os

strCurDir = ''
strDbS = "dbDance"
strDbN = "ZOUK"
strDbE = ".db"
strDbFolder = 'DB/'
strCsvFolder = 'CSV/'
strStpFolder = 'STP/'
strDbSubFolder = strDbN + '/'
strDbTree = strDbFolder + strDbSubFolder + strDbS + strDbN + strDbE


strCurDir = os.getcwd() + '/'
listTypeNo = ['root']
listTypeAD = []


################################################################################
    # Aqui eu coloco as funções públicas - Aquelas que vou chamar como usuário
################################################################################

def gerarDB(p_strDbN = "Zouk"):
    global strDbS
    global strDbN
    global strDbE
    global strDbTree
    global strDbFolder
    global strDbSubFolder
    # Atribui novo nome ao DB
    strDbN = p_strDbN
    # Atribui nova SubPasta
    strDbSubFolder = strDbN + '/'
    #Cria endereço do banco de dados final
    strDbTree = strDbFolder + strDbSubFolder + strDbS + strDbN + strDbE
    # Gera o banco de dados
    criarDBTree_Vazio()
    popularDBTree(strDbN)
    mostrar()

# Após gerado, se quiser conectar ao banco para fazer coisas
def conectarDB(p_strDbN = "Zouk"):
    global strDbS
    global strDbN
    global strDbE
    global strDbTree
    global strDbFolder
    global strDbSubFolder
    strDbN = p_strDbN
    strDbSubFolder = strDbN + '/'
    strDbTree = strDbFolder + strDbSubFolder + strDbS + strDbN + strDbE
    mostrar()

def mostrar():
    global strDbN
    global strDbTree
    print('#####-#####-#####-#####-#####')
    print('Ritmo: ' + strDbN)
    print('Arquivo: ' + strDbTree)
    print('#####-#####-#####-#####-#####')
    df_tbNO = retPandasDfFromSQL('Select * From tbNO')
    df_tbAD = retPandasDfFromSQL('Select * From tbAD')
    df_tbSTP = retPandasDfFromSQL('Select * From tbSTP')
    df_vwDePara = retPandasDfFromSQL(getStrSql_DePara())

    print('')
    print('#----------=----------#')
    print('tbNO:')
    display(df_tbNO)

    print('')
    print('#----------=----------#')
    print('tbAD:')
    display(df_tbAD)

    print('')
    print('#----------=----------#')
    print('tbSTP:')
    display(df_tbSTP)

    print('')
    print('#----------=----------#')
    print('view DePara:')
    display(df_vwDePara)

    print('')
    print('#####-#####-#####-#####-#####')
    print('#####-#####-#####-#####-#####')
    return df_vwDePara

def verificar():
    df = retPandasDfFromSQL('''
    SELECT
    tbSTP.cod as cod,
    tbSTP.strNAME as strNAME,
    tbSTP.strTYPE as strTYPE,
    tbSTP.strVALUE as strVALUE,
    tbSTP.codNO as codNO
    FROM
    tbSTP
    WHERE
    tbSTP.strTYPE = 'leaf'
    ''')
    for index,row in df.iterrows():
        recNoUpToRoot_Verifica(int(row['codNO']),row['strNAME'],int(row['codNO']))
    return df

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
########## tbSTP
####################

def tbSTP_create():
    conn=sqlite3.connect(strDbTree)
    cur=conn.cursor()
    textSQL = '''
    CREATE TABLE IF NOT EXISTS tbSTP
    (
    cod INTEGER PRIMARY KEY,
    strNAME TEXT,
    strTYPE TEXT,
    strVALUE TEXT,
    codNO INTEGER
    )
    '''
    cur.execute(textSQL)
    conn.commit()

def tbSTP_insert(p_cod,p_strNAME,p_strTYPE,p_strVALUE,p_codNO):
    conn=sqlite3.connect(strDbTree)
    cur=conn.cursor()
    textSQL = 'INSERT INTO tbSTP VALUES (?,?,?,?,?)'
    cur.execute(textSQL,(p_cod,p_strNAME,p_strTYPE,p_strVALUE,p_codNO))
    conn.commit()

def tbSTP_append(p_strNAME,p_strTYPE,p_strVALUE,p_codNO):
    nCod = nC('tbSTP')
    tbSTP_insert(nCod,p_strNAME,p_strTYPE,p_strVALUE,p_codNO)
    return nCod


def tbSTP_updateValueByCodNO(p_codNO,p_strVALUE):
    conn=sqlite3.connect(strDbTree)
    cur=conn.cursor()
    cur.execute("UPDATE tbSTP SET strVALUE=? WHERE codNO=?",(p_strVALUE,p_codNO))
    conn.commit()

###############################################################################
#       Criar Banco de Dados Vazio
###############################################################################
def criarDBTree_Vazio():
    dbCria_tbNO()
    dbCria_tbAD()
    tbSTP_create()

def newSTP(p_strNAME,p_strTYPE,p_strVALUE):
    tbCod = tbSTP_append(p_strNAME,p_strTYPE,p_strVALUE,-1)
    noCod = tbNO_append('stp',tbCod,-1,-1,-1,-1,-1,'',True)
    updateTbCodNO('tbSTP',tbCod,noCod)
    return noCod

# Procura se o parentNo possui o seguinte filho, se tiver, atualiza, se nao cria
def tbSTP_updateOrNewChildFromNo(p_parentNo,p_strNAME,p_strTYPE,p_strVALUE):
    connP=sqlite3.connect(strDbTree)
    sqlP = '''
    Select
    tbAD.cod as cod,
    tbAD.typeAD as typeAD,
    tbAD.codFrom as codFrom,
    tbAD.codTo as codTo,
    tbSTP.cod as codSTP,
    tbSTP.strNAME as strNAME,
    tbSTP.strTYPE as strTYPE,
    tbSTP.strVALUE as strVALUE,
    tbSTP.codNO as codNO
    From tbAD, tbSTP
    Where tbAD.cod > 0
    And tbAD.typeAD like '1.org'
    And tbAD.codTo = tbSTP.codNO
    And tbAD.codFrom = {0}
    And tbSTP.strNAME = '{1}'
    And tbSTP.strTYPE = '{2}'
    Order By tbSTP.codNo
    '''
    #print(sqlP.format(str(p_parentNo),p_strNAME,p_strTYPE))
    curP=connP.cursor()
    curP.execute(sqlP.format(str(p_parentNo),p_strNAME,p_strTYPE))
    colnamesP = [description[0] for description in curP.description]
    rowsP=curP.fetchall()
    dfP = pd.DataFrame.from_records(rowsP,columns=colnamesP)
    dfP.index = dfP['cod']
    dfP.drop('cod',axis=1,inplace=True)
    if len(rowsP) == 0:
        # Não tem fiho nessas condições, então criar
        auxCodNo = newSTP(p_strNAME,p_strTYPE,p_strVALUE)
        tbAD_append('1.prop',p_parentNo,auxCodNo)
    else: #Tenho pelo menos 1 filho nessas condições, então atualiza
        tbSTP_updateValueByCodNO(int(dfP['codNO'].values[0]),p_strVALUE)

###############################################################################
#   Popular dbDanceTemp
###############################################################################
def popularDBTree(csvFilenameWithoutExt):
    global strCsvFolder
    rootCod = tbNO_append('root',0,-1,-1,-1,-1,-1,'',True)
    tbSTP_insert(0,'STP','root','',1)

    with open(strCsvFolder + csvFilenameWithoutExt + '.csv') as csvfile:
        listPai = []
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        c = 0
        for row in spamreader:
            c = c + 1
            #print('Iteração ' + str(c))
            #print(row)
            numPai = int(row[0])
            strN = row[1]
            strT = row[2]
            codNo = newSTP(strN,strT,'')
            if numPai == 1:
                #Meu pai é o root
                #tbAD_append('root-' + strT,rootCod,codNo)
                tbAD_append('1.org',rootCod,codNo)
            else:
                strTP = findTbFieldByValue('tbSTP','codNO',str(listPai[numPai-2]),'strTYPE')
                #tbAD_append(strTP + '-' + strT,listPai[numPai-2],codNo)
                tbAD_append('1.org',listPai[numPai-2],codNo)
            if len(listPai) < numPai:
                listPai.append(codNo)
            else:
                listPai[numPai-1] = codNo
            #print(listPai)

def getStrSql_DePara():
    sql = '''
    SELECT
    tbAD.cod as cod,
    tbAD.typeAD as typeAD,
    tbAD.codFrom as codFrom,
    tbSTP_From.strNAME as from_strNAME,
    tbSTP_From.strTYPE as from_strTYPE,
    tbSTP_From.strVALUE as from_strVALUE,
    tbAD.codTo as codTo,
    tbSTP_To.strNAME as to_strNAME,
    tbSTP_To.strTYPE as to_strTYPE,
    tbSTP_To.strVALUE as to_strVALUE
    FROM tbAD, tbSTP as tbSTP_From, tbSTP as tbSTP_To
    WHERE tbAD.cod > 0
    AND tbAD.codTo = tbSTP_To.codNO
    AND tbAD.codFrom = tbSTP_From.codNO
    '''
    return sql

# Pesquisa EU pesqM = Não é meu pai, nem meu filho, sou eu mesmo = ME
def pesqM(intNodo):
    connR=sqlite3.connect(strDbTree)
    sqlR = '''
    Select
    tbNO.cod as cod,
    tbNO.typeNO as typeNO,
    tbNO.codPointer as codPointer,
    tbNO.drwGX as drwGX,
    tbNO.drwGY as drwGY,
    tbNO.drwLev as dwrLev,
    tbNO.drwHei as drwHei,
    tbNO.drwPos as drwPos,
    tbNO.drwRel as drwRel,
    tbNO.booActive as booActive,
    tbSTP.cod as codSTP,
    tbSTP.strNAME as strNAME,
    tbSTP.strTYPE as strTYPE,
    tbSTP.strVALUE as strVALUE,
    tbSTP.codNO as codNO
    From tbNO, tbSTP
    Where tbNO.cod > 0
    And tbSTP.codNO = tbNO.cod
    And tbSTP.cod = tbNO.codPointer
    And tbSTP.codNO = ''' + str(intNodo)
    curR=connR.cursor()
    curR.execute(sqlR)
    colnamesR = [description[0] for description in curR.description]
    rowsR=curR.fetchall()
    dfR = pd.DataFrame.from_records(rowsR,columns=colnamesR)
    dfR.index = dfR['cod']
    dfR.drop('cod',axis=1,inplace=True)
    return dfR, len(rowsR)

#Pesquisa os nós filhos = Child
def pesqC(intNodo):
    connP=sqlite3.connect(strDbTree)
    sqlP = '''
    Select
    tbAD.cod as cod,
    tbAD.typeAD as typeAD,
    tbAD.codFrom as codFrom,
    tbAD.codTo as codTo,
    tbSTP.cod as codSTP,
    tbSTP.strNAME as strNAME,
    tbSTP.strTYPE as strTYPE,
    tbSTP.strVALUE as strVALUE,
    tbSTP.codNO as codNO
    From tbAD, tbSTP
    Where tbAD.cod > 0
    And tbAD.typeAD like '1.org'
    And tbAD.codTo = tbSTP.codNO
    And tbAD.codFrom = ''' + str(intNodo) + '''
    Order By tbSTP.codNo
    '''
    curP=connP.cursor()
    curP.execute(sqlP)
    colnamesP = [description[0] for description in curP.description]
    rowsP=curP.fetchall()
    dfP = pd.DataFrame.from_records(rowsP,columns=colnamesP)
    dfP.index = dfP['cod']
    dfP.drop('cod',axis=1,inplace=True)
    return dfP, len(rowsP)


#Pesquisa os nós pais = Father = O meu pai (ou os meus pais)
def pesqF(intNodo):
    connP=sqlite3.connect(strDbTree)
    sqlP = '''
    Select
    tbAD.cod as cod,
    tbAD.typeAD as typeAD,
    tbAD.codFrom as codFrom,
    tbAD.codTo as codTo,
    tbSTP.cod as codSTP,
    tbSTP.strNAME as strNAME,
    tbSTP.strTYPE as strTYPE,
    tbSTP.strVALUE as strVALUE,
    tbSTP.codNO as codNO
    From tbAD, tbSTP
    Where tbAD.cod > 0
    And tbAD.typeAD like '1.org'
    And tbAD.codTo = ''' + str(intNodo) + '''
    And tbAD.codFrom = tbSTP.codNO
    Order By tbSTP.codNo
    '''
    curP=connP.cursor()
    curP.execute(sqlP)
    colnamesP = [description[0] for description in curP.description]
    rowsP=curP.fetchall()
    dfP = pd.DataFrame.from_records(rowsP,columns=colnamesP)
    dfP.index = dfP['cod']
    dfP.drop('cod',axis=1,inplace=True)
    return dfP, len(rowsP)

# Imprime recursivamente somente as folhas
def recPrint(intNodo='1',strRec='STP'):
    dfR,Length = pesqM(intNodo)
    #print(strRec)

    #Agora pesquisa todos os filhos do nodo pai Em Execução (não finalizado)
    dfP,Length = pesqC(intNodo)
    if Length != 0:
        # Agora vou iterar dentro de dfP
        for index,row in dfP.iterrows():
            intPARA = row['codTo']
            strFilho = row['strNAME']
            recPrint(intPARA,strRec + '>' + strFilho)
    else:
        print(strRec)

# Verifica se as folhas possuem txt associado,se não cria
# Esse fazia a busca recursiva, mas agora não vai mais precisar
# Farei um SQL mesmo procurando por tipos "LEAF" e subir até o pai
# Gerar o nome
# Se existir, abrir cada um e criar as propriedades

def recCheckLeafForTxt(intNodo='1',strRec='STP'):
    global strCurDir
    global strDbFolder
    global strDbSubFolder
    global strStpFolder

    dfR,Length = pesqM(intNodo)
    #print(strRec)

    #Agora pesquisa todos os filhos do nodo pai Em Execução (não finalizado)
    dfP,Length = pesqC(intNodo)
    if Length != 0:
        # Agora vou iterar dentro de dfP
        for index,row in dfP.iterrows():
            intPARA = row['codTo']
            strFilho = row['strNAME']
            recCheckLeafForTxt(intPARA,strRec + '_' + strFilho)
    else:
        strFileToTest = strCurDir + strDbFolder + strDbSubFolder + strStpFolder + strRec + '.txt'
        strFileToCreate = strDbFolder + strDbSubFolder + strStpFolder + strRec + '.txt'
        if os.path.isfile(strFileToTest):
            print(strRec + ' existe!')
        else:
            print(strRec + ' não existe!')
            f = open(strFileToCreate,'w')
            f.write(strRec+'\n')
            f.write('1:2:3:\n')
            f.write('2:1:1:\n')
            f.write('3:1:2:')
            f.close()

# Funcionando
def recNoUpToRoot_Verifica(intNodo,strRec,meuNo):
    #Agora pesquisa todos os filhos do nodo pai Em Execução (não finalizado)
    df,Length = pesqF(intNodo)
    if Length != 0:
        # Tenho pai
        for index,row in df.iterrows():
            intPARA = row['codNO']
            strPai = row['strNAME']
            recNoUpToRoot_Verifica(intPARA,strPai + '_' + strRec,meuNo)
    else: #Cheguei no root
        strFileToTest = strCurDir + strDbFolder + strDbSubFolder + strStpFolder + strRec + '.txt'
        strFileToCreate = strDbFolder + strDbSubFolder + strStpFolder + strRec + '.txt'
        if os.path.isfile(strFileToTest):
            print('')
            print('#########')
            print('codNo {0}:{1} existe! Coletando atributos'.format(meuNo,strRec))
            print('##########')
            print('')
            propName, propTot, propFirst, propLast =  getSTPTextProps(strFileToCreate)
            print('\nNome: {0}\n Total: {1}\n First:{2}\n Last:{3}'.format(propName,propTot,propFirst,propLast))

            # Cria nós para essas propriedades
            tbSTP_updateOrNewChildFromNo(meuNo,'NAME','prop',propName)
            tbSTP_updateOrNewChildFromNo(meuNo,'TOTAL','prop',propTot)
            tbSTP_updateOrNewChildFromNo(meuNo,'FIRST','prop',propFirst)
            tbSTP_updateOrNewChildFromNo(meuNo,'LAST','prop',propLast)

        else:
            print(strRec + ' não existe! Criado, por favor editar e reexecutar verificacao...')
            f = open(strFileToCreate,'w')
            f.write(strRec+'\n')
            f.write('1:2:3:p\n')
            f.write('2:1:1:p\n')
            f.write('3:1:2:p')
            f.close()

# Vou tratar os arquivos de steps como arquivos csv com: como delimitador
# Vamos ver o que acontece
def getSTPTextProps(strTxtFullFilename):
    with open(strTxtFullFilename) as csvfile:
        #Tomo a prerrogativa de que o arquivo .txt possui um formato step válido
        # Propriedades de Interesse
        retStrName = ''
        retNumTot = 0
        retPeFirst = ''
        retPeLast = ''
          #Abre o arquivo e coleta informações
        spamreader = csv.reader(csvfile, delimiter=':', quotechar='|')
        numLinha= 0

        for row in spamreader:
            #print(row)
            numLinha+= 1
            lenRow = len(row)
            if numLinha== 1:
                retStrName = row[0]
            else:
                if lenRow >= 4:
                    retNumTot += int(row[0])
                    retPeLast = row[3]
                    if numLinha == 2:
                        retPeFirst = row[3]
        #print('Nome = ' + retStrName)
        #print('Total = ' + str(retNumTot))
        #print('Primeiro = ' + retPeFirst[:2])
        #print('Ultimo = ' + retPeLast[:2])
        return retStrName,retNumTot,retPeFirst,retPeLast




# Melhorar o verificar criuando dois arquivos texto com o que precisa ser feito.
# E outro com o log.
