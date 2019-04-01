import ply.lex as lex
import ply.yacc as yacc
import sys
from TablaSem import *

s = Semantic()

reservada = {
    'if': 'IF',
    'dothis': 'DOTHIS',
    'orthis': 'ORTHIS',
    'startoo': 'STARTOO',
    'writeoo': 'WRITEOO',
    'vars': 'VAR',
    'intoo': 'INTOO',
    'decoo': 'DECOO',
    'wordoo': 'WORDOO',
    'charoo': 'CHAROO',
    'bool': 'BOOL',
    'trueoo': 'TRUEOO',
    'falseoo': 'FALSEOO',
    'loop': 'LOOP',
    'returnoo': 'RETURNOO',
    'arroo': 'ARROO',
    'voo': 'VOO',
    'sortoo': 'SORTOO',
    'readoo': 'READOO',
    'savoo': 'SAVOO',
    'getoo': 'GETOO',
    'main': 'MAIN',
    'funcs': 'FUNC',
}

tokens = [
    'SUMA',
    'RESTA',
    'MULT',
    'DIV',
    'MENORQUE',
    'MAYORQUE',
    'MENORIGUAL',
    'CORCHIZQ',
    'CORCHDER',
    'MAYORIGUAL',
    'IGUALIGUAL',
    'DIFERENTE',
    'IGUAL',
    'PARIZQ',
    'PARDER',
    'LLAVEIZQ',
    'LLAVEDER',
    'DP',
    'PUNTOYCOMA',
    'COMA',
    'ID',
    'CTEINTOO',
    'CTEDECOO',
    'CTEWORDOO',
    'INCMAS',
    'INCMENOS',
    'POW',
    'AND',
    'OR',
    'MOD',
    'COMILLA',
]

tokens = tokens + list(reservada.values())

# Reglas de Expresiones Regulares para token de Contexto simple
t_SUMA = r'\+'
t_RESTA = r'\-'
t_POW = 'r\^'
t_MULT = r'\*'
t_DIV = r'\/'
t_IGUAL = r'\='
t_DP = r':'

# Expresiones Logicas
t_MENORQUE = r'<'
t_MAYORQUE = r'>'
t_DIFERENTE = r'!='
t_MENORIGUAL = r'<='
t_MAYORIGUAL = r'>='
t_IGUALIGUAL = r'=='
t_PUNTOYCOMA = r'\;'
t_COMA = r','
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_LLAVEIZQ = r'\{'
t_LLAVEDER = r'\}'
t_CORCHIZQ = r'\['
t_CORCHDER = r'\]'
t_INCMAS = r'\+='
t_INCMENOS = r'\-='
t_COMILLA = r'["]'
t_MOD = r'[%]'
t_OR = r'[|]'
t_AND = r'[&]'


def t_COMMENT(p):
    r'\#.*'
    pass

# ignore characters, spaces and tabs
t_ignore = "\t\r "


def t_CTEINTOO(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_CTEDECOO(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_CTEWORDOO(t):
    r'\'[^\"]*\''
    t.value = t.value[1:-1]
    return t


def t_ID(t):
    r'[a-z][A-Za-z0-9]*'
    t.type = reservada.get(t.value, 'ID')
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    print(t.lineno)
    t.lexer.skip(1)


lexer = lex.lex()


# dictionary of names (for storing variables)

def p_startoo(p):
    'startoo : STARTOO ID PUNTOYCOMA programa_1 MAIN bloque'


def p_programa_1(p):
    '''programa_1 : VAR vars FUNC funcs '''


def p_funcs(p):
    '''funcs : func_1 ID puntoNfx PARIZQ func_2 PARDER LLAVEIZQ VAR vars func_3 LLAVEDER puntoNcont funcs
            | vacio'''

def p_puntoNfx(p):
    '''puntoNfx : vacio'''
    s.add(p[-1], p)

def p_puntoNfx1(p):
    '''puntoNfx1 : vacio'''
    s.addvar(p[-1], s.popType(), is_param=True)

def p_puntoNcont(p):
    '''puntoNcont : vacio'''
    s.setGlobalContext()  # cambiando a contexto global

def p_func_1(p):
    '''func_1 : tipo
        | VOO'''
    if p[1] != None:
        s.addType(p[1])

def p_func_2(p):
    '''func_2 : tipo ID puntoNfx1 func_21
        | vacio'''

def p_func_21(p):
    '''func_21 : COMA tipo ID puntoNfx1 func_21
            | vacio'''

def p_func_3(p):
    '''func_3 :  bloque_1
        | vacio'''

def p_vars(p):
    '''vars :  var_1
            | vacio'''

def p_var_1(p):
    '''var_1 : tipo  ID puntoN2 PUNTOYCOMA var_1
            | vacio'''

def p_puntoN2(p):
    '''puntoN2 : vacio'''
    s.addvar(p[-1], s.popType(), p)

def p_constbool(p):
    '''constbool : TRUEOO
                | FALSEOO'''

def p_tipo(p):
    '''tipo : INTOO
			| DECOO
			| WORDOO
			| CHAROO
			| BOOL'''
    s.addType(p[1])


def p_bloque(p):
    '''bloque : LLAVEIZQ bloque_1 LLAVEDER '''


def p_bloque_1(p):
    '''bloque_1 : estatuto bloque_1
				| vacio '''


def p_estatuto(p):
    '''estatuto : llamada PUNTOYCOMA
                | ciclo
    			| asignacion
				| condicion
				| writoo
				| sort
				| read
				| save
				| get
				| retorno'''


def p_asignacion(p):
    'asignacion : var_id_validation IGUAL asignacion_1 PUNTOYCOMA'
    s.appendAsignacion()


def p_asignacion_1(p):
    '''asignacion_1 : expresion
                    | arreglo'''


def p_expresion(p):
    'expresion : conjunciones'


def p_conjunciones(p):
    'conjunciones : expresioneslogicas puntoN9 conj_1'

def p_puntoN9(p):
    '''puntoN9 : vacio'''
    s.popOp(["&", "|"])


def p_conj_1(p):
    '''conj_1 : AND puntoN3 conjunciones
              | OR puntoN3 conjunciones
              | vacio'''


def p_expresioneslogicas(p):
    'expresioneslogicas : exp expresion_1'


def p_puntoN8(p):
    '''puntoN8 : vacio'''
    s.popOp([">", "<", "!=","<=", ">=", "=="])


def p_expresion_1(p):
    '''expresion_1 : MAYORQUE puntoN3 exp puntoN8
				   | MENORQUE puntoN3 exp puntoN8
				   | DIFERENTE puntoN3 exp puntoN8
				   | MENORIGUAL puntoN3 exp puntoN8
				   | MAYORIGUAL puntoN3 exp puntoN8
				   | IGUALIGUAL puntoN3 exp puntoN8
				   | vacio'''


def p_writoo(p):
    'writoo : WRITEOO PARIZQ writoo_1 PARDER PUNTOYCOMA'
    s.pushFuncion(p[1])


def p_writoo_1(p):
    '''writoo_1 : expresion'''


def p_exp(p):
    'exp : termino puntoN4 exp_1'


def p_puntoN4(p):
    '''puntoN4 : vacio'''
    s.popOp(["+", "-"])


def p_exp_1(p):
    '''exp_1 : SUMA puntoN3 exp
			 | RESTA puntoN3 exp
			 | vacio'''


def p_puntoN3(p):
    '''puntoN3 : vacio'''
    s.pushOperadores(p[-1])


def p_condicion(p):
    'condicion : IF PARIZQ expresion PARDER DOTHIS bloque condicion_1 PUNTOYCOMA'


def p_condicion_1(p):
    '''condicion_1 : ORTHIS bloque
				   | vacio'''


def p_termino(p):
    'termino : factor puntoN5 termino_1'

def p_puntoN5(p):
    'puntoN5 : vacio'
    s.popOp(["*", "/"])

def p_termino_1(p):
    '''termino_1 : MULT puntoN3 termino
				 | DIV puntoN3 termino
				 | vacio'''


def p_factor(p):
    'factor : factor_1'


def p_factor_1(p):
    '''factor_1 : PARIZQ puntoN6 expresion PARDER puntoN7
				| varcte'''

def p_puntoN6(p):
    'puntoN6 : vacio'
    s.pushOperadores("(") #push '('

def p_puntoN7(p):
    'puntoN7 : vacio'
    if s.stackOperadores[len(s.stackOperadores)-1] is "(":
        s.stackOperadores.pop()

# factor_2 antes de varcte

def p_factor_2(p):
    '''factor_2 : SUMA
				| RESTA
				| vacio'''


def p_varcte(p):
    '''varcte : var_id_validation
              | llamada
			  | CTEINTOO
			  | CTEDECOO
			  | CTEWORDOO
			  | CHAROO'''

    if p[1] != None:
        s.pushOperandos(p[1])

def p_var_id_validation(p):
    'var_id_validation : ID'
    s.pushOperandosID(p[1])


def p_ciclo(p):
    'ciclo : LOOP PARIZQ asignacion expresion PUNTOYCOMA incremento PUNTOYCOMA PARDER  bloque '


def p_incremento(p):
    '''incremento : var_id_validation  INCMAS exp
                | var_id_validation  INCMENOS exp'''
    s.pushIncremento(p[2])

def p_llamada(p):
    'llamada : ID PARIZQ llamada_1 PARDER'
    #s.pushOperandosFunc(p[1])


def p_llamada_1(p):
    '''llamada_1 : expresion llamada_2
                | arreglo llamada_2'''


def p_llamada_2(p):
    '''llamada_2 : COMA llamada_1
                | vacio'''


def p_retorno(p):
    'retorno : RETURNOO retorno_1 PUNTOYCOMA'


def p_retorno_1(p):
    '''retorno_1 : varcte
                | expresion'''


def p_arreglo(p):
    'arreglo : ARROO tipo CORCHIZQ INTOO CORCHDER'




def p_vacio(p):
    'vacio : '


def p_sort(p):
    'sort : SORTOO PARIZQ ID PARDER PUNTOYCOMA'


def p_read(p):
    'read : READOO PARIZQ var_id_validation PARDER PUNTOYCOMA'
    s.pushFuncion(p[1])


def p_save(p):
    'save : SAVOO PARIZQ expresion COMA save_3 PARDER PUNTOYCOMA'
    s.pushFuncion(p[1], True)


def p_save_3(p):
    '''save_3 : var_id_validation
             | CTEWORDOO'''

    if p[1] != None:
        s.pushOperandos(p[1])

def p_get(p):
    'get : GETOO PARIZQ get_2 COMA var_id_validation PARDER PUNTOYCOMA'
    s.pushFuncion(p[1], True)

def p_get_2(p):
    '''get_2 : var_id_validation
            | CTEWORDOO'''
    if p[1] != None:
        s.pushOperandos(p[1])

def p_error(p):
    print("Error de sintaxis")
    print(p.lineno)
    print(p)

parser = yacc.yacc()

file = open("file.txt", "r")
startoo = file.read()

if startoo:
    result = parser.parse(startoo)
    print(s.FuncsDir)
    print(s.varsConst)
    print(s.VarsDir)
    print(s.cuadruplos)

#ssavoo(num1,'hola') dato a guardar, var en donde va a quedar guardada
#getoo(num1, num1); #variable a obtener, var en donde regresa el vqalor