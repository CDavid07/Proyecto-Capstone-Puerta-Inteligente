from tkinter import *
from tkinter import messagebox as msg
import os
from cv2 import cv2
import numpy as np
import urllib.request
import face_recognition
import entrenando as registrar
import time
import RPi.GPIO as GPIO  #Importamos el paquete RPi.GPIO y en el código nos refiriremos a el como GPIO
import telegram_comunicate as tc
import urllib.error

pin_led = 18  #Variable que contiene el pin(GPIO.BCM) al cual conectamos la señal del Solenoide

GPIO.setmode(GPIO.BCM) 
GPIO.setup(pin_led, GPIO.OUT) #Configuramos el GPIO18 como salida

#Establecemos la ruta donde se almacencaran las imagenes
direccion = "/home/pi/Documents/proyecto/facial_recognition/img"
#Variable donde se guarda el nombre para una nueva carpeta de imagenes
nombre = ""

# colores para terminal
color_success = "\033[1;32;40m"
color_error = "\033[1;31;40m"
color_normal = "\033[0;37;40m"

#Url donde se trae la imagen de lo que esta registrando la ESP32CAM
url='http://192.168.8.59/cam-hi.jpg'

#Ventana emergente
def printAndShow(screen, text, flag):
   
    if flag:
        print(color_success + text + color_normal)
    else:
        print(color_error + text + color_normal)

#Funcion que abre la puerta, da un tiempo para que se cierre
def abrir():
    
    GPIO.output( pin_led , GPIO.LOW ) 
    GPIO.output( pin_led , GPIO.HIGH )
    time.sleep(10)
    GPIO.output( pin_led , GPIO.LOW )  

#Actualiza el modelo
def actualiza_Modelo(screen2):
    registrar.registrar()

#Captura de imagen donde se le pasa de parametros
# el frame de ventana, el nombre de usuario nuevo y la cantidad de fotos que se tomara segun sea el caso
def register_capture(screen1,nombreI,cantidad):
    
    nombre = nombreI

    #Inicializacion de contador
    cont=0
    carpeta = direccion + '/' + nombre
    if not os.path.exists(carpeta):
        print("Carpeta creada")
        os.makedirs(carpeta)

    while True:
        img_resp=urllib.request.urlopen(url)
        imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
        img=cv2.imdecode(imgnp,-1)
        #Eliminar el error de movimiento
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        #Correccion de color 
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            
            #Extraccion 
            cara = img[y1:y2, x1:x2]

            #Redimension de fotos
            cara = cv2.resize(cara, (150,200), interpolation=cv2.INTER_CUBIC)
            #Almacenamiento de imagenes
            cv2.imwrite(carpeta+"/rostro_{}.jpg".format(cont),cara)
            cont = cont + 1

        #Muestra de fotogramas
        cv2.imshow("Camara", img)

        #Lector de teclado
        t = cv2.waitKey(1)
        if t == 27 or cont > cantidad:
            break

    cv2.destroyAllWindows()
    cv2.imread
    #Actualiza el modelo
    registrar.registrar()
    printAndShow(screen1, "¡Éxito! Se ha registrado correctamente", 1)

#Inicio de registro de inicio de sesion
def login_capture(screen2):
    
    
    imagePaths = os.listdir(direccion)
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read('modeloLBPHFace.xml')
    validacion = 0
    intruso = 0

    while True:

        try:
            t = cv2.waitKey(1)
            #Realiza la lectura de la videocaptura
            img_resp= urllib.request.urlopen(url)
           
            imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
            img=cv2.imdecode(imgnp,-1)
            #Eliminar el error de movimiento
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            #Correccion de color 
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
                
            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                    
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                
                #Extraccion 
                cara = img[y1:y2, x1:x2]

                #Redimension de fotos
                cara = cv2.resize(cara, (150,200), interpolation=cv2.INTER_CUBIC)
                cara= cv2.cvtColor(cara, cv2.COLOR_BGR2GRAY)
                result = face_recognizer.predict(cara)

                #Mostrar resultados en pantalla
                if result[1] < 70:
                    cv2.putText(img, '{}'.format(imagePaths[result[0]]),(x1,y1-5),1,1.3,(0,0,255), 1, cv2.LINE_AA)
                    cv2.rectangle(img, (x1,y1), (x2,y2),(0,0,255),2)
                    validacion = validacion +1
                    if validacion == 5:
                        printAndShow(screen2, f"Bienvenido, {imagePaths[result[0]]}",1)
                        abrir()
                        validacion = 0   
                        tc.texto(imagePaths[result[0]])  
                else:
                    intruso = intruso +1
                    cv2.putText(img,"Desconocido",(x1,y1-5), 1, 1.3,(255,0,0), 1, cv2.LINE_AA)
                    cv2.rectangle(img, (x1,y1), (x2,y2),(255,0,0),2)
                    printAndShow(screen2, "¡Error! Incopatibilidad de datos", 0) 
                    if intruso == 20:
                        print ('Alerta')
                        cv2.imwrite("/home/pi/Documents/proyecto/facial_recognition/advertencia"+"/intruso.jpg",cara)
                        tc.alerta()
                        intruso = 0 
    
            #Muestra de fotogramas
            cv2.imshow("Camara", img)
        except ConnectionResetError as e: 
            
            GPIO.output( pin_led , GPIO.HIGH)
            GPIO.setmode(GPIO.BOARD)   #Establecemos el modo según el cual nos refiriremos a los GPIO de nuestra RPi            
            GPIO.setwarnings(False)
            GPIO.setup(8, GPIO.OUT) #Configuramos el GPIO8 como salida
            GPIO.setup(10, GPIO.OUT) #Configuramos el GPIO10 como salida
            for i in range(1):
                #Gira el motor en un sentido durante 5 segundos
                GPIO.output(8, GPIO.HIGH)
                GPIO.output(10, GPIO.LOW)
                time.sleep(5)

                #Gira el motor en el otror sentido durante 5 segundos
                GPIO.output(8, GPIO.LOW)
                GPIO.output(10, GPIO.HIGH)
                time.sleep(2)
            break

        #Lector de teclado hasta que se oprima la tecla "esc" se detiene el monitoreo
        if t == 27 :
            break 

    GPIO.cleanup()
    cv2.destroyAllWindows()
    cv2.imread
