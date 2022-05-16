def obtenerCiudad(texto: str, cuando : str):
    ciudad = texto.replace('dime el clima de ', '').replace(' de ' + cuando, '')
    ciudad = texto.replace('dime el clima en ', '').replace(' de ' + cuando, '')
    

    return ciudad.title()
