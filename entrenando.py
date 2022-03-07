from cv2 import cv2
import os
import mediapipe as mp
import numpy as np

#Entrenador para registrar las imagenes de rostros guardadas y hacer un modelo
def registrar():
	dataPath = '/home/pi/Documents/proyecto/facial_recognition/img/' 
	peopleList = os.listdir(dataPath)
	print('Lista de personas: ', peopleList)

	labels = []
	facesData = []
	label = 0

	for nameDir in peopleList:
		personPath = dataPath + '/' + nameDir
		print('Leyendo las imágenes')

		for fileName in os.listdir(personPath):
			print('Rostros: ', nameDir + '/' + fileName)
			labels.append(label)
			facesData.append(cv2.imread(personPath+'/'+fileName,0))
		label = label + 1

	face_recognizer = cv2.face.LBPHFaceRecognizer_create()

	# Entrenando el reconocedor de rostros
	print("Entrenando...")
	face_recognizer.train(facesData, np.array(labels))

	# Almacenando el modelo obtenido
	face_recognizer.write('modeloLBPHFace.xml')
	print("Modelo almacenado...")
