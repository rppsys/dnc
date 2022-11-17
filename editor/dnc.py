# coding=utf-8
# https://lazka.github.io/pgi-docs/Gtk-3.0/classes.html
# https://lazka.github.io/pgi-docs/WebKit2-4.0/classes/WebView.html

import os
from os import listdir
from os.path import isfile, join
import sys

import django
import gi
import datetime
import time
import pytz
import os.path
import argparse
import re
import math
import pandas as pd
import configparser
import json
import cairo

import matplotlib.pyplot as plt
import numpy as np

# Google (Ainda não usei para nada)
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Plotagem
from math import pi
from bokeh.plotting import figure, show, output_file, output_notebook, save
from bokeh.models import Toggle, BoxAnnotation, CustomJS, PrintfTickFormatter, ColumnDataSource, Range1d, LabelSet, Label, DatetimeTickFormatter, HoverTool
from bokeh.layouts import column, row
from bokeh.models.annotations import Span

from bokeh import events
from bokeh.models import Button, Div, TextInput, Slider

# https://www.nltk.org/
import nltk.tokenize
from nltk.tokenize import wordpunct_tokenize
from nltk.tokenize import WordPunctTokenizer
from nltk.tokenize import WhitespaceTokenizer
from nltk.tokenize import SpaceTokenizer

from unidecode import unidecode

# Imagens
import cv2
import imutils

# Meus Imports
import utils as u
import pilhaCircular as pC
import tabelaString as tS
import motorPesquisa as mP

# Meus Imports de Dança
import stepPlot as sP

strSep = os.path.sep
# strPathDir = os.getcwd()
strPathDir = '/home/ronie/prog/dnc/editor'

# Carrega INI
strINIFullFilename = strPathDir  + strSep +  "dnc.ini"
cfgINI = u.iniciarIni(strINIFullFilename)

# Carrega demais caminhos
strGladeFullFilename = strPathDir  + strSep +  "dnc.glade"
strGladeFullFilename = u.iniRead(cfgINI, 'PATH', 'strGladeFullFilename',strGladeFullFilename)

strCSSFullFilename = strPathDir  + strSep +  "dnc.css"
strCSSFullFilename = u.iniRead(cfgINI, 'PATH', 'strCSSFullFilename',strCSSFullFilename)

strExportLatexFullFilename = strPathDir  + strSep +  "latex" + strSep +  "txt" + strSep + "PRINCIPAL" + strSep + "output.tex"
strExportLatexFullFilename = u.iniRead(cfgINI, 'PATH', 'strExportLatexFullFilename',strExportLatexFullFilename)

# Imagens
strImgAxFullFilename = strPathDir  + strSep +  "IMG" + strSep + "ax-atual.png"
strImgBxFullFilename = strPathDir  + strSep +  "IMG" + strSep + "bx-atual.png"
strImgDxFullFilename = strPathDir  + strSep +  "IMG" + strSep + "dx-atual.png"

# A estratégia com os pé será sempre gerar as imagens de pes que serao usadas pelo stepPlot a partir
# de duas imagens originais que vou manter em outra pasta

# Leio daqui
strImgPE_original = strPathDir  + strSep +  "IMG" + strSep +  "ORIGINAL" + strSep + "pE-original.png"
strImgPD_original = strPathDir  + strSep +  "IMG" + strSep +  "ORIGINAL" + strSep + "pD-original.png"

# Salvo aqui
strImgPE = strPathDir  + strSep +  "IMG" + strSep + "pE-atual.png"
strImgPD = strPathDir  + strSep +  "IMG" + strSep + "pD-atual.png"

# Bibliotecas Gtk
gi.require_version('Gtk','3.0')
from gi.repository import Gtk,Gdk,Pango,GLib, GObject, Gio, GdkPixbuf

# Carrega CSS
screen = Gdk.Screen.get_default()
provider = Gtk.CssProvider()
provider.load_from_path(strCSSFullFilename)
Gtk.StyleContext.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

gi.require_version('WebKit2', '4.0')
from gi.repository import WebKit2

print("")

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

dictColors = {
'clBlack':clBlack,
'clRed':clRed,
'clGreen':clGreen,
'clOrange':clOrange,
'clBlue':clBlue,
'clPurple':clPurple,
'clCyan':clCyan,
'clLightGray':clLight_Gray,
'clDarkGray':clDark_Gray,
'clDarkRed':clLight_Red,
'clLightGreen':clLight_Green,
'clYellow':clYellow,
'clLightBlue':clLight_Blue,
'clMediumPurple':clLight_Purple,
'clDarkCyan':clLight_Cyan,
'clWhite':clWhite
}

listPrint = []
lpF = '%Y-%m-%d %H:%M:%S %f'
listColor = ['blue','red','cyan']


def retPrintStr():
    return '\r\n'.join([s for s in listPrint])

def printClear():
    listPrint.clear()

def printCor(clColor,arg):
    print(clColor + arg + clNoColor)
    listPrint.append(datetime.datetime.now().strftime(lpF) + ' > ' + arg)
    return clColor + arg + clNoColor

def printL(arg):
    print(clOrange + arg + clNoColor)
    listPrint.append(datetime.datetime.now().strftime(lpF) + ' > ' + arg)
    return clOrange + arg + clNoColor

def printR(arg):
    print(clRed + arg + clNoColor)
    listPrint.append(datetime.datetime.now().strftime(lpF) + ' > ' + arg)
    return clRed + arg + clNoColor

def printA(arg):
    print(clLight_Blue + arg + clNoColor)
    listPrint.append(datetime.datetime.now().strftime(lpF) + ' > ' + arg)
    return clLight_Blue + arg + clNoColor

def printC(arg):
    print(clLight_Cyan + arg + clNoColor)
    listPrint.append(datetime.datetime.now().strftime(lpF) + ' > ' + arg)
    return clLight_Cyan + arg + clNoColor

def printY(arg):
    print(clYellow + arg + clNoColor)
    listPrint.append(datetime.datetime.now().strftime(lpF) + ' > ' + arg)
    return clYellow + arg + clNoColor

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--developer", required=False,help="Executar como desenvolvedor")
ap.add_argument("-b", "--debug", required=False,help="Habilitar funções de testes")
args =  vars(ap.parse_args())

if args['developer'] != None:
    print("")
    printR('##### Modo Desenvolvedor #####')
    print("")
    booDev = True
else:
    print("")
    printY('##### Modo Usuário #####')
    print("")
    booDev = False

booDebug = False
if args['debug'] != None:
    print("")
    printR('***** Testes Habilitados *****')
    print("")
    booDebug = True

class Manipulador:
    # -----------------------------------------------------
                    # Eventos do Glade
    # -----------------------------------------------------
    def __init__(self):
        self.iniciarGeral()
        self.iniciarTags()
        # self.iniciarClock()
        self.teste_TestaNoInicio()

        # ----------------
        # Configurações da MainWindow
        # ----------------
        self.MainWindow: Gtk.Window = Builder.get_object("main_window")
        # https://lazka.github.io/pgi-docs/Gtk-3.0/classes/Widget.html#Gtk.Widget

        # -----------------------------
        # Configurações dos Dançarinos
        # -----------------------------
        self.Condutor = sP.ClasseAgente('Condutor',True,10,10,7,0)
        self.Condutor.plotaAgente(20)
        self.atualizarCondutorImagens()

        # ----------------
        # Por último: Tenta abrir último arquivo aberto
        # ----------------
        self.tentaAbrirUltimoFeature()

    def atualizarCondutorImagens(self):
        self.abrirImagemResize('imgAX',strImgAxFullFilename, 250, 250)
        self.abrirImagemResize('imgBX',strImgBxFullFilename, 250, 250)
        self.abrirImagemResize('imgDX',strImgDxFullFilename, 250, 250)

    def abrirImagemResize(self,strObj,strFilename,width,height):
        # https://stackoverflow.com/questions/1269320/scale-an-image-in-gtk
        # https://lazka.github.io/pgi-docs/GdkPixbuf-2.0/enums.html#GdkPixbuf.InterpType.BILINEAR
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(strFilename)
        pixbuf = pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
        Builder.get_object(strObj).set_from_pixbuf(pixbuf)


    def tentaAbrirUltimoFeature(self):
        strFile = u.iniRead(cfgINI,'PATH','strFileFeatureFullFilename','')
        if strFile != '':
            self.abrirFeature(strFile)

    def iniciarGeral(self):
        # --------------------------
        # Configurações do tvEditor
        # --------------------------
        self.strFileFeatureFullFilename = ''

        self.tvEditor: Gtk.TextView = Builder.get_object("tvEditor")
        self.tvEditor.connect("key-press-event",self.on_key_press_event)
        self.tvEditor.connect("key-release-event",self.on_key_release_event)

        textbuffer = self.tvEditor.get_buffer()
        textbuffer.name = 'tbTvEditor' # Para CSS
        textbuffer.connect("modified-changed",self.on_buffer_modified_changed)
        textbuffer.connect("changed",self.on_buffer_changed)

        # --------------------------
        # Configurações do tvLinhas
        # --------------------------
        self.tvLinhas: Gtk.TextView = Builder.get_object("tvLinhas")

        adjTvEditor = Builder.get_object("swEditor").get_vadjustment()
        adjTvEditor.connect("value_changed", self.on_tvEditor_scroll_event_meu)

        adjTvLinhas = Builder.get_object("swLinhas").get_vadjustment()
        adjTvLinhas.connect("value_changed", self.on_tvLinhas_scroll_event_meu)

        # --------------------------
        # Configurações do tvTreeCenarios
        # --------------------------
        self.tvTreeCenarios = Builder.get_object("tvTreeCenarios")
        self.tvTreeCenarios.numRowCenarioAtivo = 0

        # --------------------------
        # Configurações do dlgFileChooser
        # --------------------------
        self.dlgFileChooser: Gtk.FileChooserDialog = Builder.get_object("dlgFileChooser")
        self.dlgFileChooser.booFirst = True

        # -------------------------------------
        # Inicializações de Variáveis Globais
        # -------------------------------------
        self.tvEditor.booExisteFeatureAberta = False
        self.tvEditor.booModoEdicao = False


        # --------------------------
        # Configurações da Barra de Pesquisas
        # --------------------------
        self.boxPesquisarFechar = Builder.get_object("boxPesquisarFechar")
        self.boxPesquisarFechar.hide()

        # --------------------------
        # Outras Inicializações
        # --------------------------
        self.iniciarTbCenarios()

    def iniciarClock(self):
        self.onClockTimer()
        self.startClockTimer()

    def getAdjustValue(self,numLinha):
        adj = Builder.get_object("swEditor").get_vadjustment()
        tvEditor = Builder.get_object("tvEditor")
        buf = tvEditor.get_buffer()
        numLinhaTotal = buf.get_line_count()

        numPrimeirasLinhas = round(adj.get_page_size() / 26,0)
        numUltimoValor =  adj.get_upper() - adj.get_page_size()

        numOffset = 0
        if numUltimoValor < adj.get_upper():
            numOffset = round((adj.get_upper() - numUltimoValor)/2,0)

        if numLinha + 1 <= numPrimeirasLinhas:
            return 0
        elif numLinha + 1 == numLinhaTotal:
            return numUltimoValor + numOffset
        else:
            return numUltimoValor - (numLinhaTotal - numLinha - 1)*22 + numOffset - 350

    # Criei isso para testar propriedades
    def onClockTimer(self):
        textbuffer = self.tvEditor.get_buffer()
        numLinhaTotalTvEditor = textbuffer.get_line_count()

        bufLinhas = self.tvLinhas.get_buffer()
        numLinhaTotalTvLinhas = bufLinhas.get_line_count()

        print('')
        print('Editor = {}'.format(numLinhaTotalTvEditor))
        print('Linhas = {}'.format(numLinhaTotalTvLinhas))
        return True

    def onClockTimerOld(self):
        strDatetimenow = str(datetime.datetime.now())
        Builder.get_object("lbCenarios").set_label(strDatetimenow)
        # Testes
        adj = Builder.get_object("swEditor").get_vadjustment()
        tvEditor = Builder.get_object("tvEditor")
        buf = tvEditor.get_buffer()

        m = buf.get_insert()
        i = buf.get_iter_at_mark(m)
        numLinhaAtual = i.get_line()

        print('')
        print('Upper = {}'.format(adj.get_upper()))
        print('Lower = {}'.format(adj.get_lower()))
        print('Page = {}'.format(adj.get_page_size()))
        print('Diff U - P = {}'.format(adj.get_upper() - adj.get_page_size()))
        print('Linha = {}'.format(numLinhaAtual))
        print('Value = {}'.format(adj.get_value()))
        print('Meu = {}'.format(self.getAdjustValue(numLinhaAtual)))
        return True

    def startClockTimer(self):
        GLib.timeout_add(1000, self.onClockTimer)

    def on_main_window_destroy(self, Window):
        self.sair()

    def sair(self):
        # Sair
        print('Saindo...')
        Gtk.main_quit()

    def iniciarTags(self):
        textbuffer = self.tvEditor.get_buffer()

        # Tags que Pintam a linha toda:
        self.listTagLine = [
            'funcionalidade',
            '_condutor_',
            'contexto',
        ]

        # Tags de Keyword = Pinta somente a própria tag
        self.listTagKeyword = [
            'dado',
            'e',
            'mas',
            'quando',
            'entao',
        ]

        # Tags que pintam de onde aparece a tag até o final da linha
        self.listTagFromToEnd = [
            '#',
            '|',
            '#!',
        ]

        # Tags que pintam somente a palavra na frente
        self.listTagWordOnly = [
            '@',
        ]


        # ####################################################################
        # Definições de Fontes Pango para as Tags
        # ####################################################################
        # https://matplotlib.org/stable/gallery/color/named_colors.html

        self.dictTag = {}
        self.dictTag['funcionalidade'] = textbuffer.create_tag("funcionalidade", weight=Pango.Weight.BOLD, foreground="Red")
        self.dictTag['_condutor_'] = textbuffer.create_tag("_condutor_", weight=Pango.Weight.BOLD, foreground="Yellow")
        self.dictTag['contexto'] = textbuffer.create_tag("contexto", weight=Pango.Weight.BOLD, foreground="goldenrod")
        self.dictTag['dado'] = textbuffer.create_tag("dado", weight=Pango.Weight.BOLD, foreground="Coral")
        self.dictTag['e'] = textbuffer.create_tag("e", foreground="DodgerBlue")
        self.dictTag['mas'] = textbuffer.create_tag("mas", foreground="DodgerBlue")
        self.dictTag['quando'] = textbuffer.create_tag("quando", weight=Pango.Weight.BOLD, foreground="Coral")
        self.dictTag['entao'] = textbuffer.create_tag("entao", weight=Pango.Weight.BOLD, foreground="Coral")

        self.dictTag['bold'] = textbuffer.create_tag("bold", weight=Pango.Weight.BOLD, foreground="lemonchiffon")
        self.dictTag['italic'] = textbuffer.create_tag("italic", style=Pango.Style.ITALIC)
        self.dictTag['strike'] = textbuffer.create_tag("strike", strikethrough=True)
        self.dictTag['underline'] = textbuffer.create_tag("underline",  underline=Pango.Underline.SINGLE)
        self.dictTag['string'] = textbuffer.create_tag("string",  foreground="deepskyblue")
        self.dictTag['parametro'] = textbuffer.create_tag("parametro", foreground="turquoise")
        self.dictTag['matchAntes'] = textbuffer.create_tag("matchAntes", foreground="black", background="cyan")
        self.dictTag['matchDepois'] = textbuffer.create_tag("matchDepois", foreground="black", background="yellow")

        self.dictTag['#'] = textbuffer.create_tag("#", style=Pango.Style.ITALIC, foreground="darkturquoise")
        self.dictTag['#!'] = textbuffer.create_tag("#!", style=Pango.Style.ITALIC, foreground="springgreen")
        self.dictTag['|'] = textbuffer.create_tag("|", foreground="deepskyblue")
        self.dictTag['@'] = textbuffer.create_tag("@", style=Pango.Style.ITALIC, foreground="magenta")
        self.dictTag['$'] = textbuffer.create_tag("$", weight=Pango.Weight.BOLD, foreground="magenta")

        self.dictTag['tab'] = textbuffer.create_tag("tab", background="dimgray")
        self.dictTag['linha'] = textbuffer.create_tag("linha", background="lightgray")

        # Formatos para tvLinhas
        bufferTvLinhas = self.tvLinhas.get_buffer()
        self.dictTag['tvLinhasPadrao'] = bufferTvLinhas.create_tag("tvLinhasPadrao")
        self.dictTag['tvLinhasCenario'] = bufferTvLinhas.create_tag("tvLinhasCenario",foreground="Yellow")
        self.dictTag['tvLinhasCenarioExport'] = bufferTvLinhas.create_tag("tvLinhasCenarioExport",foreground="Lime")


        # ####################################################################
        # Definições de Fontes Latex para as Tags
        # ####################################################################
        # Arqui preciso de diversos dictLatexTags pois os tratamentos são diferentes

        # \textcolor{red}{Teste}
        # \textcolor{red}{Teste}
        # \colorbox{orange}{\textcolor{red}{Teste}}

        # Operadores Iguais
        self.dictLatexTagOpIguais = {}
        self.dictLatexTagOpIguais['**'] = '\\textbf{'
        self.dictLatexTagOpIguais['--'] = '\\emph{'
        self.dictLatexTagOpIguais['~~'] = '\\sout{'
        self.dictLatexTagOpIguais['__'] = '\\underline{'
        self.dictLatexTagOpIguais['"'] = '\\textcolor{blue}{'
        self.dictLatexTagOpIguais["'"] = '\\textcolor{blue}{'
        self.dictLatexTagOpIguais['$'] = '\\textcolor{magenta}{'

        # Operadores Duplos
        self.dictLatexTagOpDuplos = {}
        self.dictLatexTagOpDuplos['**"'] = '\\textcolor{blue}{textbf{'
        self.dictLatexTagOpDuplos["**'"] = '\\textcolor{blue}{textbf{'
        self.dictLatexTagOpDuplos['*"'] = '\\textcolor{blue}{textbf{'
        self.dictLatexTagOpDuplos["*'"] = '\\textcolor{blue}{textbf{'
        self.dictLatexTagOpDuplos["<"] = '\colorbox{blue!40}{\\textcolor{black}{'

        # Tags que Pintam a linha toda:
        self.dictLatexTagLine = {}
        self.dictLatexTagLine['funcionalidade'] = '\\textcolor{red}{textbf{'
        self.dictLatexTagLine['contexto'] = '\\textcolor{blue}{textbf{'
        # self.dictLatexTagLine['cenario'] = '\\textcolor{yellow}{textbf{' # Tirei pois cenarios viram seções

        # Tags de Keyword = Pinta somente a própria tag
        self.dictLatexTagKeyword = {}
        self.dictLatexTagKeyword['dado'] = '\\textcolor{blue}{\\textbf{'
        self.dictLatexTagKeyword['e'] =  '\\textcolor{teal}{\\textbf{'
        self.dictLatexTagKeyword['mas'] =  '\\textcolor{teal}{\\textbf{'
        self.dictLatexTagKeyword['quando'] =  '\\textcolor{blue}{\\textbf{'
        self.dictLatexTagKeyword['entao'] =  '\\textcolor{blue}{\\textbf{'

        # Tags que pintam de onde aparece a tag até o final da linha
        self.dictLatexTagFromToEnd = {}
        self.dictLatexTagFromToEnd['#'] = '\\textcolor{cyan}{\\emph{'
        self.dictLatexTagFromToEnd['#!'] = '\\textcolor{purple}{\\emph{'

        # Tags que pintam somente a palavra na frente
        self.dictLatexTagWordOnly = {}
        self.dictLatexTagWordOnly['@'] = ''


    # -----------------------------------------------------
                    # Menu Principal
    # -----------------------------------------------------

    def on_miArquivo_Exportar_activate(self,button):
        self.exportarLatex()

    def on_miArquivo_Abrir_activate(self,button):
        booRet, strFile = self.dlgAbrir()
        if booRet:
            self.abrirFeature(strFile)

    def abrirFeature(self,strFile):
        if os.path.isfile(strFile):
            self.strFileFeatureFullFilename = strFile
            fileFeature = open(self.strFileFeatureFullFilename, "r")
            strConteudo = fileFeature.read()
            textbuffer = self.tvEditor.get_buffer()
            textbuffer.set_text(strConteudo)
            fileFeature.close()
            u.iniWrite(cfgINI,'PATH','strFileFeatureFullFilename',self.strFileFeatureFullFilename)
            self.atualizarTbCenarios()
            self.atualizarTvEditor() # Tem ficar depois do atualizarTbCenarios pois usa uma lista criada lá
            self.atualizarTvLinhas()
            self.tvEditor.set_editable(False)
            self.tvLinhas.set_editable(False)
            self.pilhaUndoRedo = pC.pilhaCircular(21)

            # Propriedades
            Builder.get_object("lbStatusLeft").set_text(strFile)
            Builder.get_object("lbStatusCenter").set_text('Somente Leitura')
            Builder.get_object("lbStatusRight").set_text('Não Modificado')
            self.tvEditor.booExisteFeatureAberta = True
            self.storeUndo()
            self.iniciaMotorPesquisa()
            return True
        else:
            return False

    def iniciaMotorPesquisa(self):
        tbEditor = self.tvEditor.get_buffer()
        self.mP = mP.motorPesquisa(tbEditor)

    def on_tvEditor_scroll_event_meu(self,event):
        adjTvEditor = Builder.get_object("swEditor").get_vadjustment()
        adjTvLinhas = Builder.get_object("swLinhas").get_vadjustment()
        valorAdjTvEditor = adjTvEditor.get_value()
        adjTvLinhas.set_value(valorAdjTvEditor)

    def on_tvLinhas_scroll_event_meu(self,event):
        adjTvLinhas = Builder.get_object("swLinhas").get_vadjustment()
        adjTvEditor = Builder.get_object("swEditor").get_vadjustment()
        valorAdjTvLinhas = adjTvLinhas.get_value()
        adjTvEditor.set_value(valorAdjTvLinhas)

    def on_miEditar_HabilitarEdicao_activate(self,button):
        if self.tvEditor.booExisteFeatureAberta:
            self.tvEditor.set_editable(True)
            # Propriedades
            self.tvEditor.booModoEdicao = True
            Builder.get_object("lbStatusCenter").set_text('Modo de Edição')

    def on_btnPesquisaFechar_activate(self,button):
        self.esconderPesquisa()

    def on_btnPesquisaFechar_clicked(self,button):
        self.esconderPesquisa()

    def on_btnPesquisaTogPesquisarSubstituir_toggled(self,toggle_button):
        booEstado = toggle_button.get_active()
        if booEstado:
            Builder.get_object("boxPesquisaSubstituir").show()
        else:
            Builder.get_object("boxPesquisaSubstituir").hide()

    def on_btnPesquisaTogOpcoes_toggled(self,toggle_button):
        booEstado = toggle_button.get_active()
        if booEstado:
            Builder.get_object("boxPesquisaOpcoes").show()
        else:
            Builder.get_object("boxPesquisaOpcoes").hide()

    def iniciarPesquisa(self):
        Builder.get_object("boxPesquisarFechar").show()
        textbuffer = self.tvEditor.get_buffer()
        if textbuffer.get_has_selection():
            start, end = textbuffer.get_selection_bounds()
            strTexto = textbuffer.get_text(start,end,False)
            Builder.get_object("sePesquisar").set_text(strTexto)
            Builder.get_object("sePesquisar").grab_focus_without_selecting()
            if (len(strTexto) >= 1) and (len(strTexto) <= 3):
                self.fazPesquisa()
                numLinha,iterLineStart,iterLineEnd = self.mP.getPosAtual()
                self.selecionaTexto(numLinha,iterLineStart,iterLineEnd)
        else:
            Builder.get_object("sePesquisar").grab_focus_without_selecting()

    def esconderPesquisa(self):
        Builder.get_object("btnPesquisaTogPesquisarSubstituir").set_active(False)
        Builder.get_object("btnPesquisaTogOpcoes").set_active(False)
        Builder.get_object("sePesquisar").set_text('')
        Builder.get_object("boxPesquisarFechar").hide()
        self.atualizarTvEditor()
        self.pesquisaAtualizaStatus(False)

    def on_sePesquisar_key_press_event(self, widget, event):
        # ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)
        # alt = (event.state & Gdk.ModifierType.MOD1_MASK)
        # shift = (event.state & Gdk.ModifierType.SHIFT_MASK)
        # print(Gdk.keyval_name(event.keyval))
        if event.keyval == Gdk.KEY_Escape:
            self.esconderPesquisa()
        elif event.keyval == Gdk.KEY_Return:
            self.fazPesquisa()
            # Seleciona
            numLinha,iterLineStart,iterLineEnd = self.mP.getPosAtual()
            self.selecionaTexto(numLinha,iterLineStart,iterLineEnd)

    def fazPesquisa(self):
        sePesquisar = Builder.get_object("sePesquisar")
        strPesquisa = sePesquisar.get_text()
        self.mP.pesquisar(strPesquisa)
        self.atualizarTvEditor()
        self.mP.pintaResultados(self.dictTag['matchAntes'],self.dictTag['matchDepois'])
        self.pesquisaAtualizaStatus(True)

    def pesquisaAtualizaStatus(self,booVisivel):
        if booVisivel:
            Builder.get_object("lbStatusCenterLeft").set_text(self.mP.textoPosicao())
            Builder.get_object("sePesquisar").set_progress_fraction(self.mP.fracaoPosicao())
        else:
            Builder.get_object("lbStatusCenterLeft").set_text('')
            Builder.get_object("sePesquisar").set_progress_fraction(0.0)

    def on_sePesquisar_search_changed(self, search_entry):
        strPesquisa = Builder.get_object("sePesquisar").get_text()
        if (len(strPesquisa) > 3) or (strPesquisa == ''):
            self.fazPesquisa()
            textbuffer = self.tvEditor.get_buffer()
            if textbuffer.get_has_selection():
                numLinha,iterLineStart,iterLineEnd = self.mP.getPosAtual()
                self.selecionaTexto(numLinha,iterLineStart,iterLineEnd)

    def on_btnPesquisaNavAnterior_activate(self,button):
        if not self.mP.getAtivo():
            self.fazPesquisa()
        self.mP.anterior()
        self.pesquisaAtualizaStatus(True)
        numLinha,iterLineStart,iterLineEnd = self.mP.getPosAtual()
        self.selecionaTexto(numLinha,iterLineStart,iterLineEnd)

    def on_btnPesquisaNavAnterior_clicked(self,button):
        if not self.mP.getAtivo():
            self.fazPesquisa()
        self.mP.anterior()
        self.pesquisaAtualizaStatus(True)
        numLinha,iterLineStart,iterLineEnd = self.mP.getPosAtual()
        self.selecionaTexto(numLinha,iterLineStart,iterLineEnd)

    def on_btnPesquisaNavProximo_activate(self,button):
        if not self.mP.getAtivo():
            self.fazPesquisa()
        else:
            self.mP.proximo()
        self.pesquisaAtualizaStatus(True)
        numLinha,iterLineStart,iterLineEnd = self.mP.getPosAtual()
        self.selecionaTexto(numLinha,iterLineStart,iterLineEnd)

    def on_btnPesquisaNavProximo_clicked(self,button):
        if not self.mP.getAtivo():
            self.fazPesquisa()
        else:
            self.mP.proximo()
        self.pesquisaAtualizaStatus(True)
        numLinha,iterLineStart,iterLineEnd = self.mP.getPosAtual()
        self.selecionaTexto(numLinha,iterLineStart,iterLineEnd)

    # -----------------------------------------------------
                    # Eventos Auxiliares
    # -----------------------------------------------------
    def dlgAbrir(self):
        dlgFileChooser = self.dlgFileChooser
        # Nao funciona nao sei pq
        if os.path.isfile(self.strFileFeatureFullFilename):
            dirPath = os.path.dirname(self.strFileFeatureFullFilename)
            dlgFileChooser.set_current_folder(dirPath)
        dlgFileChooser.set_title('Escolha um arquivo para abrir:')
        if self.dlgFileChooser.booFirst:
            dlgFileChooser.add_buttons(
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OPEN,
                Gtk.ResponseType.OK,
            )
            self.add_filters(dlgFileChooser)
            self.dlgFileChooser.booFirst = False

        response = dlgFileChooser.run()

        if response == Gtk.ResponseType.OK:
            booRet = True
            strFile = dlgFileChooser.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            booRet = False
            strFile = ''
        dlgFileChooser.hide()
        return booRet, strFile

    def add_filters(self, dialog):
        filter_features = Gtk.FileFilter()
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)

        filter_py = Gtk.FileFilter()
        filter_py.set_name("Python files")
        filter_py.add_mime_type("text/x-python")
        dialog.add_filter(filter_py)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    # -----------------------------------------------------
                    # Eventos do Glade
    # -----------------------------------------------------

    def on_buffer_changed(self,textbuffer):
        if self.tvEditor.booExisteFeatureAberta:
            # Para Testes
            self.teste_separaLinha(textbuffer)

            self.atualizarTbCenarios()
            self.atualizarLinha(textbuffer)
            numLinhaTotal, bufLinhas = self.tvLinhas_VerificaAtualizaLinhas()
            self.tvLinhas_atualizarFormatos(numLinhaTotal, bufLinhas)
            Builder.get_object("lbStatusRight").set_text('Modificado')
            self.setaStatusBuffer()

    def setaStatusBuffer(self):
        numUR = self.pilhaUndoRedo.retCount()
        if numUR == 1:
            Builder.get_object("lbStatusRightBuffer").set_text('0')
        else:
            Builder.get_object("lbStatusRightBuffer").set_text('{}'.format(numUR-1))

    def on_buffer_modified_changed(self,textbuffer):
        pass

    def on_tvTreeCenarios_row_activated(self,tree_view, path, column):
        if self.tvEditor.booExisteFeatureAberta:
            # Captura Linha
            tvTree = tree_view
            lsList = tvTree.props.model
            treeiter = lsList.get_iter(path)
            numLinha = int(lsList.get_value(treeiter, 2))

            # Descobre Iter
            textbuffer = self.tvEditor.get_buffer()
            buf = textbuffer
            numLinhaTotal = buf.get_line_count()

            iterLineStart = buf.get_iter_at_line(numLinha)
            if ((numLinha + 1) != numLinhaTotal):
                iterLineEnd = buf.get_iter_at_line(numLinha+1)
                iterLineEnd.backward_char()
            else:
                iterLineEnd = buf.get_end_iter()
            strLinhaTexto = buf.get_text(iterLineStart,iterLineEnd,False)

            # Seleciona
            # Continuo usando o método que criei porque o nativo não responde bem
            self.selecionaTexto(numLinha,iterLineStart,iterLineEnd)

    def selecionaTexto(self,numLinha,iterLineStart,iterLineEnd):
        if numLinha != None:
            if iterLineStart != None:
                if iterLineEnd != None:
                    buf = self.tvEditor.get_buffer()
                    adj = Builder.get_object("swEditor").get_vadjustment()
                    numAdjValue = self.getAdjustValue(numLinha)
                    adj.set_value(numAdjValue)
                    self.tvEditor.scroll_to_iter(iterLineStart,0.0,True,0.5,0.5)
                    buf.select_range(iterLineStart,iterLineEnd)

    # https://riptutorial.com/gtk3/example/16426/simple-binding-to-a-widget-s-key-press-event
    def on_key_press_event(self, widget, event):
        if self.tvEditor.booExisteFeatureAberta:
            # -----------------------------------
            # Deixei estruturado para usar depois
            # -----------------------------------

            # print("Key press on widget: ", widget.get_name())
            # print("          Modifiers: ", event.state)
            # print("      Key val, name: ", event.keyval, Gdk.keyval_name(event.keyval))

            # check the event modifiers (can also use SHIFTMASK, etc)
            ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)
            alt = (event.state & Gdk.ModifierType.MOD1_MASK)
            shift = (event.state & Gdk.ModifierType.SHIFT_MASK)

            # see if we recognise a keypress
            if ctrl:
                if alt:
                    #ctrl + alt + h
                    if event.keyval == Gdk.KEY_h:
                        self.comutaFlagExportLatex()
                    #ctrl + alt + j
                    if event.keyval == Gdk.KEY_l:
                        if self.tvEditor.booExisteFeatureAberta:
                            if self.tvEditor.booModoEdicao:
                                self.formataTabela()
                    #ctrl + alt + k
                    if event.keyval == Gdk.KEY_k:
                        pass
                    #ctrl + alt + j
                    if event.keyval == Gdk.KEY_j:
                        self.teste()
                else:
                    if event.keyval == Gdk.KEY_s: #ctrl + s
                        if self.tvEditor.booExisteFeatureAberta:
                            if self.tvEditor.booModoEdicao:
                                self.salvar()
                    elif event.keyval == Gdk.KEY_f: # ctrl + f
                        if self.tvEditor.booExisteFeatureAberta:
                            self.iniciarPesquisa()
                    elif event.keyval == Gdk.KEY_i: # ctrl + i
                        if self.tvEditor.booExisteFeatureAberta:
                            printC('INI Configurados')
                            self.atualizaIni()
                    elif event.keyval == Gdk.KEY_g: # ctrl + g
                        if self.tvEditor.booExisteFeatureAberta:
                            printC('Recarregar CSS')
                            self.recarregaCSS()
                    elif event.keyval == Gdk.KEY_d: # ctrl + d
                        self.executaPasso()
            else:
                if alt:
                    pass
                else: # Não tem Ctrl nem Alt
                    if ((event.keyval == Gdk.KEY_Up) or (event.keyval == Gdk.KEY_Down) or (event.keyval == Gdk.KEY_Left) or (event.keyval == Gdk.KEY_Right)):
                        pass
                    elif (event.keyval == Gdk.KEY_Return):
                        if self.tvEditor.booModoEdicao:
                            pass

    def salvar(self):
        buf = self.tvEditor.get_buffer()
        strTexto = buf.get_text(buf.get_start_iter(),buf.get_end_iter(),True)
        fileFeature = open(self.strFileFeatureFullFilename, "w")
        fileFeature.write(strTexto)
        fileFeature.close()
        Builder.get_object("lbStatusRight").set_text('Salvo!')

    def on_key_release_event(self, widget, event):
        if self.tvEditor.booExisteFeatureAberta:
            if self.tvEditor.booModoEdicao:
                #print("Key release on widget: ", widget.get_name())
                #print("          Modifiers: ", event.state)
                #print("      Key val, name: ", event.keyval, Gdk.keyval_name(event.keyval))
                # check the event modifiers (can also use SHIFTMASK, etc)
                ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)
                alt = (event.state & Gdk.ModifierType.MOD1_MASK)
                shift = (event.state & Gdk.ModifierType.SHIFT_MASK)

                # see if we recognise a keypress
                if ctrl:
                    if shift:
                        if event.keyval == Gdk.KEY_Z:
                            self.redo()
                    if event.keyval == Gdk.KEY_z:
                        self.undo()
                else:
                    self.storeUndo()

    def storeUndo(self):
        # Pega Atributos do Texto
        bufferTvEditor = self.tvEditor.get_buffer()
        strTexto = bufferTvEditor.get_text(bufferTvEditor.get_start_iter(),bufferTvEditor.get_end_iter(),True)
        numPosCursor = bufferTvEditor.props.cursor_position

        # Cria tupla e adiciona na pilha circular
        tupleUR = strTexto,numPosCursor
        self.pilhaUndoRedo.push(tupleUR)
        self.setaStatusBuffer()

    def undo(self):
        booRet, tupleUR = self.pilhaUndoRedo.pop()
        if booRet:
            booRet, tupleUR = self.pilhaUndoRedo.top()
            if booRet:
                if len(tupleUR) > 1:
                    bufferTvEditor = self.tvEditor.get_buffer()
                    strTexto_Atual = bufferTvEditor.get_text(bufferTvEditor.get_start_iter(),bufferTvEditor.get_end_iter(),True)
                    numPosCursor_Atual = bufferTvEditor.props.cursor_position

                    strTexto_Undo,numPosCursor_Undo = tupleUR

                    if strTexto_Atual != strTexto_Undo:
                        bufferTvEditor.set_text(strTexto_Undo)

                    if numPosCursor_Atual != numPosCursor_Undo:
                        iterCursor = bufferTvEditor.get_start_iter()
                        iterCursor.forward_chars(numPosCursor_Undo)
                        bufferTvEditor.place_cursor(iterCursor)

                    self.atualizarTbCenarios()
                    self.atualizarTvEditor()
                    self.atualizarTvLinhas()
                    self.setaStatusBuffer()

    def redo(self):
        booRet, tupleUR = self.pilhaUndoRedo.redo()
        if booRet:
            if len(tupleUR) > 1:
                bufferTvEditor = self.tvEditor.get_buffer()
                strTexto_Atual = bufferTvEditor.get_text(bufferTvEditor.get_start_iter(),bufferTvEditor.get_end_iter(),True)
                numPosCursor_Atual = bufferTvEditor.props.cursor_position

                strTexto_Redo,numPosCursor_Redo = tupleUR

                if strTexto_Atual != strTexto_Redo:
                    bufferTvEditor.set_text(strTexto_Redo)

                if numPosCursor_Atual != numPosCursor_Redo:
                    iterCursor = bufferTvEditor.get_start_iter()
                    iterCursor.forward_chars(numPosCursor_Redo)
                    bufferTvEditor.place_cursor(iterCursor)

                self.atualizarTbCenarios()
                self.atualizarTvEditor()
                self.atualizarTvLinhas()
                self.setaStatusBuffer()

    def on_tvEditor_button_release_event(self,widget,event):
        if self.tvEditor.booExisteFeatureAberta:
            self.selecionaLinhaTvTreeCenario()

    # -----------------------------------------------------
                    # Eventos Auxiliares
    # -----------------------------------------------------

    def exportarLatex(self):
        # Primeiro preciso construir lista de cenários que serão exportados
        # Percorrer tvTreeTbCenario e verificar Exports = 'Sim'
        if self.tvEditor.booExisteFeatureAberta:
            bufferTvEditor = self.tvEditor.get_buffer()
            tvTree = self.tvTreeCenarios
            lsList = tvTree.props.model
            dCI = self.TbCenarios_dictColsIndex
            strTextoLatex = ''

            numRow = 0
            for numTvTreeCenariosRow in lsList:
                if numTvTreeCenariosRow[dCI['Exportar']] != 'Sim':
                    # Linha onde inicia o Cenário
                    numTbEditorLinhaInicial = int(numTvTreeCenariosRow[dCI['Linha']])
                    iterTbEditorLinhaInicial = bufferTvEditor.get_iter_at_line(numTbEditorLinhaInicial)

                    # Linha onde finaliza o Cenário
                    if numRow + 1 == len(lsList):
                        iterTbEditorLinhaFinal = bufferTvEditor.get_end_iter()
                    else:
                        numTbEditorLinhaProxima = int(lsList[numRow + 1][dCI['Linha']])
                        iterTbEditorLinhaFinal = bufferTvEditor.get_iter_at_line(numTbEditorLinhaProxima)

                    # Texto do Cenário Completo
                    strTextoCenario = bufferTvEditor.get_text(iterTbEditorLinhaInicial,iterTbEditorLinhaFinal,False)
                    strTextoCenarioLatex = ''

                    # Lista de Linhas do Texto
                    listTextoCenarioComArroba = list(strTextoCenario.split('\n'))

                    # Preciso remover linhas que contém '@'s
                    listTextoCenario = [strLinha for strLinha in listTextoCenarioComArroba if "@" not in strLinha]

                    # ---------------------------
                    # Aqui eu converto para Latex
                    # ---------------------------
                    if len(listTextoCenario) != 0:
                        if len(listTextoCenario) == 1:
                            # Só tem uma linha
                            # strAux = self.formataLatex(listTextoCenario[0].strip())
                            strAux = self.escapaLatex(listTextoCenario[0].strip()) # Nao vou formatar o que vai para Section, apenas escapar

                            strTextoCenarioLatex = '\section{{{}}}'.format(strAux)
                            strTextoCenarioLatex = strTextoCenarioLatex + '\n' + 'Cenário sem linhas!'
                            strTextoLatex = strTextoLatex + '\n' + strTextoCenarioLatex
                        else: # Tem mais de uma linha
                            # Primeira Linha
                            # strAux = self.formataLatex(listTextoCenario[0].strip())
                            strAux = self.escapaLatex(listTextoCenario[0].strip()) # Nao vou formatar o que vai para Section, apenas escapar

                            strTextoCenarioLatex = '\section{{{}}}'.format(strAux)
                            strTextoCenarioLatex = strTextoCenarioLatex + '\n' + '\\begin{enumerate}'
                            # Demais Linhas
                            numListTextoCenario = 1
                            while numListTextoCenario < len(listTextoCenario):
                                strLinhaTextoCenario = listTextoCenario[numListTextoCenario].strip()
                                if strLinhaTextoCenario != '':
                                    if '|' in strLinhaTextoCenario:
                                        # Se tiver pipe é porque posso estar numa tabela e aqui vou querer gerar a tabela formatada
                                        booFuncionou, strLatexTabela, numListTextoCenario = self.criaStrLatexTabela(numListTextoCenario,listTextoCenario)
                                        if booFuncionou:
                                            strTextoCenarioLatex = strTextoCenarioLatex + '\n' + strLatexTabela
                                        else:
                                            strAux = self.formataLatex(strLinhaTextoCenario)
                                            strTextoCenarioLatex = strTextoCenarioLatex + '\n' + '\t\item ' + strAux
                                    else:
                                        strAux = self.formataLatex(strLinhaTextoCenario)
                                        strTextoCenarioLatex = strTextoCenarioLatex + '\n' + '\t\item ' + strAux
                                # Incrementa contador do while
                                numListTextoCenario = numListTextoCenario + 1
                            # Fechamento
                            strTextoCenarioLatex = strTextoCenarioLatex + '\n' + '\\end{enumerate}'
                            strTextoLatex = strTextoLatex + '\n' + strTextoCenarioLatex
                        strTextoLatex = strTextoLatex + '\n'
                # Ao final do For incrementa numRow
                numRow = numRow + 1

            # Salva no arquivo
            with open(strExportLatexFullFilename, 'w') as fileLatex:
                fileLatex.write(strTextoLatex)
            printL('Arquivo "{}" gerado e salvo com sucesso!'.format(strExportLatexFullFilename))

    def comutaFlagExportLatex(self):
        if self.tvEditor.booExisteFeatureAberta:
            tvTree = self.tvTreeCenarios
            lsList = tvTree.props.model
            path = self.tvTreeCenarios.numRowCenarioAtivo
            treeiter = lsList.get_iter(path)
            strExport = lsList.get_value(treeiter, 3)
            if strExport == 'Sim':
                lsList[path][3] = 'Não'
                lsList[path][4] = 'cyan'
                self.dictTbCenarioLinhas[int(lsList[path][2])] = 'Não'
            else:
                lsList[path][3] = 'Sim'
                lsList[path][4] = 'lime'
                self.dictTbCenarioLinhas[int(lsList[path][2])] = 'Sim'
            numLinhaTotal, bufLinhas = self.tvLinhas_VerificaAtualizaLinhas()
            self.tvLinhas_atualizarFormatos(numLinhaTotal, bufLinhas)

    def criaStrLatexTabela(self,numListTextoCenario,listTextoCenario):
        def retStrRowColor(nL):
            if nL == 1:
                return '\\rowcolor{blue!40} '
            else:
                if nL % 2 == 0:
                    return '\\rowcolor{blue!10} '
                else:
                    return '\\rowcolor{blue!20} '

        strLinhaAtual = listTextoCenario[numListTextoCenario].strip()
        if '|' in strLinhaAtual:
            # Limite Anterior é a primeira ocorrencia de |
            numLinhaAnterior = numListTextoCenario

            # Limite Posterior
            numLinhaTotal = len(listTextoCenario) - 1
            numLinhaPosterior = numLinhaAnterior
            booTemPipe = True
            while (numLinhaPosterior != numLinhaTotal) and booTemPipe:
                numLinhaPosterior = numLinhaPosterior + 1
                strAux = listTextoCenario[numLinhaPosterior].strip()
                booTemPipe = '|' in strAux
            numLinhaPosterior = numLinhaPosterior - 1

            # Validação: Número de Pipes por Linha deve ser igual
            booValido = True
            countPipe = strLinhaAtual.count('|')
            for numL in range(numLinhaAnterior,numLinhaPosterior+1):
                strAux = listTextoCenario[numL].strip()
                if countPipe != strAux.count('|'):
                    booValido = False
                    break

            if booValido:
                # print('Formato Válido')
                numTotalLinhas = numLinhaPosterior - numLinhaAnterior + 1
                numTotalColunas = countPipe - 1

                # Cria tabelas auxiliares
                tabStrInput = tS.tabelaString(numTotalLinhas,numTotalColunas)
                tabStrOutput = tS.tabelaString(numTotalLinhas,numTotalColunas)

                numL = 0
                for numLinha in range(numLinhaAnterior,numLinhaPosterior+1):
                    numL = numL + 1
                    strLinha = listTextoCenario[numLinha]
                    strLinha = strLinha.strip()
                    listSep = strLinha.split('|') # Se a string for assim: | Algo | Outro | Fechou | o split vai trazer um '' antes e depois

                    for numC, strSep in enumerate(listSep):
                        # Despreza o primeiro e o último
                        if numC != 0:
                            if numC != len(listSep) - 1:
                                # Por coincidencia numC já é o numC da tabela
                                tabStrInput.putGood(numL, numC,strSep)
                # Objeto tabStrInput contém os dados da tabela
                # tabStrInput.show()

                # Agora é gerar a tabela tabStrOutput que será impressa com os tabs

                # Primeiro preciso contar quantos tabs tem no inicio da primeira linha
                strLinhaPrimeira = listTextoCenario[numLinhaAnterior]
                numCountFirstTabs = 0
                if len(strLinhaPrimeira) >= 1:
                    if strLinhaPrimeira[0] == '\t':
                        numCountFirstTabs = len(strLinhaPrimeira)
                        for numChar in range(1,len(strLinhaPrimeira)):
                            if strLinhaPrimeira[numChar] != '\t':
                                numCountFirstTabs = numChar
                                break

                # Vou percorrer a tabStrInput e gerar a tabStrOutput onde vou formatar operadores Latex
                # Gera tabStrOutput
                for nL in range(1,numTotalLinhas + 1):
                    for nC in range(1,numTotalColunas + 1):
                        strInput = tabStrInput.get(nL,nC)
                        strOutput = self.formataLatex(strInput)
                        tabStrOutput.put(nL,nC,strOutput)

                # Agora com a tabStrOutput gerar a String que será inserida no lugar do texto atual
                # Primeiro, cria o recheio da tabela, ou seja, as linhas da tabela
                strLatexTabelaLinhas = ''
                numMaxStrLinhaLength = 0
                for nL in range(1,numTotalLinhas + 1):
                    # Cria Nova Linha
                    strNovaLinha = ''
                    if numTotalColunas > 1:
                        for nC in range(1,numTotalColunas + 1):
                            if nC == 1:
                                strNovaLinha = retStrRowColor(nL) + tabStrOutput.get(nL,nC)
                            elif nC == numTotalColunas:
                                strNovaLinha = strNovaLinha + ' & ' + tabStrOutput.get(nL,nC) + ' \\\\ \\hline'
                            else:
                                strNovaLinha = strNovaLinha + ' & ' + tabStrOutput.get(nL,nC)
                    else:
                        strNovaLinha = retStrRowColor(nL) + tabStrOutput.get(nL,nC) + ' \\\\ \\hline'
                    # Insere Linha
                    strLatexTabelaLinhas = strLatexTabelaLinhas + '\t\t\t' + strNovaLinha + '\n'
                    # E atualiza numMaxStrLinhaLength para usar depois
                    if numMaxStrLinhaLength < len(strNovaLinha):
                        numMaxStrLinhaLength = len(strNovaLinha)

                # Ao final cria todo o strLatexTabela

                # HEADER
                strLatexTabela = '\n' # Linha em branco antes
                booAjuste = (numMaxStrLinhaLength > 80) or (numTotalColunas > 1) # Condição para aplicar ajuste
                if booAjuste:
                    strLatexTabela = strLatexTabela + '\t\t\\begin{adjustbox}{width=1\\linewidth}' + '\n'
                strLatexTabela = strLatexTabela + '\t\t\\begin{tabular}{|' + 'l|'*numTotalColunas + '}' + '\n'
                strLatexTabela = strLatexTabela + '\t\t\t' + '\hline'  + '\n' # Primeira \hline que sempre precisa ter

                # CONTEUDO
                strLatexTabela = strLatexTabela +  strLatexTabelaLinhas

                # FECHAMENTOS
                strLatexTabela = strLatexTabela + '\t\t\\end{tabular}'
                if booAjuste:
                    strLatexTabela = strLatexTabela + '\n' + '\t\t\\end{adjustbox}'
                strLatexTabela = strLatexTabela + '\n' # Linha em branco depois

                return True, strLatexTabela, numLinhaPosterior
            else:
                print('Formato Inválido - Número de | diverge')
                return False, '', numListTextoCenario
        else:
            print('Não encontrou |')
            return False, '', numListTextoCenario

    def formataTabela(self):
        buf = self.tvEditor.get_buffer()
        numLinhaAtual = self.getLinhaAtual(buf)
        strLinhaAtual = self.getTextFromLine(buf,numLinhaAtual)
        if '|' in strLinhaAtual:
            # Passou na primeira condição
            # Agora quero ver limites
            numLinhaTotal = buf.get_line_count()

            # Limite Anterior
            numLinhaAnterior = numLinhaAtual
            booTemPipe = True
            while (numLinhaAnterior != -1) and booTemPipe:
                numLinhaAnterior = numLinhaAnterior - 1
                strAux = self.getTextFromLine(buf,numLinhaAnterior)
                booTemPipe = '|' in strAux
            numLinhaAnterior = numLinhaAnterior + 1

            # Limite Posterior
            numLinhaPosterior = numLinhaAtual
            booTemPipe = True
            while (numLinhaPosterior != numLinhaTotal) and booTemPipe:
                numLinhaPosterior = numLinhaPosterior + 1
                strAux = self.getTextFromLine(buf,numLinhaPosterior)
                booTemPipe = '|' in strAux
            numLinhaPosterior = numLinhaPosterior - 1


            # Validação: Número de Pipes por Linha deve ser igual
            booValido = True
            countPipe = strLinhaAtual.count('|')
            for numL in range(numLinhaAnterior,numLinhaPosterior+1):
                strAux = self.getTextFromLine(buf,numL)
                if countPipe != strAux.count('|'):
                    booValido = False
                    break

            if booValido:
                # print('Formato Válido')
                numTotalLinhas = numLinhaPosterior - numLinhaAnterior + 1
                numTotalColunas = countPipe - 1

                # Cria tabelas auxiliares
                tabStrInput = tS.tabelaString(numTotalLinhas,numTotalColunas)
                tabStrOutput = tS.tabelaString(numTotalLinhas,numTotalColunas)
                tabStrTeste = tS.tabelaString(numTotalLinhas,numTotalColunas)

                numL = 0
                for numLinha in range(numLinhaAnterior,numLinhaPosterior+1):
                    numL = numL + 1
                    strLinha = self.getTextFromLine(buf,numLinha)
                    strLinha = strLinha.strip()
                    listSep = strLinha.split('|') # Se a string for assim: | Algo | Outro | Fechou | o split vai trazer um '' antes e depois

                    for numC, strSep in enumerate(listSep):
                        # Despreza o primeiro e o último
                        if numC != 0:
                            if numC != len(listSep) - 1:
                                # Por coincidencia numC já é o numC da tabela
                                tabStrInput.putGood(numL, numC,strSep)
                # Objeto tabStrInput contém os dados da tabela
                # tabStrInput.show()

                # Agora é gerar a tabela tabStrOutput que será impressa com os tabs

                # Primeiro preciso contar quantos tabs tem no inicio da primeira linha
                strLinhaPrimeira = self.getTextFromLine(buf,numLinhaAnterior)
                numCountFirstTabs = 0
                if len(strLinhaPrimeira) >= 1:
                    if strLinhaPrimeira[0] == '\t':
                        numCountFirstTabs = len(strLinhaPrimeira)
                        for numChar in range(1,len(strLinhaPrimeira)):
                            if strLinhaPrimeira[numChar] != '\t':
                                numCountFirstTabs = numChar
                                break

                # Vou percorrer a tabStrInput e gerar a tabStrOutput
                # Variáveis Iniciais
                numCharPorTab = 4
                numOffSetTabAntes = 1
                numOffSetTabDepois = 1
                # Gera tabStrOutput
                for nL in range(1,numTotalLinhas + 1):
                    for nC in range(1,numTotalColunas + 1):
                        strInput = tabStrInput.get(nL,nC)
                        numLen = len(strInput)
                        numMaxLen = tabStrInput.getColProp(nC,'maxlen')
                        numTabTotal = round(self.proxMultiploDeM(numMaxLen,numCharPorTab) / numCharPorTab)
                        numTabToInsert = numTabTotal - (numLen // numCharPorTab)
                        strOutput = numOffSetTabAntes*'\t' + strInput + numTabToInsert*'\t' + numOffSetTabDepois*'\t'
                        tabStrOutput.put(nL,nC,strOutput)
                        tabStrTeste.put(nL,nC,str(numTabToInsert))

                # Agora com a tabStrOutput gerar a String que será inserida no lugar do texto atual
                strNovaTabela = ''
                for nL in range(1,numTotalLinhas + 1):
                    # Cria Nova Linha
                    strNovaLinha = ''
                    for nC in range(1,numTotalColunas + 1):
                        if nC == 1:
                            strNovaLinha = numCountFirstTabs*'\t'
                        strNovaLinha = strNovaLinha + '|' + tabStrOutput.get(nL,nC)
                        if nC == numTotalColunas:
                            strNovaLinha = strNovaLinha + '|'
                    # Insere Linha
                    if nL != numTotalLinhas:
                        strNovaTabela = strNovaTabela + strNovaLinha + '\n'
                    else:
                        strNovaTabela = strNovaTabela + strNovaLinha

                # Finalmente vou deletar a tabela existente e inserir a nova tabela no lugar
                iterLineStart = buf.get_iter_at_line(numLinhaAnterior)
                strLinhaUltima = self.getTextFromLine(buf,numLinhaPosterior)
                iterLineEnd = buf.get_iter_at_line(numLinhaPosterior)
                iterLineEnd.forward_chars(len(strLinhaUltima))
                buf.delete(iterLineStart,iterLineEnd)
                # Deixa uma linha entre ambos no qual vai colocar a tabela
                m = buf.get_insert()
                iterNovaTabela = buf.get_iter_at_mark(m)
                # Insere Nova Tabela
                buf.insert(iterNovaTabela,strNovaTabela,-1)
                # Formata novamente cada linha de acordo com as tags
                for numLinha in range(numLinhaAnterior,numLinhaPosterior+1):
                    self.formataLinha(buf, numLinha)
                # print('')
                # print('Tab Teste')
                # tabStrTeste.show()
            else:
                print('Formato Inválido - Número de | diverge')
        else:
            print('Não encontrou |')

    def proxMultiploDeM(self,N,M):
        if N % M == 0:
            return N
        else:
            return N + (M - N % M)

    def getLinhaAtual(self,buf):
        # Linha Atual
        m = buf.get_insert()
        i = buf.get_iter_at_mark(m)
        return i.get_line()

    def getTextFromLine(self,buf,numLinha):
        numLinhaTotal = buf.get_line_count()
        iterLineStart = buf.get_iter_at_line(numLinha)
        if ((numLinha + 1) != numLinhaTotal):
            iterLineEnd = buf.get_iter_at_line(numLinha+1)
            iterLineEnd.backward_char()
        else:
            iterLineEnd = buf.get_end_iter()
        strLinhaTexto = buf.get_text(iterLineStart,iterLineEnd,False)
        return strLinhaTexto

    def atualizarTvEditor(self):
        textbuffer = self.tvEditor.get_buffer()
        numLinhaTotal = textbuffer.get_line_count()

        # Formata cada linha de acordo com as tags
        for numLinhaAtual in range(0,numLinhaTotal):
            self.formataLinha(textbuffer, numLinhaAtual)

    def atualizarTvLinhas(self):
        numLinhaTotal, bufLinhas = self.tvLinhas_escreverLinhas()
        self.tvLinhas_atualizarFormatos(numLinhaTotal, bufLinhas)

    def tvLinhas_escreverLinhas(self):
        textbuffer = self.tvEditor.get_buffer()
        numLinhaTotal = textbuffer.get_line_count()

        # Gera Linhas para tvLinhas
        strTextoLinhas = '1'
        for numLinhaAtual in range(0,numLinhaTotal - 1):
            strTextoLinhas = strTextoLinhas + '\n{}'.format(numLinhaAtual+2)

        bufLinhas = self.tvLinhas.get_buffer()
        bufLinhas.set_text(strTextoLinhas)

        # Coloca no Centro
        self.tvLinhas.set_justification(Gtk.Justification.CENTER)
        return numLinhaTotal, bufLinhas

    def tvLinhas_atualizarFormatos(self,numLinhaTotal, bufLinhas):
        for numLinhaAtual in range(0,numLinhaTotal):
            self.formataTvLinhas(bufLinhas, numLinhaAtual)

    def tvLinhas_VerificaAtualizaLinhas(self):
        textbuffer = self.tvEditor.get_buffer()
        numLinhaTotalTvEditor = textbuffer.get_line_count()

        bufLinhas = self.tvLinhas.get_buffer()
        numLinhaTotalTvLinhas = bufLinhas.get_line_count()

        if numLinhaTotalTvLinhas > numLinhaTotalTvEditor:
            # Preciso remover linhas de tvLinhas
            iterStart = bufLinhas.get_iter_at_line(numLinhaTotalTvEditor)
            iterStart.backward_char()
            iterEnd = bufLinhas.get_end_iter()
            bufLinhas.delete(iterStart,iterEnd)
        elif numLinhaTotalTvLinhas < numLinhaTotalTvEditor:
            # Preciso adicionar linhas de tvLinhas
            for numLinhaAtual in range(numLinhaTotalTvLinhas,numLinhaTotalTvEditor):
                iterStart = bufLinhas.get_end_iter()
                strTextoLinha = '\n{}'.format(numLinhaAtual+1)
                bufLinhas.insert(iterStart,strTextoLinha,-1)

        return numLinhaTotalTvEditor, bufLinhas

    def atualizarLinha(self,textbuffer):
        # Buffer Alvo
        buf = textbuffer
        # print("")
        iterStart = buf.get_start_iter()
        iterEnd = buf.get_end_iter()

        # Linha Atual
        m = buf.get_insert()
        i = buf.get_iter_at_mark(m)
        numLinhaAtual = i.get_line()
        # print("Linha Atual = {}".format(numLinhaAtual))
        self.formataLinha(textbuffer,numLinhaAtual)

    def retListSepListInd(self,strSource):
        def tupleAdd(t1,t2):
            return (t1[0],t2[1])

        listPossiveis = ['**','*"','"*']
        strRegex = '\w+|[^\w\s]'

        listSepAux = nltk.tokenize.RegexpTokenizer(strRegex).tokenize(strSource)
        listIndAux = list(nltk.tokenize.RegexpTokenizer(strRegex).span_tokenize(strSource))

        if len(listSepAux) >= 2:
            listSep = []
            listInd = []

            strToAdd = listSepAux[0]
            tupToAdd = listIndAux[0]
            strAtual = listSepAux[0]
            tupAtual = listIndAux[0]

            strNova =  strAtual + listSepAux[1]
            for i in range(0,len(listSepAux)-1):
                strNova =  strAtual + listSepAux[i+1]
                if strNova in listPossiveis:
                    strToAdd = strToAdd + listSepAux[i+1]
                    tupToAdd = tupleAdd(tupToAdd,listIndAux[i+1])
                else:
                    listSep.append(strToAdd)
                    listInd.append(tupToAdd)
                    strToAdd = listSepAux[i+1]
                    tupToAdd = listIndAux[i+1]
                    strAtual = listSepAux[i+1]
            # Último
            if strNova in listPossiveis:
                listSep.append(strToAdd)
                listInd.append(tupToAdd)
            else:
                listSep.append(listSepAux[len(listSepAux)-1])
                listInd.append(listIndAux[len(listIndAux)-1])

            return listSep, listInd
        else:
            return listSepAux, listIndAux

    def escapaLatex(self,strSource):
        strRet = strSource
        strRet = strRet.replace('#','\#')
        strRet = strRet.replace('$','\$')
        strRet = strRet.replace('"','')
        strRet = strRet.replace("'",'')
        strRet = strRet.replace("_",'\_')
        return strRet

    def formataLatex(self,strSource):
        strRet = strSource
        listSep, listInd = self.retListSepListInd(strSource)
        # *****************************************
        # Keywords = aplicaTagEmKeyword
        # *****************************************
        for strOperador in self.dictLatexTagKeyword:
            for strPalavra in listSep:
                strUnidecode = unidecode(strPalavra).lower()
                if strOperador == strUnidecode:
                    strRet = self.insereLatexEmKeyword(strOperador,strRet,strPalavra)

        # *****************************************
        # Operadores
        # *****************************************
        # Operadores Duplos = aplicaTagEmOperadores
        for strOperador in self.dictLatexTagOpDuplos:
            strRet = self.insereLatexEmOperadoresDuplos(strOperador,strRet)



        # Operadores Iguais = aplicaTagEmOperadores
        for strOperador in self.dictLatexTagOpIguais:
            strRet = self.insereLatexEmOperadoresIguais(strOperador,strRet)

        # *****************************************
        # Pintam da tag até o fim = aplicaTagFromToEnd
        # *****************************************
        for strOperador in self.dictLatexTagFromToEnd:
            strRet = self.insereLatexFromToEnd(strOperador,strRet)

        # *****************************************
        # Tags que pintam somente a palavra na frente = aplicaTagWordOnly
        # *****************************************


        # *****************************************
        # Tags que Pintam a Linha Toda
        # *****************************************


        # *****************************************
        # Escapa tags especiais para o Latex
        # *****************************************
        strRet = self.escapaLatex(strRet)

        return strRet

    def formataLinha(self,textbuffer,numLinha):
        buf = textbuffer

        # Total de Linhas e Posicao do Cursor
        numLinhaTotal = buf.get_line_count()
        numPosCursor = buf.props.cursor_position
        # print("Total de Linhas = {}".format(numLinhaTotal))
        # print("Pos Cursor = {}".format(numPosCursor))

        # Texto da Linha Atual
        #https://lazka.github.io/pgi-docs/Gtk-3.0/classes/TextIter.html#Gtk.TextIter
        iterLineStart = buf.get_iter_at_line(numLinha)
        if ((numLinha + 1) != numLinhaTotal):
            iterLineEnd = buf.get_iter_at_line(numLinha+1)
            iterLineEnd.backward_char()
        else:
            iterLineEnd = buf.get_end_iter()
        strLinhaTexto = buf.get_text(iterLineStart,iterLineEnd,False)
        # print("Texto da Linha = '{}'".format(strLinhaTexto))

        # *****************************************
        # Operações com o texto da Linha
        # *****************************************
        # https://www.nltk.org/api/nltk.tokenize.html
        #listSep = WordPunctTokenizer().tokenize(strLinhaTexto)
        # print(listSep)
        #listInd = list(WordPunctTokenizer().span_tokenize(strLinhaTexto))
        # print(listInd)
        listSep, listInd = self.retListSepListInd(strLinhaTexto)

        # Remove todas as tags sempre e depois eu refaço
        buf.remove_all_tags(iterLineStart, iterLineEnd)

        # *****************************************
        # Keywords
        # *****************************************
        for strTag in self.listTagKeyword:
            for strPalavra in listSep:
                strUnidecode = unidecode(strPalavra).lower()
                if strTag == strUnidecode:
                    self.aplicaTagEmKeyword(self.dictTag[strTag],strPalavra,strLinhaTexto,numLinha,textbuffer)

        # *****************************************
        # Operadores
        # *****************************************
        # Operadores Duplos
        self.aplicaTagEmOperadorDuplo(self.dictTag['bold'],'**"','"**',strLinhaTexto,numLinha,textbuffer)
        self.aplicaTagEmOperadorDuplo(self.dictTag['bold'],"**'","'**",strLinhaTexto,numLinha,textbuffer)
        self.aplicaTagEmOperadorDuplo(self.dictTag['bold'],'*"','"*',strLinhaTexto,numLinha,textbuffer)
        self.aplicaTagEmOperadorDuplo(self.dictTag['bold'],"*'","'*",strLinhaTexto,numLinha,textbuffer)
        self.aplicaTagEmOperadorDuplo(self.dictTag['parametro'],'<','>',strLinhaTexto,numLinha,textbuffer)
        self.aplicaTagEmOperadorDuplo(self.dictTag['parametro'],'<','>:',strLinhaTexto,numLinha,textbuffer)

        # Operadores Iguais
        self.aplicaTagEmOperadores(self.dictTag['bold'],'**',strLinhaTexto,numLinha,textbuffer)
        self.aplicaTagEmOperadores(self.dictTag['italic'],'--',strLinhaTexto,numLinha,textbuffer)
        self.aplicaTagEmOperadores(self.dictTag['strike'],'~~',strLinhaTexto,numLinha,textbuffer)
        self.aplicaTagEmOperadores(self.dictTag['underline'],'__',strLinhaTexto,numLinha,textbuffer)
        self.aplicaTagEmOperadores(self.dictTag['string'],'"',strLinhaTexto,numLinha,textbuffer)
        self.aplicaTagEmOperadores(self.dictTag['string'],"'",strLinhaTexto,numLinha,textbuffer)
        self.aplicaTagEmOperadores(self.dictTag['$'],"$",strLinhaTexto,numLinha,textbuffer)


        # *****************************************
        # Pintam da tag até o fim
        # *****************************************
        for strTag in self.listTagFromToEnd:
            self.aplicaTagFromToEnd(self.dictTag[strTag],strTag,strLinhaTexto,numLinha,iterLineEnd,textbuffer)


        # *****************************************
        # Tags que pintam somente a palavra na frente
        # *****************************************
        for strTag in self.listTagWordOnly:
            self.aplicaTagWordOnly(self.dictTag[strTag],strTag,strLinhaTexto,numLinha,textbuffer)

        # *****************************************
        # Tags que Pintam a Linha Toda
        # *****************************************
        for strTag in self.listTagLine:
            for strPalavra in listSep:
                strUnidecode = unidecode(strPalavra).lower()
                if strTag == strUnidecode:
                    buf.apply_tag(self.dictTag[strTag], iterLineStart, iterLineEnd)


        # *****************************************
        # Pinta tabs
        # *****************************************
        self.pintaTabsInicio(strLinhaTexto,numLinha,textbuffer)

        # *****************************************
        # Linha Atual
        # *****************************************

        # Linha Atual
        m = buf.get_insert()
        i = buf.get_iter_at_mark(m)
        numLinhaAtual = i.get_line()
        if numLinha == numLinhaAtual:
            self.pintaLinhaAtual(iterLineStart,iterLineEnd,textbuffer)

    def aplicaTagWordOnly(self,tag,strOperador,strLinhaTexto,numLinhaAtual,textbuffer):
        buf = textbuffer
        #listSep = WordPunctTokenizer().tokenize(strLinhaTexto)
        #listInd = list(WordPunctTokenizer().span_tokenize(strLinhaTexto))
        listSep, listInd = self.retListSepListInd(strLinhaTexto)

        # https://stackoverflow.com/questions/176918/finding-the-index-of-an-item-in-a-list
        listOperador = [i for i, j in enumerate(listSep) if j == strOperador]
        #listOperador contem os indices de quando @ aparece

        # print(listSep)
        # print(listInd)
        # print(listOperador)

        # Preciso transformar em pares de indices @ e próxima palavra se houver
        llPares = []
        for i in listOperador:
            if i + 1 != len(listSep):
                llPares.append([i,i+1])
        # print(llPares)

        #Agora vou de par em par para fazer o apply tag
        # listPar[0] contem o indice da esquerda
        # listPar[1] contem o indice da direita
        for listPar in llPares:
            # Esses abaixo incluem os operadores
            numCharStart = listInd[listPar[0]][0]
            numCharEnd = listInd[listPar[1]][1]
            # Esses abaixo não incluem os operadores
            #numCharStart = listInd[listPar[0]][1]
            #numCharEnd = listInd[listPar[1]][0]
            # Agora preciso descobrir como pegar iter no char
            # print('Vai de {} até {}'.format(numCharStart,numCharEnd))
            iterPosStart = buf.get_iter_at_line(numLinhaAtual)
            # print("1")
            # print(iterPosStart.get_char())
            iterPosStart.forward_chars(numCharStart)
            # print("2")
            # print(iterPosStart.get_char())
            iterPosEnd = buf.get_iter_at_line(numLinhaAtual)
            # print("3")
            # print(iterPosEnd.get_char())
            iterPosEnd.forward_chars(numCharEnd)
            # print("4")
            # print(iterPosEnd.get_char())
            # Finalmente aplica a tag
            buf.apply_tag(tag, iterPosStart, iterPosEnd)

    def aplicaTagFromToEnd(self,tag,strTag,strLinhaTexto,numLinhaAtual,iterLineEnd,textbuffer):
        buf = textbuffer
        #listSep = WordPunctTokenizer().tokenize(strLinhaTexto)
        #listInd = list(WordPunctTokenizer().span_tokenize(strLinhaTexto))
        listSep, listInd = self.retListSepListInd(strLinhaTexto)

        index = 0
        for palavra in listSep:
            if palavra == strTag:
                # Inicio
                numCharStart = listInd[index][0]
                iterPosStart = buf.get_iter_at_line(numLinhaAtual)
                iterPosStart.forward_chars(numCharStart)
                # Aplica a tag
                buf.apply_tag(tag, iterPosStart, iterLineEnd)
                break # Para porque basta o primeiro. Se tiver mais, não precisa pintar novamente.
            # Incrementa contador de índice
            index = index + 1

    def insereLatexFromToEnd(self,strOperador,strLinhaTexto):
        def stringInsertPos(source_str, insert_str, pos):
            return source_str[:pos]+insert_str+source_str[pos:], len(insert_str)
        strRet = strLinhaTexto
        # listSep = WordPunctTokenizer().tokenize(strLinhaTexto)
        # listInd = list(WordPunctTokenizer().span_tokenize(strLinhaTexto))
        listSep, listInd = self.retListSepListInd(strLinhaTexto)

        index = 0
        offSet = 0
        for palavra in listSep:
            if palavra == strOperador:
                # Inicio
                numCharStart = listInd[index][0]
                # Insere
                strRet, numLen = stringInsertPos(strRet,self.dictLatexTagFromToEnd[strOperador],numCharStart + offSet)
                offSet = offSet + numLen
                # Final é o final da linha
                strRet = strRet + '}}'
                break # Para porque basta o primeiro. Se tiver mais, não precisa pintar novamente.
            # Incrementa contador de índice
            index = index + 1
        return strRet

    def aplicaTagEmKeyword(self,tag,strKeyword,strLinhaTexto,numLinhaAtual,textbuffer):
        buf = textbuffer
        # listSep = WordPunctTokenizer().tokenize(strLinhaTexto)
        # listInd = list(WordPunctTokenizer().span_tokenize(strLinhaTexto))
        listSep, listInd = self.retListSepListInd(strLinhaTexto)

        index = 0
        for palavra in listSep:
            if palavra == strKeyword:
                # Inicio
                numCharStart = listInd[index][0]
                iterPosStart = buf.get_iter_at_line(numLinhaAtual)
                iterPosStart.forward_chars(numCharStart)
                # Final
                numCharEnd = listInd[index][1]
                iterPosEnd = buf.get_iter_at_line(numLinhaAtual)
                iterPosEnd.forward_chars(numCharEnd)
                # Aplica a tag
                buf.apply_tag(tag, iterPosStart, iterPosEnd)
            # Incrementa contador de índice
            index = index + 1

    def insereLatexEmKeyword(self,strOperador,strLinhaTexto,strKeyword):
        def stringInsertPos(source_str, insert_str, pos):
            return source_str[:pos]+insert_str+source_str[pos:], len(insert_str)

        strRet = strLinhaTexto
        # listSep = WordPunctTokenizer().tokenize(strLinhaTexto)
        # listInd = list(WordPunctTokenizer().span_tokenize(strLinhaTexto))
        listSep, listInd = self.retListSepListInd(strLinhaTexto)

        index = 0
        offSet = 0
        for palavra in listSep:
            if palavra == strKeyword:
                # Inicio
                numCharStart = listInd[index][0]
                numCharEnd = listInd[index][1]

                strRet, numLen = stringInsertPos(strRet,self.dictLatexTagKeyword[strOperador],numCharStart + offSet)
                offSet = offSet + numLen

                strRet, numLen = stringInsertPos(strRet,'}}',numCharEnd + offSet)
                offSet = offSet + numLen
            # Incrementa contador de índice
            index = index + 1

        return strRet

    def aplicaTagEmOperadores(self,tag,strOperador,strLinhaTexto,numLinhaAtual,textbuffer):
        buf = textbuffer
        # listSep = WordPunctTokenizer().tokenize(strLinhaTexto)
        # listInd = list(WordPunctTokenizer().span_tokenize(strLinhaTexto))
        listSep, listInd = self.retListSepListInd(strLinhaTexto)

        # https://stackoverflow.com/questions/176918/finding-the-index-of-an-item-in-a-list
        listOperador = [i for i, j in enumerate(listSep) if j == strOperador]
        #listOperador contem os indices de quando ** aparece
        # Preciso transformar em pares de indices
        llPares = []
        index = 0
        for i in listOperador:
            index = index + 1
            if (index % 2 == 0):
                llPares.append([listOperador[index-2],listOperador[index-1]])
        #Agora vou de par em par para fazer o apply tag
        # listPar[0] contem o indice da esquerda
        # listPar[1] contem o indice da direita
        for listPar in llPares:
            # Esses abaixo incluem os operadores
            numCharStart = listInd[listPar[0]][0]
            numCharEnd = listInd[listPar[1]][1]
            # Esses abaixo não incluem os operadores
            #numCharStart = listInd[listPar[0]][1]
            #numCharEnd = listInd[listPar[1]][0]
            # Agora preciso descobrir como pegar iter no char
            # print('Vai de {} até {}'.format(numCharStart,numCharEnd))
            iterPosStart = buf.get_iter_at_line(numLinhaAtual)
            # print("1")
            # print(iterPosStart.get_char())
            iterPosStart.forward_chars(numCharStart)
            # print("2")
            # print(iterPosStart.get_char())
            iterPosEnd = buf.get_iter_at_line(numLinhaAtual)
            # print("3")
            # print(iterPosEnd.get_char())
            iterPosEnd.forward_chars(numCharEnd)
            # print("4")
            # print(iterPosEnd.get_char())
            # Finalmente aplica a tag
            buf.apply_tag(tag, iterPosStart, iterPosEnd)

    def insereLatexEmOperadoresIguais(self,strOperador,strLinhaTexto):
        def stringInsertPos(source_str, insert_str, pos):
            return source_str[:pos]+insert_str+source_str[pos:], len(insert_str)

        strRet = strLinhaTexto
        # listSep = WordPunctTokenizer().tokenize(strLinhaTexto)
        # listInd = list(WordPunctTokenizer().span_tokenize(strLinhaTexto))
        listSep, listInd = self.retListSepListInd(strLinhaTexto)

        listOperador = [i for i, j in enumerate(listSep) if j == strOperador]
        llPares = []
        index = 0
        for i in listOperador:
            index = index + 1
            if (index % 2 == 0):
                llPares.append([listOperador[index-2],listOperador[index-1]])

        offSet = 0
        for listPar in llPares:
            # Esses abaixo incluem os operadores
            numCharStart = listInd[listPar[0]][0]
            numCharEnd = listInd[listPar[1]][1]

            # Esses abaixo não incluem os operadores
            #numCharStart = listInd[listPar[0]][1]
            #numCharEnd = listInd[listPar[1]][0]

            strRet, numLen = stringInsertPos(strRet,self.dictLatexTagOpIguais[strOperador],numCharStart + offSet)
            offSet = offSet + numLen

            strRet, numLen = stringInsertPos(strRet,'}',numCharEnd + offSet)
            offSet = offSet + numLen

        return strRet

    def aplicaTagEmOperadorDuplo(self,tag,strOperadorInicio,strOperadorFinal,strLinhaTexto,numLinhaAtual,textbuffer):
        buf = textbuffer
        # listSep = WordPunctTokenizer().tokenize(strLinhaTexto)
        # listInd = list(WordPunctTokenizer().span_tokenize(strLinhaTexto))
        listSep, listInd = self.retListSepListInd(strLinhaTexto)

        # https://stackoverflow.com/questions/176918/finding-the-index-of-an-item-in-a-list
        listOperador = [i for i, j in enumerate(listSep) if j == strOperadorInicio or j == strOperadorFinal]
        #listOperador contem os indices de quando ** aparece

        # Pega aos pares pois vou considerar que toda vez que abre deve fechar
        llPares = []
        index = 0
        for i in listOperador:
            index = index + 1
            if (index % 2 == 0):
                llPares.append([listOperador[index-2],listOperador[index-1]])

        #Agora vou de par em par para fazer o apply tag
        # listPar[0] contem o indice da esquerda
        # listPar[1] contem o indice da direita
        for listPar in llPares:
            # Esses abaixo incluem os operadores
            numCharStart = listInd[listPar[0]][0]
            numCharEnd = listInd[listPar[1]][1]
            # Esses abaixo não incluem os operadores
            #numCharStart = listInd[listPar[0]][1]
            #numCharEnd = listInd[listPar[1]][0]
            # Agora preciso descobrir como pegar iter no char
            # print('Vai de {} até {}'.format(numCharStart,numCharEnd))
            iterPosStart = buf.get_iter_at_line(numLinhaAtual)
            # print("1")
            # print(iterPosStart.get_char())
            iterPosStart.forward_chars(numCharStart)
            # print("2")
            # print(iterPosStart.get_char())
            iterPosEnd = buf.get_iter_at_line(numLinhaAtual)
            # print("3")
            # print(iterPosEnd.get_char())
            iterPosEnd.forward_chars(numCharEnd)
            # print("4")
            # print(iterPosEnd.get_char())
            # Finalmente aplica a tag
            buf.apply_tag(tag, iterPosStart, iterPosEnd)

    def insereLatexEmOperadoresDuplos(self,strOperadorInicio,strLinhaTexto):
        def stringInsertPos(source_str, insert_str, pos):
            return source_str[:pos]+insert_str+source_str[pos:], len(insert_str)
        # Vou reverter o operador aqui dentro mesmo
        if strOperadorInicio == '<':
            strOperadorFinal = '>'
        else:
            strOperadorFinal = strOperadorInicio[::-1]

        strRet = strLinhaTexto
        # listSep = WordPunctTokenizer().tokenize(strLinhaTexto)
        # listInd = list(WordPunctTokenizer().span_tokenize(strLinhaTexto))
        listSep, listInd = self.retListSepListInd(strLinhaTexto)

        listOperador = [i for i, j in enumerate(listSep) if j == strOperadorInicio or j == strOperadorFinal]
        llPares = []
        index = 0
        for i in listOperador:
            index = index + 1
            if (index % 2 == 0):
                llPares.append([listOperador[index-2],listOperador[index-1]])

        offSet = 0
        for listPar in llPares:
            # Esses abaixo incluem os operadores
            numCharStart = listInd[listPar[0]][0]
            numCharEnd = listInd[listPar[1]][1]

            # Esses abaixo não incluem os operadores
            #numCharStart = listInd[listPar[0]][1]
            #numCharEnd = listInd[listPar[1]][0]

            strRet, numLen = stringInsertPos(strRet,self.dictLatexTagOpDuplos[strOperadorInicio],numCharStart + offSet)
            offSet = offSet + numLen

            strRet, numLen = stringInsertPos(strRet,'}}',numCharEnd + offSet)
            offSet = offSet + numLen
        return strRet

    def pintaTabsInicio(self,strLinhaTexto,numLinhaAtual,textbuffer):
        # Procura por cadeias de tabs
        if len(strLinhaTexto) >= 1:
            if strLinhaTexto[0] == '\t':
                numPosFinal = len(strLinhaTexto)
                for numChar in range(1,len(strLinhaTexto)):
                    if strLinhaTexto[numChar] != '\t':
                        numPosFinal = numChar
                        break
                # Pinta
                buf = textbuffer
                iterPosStart = buf.get_iter_at_line(numLinhaAtual)
                iterPosEnd = buf.get_iter_at_line(numLinhaAtual)
                iterPosEnd.forward_chars(numPosFinal)
                buf.apply_tag(self.dictTag['tab'], iterPosStart, iterPosEnd)

    def pintaLinhaAtual(self,iterPosStart,iterPosEnd,textbuffer):
        pass
        # buf = textbuffer
        # buf.apply_tag(self.dictTag['linha'], iterPosStart, iterPosEnd)





    def formataTvLinhas(self,textbuffer,numLinha):
        buf = textbuffer

        # Total de Linhas
        numLinhaTotal = buf.get_line_count()

        # Texto da Linha Atual
        iterLineStart = buf.get_iter_at_line(numLinha)
        if ((numLinha + 1) != numLinhaTotal):
            iterLineEnd = buf.get_iter_at_line(numLinha+1)
            iterLineEnd.backward_char()
        else:
            iterLineEnd = buf.get_end_iter()
        strLinhaTexto = buf.get_text(iterLineStart,iterLineEnd,False)
        # print("Texto da Linha = '{}'".format(strLinhaTexto))

        # Remove todas as tags sempre e depois eu refaço
        buf.remove_all_tags(iterLineStart, iterLineEnd)

        # Preciso disso para saber a cor
        lsListTvTreeCenario = self.tvTreeCenarios.props.model

        # Aplica Formatação para tvLinhas
        if numLinha in self.dictTbCenarioLinhas:
            if self.dictTbCenarioLinhas[numLinha] == 'Não':
                buf.apply_tag(self.dictTag['tvLinhasCenario'], iterLineStart, iterLineEnd)
            else:
                buf.apply_tag(self.dictTag['tvLinhasCenarioExport'], iterLineStart, iterLineEnd)
        else:
            buf.apply_tag(self.dictTag['tvLinhasPadrao'], iterLineStart, iterLineEnd)

    def iniciarTbCenarios(self):
        # Gera Tabela Principal

        # Cria dictCols
        self.TbCenarios_dictCols = {
        'ID':'N',
        'Cenários':'T',
        'Linha':'N',
        'Exportar':'T',
        }
        dictCols = self.TbCenarios_dictCols

        # Cria dCI (dictColsIndex)
        listDictCols = list(self.TbCenarios_dictCols.keys())
        self.TbCenarios_dictColsIndex = {}
        for v in self.TbCenarios_dictCols:
            self.TbCenarios_dictColsIndex[v] = listDictCols.index(v)
        dCI = self.TbCenarios_dictColsIndex


        # Atacha
        tvTree = Builder.get_object('tvTreeCenarios')
        tvTree.props.activate_on_single_click = False

        listAux = []
        colIndex = 0
        for colTitulo in dictCols:
            if dictCols[colTitulo] == 'T':
                renderer = Gtk.CellRendererText()
                renderer.set_alignment(0.0,0.5)
                column = Gtk.TreeViewColumn(colTitulo, renderer, text = colIndex)
            elif dictCols[colTitulo] == 'N':
                renderer = Gtk.CellRendererText()
                renderer.set_alignment(0.5,0.5)
                column = Gtk.TreeViewColumn(colTitulo, renderer, text = colIndex)
            elif dictCols[colTitulo] == 'B':
                renderer = Gtk.CellRendererToggle()
                renderer.set_alignment(0.5,0.5)
                column = Gtk.TreeViewColumn(colTitulo, renderer, active = colIndex)
            else:
                renderer = Gtk.CellRendererText()
                renderer.set_alignment(0.5,0.5)
                column = Gtk.TreeViewColumn(colTitulo, renderer, text = colIndex)
            column.props.alignment = 0.02
            # column.props.max_width = 200
            column.props.min_width = 50

            if (dictCols[colTitulo] == 'T') or (dictCols[colTitulo] == 'N'):
                column.add_attribute(renderer, "foreground", len(dictCols.keys()))
                dCI['corFonte'] = len(dictCols.keys())
                # column.add_attribute(renderer, "background", len(dictCols.keys())+1)
                # dCI['corFundo'] = len(dictCols.keys()) + 1

            tvTree.append_column(column)
            listAux.append(str)
            colIndex += 1

        # Esconde colunas ID e Linha
        # tvTree.get_column(dCI['ID']).set_visible(False)
        # tvTree.get_column(dCI['Linha']).set_visible(False)

        # Gera Lista
        lsList = Gtk.ListStore(*[str]*(len(dictCols.keys())+1))
        tvTree.props.model = lsList

    def atualizarTbCenarios(self):
        # tvEditor é o TextView
        textbuffer = self.tvEditor.get_buffer()
        buf = textbuffer

        iterStart = buf.get_start_iter()
        iterEnd = buf.get_end_iter()
        srcStr = buf.get_text(iterStart,iterEnd,False)

        a = re.finditer('DNC_Zouk_V1_Condutor.*',srcStr)
        listMatch = []
        for m in a:
            listMatch.append(m)

        # tvTreeCenarios é a TreeView
        tvTreeCenarios = Builder.get_object("tvTreeCenarios")
        lsList = tvTreeCenarios.props.model
        lsList.clear()

        numID = 0
        self.dictTbCenarioLinhas = {}
        lsList.clear()
        for m in listMatch:
            # Conta ID
            numID = numID + 1
            # Descobre a Linha
            charPos = m.span(0)[0]
            i = buf.get_iter_at_offset(charPos)
            numLinha = i.get_line()
            # Pega o texto da linha toda
            numLinhaTotal = buf.get_line_count()
            iterLineStart = buf.get_iter_at_line(numLinha)
            if ((numLinha + 1) != numLinhaTotal):
                iterLineEnd = buf.get_iter_at_line(numLinha+1)
                iterLineEnd.backward_char()
            else:
                iterLineEnd = buf.get_end_iter()
            strLinhaTexto = buf.get_text(iterLineStart,iterLineEnd,False)

            # Insere
            lsList.append([
                str(numID), # ID
                strLinhaTexto, # Cenário
                str(numLinha), # Linha
                'Não',
                'cyan']) # Cor

            # Adiciona na lista de linhas para ser usado depois pelo formatador
            self.dictTbCenarioLinhas[numLinha] = 'Não'

        if len(lsList) > 0:
            Builder.get_object("lbCenarios").set_text('{} cenários'.format(len(lsList)))
            self.selecionaLinhaTvTreeCenario()


    def selecionaLinhaTvTreeCenario(self):
        if len(self.tvTreeCenarios.props.model) > 0:
            # Linha Atual do tvEditor
            buf = self.tvEditor.get_buffer()
            m = buf.get_insert()
            i = buf.get_iter_at_mark(m)
            numLinhaAtual = i.get_line()

            # Percorre tvTreeCenarios em busca das Linhas
            tvTreeCenarios = Builder.get_object("tvTreeCenarios")
            lsList = tvTreeCenarios.props.model

            # Valor da Linha do Primeiro Cenário da tabela
            treeiter = lsList.get_iter(0)
            numLinhaCenarioRowPrimeiro = int(lsList.get_value(treeiter, 2))

            # Valor da Linha do Último Cenário da tabela
            treeiter = lsList.get_iter(len(lsList)-1)
            numLinhaCenarioRowUltimo = int(lsList.get_value(treeiter, 2))

            # Seta de Acordo com a Posição
            if numLinhaAtual <= numLinhaCenarioRowPrimeiro:
                tvTreeCenarios.set_cursor(0,None,False)
                self.tvTreeCenarios.numRowCenarioAtivo = 0
            elif numLinhaAtual < numLinhaCenarioRowUltimo:
                numRowCenarioEscolhido = 0
                for numRowCenario in range(0,len(lsList)):
                    treeiter = lsList.get_iter(numRowCenario)
                    numLinhaCenarioRow = int(lsList.get_value(treeiter, 2)) # 2 é a terceira coluna do lsList
                    if numLinhaAtual >= numLinhaCenarioRow:
                        numRowCenarioEscolhido = numRowCenario
                    else:
                        break
                tvTreeCenarios.set_cursor(numRowCenarioEscolhido,None,False)
                self.tvTreeCenarios.numRowCenarioAtivo = numRowCenarioEscolhido
            else:
                tvTreeCenarios.set_cursor(len(lsList)-1,None,False)
                self.tvTreeCenarios.numRowCenarioAtivo = len(lsList)-1


    def recarregaCSS(self):
        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        provider.load_from_path(strCSSFullFilename)
        Gtk.StyleContext.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def atualizaIni(self):
        u.iniWrite(cfgINI, 'PATH', 'strGladeFullFilename',strGladeFullFilename)
        u.iniWrite(cfgINI, 'PATH', 'strCSSFullFilename',strCSSFullFilename)
        u.iniWrite(cfgINI, 'PATH', 'strExportLatexFullFilename',strExportLatexFullFilename)


    def executaPasso(self):
        textbuffer = self.tvEditor.get_buffer()
        buf = textbuffer

        # Linha Atual
        m = buf.get_insert()
        i = buf.get_iter_at_mark(m)
        numLinha = i.get_line()

        # Total de Linhas e Posicao do Cursor
        numLinhaTotal = buf.get_line_count()
        numPosCursor = buf.props.cursor_position
        # print("Total de Linhas = {}".format(numLinhaTotal))
        # print("Pos Cursor = {}".format(numPosCursor))

        # Texto da Linha Atual
        #https://lazka.github.io/pgi-docs/Gtk-3.0/classes/TextIter.html#Gtk.TextIter
        iterLineStart = buf.get_iter_at_line(numLinha)
        if ((numLinha + 1) != numLinhaTotal):
            iterLineEnd = buf.get_iter_at_line(numLinha+1)
            iterLineEnd.backward_char()
        else:
            iterLineEnd = buf.get_end_iter()
        strLinhaTexto = buf.get_text(iterLineStart,iterLineEnd,False)
        # print("Texto da Linha = '{}'".format(strLinhaTexto))

        # Vou fazer a separacao do python
        listSep = strLinhaTexto.split(sep=':')
        strFullCmd = listSep[3]
        listSepPeCmd = strFullCmd.split(sep='.')
        strPe = listSepPeCmd[0]
        strCmd = listSepPeCmd[1]

        # Vamos ver se o strCmd tem modificadores
        # Mudei a especificacao so pra facilitar aqui e depois faço codigo que pega as coisas direitinho
        strMod = ''
        if len(listSep) == 5:
            strMod = listSep[4]

        # print('')
        # print(' NumL : "{}"'.format(numLinha))
        # print('Linha : "{}"'.format(strLinhaTexto))
        # print('  Sep : "{}"'.format(str(listSep)))
        # print('  SepPeCmd : "{}"'.format(str(listSepPeCmd)))
        # print('  strPe : "{}"'.format(strPe))
        # print('  strCmd : "{}"'.format(strCmd))
        # print('  strMod : "{}"'.format(strMod))


        self.Condutor.agenteDoStep(strPe,strCmd,strMod)
        self.Condutor.plotaAgente(20)
        self.atualizarCondutorImagens()

    # -----------------------------------------------------
                    # Funções para Testes
    # -----------------------------------------------------

    def on_tvEditor_draw(self,widget, cr):
        pass

    def teste(self):

        swEditor = Builder.get_object("swEditor")
        vAdj = swEditor.get_vadjustment()
        hAdj = swEditor.get_hadjustment()

        HEIGHT = int(round(vAdj.get_upper(),0))
        WIDTH = int(round(hAdj.get_upper(),0))

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
        ctx = cairo.Context(surface)

        self.tvEditor.draw(ctx)
        surface.write_to_png("saida.png")

    def teste_TestaNoInicio(self):
        if booDebug:
            print(self.proxMultiploDeM(12,4))

    def teste_separaLinha(self,textbuffer):
        if booDebug:
            buf = textbuffer

            # Linha Atual
            m = buf.get_insert()
            i = buf.get_iter_at_mark(m)
            numLinha = i.get_line()

            # Total de Linhas e Posicao do Cursor
            numLinhaTotal = buf.get_line_count()
            numPosCursor = buf.props.cursor_position
            # print("Total de Linhas = {}".format(numLinhaTotal))
            # print("Pos Cursor = {}".format(numPosCursor))

            # Texto da Linha Atual
            #https://lazka.github.io/pgi-docs/Gtk-3.0/classes/TextIter.html#Gtk.TextIter
            iterLineStart = buf.get_iter_at_line(numLinha)
            if ((numLinha + 1) != numLinhaTotal):
                iterLineEnd = buf.get_iter_at_line(numLinha+1)
                iterLineEnd.backward_char()
            else:
                iterLineEnd = buf.get_end_iter()
            strLinhaTexto = buf.get_text(iterLineStart,iterLineEnd,False)
            # print("Texto da Linha = '{}'".format(strLinhaTexto))

            # listSep = WordPunctTokenizer().tokenize(strLinhaTexto)
            # listInd = list(WordPunctTokenizer().span_tokenize(strLinhaTexto))
            listSep, listInd = self.retListSepListInd(strLinhaTexto)

            print('')
            print(' NumL : "{}"'.format(numLinha))
            print('Linha : "{}"'.format(strLinhaTexto))
            print('  Sep : "{}"'.format(str(listSep)))
            print('  Ind : "{}"'.format(str(listInd)))
            for char in strLinhaTexto:
                if char == '\t':
                    print('tab')
            # È possível pois ele diferencia espaço de tabs
            # No NLTK não sei se tem como fazer isso
            # Eu teria que escrever meu proprio separador que indentifica posicoes onde tem tab e aplica a tag naqueles espaços
            # Tem que procurar por "\t" ou por cadeias de "\t" para aplicar a tag só uma vez nesses lugares


Builder = Gtk.Builder()
Builder.add_from_file(strGladeFullFilename)
Builder.connect_signals(Manipulador())
Window: Gtk.Window = Builder.get_object("main_window")
Window.show_all()
# Esconde widgets que devem iniciar escondidos

# Stacks
# Builder.get_object("stackLeft").hide()
# Builder.get_object("stackRight").hide()
Builder.get_object("stackBar").hide()

# Pesquisa
Builder.get_object("boxPesquisaSubstituir").hide()
Builder.get_object("boxPesquisaOpcoes").hide()
Builder.get_object("boxPesquisarFechar").hide()

Gtk.main()
