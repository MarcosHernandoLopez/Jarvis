import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = 'credentials.json'

def obtenerServicioCalendario():
    """
    Lee el fichero con las credenciales del usuario si este ya autorizó a la aplicación. 
    Si no, abre el navegador para que este haga el proceso de autorización y crea el fichero para almacenar estas. 
    """
    creds = None
    # El archivo token.pickle guarda los datos de acceso del usuario y refresca los tokens. Se crea automáticamente cuando termina la autenticación.
    # Solo ocurre la primera vez, no vuelve a pasar después de autenticarse.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Si no hay credenciales válidas el usuario se tiene que loguear.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

    # Guarda las credenciales del usuario en el archivo.
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    service = build('calendar', 'v3', credentials=creds)
    return service
