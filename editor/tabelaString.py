# coding=utf-8

class tabelaString:
    def __init__(self,numL,numC):
        self.numL = numL
        self.numC = numC
        self.data = []
        self.colProp = []

        # Cria Tabela
        numV = 0
        for L in range(0,numL):
            listaLinha = []
            for C in range(0,numC):
                numV = numV + 1
                listaLinha.append(str(numV))
            self.data.append(listaLinha)

        # Cria Lista de Propriedades por Coluna
        for C in range(0,numC):
            dictProp = {}
            dictProp['maxlen'] = 0
            self.colProp.append(dictProp)

    def show(self):
        for listLinha in self.data:
            print(listLinha)

    def showPretty(self):
        ret = ''
        for listL in self.data:
            for value in listL:
                ret = ret + str(value) + ';'
            ret = ret + '\n'
        print(ret)

    def get(self,L,C):
        return self.data[L-1][C-1]

    def put(self,L,C,strValue):
        self.data[L-1][C-1] = strValue
        if self.colProp[C-1]['maxlen'] < len(strValue):
            self.colProp[C-1]['maxlen'] = len(strValue)

    def putGood(self,L,C,strValue):
        strGood = strValue.strip()
        self.put(L,C,strGood)

    def getColProp(self,C,strKey):
        if strKey in self.colProp[C-1]:
            return self.colProp[C-1][strKey]
        else:
            return None

    def setColProp(self,C,strKey,strValue):
        self.colProp[C-1][strKey] = strValue

# sample usage
if __name__=='__main__':
    t = tabelaString(5,5)

    i = 0
    for l in range(1,6):
        for c in range(1,6):
            i = i + 1
            print(i)

    print('-----')
    t.show()
    t.put(1,1,'Esse')
    t.put(5,1,'Outro')
    t.put(5,5,'Ponta')
    t.show()
    print('')
    print(t.getColProp(1,'maxlen'))

    t.setColProp(1, 'coco', 10)
    print(t.getColProp(1,'coco'))
    print(t.getColProp(1,'coco2'))
    for d in t.colProp:
        print(d)






    
