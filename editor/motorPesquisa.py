# coding=utf-8
import re

class motorPesquisa:
    def __init__(self,tbBuffer):
        self.buf = tbBuffer
        self.i = 0
        self.booPesquisaAtiva = False

    def pesquisar(self,strTexto):
        if strTexto != '':
            # Limpa Pesquisa Anterior
            self.listDictRes = []
            self.numResultados = 0

            iterStart = self.buf.get_start_iter()
            iterEnd = self.buf.get_end_iter()
            srcStr = self.buf.get_text(iterStart,iterEnd,False)

            # Pesquisa e vou criar uma lista de dicionários de resultados com tudo que preciso
            a = re.finditer(strTexto,srcStr)
            for m in a:
                dictRes = {}
                dictRes['match'] = m.group(0)
                dictRes['start_pos'] = m.span(0)[0]
                dictRes['end_pos'] = m.span(0)[1]
                dictRes['start_iter'] = self.buf.get_iter_at_offset(m.span(0)[0])
                dictRes['end_iter'] = self.buf.get_iter_at_offset(m.span(0)[1])
                self.listDictRes.append(dictRes)

            self.numResultados = len(self.listDictRes)
            self.booPesquisaAtiva = True
            self.atualizaPos()
        else:
            # Limpa Pesquisa Anterior
            self.listDictRes = []
            self.numResultados = 0
            self.i = 0
            self.booPesquisaAtiva = False

    def atualizaPos(self):
        if self.numResultados != 0:
            insert = self.buf.get_insert()
            iter_insert = self.buf.get_iter_at_mark(insert)
            pos_insert = iter_insert.get_offset()

            j = -1
            for i,dictRes in enumerate(self.listDictRes):
                if dictRes['start_pos'] > pos_insert:
                    j = i
                    break
            # Posição
            if j >= 0:
                self.i = j
            else:
               self.i = 0
        else:
            self.i = 0

    def textoPosicao(self):
        if self.booPesquisaAtiva:
            if self.numResultados != 0:
                return '{} de {}'.format(self.i + 1,self.numResultados)
            else:
                return '0 de 0'
        else:
            return ''

    def fracaoPosicao(self):
        if self.booPesquisaAtiva:
            if self.numResultados != 0:
                return round((self.i + 1)/self.numResultados,2)
            else:
                return 0.0
        else:
            return 0.0




    # Não vou usar
    def selecionaAtual(self):
        if self.numResultados != 0:
            self.buf.select_range(self.listDictRes[self.i]['start_iter'],self.listDictRes[self.i]['end_iter'])

    def proximo(self):
        if self.numResultados != 0:
            self.i = self.i + 1
            if self.i == self.numResultados:
                self.i = 0

    def anterior(self):
        if self.numResultados != 0:
            self.i = self.i - 1
            if self.i == -1:
                self.i = self.numResultados - 1

    def getPosAtual(self):
        if self.numResultados != 0:
            iter_start = self.listDictRes[self.i]['start_iter']
            iter_end = self.listDictRes[self.i]['end_iter']
            nL = iter_start.get_line()
            return nL,iter_start,iter_end
        else:
            return None, None, None

    def getAtivo(self):
        return self.booPesquisaAtiva

    def pintaResultados(self,tagAntes,tagDepois):
        if self.numResultados != 0:
            for i,dictRes in enumerate(self.listDictRes):
                if i < self.i:
                    self.buf.apply_tag(tagAntes, dictRes['start_iter'], dictRes['end_iter'])
                else:
                    self.buf.apply_tag(tagDepois, dictRes['start_iter'], dictRes['end_iter'])
