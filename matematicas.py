from math import *

def obtenerOperacion(operacion):
    op = {'mas':'+','suma':'+','menos':'-','resta':'-',\
        'multiplicado por':'*','multiplicado':'*','por':'*','x':'*',\
        'dividido entre':'/','dividido':'/','entre':'/',\
        'abre parentesis':'(','cierra parentesis':')',\
        'al cuadrado':'** 2','al cubo':'** 3','elevado a':'**','a la':'**',\
        'raiz cuadrada':'**0.5',\
        'punto':'.','con': '.'}

    claves = list(op.keys())
    valores = list(op.values())
    for i in range(len(claves)):
        if claves[i] in operacion:
            operacion = operacion.replace(claves[i], valores[i])
    return operacion.strip()


a = obtenerOperacion('4 raiz cuadrada').replace(' ', '')
print(a)

ev = eval(a)
print(ev)