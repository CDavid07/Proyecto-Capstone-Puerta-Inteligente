from lib2to3.pgen2 import token
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import facial_recognition as fr

#Habilita registro
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

#Envía mensaje a telegram cuando el comando /start es usado.
def start(update, context):
  
    update.message.reply_text('¡Bienvenido! En SmartGate nos preocupamos por tu seguridad. Estas son las opciones y acciones que tienes a tu disposición.\nPuedes solicitar:\n1.Abrir la puerta automáticamente con comando /open \nCon el monitoreo constante te podemos informar:\n1.Quien ingresó\n2.Quien desea ingresar sin registro\n¡Suerte! que no te roben ;)')

#Envía mensaje a telegram cuando el comando /help es usado.
def help(update, context):
    update.message.reply_text('Comandos que puedes usar\n/open: Abre la puerta automáticamente')

#Envía mensaje a telegram cuando el comando /open es usado y manda señal de abrir puerta.
def openD(update, context):
    fr.abrir()
    update.message.reply_text('Puerta abierta')
    
  
#Función de notificación donde se manda mensaje cuando una persona ingresa al administrador
def texto (name):
    send= "Hola, el usuario "+name+" a accedido"
    id= "5188730482"
    token = "5249031602:AAFPAxTBeNtfzN5Iw1aLMHswHwOCr8AaBuM"
    url = "https://api.telegram.org/bot"+ token + "/sendMessage"
    params={
        'chat_id' : id,
        'text': send
    }
    requests.post(url,params=params)

#Función de notificación donde se manda mensaje de alerta
#cuando una persona esta intentando accesar sin permiso 
def alerta ():
    send= "Esta persona está intentando acceder a tu propiedad"
    id= "5188730482"
    token = "5249031602:AAFPAxTBeNtfzN5Iw1aLMHswHwOCr8AaBuM"
    url = "https://api.telegram.org/bot"+ token + "/sendPhoto"
   
    files={
        'photo': ('"/home/pi/Documents/proyecto/facial_recognition/advertencia/intruso.jpg"', open("/home/pi/Documents/proyecto/facial_recognition/advertencia/intruso.jpg", 'rb'))
    }
    
    params={
        'chat_id' : id,
        'caption': send
    }
    requests.post(url,files=files,data=params)
    

def main():
    """Inicio del bot."""
    # Declaración del token del bot de Telegram.
    updater = Updater("5249031602:AAFPAxTBeNtfzN5Iw1aLMHswHwOCr8AaBuM", use_context=True)

    #registro de los manejadores para los diferentes comandos
    dp = updater.dispatcher

    # Respuestas de telegram segun sea el comando que se utilice
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("open", openD))

    #Iniciar el bot
    updater.start_polling()

    # Arranca el bot y se detiene hasta que se oprima Ctrl-C o terminar el proceso
    updater.idle()

if __name__ == '__main__':
    main()
