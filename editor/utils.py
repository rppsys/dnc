# coding=utf-8
# Utils.py

# ############################################################################
                        # Funções Utilitárias
# ############################################################################
import os
import configparser
import datetime

clNoColor='\033[0m'
clBlack='\033[0;30m'
clRed='\033[0;31m'
clGreen='\033[0;32m'
clOrange='\033[0;33m'
clBlue='\033[0;34m'
clPurple='\033[0;35m'
clCyan='\033[0;36m'
clLight_Gray='\033[0;37m'
clDark_Gray='\033[1;30m'
clLight_Red='\033[1;31m'
clLight_Green='\033[1;32m'
clYellow='\033[1;33m'
clLight_Blue='\033[1;34m'
clLight_Purple='\033[1;35m'
clLight_Cyan='\033[1;36m'
clWhite='\033[1;37m'

def printCor(clColor,arg):
    print(clColor + arg + clNoColor)
    return clColor + arg + clNoColor

def printL(arg):
    print(clOrange + arg + clNoColor)
    return clOrange + arg + clNoColor

def printR(arg):
    print(clRed + arg + clNoColor)
    return clRed + arg + clNoColor

def printA(arg):
    print(clLight_Blue + arg + clNoColor)
    return clLight_Blue + arg + clNoColor

def printC(arg):
    print(clLight_Cyan + arg + clNoColor)
    return clLight_Cyan + arg + clNoColor

def printY(arg):
    print(clYellow + arg + clNoColor)
    return clYellow + arg + clNoColor

# ----------------------------------------------------------------------------
                                # Arquivos INI
# ----------------------------------------------------------------------------

# Com isso abaixo é possível gerenciar
# vários arquivos inis diferentes ao mesmo tempo
# basta passar no main variaveis cfgINI diferentes

def iniciarIni(paramStrINIFullFilename):
    global strFullFilename
    strFullFilename = paramStrINIFullFilename
    cfgINI = configparser.ConfigParser()
    if not os.path.isfile(strFullFilename):
        printL("Arquivo de configuração " + strFullFilename + " não existe! Será criado!")
        iniWrite(cfgINI,'data', 'hoje', datetime.datetime.today().strftime("%Y%m%d%H%M%S"))
        with open(strFullFilename, 'w') as configfile:
            cfgINI.write(configfile)
    else:
        # Se já existir, lê e atualiza data
        cfgINI.read(strFullFilename)
        iniWrite(cfgINI,'data', 'hoje', datetime.datetime.today().strftime("%Y%m%d%H%M%S"))
    return cfgINI

def iniWrite(cfgINI,strSection,strKey,strValue):
    # Insere
    listSections = cfgINI.sections()
    if strSection in listSections:
        cfgINI[strSection][strKey] = strValue
    else:
        cfgINI[strSection] = {}
        cfgINI[strSection][strKey] = strValue
    # Salva
    with open(strFullFilename, 'w') as cfgFile:
        cfgINI.write(cfgFile)

def iniRead(cfgINI,strSection,strKey,strDefault):
    listSections = cfgINI.sections()
    if strSection in listSections:
        if strKey in cfgINI[strSection]:
            return cfgINI[strSection][strKey]
        else:
            return strDefault
    else:
        return strDefault
