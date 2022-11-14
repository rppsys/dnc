# coding=utf-8

class pilhaCircular:
    def __init__(self,size_max):
        self.max = size_max
        self.data = []
        # Carrega Lista
        for i in range(1,self.max+1):
            self.data.append('')
        self.pT = 1
        self.pB = 1
        self.booVazio = True
        self.count = 0
        self.countMax = 0

    def __del__(self):
        # Deixei isso de aprendizado
        # https://stackoverflow.com/questions/63521088/destroy-object-of-class-python#:~:text=You%20cannot%20manually%20destroy%20objects,an%20object%20is%20reclaimed%20immediately.
        # print("I'm being automatically destroyed. Goodbye!")
        pass

    def incCount(self):
        ''' Incrementa contador mas não deixa passar do Máximo Total'''
        self.count = self.count + 1
        if self.count > self.max:
            self.count = self.max
        if self.countMax < self.count:
            self.countMax = self.count

    def decCount(self):
        self.count = self.count - 1
        if self.count < 0:
            self.count = 0

    def incPT(self):
        self.pT = self.pT + 1
        if self.pT > self.max:
            self.pT = 1

    def decPT(self):
        self.pT = self.pT - 1
        if self.pT == 0:
            self.pT = self.max

    def incPB(self):
        self.pB = self.pB + 1
        if self.pB > self.max:
            self.pB = 1

    def decPB(self):
        self.pB = self.pB - 1
        if self.pB == 0:
            self.pB = self.max

    def push(self,value):
        ''' Insere Valor '''
        if self.booVazio:
            self.data[self.pT-1] = value
            self.incCount()
            self.booVazio = False
        else:
            self.incPT()
            if self.pT == self.pB:
                self.incPB()
            self.data[self.pT-1] = value
            self.incCount()

    def pop(self):
        ''' Retorna Top e Retira '''
        ret = False, ''
        if not self.booVazio:
            ret = self.top()
            if self.pT != self.pB:
                self.decPT()
                self.decCount()
            else:
                self.booVazio = True
                self.decCount()
                ret = False, ''
        else:
            # print('Pop - Está vazio')
            ret = False, ''
        return ret

    def top(self):
        if not self.booVazio:
            # print('Top =',self.data[self.pT-1])
            return True, self.data[self.pT-1]
        else:
            return False, ''

    def retCount(self):
        return int(self.count)

    def redo(self): #Desfaz o que o pop fez (como se fosse um push mas sem valor pois vai ver o que tem na memoria)
        ''' Desfaz o que o pop fez ou retorna falso caso não seja possível realizar o REDO'''
        if self.count < self.countMax: # Dá para fazer REDO
            if self.booVazio:
                # print('Redo = ',self.data[self.pT-1])
                self.booVazio = False
                ret = True, self.data[self.pT-1]
                self.incCount()
            else:
                self.incPT()
                if self.pT == self.pB:  # Completou uma volta completa atingindo o máximo
                    # Volta pT para onde estava
                    self.decPT()
                    self.decCount()
                    # print('Atingiu máximo de redos')
                    ret = False, ''
                else:
                    ret = True, self.data[self.pT-1]
                    self.incCount()
        else:
            ret = False, ''
        return ret

    def show(self):
        print(self.data)

    def show1(self):
        listAux = []
        for d in self.data:
            if len(d) > 1:
                listAux.append(d[0])
            else:
                listAux.append(d)
        print(listAux)

        
