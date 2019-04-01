class LexerError(Exception):
    @staticmethod
    def raiseError(msg, p=None):
        if p != None:
            print(msg)
        else:
            print(msg)
        quit()

class Semantic:
    FuncsDir = [{'Func': "global", 'Type': "None"}]
    StackTypes = []
    VarsDir = {}
    varsConst = {}
    currentContext = 0 #global
    cuadruplos = []
    stackOperadores = []
    stackOperandos = []
    contTemps = 0

    #Direcciones de memoria
    varsmem = 0
    constmem = 499
    tempmem = 800

    #ADD Funciones
    def checkFunc(self, nameFunc):
        for f in self.FuncsDir:
            if f['Func'] == nameFunc:
                return True

        return  False

    def checkID(self, nameID):
        return nameID in self.VarsDir and (self.VarsDir[nameID]['context'] == self.currentContext or self.VarsDir[nameID]['context'] == 0) # la variable esta declarada

    def add(self, nameFunc, p=None):
        if not self.checkFunc(nameFunc): #si no esta declarada dos o mas veces la misma funcion (mismo nombre, aun con diferente parametros)
            self.FuncsDir.append({'Func': nameFunc, 'Type': self.popType()})
            self.currentContext = len(self.FuncsDir) - 1 # cambiar el contexto de la variables
        else:
            LexerError.raiseError("Error- function duplicate " + nameFunc, p)


    def addType(self, type):
        self.StackTypes.append(type)

    def popType(self):
        return self.StackTypes.pop()

    #ADD variables
    def addvar(self, nameVar, type, p=None, is_param=False):
        #checar que la variable no este declarada dos veces en el mismo contexto
        if self.checkID(nameVar):
            LexerError.raiseError("Error- variable duplicate at", p)

        self.VarsDir[nameVar] = {'Var': nameVar, 'Type' : type, 'context': self.currentContext, 'is_param': is_param, 'dir': self.varsmem}

        self.varsmem = self.varsmem + 1

    def setGlobalContext(self):
        self.currentContext = 0

    #metodos para hacer push e ir llenando los cuadruplos con las direcciones de memoria
    def pushOperadores(self, op):
        self.stackOperadores.append(op)

    def pushOperandosFunc(self, op):
        self.stackOperadores.append(op)

    #push constantes
    def pushOperandos(self, op):
        if not str(op) in self.varsConst: # si no existe ya, se le asigna una direccion
            self.varsConst[str(op)] = {'value': op, 'dir': self.constmem}
            self.constmem = self.constmem + 1

        #append la direccion que ya existe
        self.stackOperandos.append(self.varsConst[str(op)]['dir'])

    def pushOperandosID(self, id):
        if not self.checkID(id):
            LexerError.raiseError("Id no existe " + id)
        #push de direcciones de memoria en el stack en lugar de ID's
        self.stackOperandos.append(self.VarsDir[id]['dir'])

    def getTemporal(self):
        self.tempmem = self.tempmem + 1 # t1, t2... para volver a usar en la tabla
        return self.tempmem - 1

    def popOp(self, listaOperadores):
        if len(self.stackOperadores) > 0 :
            topOp = self.stackOperadores[len(self.stackOperadores)-1]
            if topOp in listaOperadores : # si el operador en la pila existe en la lista
                topOp = self.stackOperadores.pop()
                operando1 = self.stackOperandos.pop()
                operando2 = self.stackOperandos.pop()
                #check(op, op1, op2)
                temporal = self.getTemporal()
                self.cuadruplos.append([topOp, operando2,operando1,temporal])
                self.stackOperandos.append(temporal) #metemos el temporal final a la pila

    def pushIncremento(self, operador):
        t =  self.getTemporal()
        id1 = self.stackOperandos.pop()
        id2 = self.stackOperandos.pop()
        if operador is '+=':
            self.cuadruplos.append(['+', id2, id1,t])
        else:
            self.cuadruplos.append(['-', id2, id1, t])

        # despues se hace la asignacion
        self.cuadruplos.append(['=', id2,'' , t])

    # guardar la variable asignada
    def appendAsignacion(self):
        id1 = self.stackOperandos.pop()
        id2 = self.stackOperandos.pop()
        self.cuadruplos.append(['=', id2, '', id1 ])

    def pushFuncion(self, funcion, internal_id=False):

        if internal_id:
            self.cuadruplos.append([funcion, '', self.stackOperandos.pop(),  self.stackOperandos.pop()])
        else:
            self.cuadruplos.append([funcion, '', '',  self.stackOperandos.pop()])
