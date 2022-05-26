from math import *

def obtenerOperacion(operacion : str) -> str:
    """
    Convierte el texto pasado como parámetro en una operación matemática.
    """
    operacion = operacion.replace('cuanto es', '').replace('calcula', '').replace('de', '')

    op = {'por ciento': '/100*','raiz cuadrada':'**0.5', 
        'mas':'+','suma':'+','menos':'-','resta':'-',
        'multiplicado por':'*','multiplicado':'*','por':'*','x':'*',
        'dividido entre':'/','dividido':'/','entre':'/',
        'abre parentesis':'(','cierra parentesis':')',
        'al cuadrado':'** 2','al cubo':'** 3','elevado a':'**',
        'punto':'.','con': '.'}

    claves = list(op.keys())
    valores = list(op.values())
    for i in range(len(claves)):
        if claves[i] in operacion:
            operacion = operacion.replace(claves[i], valores[i])
    return operacion.strip().replace(' ', '').replace(' . ', '.')

def calcularOperacion(operacion : str) -> str:
    """
    Calcula la operación pasada como parámetro y retorna su valor.
    Si contiene 'raiz de' o 'raiz X de' retorna el formato correcto para realizar esta operación.
    Si hay algún error retorna un mensaje con este.
    """
    if 'raiz' in operacion and 'de' in operacion:
        return 'Las raíces solo pueden ser cuadradas y debe decirse raiz cuadrada después del valor del que se quiere sacar esta.'
    else:
        try:
            res = round(eval(operacion), 2)
            resStr = str(res).replace('.', ' con ')

            if 'con 0' in resStr:
                resStr = resStr.replace('con 0', '')

            return f'El resultado de la operación es {resStr}.'
        except ZeroDivisionError as zde:
            print('Error: ' + str(zde))
            return 'No se puede dividir entre 0'
        except Exception as ex:
            print('Error: ' + str(ex))
            return 'No puedo calcular eso, revisa que la operación esté bien formada'
