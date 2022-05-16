from datetime import datetime
def obtenerFecha(dt):
    fecha = datetime.utcfromtimestamp(dt)
    return fecha
