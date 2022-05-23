from logging import exception
import requests, time, urllib
from bs4 import BeautifulSoup

def obtenerConversion(query : str) -> str:
    """
    Busca la conversión en Google, mediante web scraping obtiene el resultado.
    """
    try:
        base = "https://www.google.com/search?"
        url = base + urllib.parse.urlencode({"q": query, "lr":'lang_es'})
        r = requests.get(url, cookies={'CONSENT':'YES+'})
        time.sleep(2)

        sopa = BeautifulSoup(r.text, 'lxml')
        texto = sopa.find("div", class_ = "BNeawe iBp4i AP7Wnd").text

        return texto.replace(chr(160), '')
    except Exception as ex:
        print('Error: ' + str(ex))
        return 'Hubo un problema, revisa que todas las monedas sean válidas.'
